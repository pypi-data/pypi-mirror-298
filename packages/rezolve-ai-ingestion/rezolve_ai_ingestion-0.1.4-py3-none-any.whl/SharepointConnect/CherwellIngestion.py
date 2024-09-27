import requests

class CherwellIngestion:
    def __init__(self, headers):
        self.headers = headers
        self.ingested = {'Article Titles': [], 'URLs': []}
        self.items = []

    def stored(self, stored_search):
        response = requests.get(stored_search.stored_search, headers=self.headers)

        for business_object in response.json():

            item = {}

            text = business_object['Body Text']
            text = text.replace(u"\xa0", "")

            item["public_id"] = business_object['Article ID']
            item["file"] = text
            item["text"] = text
            item["source"] = business_object['Title']
            item["file_name"] = business_object['Title']
            item["type"] = 'CherwellConnect'
            item["file_last_modified_datetime"] = business_object.get('Last Modified', 'Unavailable')
            item["view_url"] = business_object.get('TangoArticle') if business_object.get('TangoArticle') else f'{stored_search.view_url_prefix}{item["public_id"]}'

            self.items.append(item)
            self.ingested['Article Titles'] += [item["source"]]
            self.ingested['URLs'] += [item["view_url"]]