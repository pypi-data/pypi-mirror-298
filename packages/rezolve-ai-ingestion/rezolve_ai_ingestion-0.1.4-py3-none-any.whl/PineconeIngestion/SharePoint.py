from PineconeIngestion.PineconeOperations import PineconeOperations
from SharepointConnect.Models.Ingest import IngestSharepoint
from SharepointConnect.SharePointAPI import SharePointAPI
from datetime import datetime, timezone, timedelta
from utils.sharepoint_functions import get_text
from utils.text_treatment import create_vector
from tqdm import tqdm

def sync(request_data: IngestSharepoint, frequency: int) -> None:
    """
    Synchronizes SharePoint files with Pinecone. This function:
    - Fetches the files from SharePoint.
    - Identifies new and modified files to be upserted into Pinecone.
    - Deletes files from Pinecone that are no longer present in SharePoint.

    Args:
        request_data: Contains configuration details for Pinecone, SharePoint, and other necessary keys.
        frequency: How frequently the data should be considered for updating.
    """

    pine_ops = PineconeOperations(request_data.pinecone_config)
    api_manager = SharePointAPI(request_data)

    # Get the list of files from SharePoint
    files = api_manager.get_drive_files()
    print(f">>> Found {len(files)} for {request_data.authorization.sharepoint_prefix}")

    last_sync = datetime.now(timezone.utc) - timedelta(hours=frequency)

    print(">>> Getting SharePoint Data from Pinecone")
    
    pinecone_data = pine_ops.get_data_by_type("SharepointConnect")
    pinecone_article_ids = {article.get("metadata").get("article_id") for article in pinecone_data}

    print(f">>> Sync started for {request_data.pinecone_config.namespace}")

    vector_list = []

    # Process the files from SharePoint
    with tqdm(total=len(files), desc="Processing Files", unit="files") as pbar:
        for file in files:
            timestamp = datetime.fromisoformat(file.get('timestamp'))
            article_id = file.get("id")
            
            # If the article is new, retrieve the text and create vectors for it
            if article_id not in pinecone_article_ids:
                get_text(file, api_manager.headers)
                vector_list.extend(create_vector(file, request_data.llm_key, request_data.embedding_model))

            # If the article has been modified since the last sync, update it
            elif timestamp > last_sync:
                get_text(file, api_manager.headers)
                vector_list.extend(create_vector(file, request_data.llm_key, request_data.embedding_model))
            
            pbar.update()

    # Identify articles that exist in Pinecone but not in SharePoint anymore
    sharepoint_file_ids = {file.get("id") for file in files}
    to_del = [article.get("id") for article in pinecone_data if article.get("metadata").get("article_id") not in sharepoint_file_ids]

    if to_del:
        print(f">>> Deleting {len(to_del)} vectors.")
        pine_ops.delete(to_del)

    if len(vector_list) > 0:
        print(f">>> Upserting {len(vector_list)} vectors")
        pine_ops.upsert_in_batches(vector_list)
