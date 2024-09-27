import requests
from typing import Dict, Any, Optional

class Pages:
    def __init__(self, headers: Dict[str, str]):
        """
        Initialize the Pages class with the provided headers.

        :param headers: Dictionary containing authentication headers for Microsoft Graph API.
        """
        self.graph_headers = headers

    def site(self, site_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve pages for a specific SharePoint site using Microsoft Graph API.

        :param site_id: The ID of the SharePoint site.
        :return: A dictionary containing the site's pages, or None if an error occurs.
        """
        try:
            url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/pages/"
            response = requests.get(url, headers=self.graph_headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching site pages: {e}")
            return None
