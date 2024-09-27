import urllib.parse
import requests
from typing import List, Dict, Optional
from bs4 import BeautifulSoup

class WebParts:
    def __init__(self, headers: Dict[str, str]):
        """
        Initialize the WebParts class with the provided headers.

        :param headers: Dictionary containing authentication headers for Microsoft Graph API.
        """
        self.graph_headers = headers

    @staticmethod
    def links(web_parts: List[Optional[str]]) -> List[str]:
        """
        Extract and decode all links from a list of web part HTML content.

        :param web_parts: List of HTML content from web parts.
        :return: List of decoded URLs found in the HTML content.
        """
        all_links = []

        for html in web_parts:
            if html:
                soup = BeautifulSoup(html, "html.parser")
                links = [link["href"] for link in soup.find_all("a", href=True)]
                decoded_links = [urllib.parse.unquote(link) for link in links]
                all_links.extend(decoded_links)

        return all_links

    def page(self, site_id: str, page_id: str) -> List[str]:
        """
        Retrieve the inner HTML content of web parts on a specific SharePoint page.

        :param site_id: The ID of the SharePoint site.
        :param page_id: The ID of the SharePoint page.
        :return: List of inner HTML strings from the web parts on the page.
        """
        url = f"https://graph.microsoft.com/beta/sites/{site_id}/pages/{page_id}/microsoft.graph.sitepage/webparts"
        response = requests.get(url, headers=self.graph_headers).json()
        return [part["innerHtml"] for part in response.get("value", []) if part.get("innerHtml")]
