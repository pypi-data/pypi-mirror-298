from collections.abc import Callable
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.exc import ProgrammingError, OperationalError, StatementError
from sqlalchemy.inspection import inspect
from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import ForeignKeyConstraint
from sqlalchemy.pool import NullPool
from navconfig.logging import logging
from querysource.conf import sqlalchemy_url
from ...exceptions import ComponentError


class PgOutput:
    def __init__(
        self, parent: Callable, dsn: str = None, do_update: bool = True
    ) -> None:
        self._engine: Callable = None
        self._parent = parent
        self._results: list = []
        self._columns: list = []
        self._do_update: bool = do_update
        if not dsn:
            dsn = sqlalchemy_url
        try:
            self._engine = create_engine(dsn, echo=False, poolclass=NullPool)
        except Exception as err:
            logging.exception(err, stack_info=True)
            raise ComponentError(
                message=f"Connection Error: {err}"
            ) from err

    def engine(self):
        return self._engine

    def close(self):
        """Closing Operations."""
        try:
            self._engine.dispose()
        except Exception as err:
            logging.error(err)

    def result(self):
        return self._results

    @property
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, columns: list):
        self._columns = columns

    def db_upsert(self, table, conn, keys, data_iter):
        """
        Execute SQL statement for upserting data

        Parameters
        ----------
        table : pandas.io.sql.SQLTable
        conn : sqlalchemy.engine.Engine or sqlalchemy.engine.Connection
        keys : list of str of Column names
        data_iter : Iterable that iterates the values to be inserted
        """
        args = []
        try:
            tablename = str(table.name)
        except Exception:
            tablename = self._parent.tablename
        if self._parent.foreign_keys():
            fk = self._parent.foreign_keys()
            fn = ForeignKeyConstraint(fk["columns"], fk["fk"], name=fk["name"])
            args.append(fn)
        metadata = MetaData()
        metadata.bind = self._engine
        constraint = self._parent.constraints()
        options = {"schema": self._parent.get_schema(), "autoload_with": self._engine}
        tbl = Table(tablename, metadata, *args, **options)
        # removing the columns from the table definition
        columns = self._columns
        # for column in columns:
        col_instances = [col for col in tbl._columns if col.name not in columns]
        for col in col_instances:
            tbl._columns.remove(col)

        primary_keys = []
        try:
            primary_keys = self._parent.primary_keys()
        except AttributeError as err:
            primary_keys = [key.name for key in inspect(tbl).primary_key]
            if not primary_keys:
                raise ComponentError(
                    f"No Primary Key on table {tablename}."
                )
        for row in data_iter:
            row_dict = dict(zip(keys, row))
            insert_stmt = postgresql.insert(tbl).values(**row_dict)
            # define dict of non-primary keys for updating
            # get the list of columns that are not part of the primary key
            # create a dictionary of the values to be updated
            if self._do_update is True:
                if len(columns) > 1:
                    # TODO: add behavior of on_conflict_do_nothing
                    update_dict = {
                        c.name: c
                        for c in insert_stmt.excluded
                        if not c.primary_key and c.name in columns
                    }
                    if constraint is not None:
                        upsert_stmt = insert_stmt.on_conflict_do_update(
                            constraint=constraint, set_=update_dict
                        )
                    else:
                        upsert_stmt = insert_stmt.on_conflict_do_update(
                            index_elements=primary_keys, set_=update_dict
                        )
                else:
                    upsert_stmt = insert_stmt.on_conflict_do_nothing(
                        index_elements=primary_keys
                    )
            else:
                # Do nothing on conflict
                upsert_stmt = insert_stmt.on_conflict_do_nothing(
                    index_elements=primary_keys
                )
            try:
                conn.execute(upsert_stmt)
            except (ProgrammingError, OperationalError) as err:
                raise ComponentError(f"SQL Operational Error: {err}") from err
            except StatementError as err:
                raise ComponentError(f"Statement Error: {err}") from err
            except Exception as err:
                raise ComponentError(f"Error on PG UPSERT: {err}") from err
