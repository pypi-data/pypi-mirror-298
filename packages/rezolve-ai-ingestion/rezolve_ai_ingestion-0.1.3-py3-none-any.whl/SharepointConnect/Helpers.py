from datetime import datetime
import pandas as pd
import json
import os

from SharepointConnect.Drives import Drives
from SharepointConnect.Lists import Lists
from SharepointConnect.PineconeOperations import PineconeOperations


def file_info(process_drives, found):
    files = []

    try:
        for link in found["links"]:
            files.append(process_drives.path(link["drive"]["id"], link["path"]))
    except:
        pass
    
    return files

def get_links(process_parts, root_site, page_ids):
    all_links = []

    for page_id in page_ids:
        parts = process_parts.page(root_site, page_id)
        links = process_parts.links(parts)
        all_links.extend(links)
    return all_links

def process_links(all_links, drives, lists):
    found = {"drives": set(), "lists": set(), "links": []}

    sites_start = 0; sites_left = 1

    while sites_start != sites_left:
        sites_start = len(all_links)

        for url in all_links:
            Drives.match_drives(all_links, drives, found, url)
            Lists.match_lists(all_links, lists, found, url)
            
        sites_left = len(all_links)
    return found


def remove_duplicates_keep_newest(df, duplicate_col, date_col):
    df_sorted = df.sort_values(by=[duplicate_col, date_col], ascending=[True, False])
    
    df_deduplicated = df_sorted.drop_duplicates(subset=duplicate_col, keep='first')
    
    df_deduplicated = df_deduplicated.reset_index(drop=True)
    
    return df_deduplicated

def DeduplicateFiles(processed_files, namespace):
    df = pd.DataFrame(processed_files)

    duplicate_check_one = 'id'
    duplicate_check_two = 'file_name'
    date_column = "modified"

    df_result = remove_duplicates_keep_newest(df, duplicate_check_one, date_column)
    df_result = remove_duplicates_keep_newest(df_result, duplicate_check_two, date_column)

    keys_to_remove = ['download', 'type', 'view_url', 'source']  
    df_result = df_result.drop(columns=keys_to_remove, errors='ignore')

    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    home_directory = os.path.expanduser("~")
    folder_path = os.path.join(home_directory, namespace)

    os.makedirs(folder_path, exist_ok=True)
    output_file = f'{current_datetime} - With Duplicate Files Removed.xlsx'
    output_path = os.path.join(folder_path, output_file)

    df_result.to_excel(output_path, index=False, header=True)

    return json.loads(df_result.to_json(orient='records'))



def Differential(rezolve, three_hours_ago, process_files, processed_files):

    json_data = DeduplicateFiles(processed_files, rezolve.namespace)
    
    pine_ops = PineconeOperations(rezolve)
    existing = pine_ops.get_sharepoint_data_by_namespace()

    existing_ids = list(set([file["identifier"] for file in existing]))
    new_ids = list(set([file["id"] for file in json_data]))

    to_remove = [id for id in existing_ids if id not in new_ids]
    to_add = [id for id in new_ids if id not in existing_ids]

    recent_objects = [
        obj for obj in json_data
        if datetime.fromisoformat(obj['modified'].replace('Z', '+00:00')) >= three_hours_ago
    ]

    recent_ids = [file['id'] for file in recent_objects]

    to_remove.extend(recent_ids)
    to_add.extend(recent_ids)

    remove_ids = [id['vector'] for id in existing if id['identifier'] in to_remove]
    add_files = [file for file in json_data if file['id'] in to_add]

    if remove_ids:

        batch_size = 999
        for i in range(0, len(remove_ids), batch_size):
            batch = remove_ids[i:i + batch_size]
            pine_ops.delete(batch)
    
    if add_files:
        process_files.process(add_files)


        

