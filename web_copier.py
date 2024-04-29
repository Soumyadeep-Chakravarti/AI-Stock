"""
Module: web_table_copy

This module provides a class to copy tables from a given website.

Classes:
    WebTableCopier: A class for copying tables from websites.

Example usage:
    if __name__ == "__main__":
        WEBSITE_URL = "https://example.com"
        OUTPUT_DIR = "tables"
        web_copier = WebTableCopier()
        web_copier.save_tables_from_url(WEBSITE_URL, OUTPUT_DIR)
"""

import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

class WebTableCopier:
    """
    WebTableCopier Class

    This class provides a method to copy tables from a given website.
    """

    def __init__(self, timeout=10):
        """
        Initialize the WebTableCopier object.

        Args:
            timeout (int, optional): The number of seconds to wait for the server to respond.
                                     Defaults to 10 seconds.
        """
        self.timeout = timeout

    def save_table_as_csv(self, table, filename):
        """
        Save a table as a CSV file.

        Args:
            table (bs4.element.Tag): The BeautifulSoup table object.
            filename (str): The file path to save the CSV file.
        """
        try:
            # Convert the table to a DataFrame
            df = pd.read_html(str(table))[0]

            # Save the DataFrame to a CSV file
            df.to_csv(filename, index=False)
            print(f"Table saved as CSV: {filename}")
        except Exception as e:
            print(f"Error saving table as CSV: {e}")

    def download_webpage(self, url, output_file):
        """
        Download the HTML content of a webpage and save it to a file.

        Args:
            url (str): The URL of the webpage to download.
            output_file (str): The file path where the webpage content will be saved.

        Returns:
            str: The HTML content of the webpage as a string, or None if the download fails.
        """
        try:
            # Send a GET request to the URL
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

            # Create the directory if it doesn't exist
            os.makedirs(os.path.dirname(output_file), exist_ok=True)

            # Save the content to the output file
            with open(output_file, "wb") as f:
                f.write(response.content)

            return response.text  # Return the HTML content
        except requests.RequestException as e:
            print(f"Error downloading the webpage: {e}")
            return None
        except IOError as e:
            print(f"Error saving the webpage content: {e}")
            return None

    def save_tables_from_url(self, url, output_dir):
        """
        Download webpage, parse tables, and save them as CSV files.

        Args:
            url (str): The URL of the webpage.
            output_dir (str): The directory to save the CSV files.
        """
        webpage_content = self.download_webpage(url, os.path.join(output_dir, "webpage.html"))
        if webpage_content is not None:  # Check if webpage content is not None
            soup = BeautifulSoup(webpage_content, 'html.parser')
            tables = soup.find_all('table')
            print(f"Found {len(tables)} tables on the webpage.")

            # Create the output directory if it doesn't exist
            if len(tables) > 1:
                os.makedirs(output_dir, exist_ok=True)

            # Save each table as a separate CSV file
            for i, table in enumerate(tables, start=1):
                if len(tables) > 1:
                    filename = os.path.join(output_dir, f"table_{i}.csv")
                else:
                    filename = os.path.join(output_dir, "table.csv")
                self.save_table_as_csv(table, filename)
        else:
            print("Failed to download the webpage.")

    
# Example usage:
if __name__ == "__main__":
    WEBSITE_URL = "https://www.topstockresearch.com/rt/Screener/Technical/PivotPoint/StandardPivotPoint/ListSupportOrResistance"
    OUTPUT_DIR = "tables"
    web_copier = WebTableCopier()
    web_copier.save_tables_from_url(WEBSITE_URL, OUTPUT_DIR)
