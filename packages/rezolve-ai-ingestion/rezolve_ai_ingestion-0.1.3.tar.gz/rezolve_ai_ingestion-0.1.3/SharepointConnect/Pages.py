import requests
from SharepointConnect.Sites import Sites
from SharepointConnect.Helpers import get_links, process_links, file_info

class Pages:
    def __init__(self, headers):
        self.graph_headers = headers
        self.sites = Sites(headers)
    
    @staticmethod
    def main(pages_to_ingest, process_parts, process_drives, process_lists, process_sites, process_files, process_pages, processed_files):
        root_site = process_sites.root()
        all_sites = process_sites.all()
        site_ids = [site["id"] for site in all_sites]

        site_pages = process_pages.site(root_site)
        
        if pages_to_ingest.pages is not None:
            page_ids = [this.get("id") for this in site_pages if this["name"] in pages_to_ingest.pages]
            all_links = get_links(process_parts, root_site, page_ids)

            drives = process_drives.sites([root_site])
            lists = process_lists.sites([root_site])

            drives.extend(process_drives.sites(site_ids))
            lists.extend(process_lists.sites(site_ids))

            found = process_links(all_links, drives, lists)
            files_info = file_info(process_drives, found)

            process_files.info(processed_files, files_info)
    
    def site(self, site_id):
        url = f"https://graph.microsoft.com/beta/sites/{site_id}/pages/"
        return requests.get(url, headers=self.graph_headers).json()["value"]
        