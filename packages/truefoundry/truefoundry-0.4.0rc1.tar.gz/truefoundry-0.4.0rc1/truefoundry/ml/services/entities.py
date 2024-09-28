import enum
import time
from typing import Optional
from urllib.parse import urlparse

import jwt
from typing_extensions import TypedDict

from truefoundry.pydantic_v1 import BaseModel, Field, NonEmptyStr, validator


class HostCreds(BaseModel):
    host: str
    token: Optional[str] = None


class AuthServerInfo(BaseModel):
    tenant_name: NonEmptyStr
    auth_server_url: str

    class Config:
        allow_mutation = False


class ArtifactCredential(BaseModel):
    run_id: str
    path: str
    signed_uri: str


class UserType(enum.Enum):
    user = "user"
    serviceaccount = "serviceaccount"


class UserInfo(BaseModel):
    user_id: NonEmptyStr
    user_type: UserType = UserType.user
    email: Optional[str] = None
    tenant_name: NonEmptyStr = Field(alias="tenantName")

    class Config:
        allow_population_by_field_name = True
        allow_mutation = False


class _DecodedToken(TypedDict):
    tenantName: str
    exp: int
    username: str
    email: str
    userType: UserType


class Token(BaseModel):
    access_token: NonEmptyStr = Field(alias="accessToken", repr=False)
    refresh_token: Optional[NonEmptyStr] = Field(alias="refreshToken", repr=False)
    decoded_value: Optional[_DecodedToken] = Field(exclude=True, repr=False)

    class Config:
        allow_population_by_field_name = True
        allow_mutation = False

    @validator("decoded_value", always=True, pre=True)
    def _decode_jwt(cls, v, values, **kwargs):
        access_token = values["access_token"]
        return jwt.decode(
            access_token,
            options={
                "verify_signature": False,
                "verify_aud": False,
                "verify_exp": False,
            },
        )

    @property
    def tenant_name(self) -> str:
        assert self.decoded_value is not None
        return self.decoded_value["tenantName"]

    def is_going_to_be_expired(self, buffer_in_seconds: int = 120) -> bool:
        assert self.decoded_value is not None
        exp = int(self.decoded_value["exp"])
        return (exp - time.time()) < buffer_in_seconds

    def to_user_info(self) -> UserInfo:
        assert self.decoded_value is not None
        return UserInfo(
            user_id=self.decoded_value["username"],
            email=(
                self.decoded_value["email"] if "email" in self.decoded_value else None
            ),
            user_type=UserType(self.decoded_value.get("userType", UserType.user.value)),
            tenant_name=self.tenant_name,  # type: ignore[call-arg]
        )


class DeviceCode(BaseModel):
    user_code: str = Field(alias="userCode")
    device_code: str = Field(alias="deviceCode")

    class Config:
        allow_population_by_field_name = True
        allow_mutation = False

    def get_user_clickable_url(self, tracking_uri: str) -> str:
        parsed_tracking_uri = urlparse(tracking_uri)
        return f"{parsed_tracking_uri.scheme}://{parsed_tracking_uri.netloc}/authorize/device?userCode={self.user_code}"
