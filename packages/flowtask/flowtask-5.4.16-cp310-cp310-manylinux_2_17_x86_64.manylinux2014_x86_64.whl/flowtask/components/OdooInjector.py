import asyncio
from collections.abc import Callable
from urllib.parse import urljoin
import pandas as pd
from flowtask.components.abstract import DtComponent
from flowtask.components.interfaces.http import HTTPService
from flowtask.exceptions import ComponentError


class OdooInjector(DtComponent, HTTPService):

    accept: str = "application/json"
    auth_type: str = "api_key"
    download = None
    _credentials: dict = {
        "HOST": str,
        "PORT": str,
        "APIKEY": str,
        "INJECTOR_URL": str,
    }

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self.credentials: dict = {}

        DtComponent.__init__(self, loop=loop, job=job, stat=stat, **kwargs)
        HTTPService.__init__(self, **kwargs)

    async def start(self, **kwargs):
        if self.previous and isinstance(self.input, pd.DataFrame):
            self.data = self.input.to_dict(orient="records")

        self.processing_credentials()

        self.headers = {"api-key": self.credentials["APIKEY"]}

        self.url = self.get_url()

        return True

    async def run(self):
        payload = self.get_payload()
        result, error = await self.session(
            url=self.url, method="post", data=payload, use_json=True
        )

        if not result or (
            not error
            and 'error' not in result
            and not "error" in result.get("result")
            and result["result"].get("ids")
        ):
            self._logger.debug(result)
            return True

        error_msg = str(
            error or result.get('error') or result["result"].get("error") or result["result"]["messages"]
        )
        raise ComponentError(error_msg)

    async def close(self):
        return True

    def get_url(self):
        port = (
            f":{self.credentials['PORT']}" if self.credentials["PORT"] != "80" else ""
        )
        base_url = f"{self.credentials['HOST']}{port}"
        url = urljoin(base_url, self.credentials["INJECTOR_URL"])
        return url

    def get_payload(self):
        return {
            # "model": "res.partner",
            "model": self.model,
            "options": {
                # 'has_headers': True,
                "advanced": False,
                "keep_matches": False,
                # 'name_create_enabled_fields': {'country_id': False},
                "name_create_enabled_fields": {},
                "import_set_empty_fields": [],
                "import_skip_records": [],
                "fallback_values": {},
                "skip": 0,
                "limit": 2000,
                # 'encoding': '',
                # 'separator': '',
                "quoting": '"',
                # 'sheet': 'Sheet1',
                "date_format": "",
                "datetime_format": "",
                "float_thousand_separator": ",",
                "float_decimal_separator": ".",
                "fields": [],
            },
            "data": self.data,
        }

    def processing_credentials(self):
        if self.credentials:
            for value, dtype in self._credentials.items():
                try:
                    if type(self.credentials[value]) == dtype:
                        default = getattr(self, value, self.credentials[value])
                        val = self.get_env_value(
                            self.credentials[value], default=default
                        )
                        self.credentials[value] = val
                except (TypeError, KeyError) as ex:
                    self._logger.error(f"{__name__}: Wrong or missing Credentials")
                    raise ComponentError(
                        f"{__name__}: Wrong or missing Credentials"
                    ) from ex
