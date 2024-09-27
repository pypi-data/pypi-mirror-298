from utils.sharepoint_functions import parse_sharepoint_url
from typing import List, Dict, Any
from urllib.parse import urlparse
import requests
import re

class Sites:
    def __init__(self, headers: Dict[str, str]):
        """
        Initialize the Sites class with the provided headers.

        :param headers: A dictionary of headers for authentication.
        """
        self.headers = headers

    def all_sites(self) -> List[Dict[str, Any]]:
        """
        Retrieve all non-personal SharePoint sites.

        :return: List of dictionaries containing site information.
        """
        all_sites = []
        url = "https://graph.microsoft.com/v1.0/sites/microsoft.graph.getAllSites()"

        sites = requests.get(url, headers=self.headers, stream=True).json()
        next_link = sites.get("@odata.nextLink")
        all_sites.extend(sites.get("value", []))

        while next_link:
            sites = requests.get(next_link, headers=self.headers, stream=True).json()
            next_link = sites.get("@odata.nextLink")
            all_sites.extend(sites.get("value", []))

        return [site for site in all_sites if site.get("isPersonalSite") == False]

    def search_by_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Search for SharePoint sites by keyword.

        :param keyword: The keyword to search for.
        :return: List of dictionaries containing site information.
        """
        url = f"https://graph.microsoft.com/v1.0/sites?search={keyword}"
        sites = requests.get(url, headers=self.headers, stream=True).json()
        return sites.get('value', [])

    def sites_selected_id(self, site_url: str) -> str:
        """
        Get the site ID for the provided SharePoint site URL.

        :param site_url: The target SharePoint site URL.
        :param sharepoint_prefix: The SharePoint prefix (e.g., the SharePoint domain without '.sharepoint.com').
        :return: The site ID as a string.
        """
        # Parse the path from the provided site URL
        path = urlparse(site_url).path
        sharepoint_prefix = urlparse(site_url).hostname.split(".")[0]
        
        # Check if the URL contains 'site' in it
        if 'site' in site_url:
            try:
                # Extract site name from the URL
                items = path.split("/sites/")[1]
                if "/" in items:
                    site_name = items.split("/")[0]
                else:
                    site_name = items

                # Construct the API URL for fetching site details
                api_url = f"https://graph.microsoft.com/v1.0/sites/{sharepoint_prefix}.sharepoint.com:/sites/{site_name}"

                # Make the GET request to fetch the site ID
                response = requests.get(api_url, headers=self.headers, stream=True)
                response.raise_for_status()  # Raise an error for bad responses

                # Extract the site ID from the response JSON
                site_id = response.json().get('id')
                if site_id:
                    return site_id
                else:
                    raise RuntimeError(f"Site ID not found for URL: {site_url}")

            except IndexError:
                raise ValueError(f"Could not parse the site name from the URL: {site_url}")
        
        else:
            raise ValueError(f"The given URL '{site_url}' is not a valid SharePoint site URL")
        
    def site_ids(self, target_sites):
        ids = set()
        # Define the regex pattern to match 'and' within words, hyphens (-), and underscores (_)
        pattern = r"(?i)(?<=\w)and(?=\w)|[-_]"

        for site in target_sites:
            host_name = urlparse(site).hostname
            info = parse_sharepoint_url(site)
            
            if info.get("type") == "site":
                keywords = re.split(pattern, info.get("site_name"))
                sites = Sites(self.headers).search_by_keyword(keywords[0])
                site_id = [site.get("id").split(',')[1] for site in sites if site.get("webUrl") == f"https://{host_name}/sites/{info.get("site_name")}"][0]
        
            elif info.get("type") == "team":
                keywords = re.split(pattern, info.get("team_name"))
                sites = Sites(self.headers).search_by_keyword(keywords[0])

            elif info.get("type") == "root":
                url = "https://graph.microsoft.com/v1.0/sites/root"
                response = requests.get(url, headers=self.headers)
                site_id = response.json().get("id").split(',')[1]
            else:
                raise ValueError(f"The given URL '{site}' is not a site URL")

            ids.add(site_id)

        return list(ids)
        