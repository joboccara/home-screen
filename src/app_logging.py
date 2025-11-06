import logging
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.models import *

from app_secrets import DATADOG_API_KEY

class DatadogLogHandler(logging.Handler):
    def __init__(self, api_key, site="datadoghq.eu"):
        super().__init__()
        configuration = Configuration()
        configuration.api_key["apiKeyAuth"] = api_key
        configuration.server_variables["site"] = site
        self.client = ApiClient(configuration)
        self.api = LogsApi(self.client)

    def emit(self, record):
        log_entry = HTTPLogItem(
            message=self.format(record),
            ddsource="python",
            service="my-app",
            status=record.levelname.lower(),
        )
        try:
            self.api.submit_log(body=[log_entry])
        except Exception:
            self.handleError(record)

logger = logging.getLogger("datadog")
logger.setLevel(logging.INFO)
logger.addHandler(DatadogLogHandler(DATADOG_API_KEY))
