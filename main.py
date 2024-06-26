import os
import threading
import data_formating as data_format
import file_downloader as fd
import web_copier as wc
import imp_items
import GUI

OUTPUT_DIR = os.path.join(imp_items.paths[1], imp_items.formatted_today_date)
second_OUTPUT_DIR = os.path.join(imp_items.paths[1], imp_items.formatted_yestrday_date)
WEBSITE_URL = imp_items.website_urls[1]

# Define functions for file downloading and HTML copying
def file(path_dir):
    downloader = fd.BhavcopyDownloader(path_dir)
    return downloader.download_bhavcopy_data()

def html_copy():
    web_copier = wc.WebTableCopier()
    web_copier.save_tables_from_url(WEBSITE_URL, OUTPUT_DIR)

# Run the file and HTML copying processes simultaneously
if __name__ == "__main__":
    # Create threads for each process
    file_thread = threading.Thread(target=file)
    html_copy_thread = threading.Thread(target=html_copy)

    # Start both threads
    file_thread.start()
    html_copy_thread.start()

    # Wait for both threads to finish
    file_thread.join()
    html_copy_thread.join()

    # After both threads have finished, merge and save the data
    path1 = file(OUTPUT_DIR)
    if path1 is None:
        path1 = file(second_OUTPUT_DIR)
    processor = data_format.CompanyDataProcessor(path1, os.path.join(OUTPUT_DIR, 'table.csv'))
    processor.merge_and_save()
    GUI.main()
