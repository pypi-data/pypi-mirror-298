from typing import List, Dict, Any, Optional
import requests
from io import BytesIO
from Attachments.FileProcessor import FileProcessor
from tqdm import tqdm

class Files:
    def __init__(self, headers):
        self.headers = headers

    def get_text(self, files: List[Dict[Any]]):
        """
        Downloads and processes the text content of files. Updates file_info with the extracted text.
        """
        failed = []
        
        # Process each file using tqdm for progress display
        with tqdm(total=len(files), desc="Processing Files", unit="attachment") as pbar:
            for file in files:
                response = requests.get(file.get("download"), headers=self.headers)
                if response.status_code == 200:
                    file_content = BytesIO(response.content)
                    file['text'] = FileProcessor.process_file_content(file_content, file.get("source"))
                    
                    # Check if file content is empty or None
                    if not file.get("text"):
                        failed.append(file)
                pbar.update()

        # Remove failed files from file_info
        for file in failed:
            files.remove(file)

        return failed
