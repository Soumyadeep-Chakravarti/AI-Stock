"""
Module: company_data_processor

This module provides a class for merging and saving company data from two CSV files.

Classes:
    CompanyDataProcessor: A class for merging and saving company data from two CSV files.

Example usage:
    from company_data_processor import CompanyDataProcessor

    # Create an instance of CompanyDataProcessor
    processor = CompanyDataProcessor("file1.csv", "file2.csv", "common_column")

    # Merge and save the data
    processor.merge_and_save()
"""

import csv
import os

import imp_items

class CompanyDataProcessor:
    """
    A class to merge and save company data from two CSV files.

    Attributes:
        file1_path (str): The file path of the first CSV file.
        file2_path (str): The file path of the second CSV file.
        common_column (str): The common column used for merging the data.
    """

    def __init__(self, file1_path, file2_path):
        """
        Initialize the CompanyDataProcessor object.

        Args:
            file1_path (str): The file path of the first CSV file.
            file2_path (str): The file path of the second CSV file.
        """
        self.file1_path = file1_path
        self.file2_path = file2_path
        self.output_dir = imp_items.paths[3]


    def merge_and_save(self):
        """
        Merge the data from two CSV files and save it for each company.

        Args:
            output_dir (str): The directory where the merged CSV files will be saved.
                              Defaults to "company_data".
        """
        try:
            # Create the output directory if it doesn't exist
            os.makedirs(self.output_dir, exist_ok=True)

            # Load the CSV files
            data1 = self.load_csv(self.file1_path)
            data2 = self.load_csv(self.file2_path)

            # Merge the data
            merged_data = self.merge_data(data1, data2)

            # Save merged data for each company
            for company, company_data in merged_data.items():
                output_file_path = os.path.join(self.output_dir, f"{company}.csv")
                self.save_to_csv(company_data, output_file_path)
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        except csv.Error as e:
            print(f"CSV error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def merge_data(self, data1, data2):
        """
        Merge the data from two dictionaries based on a common column.

        Args:
            data1 (dict): The data from the first CSV file.
            data2 (dict): The data from the second CSV file.

        Returns:
            dict: A dictionary containing merged data for each company.
        """
        merged_data = {}
        try:
            for symbol in data1['SYMBOL']:
                if symbol in data2['Name']:
                    merged_data[symbol] = {
                        'Company Name': symbol,
                        'Series': data1['SERIES'][data1['SYMBOL'].index(symbol)],
                        'OPEN': data1['OPEN'][data1['SYMBOL'].index(symbol)],
                        'HIGH': data1['HIGH'][data1['SYMBOL'].index(symbol)],
                        'LOW': data1['LOW'][data1['SYMBOL'].index(symbol)],
                        'CLOSE': data1['CLOSE'][data1['SYMBOL'].index(symbol)],
                        'LAST': data1['LAST'][data1['SYMBOL'].index(symbol)],
                        'PREVCLOSE': data1['PREVCLOSE'][data1['SYMBOL'].index(symbol)],
                        'TOTTRDQTY': data1['TOTTRDQTY'][data1['SYMBOL'].index(symbol)],
                        'TOTTRDVAL': data1['TOTTRDVAL'][data1['SYMBOL'].index(symbol)],
                        'TIMESTAMP': data1['TIMESTAMP'][data1['SYMBOL'].index(symbol)],
                        'TOTALTRADES': data1['TOTALTRADES'][data1['SYMBOL'].index(symbol)],
                        'ISIN': data1['ISIN'][data1['SYMBOL'].index(symbol)],
                        'Current Price': data2['Current Price'][data2['Name'].index(symbol)],
                        'S3': data2['S3'][data2['Name'].index(symbol)],
                        'S2': data2['S2'][data2['Name'].index(symbol)],
                        'S1': data2['S1'][data2['Name'].index(symbol)],
                        'Pivot': data2['Pivot'][data2['Name'].index(symbol)],
                        'R1': data2['R1'][data2['Name'].index(symbol)],
                        'R2': data2['R2'][data2['Name'].index(symbol)],
                        'R3': data2['R3'][data2['Name'].index(symbol)]
                    }
        except KeyError as e:
            print(f"KeyError: {e}")
        except Exception as e:
            print(f"An unexpected error occurred during data merge: {e}")
        return merged_data

    def save_to_csv(self, data, file_path):
        """
        Save the data to a CSV file.

        Args:
            data (dict): The data to be saved.
            file_path (str): The file path of the CSV file.
        """
        try:
            # Check if the file exists
            file_exists = os.path.isfile(file_path)
            with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=data.keys())
                # Write the header only if the file doesn't exist
                if not file_exists:
                    writer.writeheader()
                writer.writerow(data)
        except IOError as e:
            print(f"IOError: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while saving to CSV: {e}")


    def load_csv(self, file_path):
        """
        Load data from a CSV file into a dictionary.

        Args:
            file_path (str): The file path of the CSV file.

        Returns:
            dict: A dictionary containing the data from the CSV file.
        """
        data = {}
        try:
            with open(file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    for key, value in row.items():
                        if key not in data:
                            data[key] = []
                        data[key].append(value)
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        except IOError as e:
            print(f"IOError: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while loading CSV: {e}")
        return data
