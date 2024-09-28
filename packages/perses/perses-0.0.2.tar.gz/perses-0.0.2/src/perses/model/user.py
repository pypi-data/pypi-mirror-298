from typing import Literal, Optional

from pydantic import Field

from perses.model.common import BaseModel, ObjectMetadata


class NativeProvider(BaseModel):
    password: Optional[str] = None


class OAuthProvider(BaseModel):
    issuer: str
    email: str
    subject: str


class UserSpec(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    native_provider: Optional[NativeProvider] = None
    oauth_providers: list[OAuthProvider] = Field(default_factory=list)


class User(BaseModel):
    kind: Literal["User"] = "User"
    metadata: ObjectMetadata
    spec: UserSpec
