import re
import os
import json
import requests
import tempfile
import mimetypes
import email
from bs4 import BeautifulSoup
from PIL import Image, ImageEnhance
import pytesseract
import nltk
import pandas as pd
import io
import chardet
import numpy as np

from langchain_text_splitters import NLTKTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from tempenv import TemporaryEnvironment

nltk.download("punkt", quiet=True)

try:
    import textract
except ImportError:
    print("textract is not installed. Some features may not be available.")


class Files:
    def __init__(self, headers, rezolve):
        self.graph_headers = headers
        self.text_splitter = NLTKTextSplitter(chunk_size=3500)
        self.embeddings = OpenAIEmbeddings(
            model=rezolve.embedding_model,
            openai_api_key=rezolve.llm_key,
        )
        
        self.rezolve = rezolve
     
    @staticmethod
    def get(url, name, confidence_threshold=50):
        if name and url:
            suffix = name.split(".")[-1].lower()

            response = requests.get(url, stream=True, timeout=3)
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}") as tmp_file:
                for chunk in response.iter_content(chunk_size=1024):
                    tmp_file.write(chunk)
                tmp_file.flush()

            mime_type, _ = mimetypes.guess_type(tmp_file.name)

            try:
                if mime_type and mime_type.startswith('image'):
                    text, confidence = Files.process_image(tmp_file.name)
                    if confidence < confidence_threshold:
                        print(f"Skipping low confidence image: {name} (Confidence: {confidence:.2f})")
                        return ""
                elif suffix in ['xlsx', 'xls']:
                    text = Files.process_excel(tmp_file.name)
                elif suffix in ['mht', 'mhtml']:
                    text = Files.process_mht(tmp_file.name)
                elif suffix in ['bat', 'cmd', 'ps1', 'sh', 'bash', 'zsh', 'fish']:
                    text = Files.process_script(tmp_file.name)
                else:
                    text = textract.process(tmp_file.name).decode('utf-8')

                return text
            except Exception as e:
                print(f"Error processing file {name}: {e}")
                return ""
            finally:
                os.remove(tmp_file.name)

        return ""

    @staticmethod
    def process_image(file_path):
        try:
            with Image.open(file_path) as img:
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(1.5)

                enhancer = ImageEnhance.Sharpness(img)
                img = enhancer.enhance(1.5)

                data = pytesseract.image_to_data(img, lang='eng', output_type=pytesseract.Output.DICT)

                confidences = [conf for conf in data['conf'] if conf > 0]
                avg_confidence = np.mean(confidences) if confidences else 0

                text = ' '.join([word for word in data['text'] if word.strip()])

                return text, avg_confidence
        except Exception as e:
            print(f"Error processing image file: {e}")
            return "", 0

    @staticmethod
    def process_excel(file_path):
        try:
            xls = pd.ExcelFile(file_path)
            sheets = xls.sheet_names

            all_text = []
            for sheet in sheets:
                df = pd.read_excel(file_path, sheet_name=sheet)
                
                buffer = io.StringIO()
                df.to_csv(buffer, index=False)
                text = buffer.getvalue()
                
                all_text.append(f"Sheet: {sheet}\n{text}\n")

            return "\n".join(all_text)
        except Exception as e:
            print(f"Error processing Excel file: {e}")
            return ""

    @staticmethod
    def process_mht(file_path):
        try:
            with open(file_path, 'rb') as f:
                msg = email.message_from_binary_file(f)

            text_parts = []
            for part in msg.walk():
                if part.get_content_type() == 'text/html':
                    html_content = part.get_payload(decode=True)
                    soup = BeautifulSoup(html_content, 'html.parser')
                    text_parts.append(soup.get_text())
                elif part.get_content_type() == 'text/plain':
                    text_parts.append(part.get_payload(decode=True).decode())

            return "\n".join(text_parts)
        except Exception as e:
            print(f"Error processing MHT file: {e}")
            return ""

    @staticmethod
    def process_script(file_path):
        try:
            with open(file_path, 'rb') as f:
                raw_content = f.read()
            
            detected = chardet.detect(raw_content)
            encoding = detected['encoding']

            content = raw_content.decode(encoding)

            cleaned_content = re.sub(r'[\r\n]+', '\n', content)
            cleaned_content = re.sub(r'[\t ]+', ' ', cleaned_content)

            return cleaned_content
        except Exception as e:
            print(f"Error processing script file: {e}")
            return ""

    def split(self, text):    
        if text:
            try:
                text = text.decode("utf-8")
            except (UnicodeDecodeError, AttributeError):
                pass
            text = " ".join([line for line in text.strip().split("\n") if line.strip() and line.count(".") <= 10])
            return self.text_splitter.split_text(text) 

    def upload(self, file, chunks, vectorstore):
        documents_with_meta = self.text_splitter.create_documents(texts=chunks, metadatas=[file for _ in chunks])
        
        with TemporaryEnvironment(
            {
                'PINECONE_API_KEY': self.rezolve.db_key,
                'PINECONE_ENVIRONMENT': self.rezolve.environment
            }
        ):
            vectorstore.from_documents(
                index_name=self.rezolve.index, 
                documents=documents_with_meta,
                embedding=self.embeddings,
                namespace=self.rezolve.namespace,
                pinecone_api_key=self.rezolve.db_key
            )

    def process(self, files):
        
        #vectorstore = PineconeVectorStore(self.rezolve.index, self.embeddings, self.rezolve.namespace)
             
        with TemporaryEnvironment(
            {
                'PINECONE_API_KEY': self.rezolve.db_key,
                'PINECONE_ENVIRONMENT': self.rezolve.environment
            }
        ):
            
            vectorstore = PineconeVectorStore(
                index_name = self.rezolve.index, 
                embedding = self.embeddings, 
                namespace = self.rezolve.namespace,
                pinecone_api_key=self.rezolve.db_key
            )
            
            for file in files:
                    url = file.get('download')
                    name = file.get('source')
                    
                    text = self.get(url, name)
                    if text:
                        chunks = self.split(text)
                        self.upload(file, chunks, vectorstore)
                    else:
                        print(f"Skipping file due to low confidence or empty text: {name}")




    @staticmethod    
    def info(files, drive_files):
        for file in drive_files:
            item = {
                "download": file.get("@microsoft.graph.downloadUrl"),
                "modified": file.get("lastModifiedDateTime"),
                "scope": json.dumps(file.get("shared", None)),
                "id": file.get("id"),
                "source": file.get("name"),
                "file_name": file.get("name"),
                "view_url": file.get("webUrl"),
                "url": file.get("webUrl"),
                "type": "SharepointConnect"
            }
            files.append(item)
            
    @staticmethod
    def filter(file_objects):
        pattern = re.compile(r'.*[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}.*\d{4}-\d{2}-\d{2}.*\.(pdf|png|jpg|jpeg|docx)', re.IGNORECASE)
        
        non_matching_files = [file for file in file_objects if not pattern.search(file['source'])]
        return non_matching_files