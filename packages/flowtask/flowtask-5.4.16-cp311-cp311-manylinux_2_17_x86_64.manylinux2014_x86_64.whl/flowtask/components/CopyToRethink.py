import asyncio
from collections.abc import Callable
import pandas as pd
from asyncdb import AsyncDB
from asyncdb.exceptions import (
    StatementError,
    DataError
)
from .CopyTo import CopyTo
from .interfaces.dataframes import PandasDataframe
from ..exceptions import (
    ComponentError,
    DataNotFound
)
from ..conf import (
    RT_DRIVER,
    RT_HOST,
    RT_PORT,
    RT_USER,
    RT_PASSWORD,
    RT_DATABASE
)


class CopyToRethink(CopyTo, PandasDataframe):
    """
    CopyToRethink.

    Overview

        This component allows copy data into a RethinkDB table,
        Copy into main rethinkdb using write functionality.

    .. table:: Properties
       :widths: auto


    +--------------+----------+-----------+--------------------------------------------+
    | Name         | Required | Summary                                                |
    +--------------+----------+-----------+--------------------------------------------+
    | tablename    |   Yes    | Name of the table in                                   |
    |              |          | the database                                           |
    +--------------+----------+-----------+--------------------------------------------+
    | schema       |   Yes    | Name of the schema                                     |
    |              |          | where is to the table, alias: database                 |
    +--------------+----------+-----------+--------------------------------------------+
    | truncate     |   Yes    | This option indicates if the component should empty    |
    |              |          | before coping the new data to the table. If set to true|
    |              |          | the table will be truncated before saving the new data.|
    +--------------+----------+-----------+--------------------------------------------+
    | use_buffer   |   No     | When activated, this option allows optimizing the      |
    |              |          | performance of the task, when dealing with large       |
    |              |          | volumes of data.                                       |
    +--------------+----------+-----------+--------------------------------------------+
    | credentials  |   No     | Supporting manual rethinkdb credentials                |
    |              |          |                                                        |
    +--------------+----------+-----------+--------------------------------------------+
    | datasource   |   No     | Using a Datasource instead manual credentials          |
    |              |          |                                                        |
    +--------------+----------+-----------+--------------------------------------------+
    """
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self.pk = []
        self.truncate: bool = False
        self.data = None
        self._engine = None
        self.tablename: str = ""
        self.schema: str = ""
        self.use_chunks = False
        self.chunksize: int = kwargs.get('chunksize', 100)
        self._connection: Callable = None
        self._driver: str = RT_DRIVER
        try:
            self.multi = bool(kwargs["multi"])
            del kwargs["multi"]
        except KeyError:
            self.multi = False
        super(CopyToRethink, self).__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )

    def default_connection(self):
        """default_connection.

        Default Connection to RethinkDB.
        """
        try:
            kwargs: dict = {
                "host": RT_HOST,
                "port": int(RT_PORT),
                "db": RT_DATABASE,
                "user": RT_USER,
                "password": RT_PASSWORD
            }
            self._connection = AsyncDB(
                RT_DRIVER,
                params=kwargs,
                loop=self._loop,
                **kwargs
            )
            return self._connection
        except Exception as err:
            raise ComponentError(
                f"Error configuring Pg Connection: {err!s}"
            ) from err

    async def run(self):
        """Run Copy into table functionality."""
        self._result = None
        if self.data is None or self.data.empty:
            raise DataNotFound(
                "CopyToRethink Error: No data in Dataframe"
            )
        self._result = self.data
        if isinstance(self.data, pd.DataFrame):
            columns = list(self.data.columns)
            self.add_metric("NUM_ROWS", self.data.shape[0])
            self.add_metric("NUM_COLUMNS", self.data.shape[1])
            print("Debugging: COPY TO Rethink ===")
            for column in columns:
                t = self.data[column].dtype
                print(
                    column,
                    "->",
                    t,
                    "->",
                    self.data[column].iloc[0]
                )
        if hasattr(self, "create_table"):
            # Create a Table using Model
            self._logger.debug(
                f":: Creating table: {self.schema}.{self.tablename}"
            )
            async with await self._connection.connection() as conn:
                await conn.use(self.schema)
                await self._connection.create_table(
                    table=self.tablename
                )
        if self.truncate is True:
            if self._debug:
                self._logger.debug(
                    f"Truncating table: {self.schema}.{self.tablename}"
                )
            async with await self._connection.connection() as conn:
                await conn.use(self.schema)
                await self._connection.delete(
                    table=self.tablename
                )
        # saving directly the dataframe with write
        try:
            async with await self._connection.connection() as conn:
                await conn.use(self.schema)
                await self._connection.write(
                    table=self.tablename,
                    data=self.data,
                    batch_size=self.chunksize,
                    on_conflict="replace",
                    changes=True,
                    durability="soft"
                )
        except StatementError as err:
            raise ComponentError(
                f"Statement error: {err}"
            ) from err
        except DataError as err:
            raise ComponentError(
                f"Data error: {err}"
            ) from err
        except Exception as err:
            raise ComponentError(
                f"{self.TaskName} Error: {err!s}"
            ) from err
        self._logger.debug(
            f"CopyToRethink: Saving results into: {self.schema}.{self.tablename}"
        )
        # passing through
        return self._result
