# Rezolve AI Ingestion

Rezolve AI Ingestion is a proprietary package developed by Rezolve.ai for ingesting and processing SharePoint data with AI capabilities. This package is designed for internal use within Rezolve.ai and is not intended for public distribution.

## Features

- Connect to SharePoint and retrieve data
- Process and analyze SharePoint content using AI
- Integrate with Pinecone for efficient data storage and retrieval
- Utilize OpenAI's language models for advanced text processing

## Installation

This package is not available on public package repositories. To install, clone the repository from our private Git server:

```
git clone https://your-private-repo-url.com/rezolve-ai-ingestion.git
cd rezolve-ai-ingestion
pip install -e .
```

## Usage

Here's a basic example of how to use the Rezolve AI Ingestion package:

```python
from SharepointConnect.Models.Ingest import IngestSharepoint
from SharepointConnect.Processor import SharePointProcessor

# Set up your configuration
request_data = IngestSharepoint()
request_data.authorization.azure_tid = "YOUR_TENANT_ID"
request_data.authorization.client_id = "YOUR_CLIENT_ID"
request_data.authorization.thumbprint = "YOUR_THUMBPRINT"
request_data.authorization.key = "YOUR_PRIVATE_KEY"

request_data.rezolve.index = "YOUR_PINECONE_INDEX"
request_data.rezolve.namespace = "YOUR_REZOLVE_NAMESPACE"
request_data.rezolve.environment = "YOUR_PINECONE_ENVIRONMENT"
request_data.rezolve.db_key = "YOUR_PINECONE_API_KEY"

request_data.rezolve.llm_key = "YOUR_OPENAI_API_KEY"
request_data.rezolve.embedding_model = "YOUR_EMBED_MODEL"

request_data.drives.sites = ["YOUR_SITE_URLS"]
request_data.pages.pages = ["YOUR_SITE_PAGES"]

# Process SharePoint data
processor = SharePointProcessor(request_data)
processor.process_sharepoint()
processed_files = processor.processed_files

# You can now work with the processed_files data
```

## Configuration

Ensure you have the following environment variables set or provide them in your configuration:

- TENANT_ID
- CLIENT_ID
- THUMBPRINT
- PRIVATE_KEY
- PINECONE_INDEX
- REZOLVE_NAMESPACE
- PINECONE_ENVIRONMENT
- PINECONE_API_KEY
- OPENAI_API_KEY
- EMBED_MODEL

### Windows

Save the following script as `setup_windows.ps1`:

```powershell
# Check if running as administrator
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Warning "You do not have Administrator rights to run this script!`nPlease re-run this script as an Administrator!"
    Break
}

# Install Chocolatey
Set-ExecutionPolicy Bypass -Scope Process -Force; 
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; 
iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

# Install dependencies using Chocolatey
choco install -y python3 wget gnupg2 xvfb unzip ffmpeg lame sox

# Install Tesseract OCR
choco install -y tesseract
$env:Path += ";C:\Program Files\Tesseract-OCR"
[Environment]::SetEnvironmentVariable("Path", $env:Path, [EnvironmentVariableTarget]::Machine)

# Download and install additional language data for Tesseract
$tessDataUrl = "https://github.com/tesseract-ocr/tessdata/raw/main/"
$tessDataDir = "C:\Program Files\Tesseract-OCR\tessdata"
$languages = @("eng", "deu", "fra", "spa") # Add or remove languages as needed

foreach ($lang in $languages) {
    $url = $tessDataUrl + $lang + ".traineddata"
    $output = $tessDataDir + "\" + $lang + ".traineddata"
    Invoke-WebRequest -Uri $url -OutFile $output
}

# Refresh environment variables
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Upgrade pip
python -m pip install --upgrade pip

# Install the Rezolve AI Ingestion package
pip install git+https://your-private-repo-url.com/rezolve-ai-ingestion.git

Write-Host "Installation complete. Please restart your PowerShell."

## Support

For support, please contact the internal development team at Rezolve.ai.

## License

This project is proprietary and confidential. Unauthorized copying, transferring or reproduction of the contents of this project, via any medium is strictly prohibited.

Copyright (c) 2024 Rezolve.ai. All Rights Reserved.