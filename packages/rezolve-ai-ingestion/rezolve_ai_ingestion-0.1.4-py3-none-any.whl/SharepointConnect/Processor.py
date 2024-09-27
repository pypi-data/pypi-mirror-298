from SharepointConnect.Drives import Drives
from SharepointConnect.Lists import Lists
from SharepointConnect.Sites import Sites
from SharepointConnect.Files import Files
from SharepointConnect.Pages import Pages
from SharepointConnect.WebParts import WebParts

from SharepointConnect.Authorization import Authorize
from SharepointConnect.Helpers import Differential, get_links, file_info, process_links

from datetime import datetime, timedelta, timezone

class SharePointProcessor:
    def __init__(self, request_data):
        self.request_data = request_data
        self.authorization = request_data.authorization
        self.rezolve = request_data.rezolve
        self.pages_to_ingest = request_data.pages
        self.sites = request_data.drives.sites
        self.processed_files = []
        self._initialize_processors()

    def _initialize_processors(self):
        headers = Authorize(self.authorization)
        self.process_parts = WebParts(headers)
        self.process_drives = Drives(headers)
        self.process_lists = Lists(headers)
        self.process_sites = Sites(headers)
        self.process_files = Files(headers, self.rezolve)
        self.process_pages = Pages(headers)

    def process_sharepoint(self):
        self.process_pages.main(
            self.pages_to_ingest, 
            self.process_parts, 
            self.process_drives, 
            self.process_lists, 
            self.process_sites, 
            self.process_files, 
            self.process_pages, 
            self.processed_files
        )


        all_sites = self.process_sites.all()
        root_site = self.process_sites.root()

        site_pages = self.process_pages.site(root_site)
        drives = self.process_drives.sites([root_site])
        lists = self.process_lists.sites([root_site])

        site_ids = [sit['id'] for sit in all_sites if any(site in sit['webUrl'] for site in self.sites)]
        page_ids = [this.get("id") for this in site_pages if this["name"] in self.pages_to_ingest.pages]

        links = get_links(self.process_parts, root_site, page_ids)
        found_links = process_links(links, drives, lists)

        drives.extend(self.process_drives.sites(site_ids))
        lists.extend(self.process_lists.sites(site_ids))

        files_info = file_info(self.process_drives, found_links)
        self.process_files.info(self.processed_files, files_info)

        current_time = datetime.now(timezone.utc)
        three_hours_ago = current_time - timedelta(hours=24)

        Differential(self.rezolve, three_hours_ago, self.process_files, self.processed_files)