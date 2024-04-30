"""
Bhavcopy Downloader Module

This module provides a class, BhavcopyDownloader, to download Bhavcopy data for a specified time period
and save it to a specified directory.

Classes:
    BhavcopyDownloader: A class to download Bhavcopy data for a specified time period.

Usage:
    1. Import the BhavcopyDownloader class from this module.
    2. Create an instance of BhavcopyDownloader with the desired save path.
    3. Call the download_bhavcopy_data() method to download Bhavcopy data for the specified time period.

Example:
    from bhavcopy_downloader import BhavcopyDownloader

    # Set the save path for Bhavcopy data
    save_path = "/path/to/save/data"

    # Create an instance of BhavcopyDownloader
    downloader = BhavcopyDownloader(save_path)

    # Download Bhavcopy data
    downloaded_file_path = downloader.download_bhavcopy_data()
    print("Bhavcopy data downloaded and saved at:", downloaded_file_path)
"""

import os
import imp_items
import bhavcopy

class BhavcopyDownloader:
    """
    A class to download Bhavcopy data for a specified time period.

    Attributes:
        save_path (str): The directory path where Bhavcopy data will be saved.
    """

    def __init__(self, path):
        """
        Initialize the BhavcopyDownloader class with the specified save path.

        Args:
            path (str): The directory path where Bhavcopy data will be saved.
        """
        self.save_path = path

    def download_bhavcopy_data(self):
        """
        Download Bhavcopy data for the specified time period and save it to the specified path.

        Returns:
            str: The file path of the downloaded Bhavcopy data.
        """
        if not self.save_path:
            raise ValueError("Save path not set. Please set the save path using set_save_path method.")

        # Define wait time in seconds to avoid getting blocked
        wait_time = [1, 2]

        # Place where data needs to be stored
        data_storage = os.path.abspath(self.save_path)

        # Create the data storage directory if it doesn't exist
        if not os.path.exists(data_storage):
            os.makedirs(data_storage)

        # Print current working directory before changing
        print("Current working directory before change:", os.getcwd())

        # Change the current working directory to the specified save path
        os.chdir(data_storage)
        print("Current working directory after change:", os.getcwd())

        # Instantiate Bhavcopy class for equities, indices, and derivatives
        nse_equities = bhavcopy.bhavcopy('equities', imp_items.yesterday_date, imp_items.today_date, data_storage, wait_time)
        nse_equities.get_data()

        file_path = os.path.join(data_storage,'equities.csv')

        return file_path

if __name__ == "__main__":
    save_path = input("Enter the save path for Bhavcopy data: ")
    downloader = BhavcopyDownloader(save_path)
    downloaded_file_path = downloader.download_bhavcopy_data()
    print("Bhavcopy data downloaded and saved at:", downloaded_file_path)
