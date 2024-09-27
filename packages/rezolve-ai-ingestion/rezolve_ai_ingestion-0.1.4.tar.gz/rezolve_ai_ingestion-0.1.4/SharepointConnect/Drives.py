import re
import requests
from typing import List, Dict, Any
from urllib.parse import urlparse
from utils.sharepoint_functions import info_files

class Drives:
    def __init__(self, headers: Dict[str, str]):
        """
        Initialize the Drives class with the provided headers.

        :param headers: Dictionary containing authentication headers for Microsoft Graph API.
        """
        self.headers = headers

    def get_drives(self, site_ids: List[str]) -> List[Dict[str, Any]]:
        """
        Get drives for a list of site IDs.

        :param site_ids: A list of SharePoint site IDs.
        :return: A list of dictionaries containing drive information (id, name, webUrl).
        """
        drives = []
        for id in site_ids:
            url = f"https://graph.microsoft.com/v1.0/sites/{id}/drives?select=id,name,webUrl"
            drives.extend(requests.get(url, headers=self.headers, stream=True).json()['value'])
        return drives   
    
    def files(self, drive_ids: List) -> List[Dict[str, Any]]:
        """
        Retrieve the list of files from the given list of drives.

        :param drives: List of dictionaries, each containing information about a drive.
        :return: List of dictionaries, each containing information about a file.
        """
        files = []

        for drive_id in drive_ids:
            url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/root/children?expand="
            children = requests.get(url, headers=self.headers).json().get('value', [])
            
            drive_folders = [child for child in children if child.get('folder')]
            drive_files = [child for child in children if child.get('file')]

            while drive_folders:
                folder = drive_folders.pop(0)
                folder_id = folder['id']
                url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{folder_id}/children"
                children = requests.get(url, headers=self.headers).json().get('value', [])

                drive_files.extend([child for child in children if child.get('file')])
                drive_folders.extend([child for child in children if child.get('folder')])

            info_files(files, drive_files)
        
        return files
    
    def path(self, drive_id: str, path_url: str) -> Dict[str, Any]:
        """
        Retrieve metadata about an item in a drive based on its path.

        :param drive_id: The ID of the drive.
        :param path_url: The URL path to the item within the drive.
        :return: A dictionary containing metadata about the item.
        """
        parsed_url = urlparse(path_url)
        path = parsed_url.path
        url = f"https://graph.microsoft.com/beta/drives/{drive_id}/root:{path}"
        return requests.get(url, headers=self.headers).json()

