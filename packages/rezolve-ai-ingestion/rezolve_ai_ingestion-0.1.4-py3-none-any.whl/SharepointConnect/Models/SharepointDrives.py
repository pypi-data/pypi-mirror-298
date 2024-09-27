# pylint: disable=missing-function-docstring,missing-module-docstring,missing-class-docstring,broad-exception-caught,invalid-name,line-too-long

from typing import Optional
from pydantic import BaseModel, Field
from typing import List

class SharepointDrives(BaseModel):
    drives: Optional[List] = Field(
        default=None,
        description="",
        example=[""],
    )