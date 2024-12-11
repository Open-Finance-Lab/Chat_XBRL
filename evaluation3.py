import requests
from bs4 import BeautifulSoup
import os
import re
from urllib.parse import urljoin

# Get XBRL file links from the SEC page 
def get_xbrl_links(link):
    try:
        session = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
        session.headers.update(headers)

        response = session.get(link)
        response.raise_for_status()  # Raise an HTTP error if one occurs
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve the webpage for link {link}: {e}")
        return [], None

    print(f"Accessing URL: {link}")
    print(f"Status Code: {response.status_code}")

    file_links = []
    folder_name = None

    try:
        soup = BeautifulSoup(response.content, 'html.parser')
        for a_tag in soup.find_all('a', href=True):
            file_link = urljoin(link, a_tag['href'])
            if file_link.endswith(('.xml', '.xsd')):
                print(f"Found file link: {file_link}")
                folder_name_new = file_link.split('/')[-1].split('.')[0]
                if folder_name is None:
                    folder_name = folder_name_new
                file_links.append(file_link)
    except Exception as e:
        print(f"Error parsing the HTML content for link {link}: {e}")

    return file_links, folder_name


# Download a file from its link
def download_file(session, file_link, folder_name):
    for attempt in range(3):
        try:
            file_response = session.get(file_link, timeout=10)
            file_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to download file: {file_link} (Attempt {attempt + 1}) - {e}")
            continue

        if file_response.status_code == 200:
            file_name = file_link.split('/')[-1]
            folder_path = os.path.join(folder_name)
            os.makedirs(folder_path, exist_ok=True)
            file_path = os.path.join(folder_path, file_name)

            try:
                with open(file_path, 'wb') as file:
                    file.write(file_response.content)
                print(f"Downloaded: {file_path}")
                return file_path
            except Exception as e:
                print(f"Error writing file {file_path}: {e}")
                continue
    return None


# Load 10-K XBRL links
def load_10k_xbrl(cik_num=None, years=None):
    if not cik_num:
        print("CIK number is required.")
        return []

    url_to_all_10k = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik_num}&type=10-K&count=40"
    try:
        response = requests.get(url_to_all_10k)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Network error when accessing {url_to_all_10k}: {e}")
        return []

    try:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', class_='tableFile2')
        if not table:
            print(f"No table found at {url_to_all_10k}")
            return []

        full_links = []
        for row in table.find_all('tr')[1:]:
            cols = row.find_all('td')
            if len(cols) > 3:
                filing_type = cols[0].text.strip()
                filing_date = cols[3].text.strip()

                if filing_type == '10-K' and any(target_year in filing_date for target_year in years):
                    doc_link = cols[1].find('a', href=True)['href']
                    full_links.append(f"https://www.sec.gov{doc_link}")
        return full_links
    except Exception as e:
        print(f"Error parsing the HTML content at {url_to_all_10k}: {e}")
        return []
