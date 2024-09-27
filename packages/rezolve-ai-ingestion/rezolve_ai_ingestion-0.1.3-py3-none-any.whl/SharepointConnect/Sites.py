import requests
from urllib.parse import urlparse

class Sites:
    def __init__(self, headers):
        self.graph_headers = headers

    def all(self):
        
        all_sites = []

        url = "https://graph.microsoft.com/beta/sites"

        sites = requests.get(url, headers=self.graph_headers, stream=True).json()
        next = sites.get("@odata.nextLink")
        all_sites.extend(sites["value"])

        while next:
            sites = requests.get(next, headers=self.graph_headers, stream=True).json()
            next = sites.get("@odata.nextLink")
            all_sites.extend(sites["value"])

        return [site for site in all_sites if site["isPersonalSite"] is False]

    def root(self):
      url = "https://graph.microsoft.com/v1.0/sites/root"
      return requests.get(url, headers=self.graph_headers).json().get("id")       
    
    def ids(self,sites):
      collect = []

      for site in sites:
        parsed = urlparse(site)
        netloc = parsed.netloc
        path = (urlparse(site).path).replace("/sites/","")

        url = f"https://graph.microsoft.com/v1.0/sites/{netloc}:/sites/{path}?$select=id"
        id = requests.get(url, headers=self.graph_headers).json().get("id")
        collect.append(id)

      return collect

    def id(self,site):
        netloc = urlparse(site).netloc
        path = (urlparse(site).path).replace("/sites/","")

        url = f"https://graph.microsoft.com/v1.0/sites/{netloc}:/sites/{path}?$select=id"
        
        return requests.get(url, headers=self.graph_headers).json().get("id")

