# This code is reliant on the code found within the "download_XBRL.ipynb" file.

import requests
from bs4 import BeautifulSoup
import os
import re
from urllib.parse import urljoin

# This function takes in a file path for the CIK JSON data.
# It will take all CIK values and use them to download all 10k files into a specified directory
def downloadAll10k(fileName):
  #Gather all CIK files from JSON
  tempUrl = ""
  download_dir = os.path.abspath("downloads")
  file = open(fileName, 'r')
  for line in file:
    loc = line.find("cik")
    if(loc == -1):
      continue
    tempCIK = line[loc + 6 : loc + 17 : 1]
    print(tempCIK)
    urls = load_10k_xbrl(tempCIK, ["2019","2020","2021","2022", "2023"]) # Years can be modified
    for item in urls:
      folder, xbrl_file = download_sec_files(item, download_dir)
      # print(f"Folder: {folder}, XBRL File: {xbrl_file}")
      pass

    
downloadAll10k("parsed_companies.json")
