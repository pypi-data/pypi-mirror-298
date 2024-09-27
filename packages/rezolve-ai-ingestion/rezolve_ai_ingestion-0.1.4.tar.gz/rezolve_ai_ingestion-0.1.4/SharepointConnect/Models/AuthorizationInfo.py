# pylint: disable=missing-function-docstring,missing-module-docstring,missing-class-docstring,broad-exception-caught,invalid-name,line-too-long

from typing import Optional
from pydantic import BaseModel, Field

class AuthorizationInfo(BaseModel):
    sharepoint_prefix: Optional[str] = Field(
        default=None,
        description="",
        example="",
    )
    azure_tid: Optional[str] = Field(
        default=None,
        description="",
        example='',
    )
    client_id: Optional[str] = Field(
        default=None,
        description="",
        example="",
    )
    client_secret: Optional[str] = Field(
        default=None,
        description="",
        example="",
    )
    thumbprint: Optional[str] = Field(
        default=None,
        description="",
        example="",
    )
    key: Optional[str] = Field(
        default=None,
        description="",
        example="",
    )
    sharepoint_auth: Optional[bool] =Field(
        default=False,
        description="Graph or Sharepoint as per client",
        example="",
    )
    