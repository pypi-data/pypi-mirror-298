# pylint: disable=missing-function-docstring,missing-module-docstring,missing-class-docstring,broad-exception-caught,invalid-name,line-too-long

from typing import Optional
from pydantic import BaseModel, Field

class RezolveInfo(BaseModel):
    index: Optional[str] = Field(
        default=None,
        description="",
        example="",
    )
    namespace: Optional[str] = Field(
        default=None,
        description="",
        example="",
    )
    environment: Optional[str] = Field(
        default=None,
        description="",
        example="",
    )
    db_key: Optional[str] = Field(
        default=None,
        description="",
        example="",
    )
    llm_key: Optional[str] = Field(
        default=None,
        description="",
        example="",
    )
    host: Optional[str] = Field(
        default=None,
        description="",
        example="",
    )
    embedding_model: Optional[str] = Field(
        default=None,
        description="",
        example="",
    )

