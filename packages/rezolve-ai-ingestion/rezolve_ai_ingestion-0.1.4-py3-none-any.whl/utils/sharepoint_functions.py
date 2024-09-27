from Attachments.FileProcessor import FileProcessor
from typing import Dict, Union, List, Any
from urllib.parse import urlparse
from io import BytesIO
import requests

def parse_sharepoint_url(url: str) -> Dict[str, Union[str, None]]:
    """
    Determine the type of SharePoint URL and extract relevant components.

    Parameters:
    url (str): The SharePoint URL to be analyzed.

    Returns:
    Dict[str, Union[str, None]]: A dictionary containing the type of SharePoint
    entity ('site', 'team', or 'root'), the corresponding name (site or team),
    and the drive or folder path if applicable. The dictionary will contain 
    `None` for values that are not applicable.
    """
    path = urlparse(url).path

    # Check the leading part of the path to determine its type
    if path.startswith("/sites/"):
        parts = path.split("/")
        site_name = parts[2]
        drive_or_folder = "/".join(parts[3:]) if len(parts) > 3 else None
        return {"type": "site", "site_name": site_name, "drive_or_folder": drive_or_folder}

    elif path.startswith("/teams/"):
        parts = path.split("/")
        team_name = parts[2]
        drive_or_folder = "/".join(parts[3:]) if len(parts) > 3 else None
        return {"type": "team", "team_name": team_name, "drive_or_folder": drive_or_folder}
    
    else:
        # Root level folders or paths
        return {"type": "root", "drive_or_folder": path.lstrip("/")}
    
def get_text(file: Dict, headers: Dict[str, str]):
    """
    Downloads and processes the text content of a file. Updates file_info with the extracted text.
    """
    response = requests.get(file.get("download"), headers=headers)
    if response.status_code == 200:
        file_content = BytesIO(response.content)
        file['text'] = FileProcessor.process_file_content(file_content, file.get("source"))                

def info_files(files: List[Dict[str, Any]], drive_files: List[Dict[str, Any]]) -> None:
    """
    Append file information from drive files to the files list.

    :param files: List to which file information will be appended.
    :param drive_files: List of drive files containing metadata.
    """
    for file in drive_files:
        item = {
            "download": file.get("@microsoft.graph.downloadUrl"),
            "timestamp": file.get("lastModifiedDateTime"),
            "id": file.get("id"),
            "source": file.get("name"),
            "url": file.get("webUrl"),
            "type": "SharepointConnect"
        }
        files.append(item)
