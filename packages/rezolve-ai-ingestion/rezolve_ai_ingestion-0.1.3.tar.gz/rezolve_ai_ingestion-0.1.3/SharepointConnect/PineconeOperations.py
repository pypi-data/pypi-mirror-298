from pinecone import Pinecone

import random
from typing import List, Dict, Any


class PineconeOperations:
    def __init__(self, pinecone_setting):
        self.long_loop_setting: int = 60
        self.pc = Pinecone(api_key=pinecone_setting.db_key)
        self.index =  self.pc.Index(host=pinecone_setting.host)
        self.namespace = pinecone_setting.namespace

    def get_vector_count_for_namespace(self) -> int:
        index_stats = self.index.describe_index_stats()
        vector_count = index_stats['namespaces'].get(self.namespace, {}).get('vector_count', 0)
        return vector_count

    def get_vector_ids_for_namespace(self) -> List[str]:
        vector_count = self.get_vector_count_for_namespace()
        vector_ids = set()
        loop_counter = 0

        while len(vector_ids) < vector_count and loop_counter < self.long_loop_setting:
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
                pass

        return list(vector_ids)

    def get_filtered_vector_ids_for_namespace(self, filter: dict ) -> List[str]:
        vector = [random.random() for _ in range(1536)]
        top_k = 9999

        query_response = self.index.query(
            namespace=self.namespace,
            top_k=top_k,
            include_values=False,
            include_metadata=False,
            vector=vector,
            filter=filter
        )

        vector_ids = [match['id'] for match in query_response['matches']]

        print(f'>>> >>> Retrieved {len(vector_ids)} vectors')
        return vector_ids

    def get_sharepoint_data_by_namespace(self) -> List[Dict[str, Any]]:
        vector_ids = self.get_vector_ids_for_namespace()
        all_vector_data = []

        batch_size = 200
        for i in range(0, len(vector_ids), batch_size):
            vector_ids_chunk = vector_ids[i:i+batch_size]
            try:
                vectors_info = self.index.fetch(ids=vector_ids_chunk, namespace=self.namespace).to_dict()['vectors']
                all_vector_data.extend(vectors_info.values())
            except Exception as e:
                pass
        try:            
            return [{"vector":vec.get('id'),"name":vec["metadata"].get('source'),"identifier":vec["metadata"].get('id')} for vec in all_vector_data if vec["metadata"].get('type') == "SharepointConnect"]
        except:
            return [{"vector":"1","name":"source","identifier":"1"}]

    def get_cherwell_data_by_namespace(self) -> List[Dict[str, Any]]:
        vector_ids = self.get_vector_ids_for_namespace()
        all_vector_data = []

        batch_size = 200
        for i in range(0, len(vector_ids), batch_size):
            vector_ids_chunk = vector_ids[i:i+batch_size]
            try:
                vectors_info = self.index.fetch(ids=vector_ids_chunk, namespace=self.namespace).to_dict()['vectors']
                all_vector_data.extend(vectors_info.values())
            except Exception as e:
                pass
        try:            
            return [{"vector":vec.get('id'),"name":vec["metadata"].get('source'),"identifier":vec["metadata"].get('id')} for vec in all_vector_data if vec["metadata"].get('ingestion_type') == "Cherwell"]
        except:
            return [{"vector":"1","name":"source","identifier":"1"}]
        
    def delete(self, ids):
        self.index.delete(ids=ids, namespace=self.namespace)


    def delete_filtered(self, filter):
        try:
            return self.index.delete(filter=filter, namespace=self.namespace)
        except:
            pass
