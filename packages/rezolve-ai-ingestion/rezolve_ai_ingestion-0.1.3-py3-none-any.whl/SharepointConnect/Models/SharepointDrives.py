# pylint: disable=missing-function-docstring,missing-module-docstring,missing-class-docstring,broad-exception-caught,invalid-name,line-too-long

from typing import Optional
from pydantic import BaseModel, Field

class SharepointDrives(BaseModel):
    sites: Optional[object] = Field(
        default=None,
        description="",
        example="",
    )
