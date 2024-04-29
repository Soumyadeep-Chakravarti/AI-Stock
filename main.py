import os

import file_downloader as fd
import web_copier as wc
import imp_items

downloader = fd.FileDownloader()
WEBSITE_URL = imp_items.website_urls[1]
OUTPUT_DIR = os.path.join(imp_items.paths[1],imp_items.formatted_today_date)
web_copier = wc.WebTableCopier()
web_copier.save_tables_from_url(WEBSITE_URL, OUTPUT_DIR)
downloader.download_and_extract(imp_items.website_urls[0],OUTPUT_DIR)
