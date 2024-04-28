import os

import file_downloader as fd
import web_copier as wc
import imp_items
#downloader = fd.FileDownloader()
web_copier = wc.WebTableCopier()
copied_table = web_copier.copy_table(imp_items.website_urls[1], , os.path.join(imp_items.paths[1],imp_items.formatted_today_date))
#downloader.download_and_extract("https://example.com/example.zip")
