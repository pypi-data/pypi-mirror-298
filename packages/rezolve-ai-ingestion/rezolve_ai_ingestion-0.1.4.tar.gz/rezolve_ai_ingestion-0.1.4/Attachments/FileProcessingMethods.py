import os
import cv2
import json
import fitz  # PyMuPDF
import email
import chardet
import tempfile
import textract
import subprocess
import numpy as np
import pandas as pd
from PIL import Image
from io import BytesIO
from email import policy
from bs4 import BeautifulSoup

class FileProcessingMethods:
    """Class for handling various file processing tasks."""

    @staticmethod
    def read_plain_text(file_content: BytesIO) -> str:
        """
        Reads plain text from a file-like object and decodes it.

        Args:
            file_content (BytesIO): The file-like object containing the text.

        Returns:
            str: The decoded plain text.
        """
        raw_data = file_content.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        return raw_data.decode(encoding)

    @staticmethod
    def read_json(file_content: BytesIO) -> str:
        """
        Reads and formats JSON content from a file-like object.

        Args:
            file_content (BytesIO): The file-like object containing the JSON data.

        Returns:
            str: The formatted JSON string.
        """
        return json.dumps(json.load(file_content), indent=2)

    @staticmethod
    def read_sql(file_content: BytesIO) -> str:
        """
        Reads SQL content from a file-like object (treated as plain text).

        Args:
            file_content (BytesIO): The file-like object containing the SQL data.

        Returns:
            str: The SQL content as plain text.
        """
        return FileProcessingMethods.read_plain_text(file_content)

    @staticmethod
    def extract_text_from_email(file_content: BytesIO) -> str:
        """
        Extracts text from an email file-like object.

        Args:
            file_content (BytesIO): The file-like object containing the email.

        Returns:
            str: The extracted text from the email.
        """
        file_content.seek(0)
        msg = email.message_from_binary_file(file_content, policy=policy.default)

        text_parts = []
        for part in msg.walk():
            if part.get_content_type() == 'text/html':
                html_content = part.get_payload(decode=True)
                soup = BeautifulSoup(html_content, 'html.parser')
                text_parts.append(soup.get_text())
            elif part.get_content_type() == 'text/plain':
                text_content = part.get_payload(decode=True)
                text_parts.append(text_content.decode(part.get_content_charset() or 'utf-8', errors='replace'))

        return "\n".join(text_parts)

    @staticmethod
    def process_image_file(file_content: BytesIO) -> str:
        """
        Processes an image file-like object to extract text using OCR.

        Args:
            file_content (BytesIO): The file-like object containing the image.

        Returns:
            str: The text extracted from the image.
        """
        # Check image size
        file_content.seek(0,2)
        if file_content.tell() == 0:
            print(">>> Image size 0 skipping file...")
            return None
        
        file_content.seek(0)
        file_bytes = np.frombuffer(file_content.read(), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)

        _, thresh = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
        pil_image = Image.fromarray(thresh)

        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
            temp_filename = temp_file.name
            pil_image.save(temp_filename)

        try:
            result = subprocess.run(
                ['tesseract', temp_filename, 'stdout'],
                capture_output=True,
                text=True,
                check=True
            )
            text = result.stdout.strip()
        finally:
            os.unlink(temp_filename)

        return text

    @staticmethod
    def process_pdf_file(file_content: BytesIO) -> str:
        """
        Extracts text from a PDF file-like object.

        Args:
            file_content (BytesIO): The file-like object containing the PDF.

        Returns:
            str: The text extracted from the PDF.
        """
        temp_file_path = None

        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                temp_file.write(file_content.getbuffer())
                temp_file_path = temp_file.name

            document = fitz.open(temp_file_path)

            text = ""
            for page_num in range(len(document)):
                page = document.load_page(page_num)
                text += page.get_text()

            return text
        except Exception as e:
            print(f"Failed to process PDF file: {e}")
            return ""
        finally:
            if temp_file_path:
                try:
                    os.remove(temp_file_path)
                except Exception as e:
                    print(f"Failed to delete temporary file: {e}")

    @staticmethod
    def process_spreadsheet_file(file_content: BytesIO, file_name: str) -> str:
        """
        Processes a spreadsheet file-like object and extracts text.

        Args:
            file_content (BytesIO): The file-like object containing the spreadsheet.
            file_name (str): The name of the file, used to determine the file extension.

        Returns:
            str: The text extracted from the spreadsheet.
        """
        try:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file_name)[1])
            temp_file.write(file_content.getvalue())
            temp_file.close()

            try:
                if file_name.lower().endswith('.csv'):
                    df = pd.read_csv(temp_file.name)
                elif file_name.lower().endswith(('.xls', '.xlsx', '.xlsm', '.xlsb')):
                    df = pd.read_excel(temp_file.name, engine='openpyxl' if file_name.lower().endswith(('.xlsx', '.xlsm')) else 'xlrd')
                elif file_name.lower().endswith('.ods'):
                    df = pd.read_excel(temp_file.name, engine='odf')
                else:
                    raise ValueError("Unsupported spreadsheet format")

                df['combined'] = df.apply(lambda row: ' '.join(row.astype(str)), axis=1)
                text = ' '.join(df['combined'].tolist())
            except Exception as e:
                print(f"Pandas error: {e}")
                text = ""

            os.unlink(temp_file.name)
            return text

        except Exception as e:
            print(f"Failed to process spreadsheet file: {e}")
            return ""

    @staticmethod
    def process_presentation_file(file_content: BytesIO, file_name: str) -> str:
        """
        Extracts text from a presentation file-like object.

        Args:
            file_content (BytesIO): The file-like object containing the presentation.
            file_name (str): The name of the file, used to determine the file extension.

        Returns:
            str: The text extracted from the presentation.
        """
        try:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file_name)[1])
            temp_file.write(file_content.getvalue())
            temp_file.close()

            text = textract.process(temp_file.name).decode('utf-8')
            os.unlink(temp_file.name)
            return text
        except Exception as e:
            print(f"Failed to process presentation file: {e}")
            return ""

    @staticmethod
    def extract_text_from_certificate(file_content: BytesIO) -> str:
        """
        Extracts text from a certificate file-like object.

        Args:
            file_content (BytesIO): The file-like object containing the certificate.

        Returns:
            str: The extracted certificate details.
        """
        file_content.seek(0)
        cert_data = file_content.read()

        try:
            cert = x509.load_der_x509_certificate(cert_data, default_backend())
        except (ValueError, InvalidSignature):
            cert = x509.load_pem_x509_certificate(cert_data, default_backend())

        text = f"Subject: {cert.subject}\n"
        text += f"Issuer: {cert.issuer}\n"
        text += f"Version: {cert.version}\n"
        text += f"Serial Number: {cert.serial_number}\n"
        text += f"Not Valid Before: {cert.not_valid_before}\n"
        text += f"Not Valid After: {cert.not_valid_after}\n"

        return text
