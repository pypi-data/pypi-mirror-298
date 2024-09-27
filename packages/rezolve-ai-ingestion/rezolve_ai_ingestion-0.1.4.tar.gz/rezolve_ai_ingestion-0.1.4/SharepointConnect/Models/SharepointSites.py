# pylint: disable=missing-function-docstring,missing-module-docstring,missing-class-docstring,broad-exception-caught,invalid-name,line-too-long

from typing import Optional
from pydantic import BaseModel, Field
from typing import List

class SharepointSites(BaseModel):
    sites: Optional[List] = Field(
        default=None,
        description="",
        example="",
    )