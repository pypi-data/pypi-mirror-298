from typing import Optional

from truefoundry.common.request_utils import requests_retry_session
from truefoundry.ml.exceptions import MlFoundryException
from truefoundry.ml.run_utils import append_servicefoundry_path_to_tracking_ui
from truefoundry.ml.services.entities import HostCreds
from truefoundry.ml.services.utils import http_request_safe


class ServicefoundryService:
    def __init__(self, tracking_uri: str, token: Optional[str] = None):
        self.host_creds = HostCreds(
            host=append_servicefoundry_path_to_tracking_ui(tracking_uri), token=token
        )

    def get_integration_from_id(self, integration_id: str):
        integration_id = integration_id or ""
        data = http_request_safe(
            method="get",
            host_creds=self.host_creds,
            endpoint="v1/provider-accounts/provider-integrations",
            session=requests_retry_session(retries=1),
            params={"id": integration_id, "type": "blob-storage"},
            timeout=3,
        )
        if (
            data.get("providerIntegrations")
            and len(data["providerIntegrations"]) > 0
            and data["providerIntegrations"][0]
        ):
            return data["providerIntegrations"][0]
        else:
            raise MlFoundryException(
                f"Invalid storage integration id: {integration_id}"
            )
