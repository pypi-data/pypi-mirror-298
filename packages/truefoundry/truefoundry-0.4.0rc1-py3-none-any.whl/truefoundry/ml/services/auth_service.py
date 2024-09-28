import time
from urllib.parse import urlparse

from truefoundry.ml.autogen.client import (  # type: ignore[attr-defined]
    ApiClient,
    AuthApi,
    Configuration,
)
from truefoundry.ml.exceptions import MlFoundryException
from truefoundry.ml.logger import logger
from truefoundry.ml.run_utils import append_path_to_rest_tracking_uri
from truefoundry.ml.services.entities import (
    AuthServerInfo,
    DeviceCode,
    HostCreds,
    Token,
)
from truefoundry.ml.services.utils import http_request, http_request_safe

# TODO: This will eventually go away, this is duplicate of AuthServiceClient


class AuthService:
    def __init__(self, url: str, tenant_name: str):
        self._host_creds = HostCreds(host=url.rstrip("/"), token=None)
        self._tenant_name = tenant_name

    def refresh_token(self, token: Token) -> Token:
        if not token.refresh_token:
            # TODO: Add a way to propagate error messages without traceback to the output interface side
            raise MlFoundryException(
                "Unable to resume login session. Please log in again using `tfy login [--host HOST] --relogin`"
            )
        try:
            response = http_request_safe(
                method="post",
                host_creds=self._host_creds,
                endpoint="api/v1/oauth/token/refresh",
                json={
                    "tenantName": token.tenant_name,
                    "refreshToken": token.refresh_token,
                },
                timeout=3,
            )
        except MlFoundryException as e:
            if e.status_code and (400 <= e.status_code < 500):
                raise MlFoundryException(
                    "Unable to resume login session. "
                    "Please log in again using `tfy login [--host HOST] --relogin`"
                ) from None
            raise
        return Token.parse_obj(response)

    def get_device_code(self) -> DeviceCode:
        response = http_request_safe(
            method="post",
            host_creds=self._host_creds,
            endpoint="api/v1/oauth/device",
            json={"tenantName": self._tenant_name},
            timeout=3,
        )
        return DeviceCode.parse_obj(response)

    def get_token_from_device_code(
        self, device_code: str, timeout: float = 60
    ) -> Token:
        start_time = time.monotonic()
        while (time.monotonic() - start_time) <= timeout:
            response = http_request(
                method="post",
                host_creds=self._host_creds,
                endpoint="api/v1/oauth/device/token",
                json={"tenantName": self._tenant_name, "deviceCode": device_code},
                timeout=3,
            )
            if response.status_code == 202:
                logger.debug("User has not authorized yet. Checking again.")
                time.sleep(1.0)
                continue
            if response.status_code == 201:
                response = response.json()
                return Token.parse_obj(response)
            raise MlFoundryException(
                "Failed to get token using device code.\n"
                f"Status Code: {response.status_code},\nResponse: {response.text}"
            )
        raise MlFoundryException(f"Did not get authorized within {timeout} seconds.")


def get_auth_service(tracking_uri: str) -> AuthService:
    tracking_uri = append_path_to_rest_tracking_uri(tracking_uri)
    parsed_tracking_uri = urlparse(tracking_uri)
    host = parsed_tracking_uri.netloc
    # Anonymous api
    api_client = ApiClient(
        configuration=Configuration(
            host=tracking_uri.rstrip("/"),
            access_token=None,
        )
    )
    auth_api = AuthApi(api_client=api_client)
    auth_server_info = auth_api.get_tenant_id_get(
        host_name=host,
        _request_timeout=3,
    )
    tenant_info = AuthServerInfo.parse_obj(auth_server_info.dict())
    return AuthService(
        url=tenant_info.auth_server_url, tenant_name=tenant_info.tenant_name
    )
