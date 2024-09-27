from typing import Optional, List
from pydantic import BaseModel, Field

# from DocumentIngestion.UploadFile import FileUpload
from SharepointConnect.Models.AuthorizationInfo import AuthorizationInfo
from PineconeIngestion.Models.PineconeConfig import PineconeConfig

class IngestSharepoint(BaseModel):
    authorization: AuthorizationInfo = Field(default_factory=AuthorizationInfo)
    pinecone_config: PineconeConfig = Field(default_factory=PineconeConfig)
    
    drives: Optional[List[str]] = Field(
        default=None,
        description="Drives that need to be ingested into pinecone.",
        example=[],
    )
    pages: Optional[List[str]] = Field(
        default=None,
        description="A list of SharePoint Page URLs you want to extract text from.",
        example=[],
    )
    sites: Optional[List[str]] = Field(
        default=None,
        description="A list of URLs of the sites you want to crawl.",
        example=[],
    )
    llm_key: str = Field(
        default=None,
        description="Embedding Model API Key",
    )
    embedding_model: str = Field(
        default=None,
        description="Embedding Model",
    )

class SharepointListing(BaseModel, arbitrary_types_allowed=True):
    authorization: Optional[AuthorizationInfo] = Field(default_factory=AuthorizationInfo)
    drives: Optional[List] = Field(
        default=None,
        description="",
        example="",
    )
    # ids: Optional[SharepointIds] = Field(default_factory=SharepointIds)
    # pages: Optional[SharepointPages] = Field(default_factory=SharepointPages)
    pinecone_config: PineconeConfig = Field(Field(default_factory=PineconeConfig))
