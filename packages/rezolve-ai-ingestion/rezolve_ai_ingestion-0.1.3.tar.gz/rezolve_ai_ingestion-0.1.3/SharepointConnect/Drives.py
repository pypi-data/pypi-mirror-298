import re
import requests

from typing import List, Dict
from urllib.parse import parse_qs, unquote, urlparse

from SharepointConnect.Files import Files

class Drives:
    def __init__(self, headers):
        self.graph_headers = headers

    def main(self, sites, process_sites, process_files, processed_files, folder_path=None):
        site_ids = process_sites.ids(sites)
        drive_items = self.sites(site_ids)
        drive_ids = [drive["id"] for drive in drive_items if "PreservationHoldLibrary" not in drive["webUrl"]]
        drive_files = self.files(drive_ids, folder_path)
        processed_files.extend(process_files.filter(drive_files))

        return processed_files
    
    def sites(self, site_ids):
        drives = []
        
        for id in site_ids:
            url = f"https://graph.microsoft.com/beta/sites/{id}?$expand=drives($select=id,name,webUrl)"
            response = requests.get(url, headers=self.graph_headers).json()

            drive_items = response.get("drives")

            if drive_items:
                for drive in drive_items:
                    drives.append(drive)

        return drives

    def files(self, drives: List[Dict[str, str]], folder_path: str = None) -> List[Dict[str, str]]:
        files = []

        for drive_id in drives:
            if folder_path:
                children = self.filter_folder(drive_id, folder_path)
            else:
                url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/root/children"
                children = requests.get(url, headers=self.graph_headers).json().get('value', [])
            
            drive_folders = []
            drive_files = []
            
            if children:
                drive_files.extend([child for child in children if child.get('file')])
                drive_folders.extend([child for child in children if child.get('folder')])

            while drive_folders:
                folder = drive_folders.pop(0)
                folder_id = folder['id']

                url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{folder_id}/children"
                children = requests.get(url, headers=self.graph_headers).json().get('value', [])
                
                if children:
                    drive_files.extend([child for child in children if child.get('file')])
                    drive_folders.extend([child for child in children if child.get('folder')])

            Files.info(files, drive_files)

        return files

    def filter_folder(self, drive_id, folder_path):
        folder_path = unquote(folder_path).strip('/')
        url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root:/{folder_path}:/children"
        response = requests.get(url, headers=self.graph_headers)
        if response.status_code == 200:
            return response.json().get('value', [])
        else:
            print(f"Error fetching folder contents: {response.status_code}")
            return []
    
    def path(self, drive, path):
        url = f"https://graph.microsoft.com/beta/drives/{drive}/root:/{path}"
        return requests.get(url, headers=self.graph_headers).json()

    @staticmethod
    def match_drives(all_links, drives, found, url):
        for drive in drives:
            decoded_drive = unquote(drive["webUrl"])
                    
            check = url
            parsed_url = urlparse(check)
            query_params = parse_qs(parsed_url.query)

            if 'id' in query_params:
                check = query_params['id'][0]

            urlObject = {}

            url_check = "https://sfbartd.sharepoint.com/" + re.sub(r'\/:[a-z]:/[a-z]/', '', check).replace("sites/Intranet/","")
            url_check = url_check.replace(".com//",".com/")
                    
            if decoded_drive in url_check:
                all_links.remove(url)
                        
                urlObject["drive"] = drive
                urlObject["path"] = url_check.replace(drive["webUrl"],"")

                found['drives'].add(drive.get("id"))
                found['links'].append(urlObject)

                break