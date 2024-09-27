from SharepointConnect.Sites import Sites
from SharepointConnect.Drives import Drives
from SharepointConnect.Authorization import Authorize
from SharepointConnect.Models.Ingest import IngestSharepoint
from typing import List, Dict, Any

class SharePointAPI:
    """
    A class to interact with SharePoint sites and drives using the SharepointConnect library.

    This class takes `request_data` as input and provides a method to fetch drive files 
    associated with the given SharePoint sites.

    Attributes:
        request_data (Any): The input request data containing authorization and site information.
    """

    def __init__(self, request_data: IngestSharepoint) -> None:
        self.request_data = request_data
        self.headers = Authorize(request_data.authorization)
        self.site_processor = Sites(self.headers)
        self.drive_processor = Drives(self.headers)

    def get_drive_files(self) -> List[Dict[str, Any]]:
        """
        Fetches the files from the drives associated with the given SharePoint sites.

        Returns:
            List[Dict[str, Any]]: A list of files retrieved from the SharePoint drives.
        """

        site_ids = self.site_processor.site_ids(self.request_data.sites)
        drives = self.drive_processor.get_drives(site_ids)

        drive_ids= [drive.get("id") for drive in drives if drive.get("webUrl") in self.request_data.sites]

        files: List[Dict[str, Any]] = self.drive_processor.files(drive_ids)

        return files
