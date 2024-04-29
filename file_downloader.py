from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
import zipfile
import time

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
        self.driver = None

    def _create_driver(self):
        """
        Create a WebDriver instance with custom settings.

        Returns:
            WebDriver: A WebDriver instance.
        """
        # Use WebDriver Manager to automatically download and manage Chrome WebDriver binary
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode (without opening browser window)
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        return driver

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
        self.driver = self._create_driver()

        for attempt in range(1, retries + 1):
            try:
                if verbose:
                    print(f"Attempt #{attempt} to download file from:", url)
                
                self.driver.get(url)
                time.sleep(3)  # Wait for the page to load (adjust as needed)

                # Assuming the download starts automatically, wait for some time for it to complete
                time.sleep(10)  # Adjust as needed

                # Move the downloaded file to the target directory
                file_path = os.path.join(target_dir, os.path.basename(url))
                os.rename(file_path, os.path.join(target_dir, "downloaded_file.zip"))

                if verbose:
                    print("File downloaded successfully.")

                # Extract the contents of the ZIP file
                with zipfile.ZipFile(os.path.join(target_dir, "downloaded_file.zip"), 'r') as zip_ref:
                    zip_ref.extractall(target_dir)

                if verbose:
                    print("File extracted successfully.")
                
                return file_path  # Return the path of the saved file

            except (WebDriverException, zipfile.BadZipFile) as e:
                print(f"Error during download attempt #{attempt}: {e}")
                if attempt < retries:
                    print("Retrying...")
                    continue
                else:
                    print("Max retries exceeded. Download failed.")
                    break

            finally:
                # Clean up resources
                self.driver.quit()

if __name__ == "__main__":
    OUTPUT_DIR = "downloads"
    URL = "https://nsearchives.nseindia.com/content/historical/EQUITIES/2024/APR/cm29APR2024bhav.csv.zip"
    downloader = FileDownloader()
    save_path = downloader.download_and_extract(URL, OUTPUT_DIR, verbose=True)
