"""
Created on Fri Oct  4 18:56:17 2024

@author: Henry
"""

import requests
from xml.etree import ElementTree

def get_cik(ticker):
    company_name = ticker
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8'
    })

    base_url = "https://www.sec.gov/cgi-bin/browse-edgar"
    params = {
        "action": "getcompany",
        "CIK": ticker,
        "output": "xml"
    }

    response = session.get(base_url, params=params)

    print(f"URL used for request: {response.url}")
    print(f"Response Status Code: {response.status_code}")

    if response.status_code == 200:
        root = ElementTree.fromstring(response.content)
        cik_element = root.find('.//CIK')
        if cik_element is not None:
            if company_name == 'shortName not found':
                company_name = root.find('.//name').text
            return cik_element.text, company_name
        else:
            return "CIK not found", company_name
    else:
        return "Request failed with status code " + str(response.status_code), company_name

# # Example usage
ticker_symbol = "META"
cik_number, company_name = get_cik(ticker_symbol)
print(f"CIK Number for {company_name}: {cik_number}")
print(f"Ticker Symbol for {company_name}: {ticker_symbol}")
import requests
from bs4 import BeautifulSoup

def load10k_xbrl(cik_num=None):
    if cik_num is None:
        print("CIK number is required.")
        return []

    url_to_all_10k = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik_num}&type=10-K&dateb=&owner=include&count=40&search_text="


    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8'
    }

    try:
        response = requests.get(url_to_all_10k, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', class='tableFile2')

        if table:
            full_links = []
            for row in table.find_all('tr')[1:]:  # Skipping the header row
                cols = row.find_all('td')
                if len(cols) > 3:
                    filing_type = cols[0].text.strip()
                    filing_date = cols[3].text.strip()

                    if filing_type == '10-K':
                        doc_link = cols[1].find('a', href=True)['href']
                        full_links.append(f"https://www.sec.gov{doc_link}"/)
            if full_links:
                return full_links
            else:
                print("No 10-K filings.")
                return []
        else:
            print("No table found on the SEC page.")
            return []
    except requests.RequestException as e:
        print(f"Network error: {e}")
        return []

# # Example usage
urls = load_10k_xbrl('0000320193')
print(urls)

import requests
from bs4 import BeautifulSoup
import os
import re
from urllib.parse import urljoin

# Function to get XBRL file links from the given SEC page link
def get_xbrl_links(link):
    session = requests.Session()  # Start a new session
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }
    session.headers.update(headers)  # Set headers for the session

    response = session.get(link)  # Get the content of the SEC page
    print(f"Accessing URL: {link}")
    print(f"Status Code: {response.status_code}")

    file_links = []  # List to store the XBRL file links
    folder_name = None

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')  # Parse the page content

        for a_tag in soup.find_all('a', href=True):
            file_link = urljoin(link, a_tag['href'])  # Create full URL for the file link

            if file_link.endswith(('.xml', '.xsd')):  # Check if the link is a downloadable file
                print(f"Found file link: {file_link}")
                folder_name_new = file_link.split('/')[-1]
                folder_name_new = re.split(r'[._]', folder_name_new)[0]

                if folder_name is None:
                    folder_name = folder_name_new

                file_links.append(file_link)  # Add the file link to the list
    else:
        print("Failed to retrieve the webpage")

    return file_links, folder_name

# Function to download a file given its link
def download_file(session, file_link, folder_name):
    for attempt in range(3):  # Try to download up to 3 times
        file_response = session.get(file_link)
        if file_response.status_code == 200:
            file_name = file_link.split('/')[-1]
            file_path = os.path.join(folder_name, file_name)
            with open(file_path, 'wb') as file:
                file.write(file_response.content)  # Write the file content
            print(f"Downloaded: {file_path}")
            return file_path
        else:
            print(file_response.status_code)
            print(f"Failed to download file: {file_link} (Attempt {attempt + 1})")
    return None

# Main function to handle the downloading of SEC files
def download_sec_files(link, download_dir):
    file_links, folder_name = get_xbrl_links(link)  # Get XBRL links

    if not file_links:
        print("No files to download")
        return folder_name, None

    session = requests.Session()  # Start a new session
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }
    session.headers.update(headers)  # Set headers for the session

    if not os.path.exists(os.path.join(download_dir, folder_name)):
        os.makedirs(os.path.join(download_dir, folder_name))  # Create folder if it doesn't exist

    xbrl_name = None

    for file_link in file_links:
        downloaded_file_path = download_file(session, file_link, os.path.join(download_dir, folder_name))
        if downloaded_file_path and '_htm.xml' in downloaded_file_path:
            xbrl_name = downloaded_file_path  # Update xbrl_name if the file is the main XBRL file

    return folder_name, xbrl_name

# Example usage
# download_dir = os.path.abspath("downloads")  # Define your download directory
# sec_link = 'https://www.sec.gov/Archives/edgar/data/1326801/000132680124000012/0001326801-24-000012-index.htm'

# folder, xbrl_file = download_sec_files(urls[1], download_dir)
# print(f"Folder: {folder}, XBRL File: {xbrl_file}")

# List of tickers and years

# Loop through each ticker and year to download XBRL files

''' cik_number;
print(f"CIK Number for {cik_number}")
cik_number = '0001326801'
urls = load_10k_xbrl(cik_number)
print(f"URLs for {company_name}: {urls}") '''

input_file_path = '/3_test.txt'

''' print(f"CIK Number for {cik_number}")
cik_number = '0001326801'
urls = load_10k_xbrl(cik_number)
print(f"URLs for {company_name}: {urls}")

#download_dir = '.'  # Current working directory
download_dir = '/content'
for url in (urls):
  folder, xbrl_file = download_sec_files(url, download_dir)
  print(f"Folder: {folder}, XBRL File: {xbrl_file}") '''

try:
    with open(input_file_path, 'r') as file:
        # Loop through each line in the file
        for line in file:
            cik_number = line.strip()  # Remove any leading/trailing whitespace
            print("CIK NUMBER CHANGED TO {}".format(cik_number))
            print(f"CIK Number for {cik_number}")
            urls = load_10k_xbrl(cik_number)
            print(f"URLs for {company_name}: {urls}")

            sub_dir = cik_number
            parent_dir = "/content"

            full_path = os.path.join(parent_dir, sub_dir)

            # Create the subdirectory
            os.mkdir(full_path)

            #download_dir = '.'  # Current working directory
            download_dir = full_path
            for url in (urls):
              folder, xbrl_file = download_sec_files(url, download_dir)
              print(f"Folder: {folder}, XBRL File: {xbrl_file}")


except FileNotFoundError:
    print(f'Error: The file "{input_file_path}" was not found.')
except Exception as e:
    print(f'An error occurred: {e}')

''' download_dir = '.'  # Current working directory
for url in (urls):
  folder, xbrl_file = download_sec_files(url, download_dir)
  print(f"Folder: {folder}, XBRL File: {xbrl_file}") '''


