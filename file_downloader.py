"""
module: file_downloader

This module provides a class for downloading and extracting files from URLs.

Classes:
    FileDownloader: A class for downloading and extracting files from URLs.

Example usage:
    if __name__ == "__main__":
        downloader = FileDownloader()
        downloader.download_and_extract("https://example.com/example.zip", "/your/target/directory/path")
"""


import zipfile
import io
import requests


class FileDownloader:
    """
    file_downloader class

    This class provides methods to download and extract files from URLs.

    methods:
        __init__: Initializes the FileDownloader object.
        download_and_extract: Downloads a ZIP file from a URL and extracts its contents.
    """

    def __init__(self):
        """
        Initialize the FileDownloader object.
        """
        self.session = requests.Session()

    def download_and_extract(self, url, target_dir):
        """
        Download a ZIP file from the given URL and extract its contents.

        Args:
            url (str): The URL of the ZIP file.
            target_dir (str): The directory where the extracted files will be saved.
        """
        try:
            # Send a GET request to the URL
            response = self.session.get(url)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

            # Extract the contents of the ZIP file
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
                zip_file.extractall(path=target_dir)

            print("File extracted successfully.")
        except requests.RequestException as e:
            print(f"Error downloading the file: {e}")
        except zipfile.BadZipFile as e:
            print(f"Error extracting the ZIP file: {e}")