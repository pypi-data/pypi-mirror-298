import abc
import atexit
import os
import threading
import weakref
from typing import TYPE_CHECKING, Dict, Optional

from truefoundry.common.request_utils import urllib3_retry
from truefoundry.ml import env_vars
from truefoundry.ml.autogen.client import (  # type: ignore[attr-defined]
    ApiClient,
    Configuration,
)
from truefoundry.ml.exceptions import MlFoundryException
from truefoundry.ml.logger import logger
from truefoundry.ml.login import CredentialsFileContent, CredentialsFileManager
from truefoundry.ml.run_utils import (
    append_path_to_rest_tracking_uri,
    resolve_tracking_uri,
)
from truefoundry.ml.services.auth_service import get_auth_service
from truefoundry.ml.services.entities import HostCreds, Token, UserInfo

if TYPE_CHECKING:
    from truefoundry.ml.mlfoundry_run import MlFoundryRun

TOKEN_REFRESH_LOCK = threading.RLock()


class CredentialProvider(abc.ABC):
    @property
    @abc.abstractmethod
    def token(self) -> Token: ...

    @staticmethod
    @abc.abstractmethod
    def can_provide() -> bool: ...

    @property
    @abc.abstractmethod
    def tracking_uri(self) -> str: ...


class EnvCredentialProvider(CredentialProvider):
    def __init__(self):
        logger.debug("Using env var credential provider")
        self._tracking_uri = resolve_tracking_uri(tracking_uri=None)
        self._auth_service = get_auth_service(tracking_uri=self._tracking_uri)
        api_key = os.getenv(env_vars.API_KEY_GLOBAL)
        if not api_key:
            raise MlFoundryException(
                f"Value of {env_vars.API_KEY_GLOBAL} env var should be non-empty string"
            )
        self._token: Token = Token(access_token=api_key, refresh_token=None)  # type: ignore[call-arg]

    @staticmethod
    def can_provide() -> bool:
        return env_vars.API_KEY_GLOBAL in os.environ

    @property
    def token(self) -> Token:
        with TOKEN_REFRESH_LOCK:
            if self._token.is_going_to_be_expired():
                logger.info("Refreshing access token")
                self._token = self._auth_service.refresh_token(self._token)
            return self._token

    @property
    def tracking_uri(self) -> str:
        return self._tracking_uri


class FileCredentialProvider(CredentialProvider):
    def __init__(self):
        logger.debug("Using file credential provider")
        self._cred_file = CredentialsFileManager()

        with self._cred_file:
            self._last_cred_file_content = self._cred_file.read()
            self._tracking_uri = self._last_cred_file_content.host
            self._token = self._last_cred_file_content.to_token()
            self._auth_service = get_auth_service(tracking_uri=self._tracking_uri)

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
                new_tracking_uri = new_cred_file_content.host

                if new_cred_file_content == self._last_cred_file_content:
                    self._token = self._auth_service.refresh_token(self._token)
                    self._last_cred_file_content = CredentialsFileContent(
                        host=self._tracking_uri,
                        access_token=self._token.access_token,
                        refresh_token=self._token.refresh_token,
                    )
                    self._cred_file.write(self._last_cred_file_content)
                    return self._token

                if (
                    new_tracking_uri == self._tracking_uri
                    and new_token.to_user_info() == self._token.to_user_info()
                ):
                    self._last_cred_file_content = new_cred_file_content
                    self._token = new_token
                    # recursive
                    return self.token

                raise MlFoundryException(
                    "Credentials on disk changed while mlfoundry was running."
                )

    @property
    def tracking_uri(self) -> str:
        return self._tracking_uri


SESSION_LOCK = threading.RLock()


class ActiveRuns:
    def __init__(self):
        self._active_runs: Dict[str, weakref.ReferenceType["MlFoundryRun"]] = {}

    def add_run(self, run: "MlFoundryRun"):
        with SESSION_LOCK:
            self._active_runs[run.run_id] = weakref.ref(run)

    def remove_run(self, run: "MlFoundryRun"):
        with SESSION_LOCK:
            if run.run_id in self._active_runs:
                del self._active_runs[run.run_id]

    def close_active_runs(self):
        with SESSION_LOCK:
            for run_ref in list(self._active_runs.values()):
                run = run_ref()
                if run and run.auto_end:
                    run.end()
            self._active_runs.clear()


ACTIVE_RUNS = ActiveRuns()
atexit.register(ACTIVE_RUNS.close_active_runs)


class Session:
    def __init__(self, cred_provider: CredentialProvider):
        # Note: Whenever a new session is initialized all the active runs are ended
        self._closed = False
        self._cred_provider: CredentialProvider = cred_provider
        self._user_info: UserInfo = self._cred_provider.token.to_user_info()

    def close(self):
        logger.debug("Closing existing session")
        self._closed = True
        self._user_info = None
        self._cred_provider = None

    def _assert_not_closed(self):
        if self._closed:
            raise MlFoundryException(
                "This session has been deactivated.\n"
                "At a time only one `client` (received from "
                "`truefoundry.ml.get_client()` function call) can be used"
            )

    @property
    def token(self) -> Token:
        return self._cred_provider.token

    @property
    def user_info(self) -> UserInfo:
        self._assert_not_closed()
        return self._user_info

    @property
    def tracking_uri(self) -> str:
        return self._cred_provider.tracking_uri

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Session):
            return False
        return (
            type(self._cred_provider) == type(other._cred_provider)  # noqa: E721
            and self.user_info == other.user_info
            and self.tracking_uri == other.tracking_uri
        )

    def get_host_creds(self) -> HostCreds:
        tracking_uri = append_path_to_rest_tracking_uri(
            self._cred_provider.tracking_uri
        )
        return HostCreds(
            host=tracking_uri, token=self._cred_provider.token.access_token
        )


ACTIVE_SESSION: Optional[Session] = None


def get_active_session() -> Optional[Session]:
    return ACTIVE_SESSION


def _get_api_client(
    session: Optional[Session] = None,
    allow_anonymous: bool = False,
) -> ApiClient:
    session = session or get_active_session()
    if session is None:
        if allow_anonymous:
            return ApiClient()
        else:
            raise MlFoundryException(
                "No active session found. Perhaps you are not logged in?\n"
                "Please log in using `tfy login [--host HOST] --relogin"
            )

    creds = session.get_host_creds()
    configuration = Configuration(
        host=creds.host.rstrip("/"),
        access_token=creds.token,
    )
    configuration.retries = urllib3_retry(retries=2)
    api_client = ApiClient(configuration=configuration)
    return api_client


def init_session() -> Session:
    with SESSION_LOCK:
        final_cred_provider = None
        for cred_provider in [EnvCredentialProvider, FileCredentialProvider]:
            if cred_provider.can_provide():
                final_cred_provider = cred_provider()
                break
        if final_cred_provider is None:
            raise MlFoundryException(
                "Please login using `mlfoundry login` command "
                "or `truefoundry.ml.login()` function call"
            )
        new_session = Session(cred_provider=final_cred_provider)

        global ACTIVE_SESSION
        if ACTIVE_SESSION and ACTIVE_SESSION == new_session:
            return ACTIVE_SESSION

        ACTIVE_RUNS.close_active_runs()

        if ACTIVE_SESSION:
            ACTIVE_SESSION.close()
        ACTIVE_SESSION = new_session

        logger.info(
            "Logged in to %r as %r (%s)",
            ACTIVE_SESSION.tracking_uri,
            ACTIVE_SESSION.user_info.user_id,
            ACTIVE_SESSION.user_info.email or ACTIVE_SESSION.user_info.user_type.value,
        )
        return ACTIVE_SESSION
