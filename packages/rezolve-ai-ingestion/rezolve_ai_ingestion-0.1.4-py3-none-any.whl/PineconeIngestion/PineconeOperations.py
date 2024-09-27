from PineconeIngestion.Models.PineconeConfig import PineconeConfig
from utils.text_treatment import get_text_embedding
from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta
from pinecone import Pinecone
from tqdm import tqdm
import logging
import random
import os

class PineconeOperations:
    
    def __init__(self, pinecone_config: PineconeConfig):
        self.pc = Pinecone(api_key=pinecone_config.key)
        self.index = self.pc.Index(pinecone_config.index)
        self.namespace = pinecone_config.namespace

    def get_vector_count_for_namespace(self) -> int:
        """
        Get the total number of vectors in the specified namespace.
        """
        try:
            index_stats = self.index.describe_index_stats()
            return index_stats['namespaces'].get(self.namespace, {}).get('vector_count', 0)
        except Exception as e:
            logging.error(f"Error getting vector count: {e}")
            return 0

    def get_vector_ids_for_namespace(self, long_loop_setting: int = 60) -> List[str]:
        """
        Fetch all vector IDs in the namespace using a looped query.
        """
        vector_count = self.get_vector_count_for_namespace()
        vector_ids = set()
        loop_counter = 0

        while len(vector_ids) < vector_count and loop_counter < long_loop_setting:
            loop_counter += 1
            vector_dim = 1536
            vector = [random.random() for _ in range(vector_dim)]
            top_k = 9999

            try:
                query_response = self.index.query(
                    namespace=self.namespace,
                    top_k=top_k,
                    include_values=False,
                    include_metadata=False,
                    vector=vector
                )
                vector_ids.update(match['id'] for match in query_response['matches'])
            except Exception as e:
                logging.error(f"Error querying vector IDs: {e}")

        return list(vector_ids)

    def fetch_vector_data(self, vector_ids: List[str]) -> List[Dict[str, Any]]:
        """
        Fetch vector data for a list of vector IDs in batches.
        """
        all_vector_data = []
        batch_size = 200

        for i in range(0, len(vector_ids), batch_size):
            vector_ids_chunk = vector_ids[i:i + batch_size]
            try:
                vectors_info = self.index.fetch(
                    ids=vector_ids_chunk, 
                    namespace=self.namespace
                ).to_dict()['vectors']

                all_vector_data.extend(vectors_info.values())
            except Exception as e:
                logging.error(f"Error fetching vector data: {e}")

        return all_vector_data

    def get_data_by_type(
            self, type_key: str, 
            include_metadata: bool=True, 
            top_k: int=999,
            long_loop_setting: int=60
        ) -> List[Dict[str, Any]]:
        """
        Retrieve data based on a specified metadata key and value.
        """        
        vector_count = self.get_vector_count_for_namespace()
        vectors = []
        loop_counter = 0

        while len(vectors) < vector_count and loop_counter < long_loop_setting:
            loop_counter += 1
            vector_dim = 1536
            vector = [random.random() for _ in range(vector_dim)]
            try:
                query_response = self.index.query(
                    namespace=self.namespace,
                    top_k=top_k,
                    include_values=False,
                    include_metadata=include_metadata,
                    vector=vector,
                    filter={"type": {"$eq": type_key}}
                )
                vectors.extend(query_response['matches'])
            except Exception as e:
                logging.error(f"Error querying vector IDs: {e}")

        return vectors
    def delete(self, ids: List[str], batch_size: int=100):
        """
        Delete vectors with the specified IDs from the Pinecone index.
        """
        for i in range(0, len(ids), batch_size):
            batch = ids[i:i + batch_size]
            try:
                self.index.delete(ids=batch, namespace=self.namespace)
                logging.info(f"Deleted vectors: {ids}")
            except Exception as e:
                logging.error(f"Error deleting vectors: {e}")

    def upsert_in_batches(self, vector_list: List[Dict[str, Any]], batch_size=100):
        """
        Upsert vectors in batches with progress tracking.
        """
        failed_ids = []

        with tqdm(total=len(vector_list), desc="Upserting batches", unit="vector") as pbar:
            for i in range(0, len(vector_list), batch_size):
                batch = vector_list[i:i + batch_size]
                try:
                    self.index.upsert(vectors=batch, namespace=self.namespace)
                except Exception as e:
                    failed_ids.extend([vector['id'] for vector in batch])
                    logging.error(f"Failed to upsert batch: {e}")
                
                pbar.update(len(batch))

        if failed_ids:
            with open('failed_ids.txt', 'a') as f:
                for id in failed_ids:
                    f.write(f"{id}\n")
            logging.warning(f"Failed IDs written to 'failed_ids.txt'.")

    def filter_ids(self, metadata_list: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[str], List[str]]:
        """
        Filter metadata IDs to find those that need to be upserted or deleted.
        """
        metadata_to_upsert = []
        metadata_ids = [metadata['id'] for metadata in metadata_list]
        one_day_ago_timestamp = datetime.now() - timedelta(days=1)
        
        pinecone_ids = self.get_vector_ids_for_namespace()
        pinecone_ids_set = set(pinecone_ids)

        for metadata in metadata_list:
            metadata_timestamp = datetime.fromisoformat(metadata['timestamp'])
            if metadata_timestamp > one_day_ago_timestamp:
                metadata_to_upsert.append(metadata)
        
        metadata_ids_set = set(metadata_ids)
        vectors_to_delete = list(pinecone_ids_set - metadata_ids_set)

        return metadata_to_upsert, vectors_to_delete, metadata_ids
    
    def query(
            self, 
            API_KEY: str,
            EMBED_MODEL: str,
            question: str, 
            top_k: int = 10, 
            include_values: bool = False) -> Dict[str, Any]:
        """
        Query Pinecone using a question to search the index.
        
        Args:
            question (str): The question or query text.
            top_k (int): Number of top results to return.
            include_values (bool): Whether to include vector values in the response.
        
        Returns:
            Dict[str, Any]: Query results from Pinecone.
        """
        try:
            query_response = self.index.query(
                vector=get_text_embedding(question, API_KEY, EMBED_MODEL),
                top_k=top_k,
                include_metadata=True,
                include_values=include_values,
                namespace=self.namespace
            )
            return query_response.get('matches')
        except Exception as e:
            logging.error(f"Error querying Pinecone with question '{question}': {e}")
            return {}
        