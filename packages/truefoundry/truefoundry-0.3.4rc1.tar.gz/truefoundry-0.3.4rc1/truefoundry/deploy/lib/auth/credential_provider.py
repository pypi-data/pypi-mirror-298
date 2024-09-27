import os
import threading
from abc import ABC, abstractmethod

from truefoundry.deploy.lib.auth.auth_service_client import AuthServiceClient
from truefoundry.deploy.lib.auth.credential_file_manager import (
    CredentialsFileContent,
    CredentialsFileManager,
)
from truefoundry.deploy.lib.clients.utils import resolve_base_url
from truefoundry.deploy.lib.const import API_KEY_ENV_NAME
from truefoundry.deploy.lib.model.entity import Token
from truefoundry.logger import logger

TOKEN_REFRESH_LOCK = threading.RLock()


class CredentialProvider(ABC):
    @property
    @abstractmethod
    def token(self) -> Token: ...

    @property
    @abstractmethod
    def base_url(self) -> str: ...

    @staticmethod
    @abstractmethod
    def can_provide() -> bool: ...


class EnvCredentialProvider(CredentialProvider):
    def __init__(self) -> None:
        from truefoundry.deploy.lib.clients.servicefoundry_client import (
            ServiceFoundryServiceClient,
        )

        logger.debug("Using env var credential provider")
        api_key = os.getenv(API_KEY_ENV_NAME)
        if not api_key:
            raise Exception(
                f"Value of {API_KEY_ENV_NAME} env var should be non-empty string"
            )
        # TODO: Read host from cred file as well.
        base_url = resolve_base_url().strip("/")
        self._host = base_url
        self._auth_service = AuthServiceClient.from_base_url(base_url=base_url)

        servicefoundry_client = ServiceFoundryServiceClient(
            init_session=False, base_url=base_url
        )
        self._token: Token = servicefoundry_client.get_token_from_api_key(
            api_key=api_key
        )

    @staticmethod
    def can_provide() -> bool:
        return API_KEY_ENV_NAME in os.environ

    @property
    def token(self) -> Token:
        with TOKEN_REFRESH_LOCK:
            if self._token.is_going_to_be_expired():
                logger.info("Refreshing access token")
                self._token = self._auth_service.refresh_token(
                    self._token, self.base_url
                )
            return self._token

    @property
    def base_url(self) -> str:
        return self._host


class FileCredentialProvider(CredentialProvider):
    def __init__(self) -> None:
        logger.debug("Using file credential provider")
        self._cred_file = CredentialsFileManager()

        with self._cred_file:
            self._last_cred_file_content = self._cred_file.read()
            self._token = self._last_cred_file_content.to_token()
            self._host = self._last_cred_file_content.host

        self._auth_service = AuthServiceClient.from_base_url(base_url=self._host)

    @staticmethod
    def can_provide() -> bool:
        with CredentialsFileManager() as cred_file:
            return cred_file.exists()

    @property
    def token(self) -> Token:
        with TOKEN_REFRESH_LOCK:
            if not self._token.is_going_to_be_expired():
                return self._token

            logger.info("Refreshing access token")
            with self._cred_file:
                new_cred_file_content = self._cred_file.read()
                new_token = new_cred_file_content.to_token()
                new_host = new_cred_file_content.host

                if new_cred_file_content == self._last_cred_file_content:
                    self._token = self._auth_service.refresh_token(
                        self._token, self.base_url
                    )
                    self._last_cred_file_content = CredentialsFileContent(
                        host=self._host,
                        access_token=self._token.access_token,
                        refresh_token=self._token.refresh_token,
                    )
                    self._cred_file.write(self._last_cred_file_content)
                    return self._token

                if (
                    new_host == self._host
                    and new_token.to_user_info() == self._token.to_user_info()
                ):
                    self._last_cred_file_content = new_cred_file_content
                    self._token = new_token
                    # recursive
                    return self.token

                raise Exception(
                    "Credentials on disk changed while mlfoundry was running."
                )

    @property
    def base_url(self) -> str:
        return self._host
