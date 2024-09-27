import requests

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