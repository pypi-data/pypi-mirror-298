# pylint: disable=missing-function-docstring,missing-module-docstring,missing-class-docstring,broad-exception-caught,invalid-name,line-too-long

from typing import Optional
from pydantic import BaseModel, Field

class CherwellStoredSearch(BaseModel):
    stored_search: Optional[str] = Field(
        default=None,
        description="",
        example="",
    )
    view_url_prefix: Optional[str] = Field(
        default=None,
        description="",
        example="",
    )