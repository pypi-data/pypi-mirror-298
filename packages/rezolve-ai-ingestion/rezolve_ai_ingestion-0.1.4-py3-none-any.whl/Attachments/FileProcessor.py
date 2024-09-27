from io import BytesIO
from utils.text_treatment import clean_text
from Attachments.Documents import DocumentReader
from Attachments.AttachmentCategories import FileCategories
from Attachments.FileProcessingMethods import FileProcessingMethods

class FileProcessor:
    """Class for processing files based on their type."""

    @staticmethod
    def _process_structured_text(file_content: BytesIO, file_name: str) -> str:
        """
        Processes structured text files (e.g., JSON, SQL).

        Args:
            file_content (BytesIO): The file-like object containing the structured text.
            file_name (str): The name of the file, used to determine the file extension.

        Returns:
            str: The processed structured text.
        """
        extension = file_name.lower().split('.')[-1]
        structured_methods = {
            'json': FileProcessingMethods.read_json,
            'sql': FileProcessingMethods.read_sql
        }

        if extension in structured_methods:
            return structured_methods[extension](file_content)

        print(f"Structured text type not supported for extension {extension}")
        return None

    @staticmethod
    def process_file_content(file_content: BytesIO, file_name: str) -> str:
        """
        Processes file content based on file type.

        Args:
            file_content (BytesIO): The file-like object containing the file data.
            file_name (str): The name of the file, used to determine the file type.

        Returns:
            str: The cleaned text extracted from the file.
        """
        file_content.seek(0)  # Ensure the file pointer is at the start of the file

        extension = file_name.lower().split('.')[-1]
        file_mapping = {
            'PlainText': FileCategories.PlainText,
            'StructuredText': FileCategories.StructuredText,
            'Document': FileCategories.Document,
            'PDF': FileCategories.PDF,
            # 'Image': FileCategories.Image,
            'Presentation': FileCategories.Presentation,
            'Spreadsheet': FileCategories.Spreadsheet,
            'Email': FileCategories.Email,
            'Certificate': FileCategories.Certificate,
        }

        process_methods = {
            'PlainText': FileProcessingMethods.read_plain_text,
            'StructuredText': FileProcessor._process_structured_text,
            'Document': DocumentReader.process_file_content,
            'PDF': FileProcessingMethods.process_pdf_file,
            # 'Image': FileProcessingMethods.process_image_file,
            'Presentation': FileProcessingMethods.process_presentation_file,
            'Spreadsheet': FileProcessingMethods.process_spreadsheet_file,
            'Email': FileProcessingMethods.extract_text_from_email,
            'Certificate': FileProcessingMethods.extract_text_from_certificate,
        }

        raw_text = None
        for category, extensions in file_mapping.items():
            if any(file_name.lower().endswith(ext) for ext in extensions):
                method = process_methods[category]
                
                # Check if the method requires both file_content and file_name
                if category in ['StructuredText', 'Document', 'Presentation', 'Spreadsheet']:
                    raw_text = method(file_content, file_name)
                else:
                    raw_text = method(file_content)
                    
                break

        if raw_text is None:
            print(f"File type not supported for extension {extension}")
            return None
        raw_text = raw_text.replace("nan", "")
        return clean_text(raw_text)
    