import urllib
import requests
from bs4 import BeautifulSoup


class WebParts:
    def __init__(self, headers):
        self.graph_headers = headers

    @staticmethod
    def links(web_parts):
        all_links = []

        for html in web_parts:
            if html is not None:
                soup = BeautifulSoup(html, "html.parser")

                links = [link["href"] for link in soup.find_all("a", href=True)]
                decoded_links = [urllib.parse.unquote(link) for link in links]
                all_links.extend(decoded_links)

        return all_links

    def page(self, site_id, page_id):
        url = f"https://graph.microsoft.com/beta/sites/{site_id}/pages/{page_id}/microsoft.graph.sitepage/webparts"
        response = requests.get(url, headers=self.graph_headers).json()

        return [part["innerHtml"] for part in response["value"] if part.get("innerHtml")]
    