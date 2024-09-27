import re
import requests
from urllib.parse import unquote

class Lists:
    def __init__(self, headers):
        self.graph_headers = headers
    
    def sites(self, site_ids):
        
        lists = []

        for id in site_ids:
            url = f"https://graph.microsoft.com/beta/sites/{id}?$expand=lists($select=id,name,displayName,webUrl,list)&$select=id,name,displayName,webUrl"
            response = requests.get(url, headers=self.graph_headers).json()

            list_items = [lst for lst in response.get('lists', []) if lst.get('list', {}).get('template') != 'documentLibrary']

            if list_items:
                for list in list_items:
                    lists.append(list)

        return lists
    
    @staticmethod
    def match_lists(all_links, lists, found, url):
        for list in lists:
            decoded_list = unquote(list["webUrl"])
                    
            urlObject = {}
            url_check = "https://sfbartd.sharepoint.com/" + re.sub(r'\/:[a-z]:/[a-z]/', '', url).replace("sites/Intranet/","")
            url_check = url_check.replace(".com//",".com/")
                    
            if decoded_list in url_check:
                all_links.remove(url)

                urlObject["list"] = list
                urlObject["path"] = url_check.replace(list["webUrl"],"")

                found['lists'].add(list.get("id"))
                found['links'].append(urlObject)

                break