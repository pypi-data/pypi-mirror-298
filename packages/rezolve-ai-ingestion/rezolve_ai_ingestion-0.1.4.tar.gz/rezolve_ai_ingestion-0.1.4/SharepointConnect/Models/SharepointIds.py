from typing import Optional
from pydantic import BaseModel, Field
from typing import List

class SharepointIds(BaseModel):
    site_ids: Optional[List] = Field(
        default=None,
        description="",
        example="",
    )