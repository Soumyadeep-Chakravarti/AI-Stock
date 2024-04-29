import zipfile
import io
import os
import imp_items
import requests
from requests.exceptions import RequestException

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

    def download_and_extract(self, url, target_dir, verbose=False):
        """
        Download a ZIP file from the given URL and extract its contents.

        Args:
            url (str): The URL of the ZIP file.
            target_dir (str): The directory where the extracted files will be saved.
            verbose (bool): Whether to print verbose messages. Defaults to False.

        Returns:
            str: The path of the saved file.
        """
        try:
            if verbose:
                print("Downloading file from:", url)
            # Send a GET request to the URL
            response = self.session.get(url)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

            # Extract the contents of the ZIP file
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
                # Extract the filename from the ZIP file
                extracted_filename = zip_file.namelist()[0]

                # Construct the path of the saved file
                saved_file_path = os.path.join(target_dir, extracted_filename)
                zip_file.extractall(path=target_dir)

            if verbose:
                print("File extracted successfully.")
            return saved_file_path  # Return the path of the saved file
        except RequestException as e:
            print(f"Error downloading the file: {e}")
        except zipfile.BadZipFile as e:
            print(f"Error extracting the ZIP file: {e}")


if __name__ == "__main__":
    OUTPUT_DIR = os.path.join(imp_items.paths[1], imp_items.formatted_today_date)
    downloader = FileDownloader()
    save_path = downloader.download_and_extract(
                                            imp_items.website_urls[0], OUTPUT_DIR, verbose=True
                                        )
