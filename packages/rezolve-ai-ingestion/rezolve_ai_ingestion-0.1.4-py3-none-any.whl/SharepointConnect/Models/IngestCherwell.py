from typing import Optional
from pydantic import BaseModel, Field

from SharepointConnect.Models.CherwellAuthorization import CherwellAuthorization
from SharepointConnect.Models.CherwellStoredSearch import CherwellStoredSearch
from PineconeIngestion.Models import PineconeConfig

class IngestCherwell(BaseModel, arbitrary_types_allowed=True):
    authorization: Optional[CherwellAuthorization] = Field(default_factory=CherwellAuthorization)
    stored_search: Optional[CherwellStoredSearch] = Field(default_factory=CherwellStoredSearch)
    pinecone_settings: Optional[PineconeConfig] = Field(default_factory=PineconeConfig)