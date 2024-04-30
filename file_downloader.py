import urllib.request
import os
import zipfile
import time
import math

class FileDownloader:
    """
    FileDownloader class

    This class provides methods to download and extract files from URLs.

    Methods:
        __init__: Initializes the FileDownloader object.
        download_and_extract: Downloads a ZIP file from a URL and extracts its contents.
    """

    def __init__(self):
        """
        Initialize the FileDownloader object.
        """
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}

    def download_and_extract(self, url, target_dir, retries=3, timeout=30, verbose=False):
        """
        Download a ZIP file from the given URL and extract its contents.

        Args:
            url (str): The URL of the ZIP file.
            target_dir (str): The directory where the extracted files will be saved.
            retries (int): Number of retries in case of download failure. Defaults to 3.
            timeout (int): Timeout duration for each download attempt. Defaults to 30 seconds.
            verbose (bool): Whether to print verbose messages. Defaults to False.

        Returns:
            str: The path of the saved file.
        """
        for attempt in range(1, retries + 1):
            try:
                if verbose:
                    print(f"Attempt #{attempt} to download file from:", url)
                
                # Create a request object with custom headers
                req = urllib.request.Request(url, headers=self.headers)
                
                # Open the URL and read the content
                with urllib.request.urlopen(req, timeout=timeout) as response:
                    content = response.read()

                # Save the content to a file
                file_path = os.path.join(target_dir, os.path.basename(url))
                with open(file_path, 'wb') as f:
                    f.write(content)

                if verbose:
                    print("File downloaded successfully.")

                # Extract the contents of the ZIP file
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(target_dir)

                if verbose:
                    print("File extracted successfully.")
                
                return file_path  # Return the path of the saved file

            except Exception as e:
                print(f"Error during download attempt #{attempt}: {e}")
                if attempt < retries:
                    print("Retrying...")
                    delay = 2 ** attempt  # Exponential backoff: increase delay exponentially with each retry
                    print(f"Waiting for {delay} seconds before retrying...")
                    time.sleep(delay)
                    continue
                else:
                    print("Max retries exceeded. Download failed.")
                    break

if __name__ == "__main__":
    OUTPUT_DIR = "downloads"
    URL = "https://nsearchives.nseindia.com/content/historical/EQUITIES/2024/APR/cm29APR2024bhav.csv.zip"
    downloader = FileDownloader()
    save_path = downloader.download_and_extract(URL, OUTPUT_DIR, verbose=True)
