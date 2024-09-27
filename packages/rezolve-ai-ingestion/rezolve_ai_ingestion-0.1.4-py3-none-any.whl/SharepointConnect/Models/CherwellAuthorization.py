# pylint: disable=missing-function-docstring,missing-module-docstring,missing-class-docstring,broad-exception-caught,invalid-name,line-too-long

from typing import Optional
from pydantic import BaseModel, Field

class CherwellAuthorization(BaseModel):
    client_id: Optional[str] = Field(
        default=None,
        description="",
        example="",
    )
    username: Optional[str] = Field(
        default=None,
        description="",
        example='',
    )
    password: Optional[str] = Field(
        default=None,
        description="",
        example="",
    )
    grant_type: Optional[str] = Field(
        default=None,
        description="",
        example="",
    )
    token_url: Optional[str] = Field(
        default=None,
        description="",
        example="",
    )
    