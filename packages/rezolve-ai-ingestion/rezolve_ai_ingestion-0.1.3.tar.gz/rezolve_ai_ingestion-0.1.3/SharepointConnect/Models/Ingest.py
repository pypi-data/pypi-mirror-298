from typing import Optional
from pydantic import BaseModel, Field

from SharepointConnect.Models.SharepointDrives import SharepointDrives
from SharepointConnect.Models.RezolveInfo import RezolveInfo
from SharepointConnect.Models.AuthorizationInfo import AuthorizationInfo
from SharepointConnect.Models.SharepointPages import SharepointPages


class IngestSharepoint(BaseModel, arbitrary_types_allowed=True):
    authorization: Optional[AuthorizationInfo] = Field(default_factory=AuthorizationInfo)
    drives: Optional[SharepointDrives] = Field(default_factory=SharepointDrives)
    pages: Optional[SharepointPages] = Field(default_factory=SharepointPages)
    rezolve: Optional[RezolveInfo] = Field(default_factory=RezolveInfo)

