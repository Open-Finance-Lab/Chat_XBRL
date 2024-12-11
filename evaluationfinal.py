import requests
import os
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def create_session():
    """
    Create and return a requests session with standard headers.

    The session ensures that all requests use the same headers and configurations, 
    which is useful for maintaining persistent settings across multiple requests.

    Returns:
        requests.Session: A session object with default headers set.
    """
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }
    session.headers.update(headers)
    return session


def extract_file_links(soup, link):
    """
    Extract file links from an SEC webpage.

    Extracts links to .xml and .xsd files from the SEC webpage. 
    The links are returned as absolute URLs.

    Args:
        soup (BeautifulSoup): The parsed HTML content of the webpage.
        link (str): The base URL of the page where the links are being extracted.

    Returns:
        tuple: 
            - file_links (list): A list of URLs to .xml and .xsd files.
            - folder_name (str): The name of the folder to save files in.
    """
    file_links = []
    folder_name = None

    try:
        for a_tag in soup.find_all('a', href=True):
            file_link = urljoin(link, a_tag['href'])
            if file_link.endswith(('.xml', '.xsd')):
                print(f"Found file link: {file_link}")
                folder_name_new = file_link.split('/')[-1].split('.')[0]
                if folder_name is None:
                    folder_name = folder_name_new
                file_links.append(file_link)
    except Exception as e:
        print(f"Error extracting file links from {link}: {e}")
    
    return file_links, folder_name


def get_xbrl_links(link):
    """
    Fetch XBRL file links from an SEC page, with retry logic and exponential backoff.

    This function attempts to retrieve and parse the given URL for XBRL links 
    to .xml and .xsd files. If the request fails, it retries up to 5 times.

    Args:
        link (str): The URL of the SEC page containing XBRL file links.

    Returns:
        tuple:
            - file_links (list): A list of URLs for .xml and .xsd files.
            - folder_name (str): The name of the folder to store files.
    """
    session = create_session()

    for attempt in range(5):  # Retry up to 5 times
        try:
            response = session.get(link, timeout=10)
            response.raise_for_status()  # Raise an HTTP error if one occurs
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed to retrieve the webpage for link {link}: {e}")
            time.sleep(2 ** attempt)  # Exponential backoff (1, 2, 4, 8, 16 seconds)
            continue

        print(f"Accessing URL: {link}")
        print(f"Status Code: {response.status_code}")

        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            file_links, folder_name = extract_file_links(soup, link)
            return file_links, folder_name
        except Exception as e:
            print(f"Error parsing the HTML content for link {link}: {e}")
            continue

    print(f"Failed to retrieve the webpage after 5 attempts for link {link}")
    return [], None


def download_file(session, file_link, folder_name=None, max_retries=5):
    """
    Downloads a file from the given file_link and saves it to the folder_name.

    Args:
        session (requests.Session): The session object for making HTTP requests.
        file_link (str): The URL of the file to be downloaded.
        folder_name (str, optional): The directory where the file will be saved. Defaults to './downloads'.
        max_retries (int, optional): Maximum number of retry attempts. Defaults to 5.

    Returns:
        str: The path to the downloaded file, or None if the download failed.
    """
    folder_name = folder_name or os.getenv('DOWNLOAD_DIR', './downloads')
    file_name = file_link.split('/')[-1]
    folder_path = os.path.join(folder_name)
    os.makedirs(folder_path, exist_ok=True)  # Ensure the folder exists
    file_path = os.path.join(folder_path, file_name)

    if os.path.isfile(file_path):
        print(f"File already exists: {file_path}. Skipping download.")
        return file_path

    attempt = 0
    while attempt < max_retries:
        try:
            print(f"Attempt {attempt + 1} to download file: {file_link}")
            file_response = session.get(file_link, timeout=10)
            file_response.raise_for_status()

            with open(file_path, 'wb') as file:
                file.write(file_response.content)
            
            print(f"Successfully downloaded: {file_path}")
            return file_path
        except requests.exceptions.RequestException as e:
            attempt += 1
            print(f"Attempt {attempt} failed to download file: {file_link} - {e}")
            time.sleep(2 ** attempt)  # Exponential backoff
        except Exception as e:
            print(f"Unexpected error while downloading {file_link}: {e}")
            break

    print(f"Failed to download file after {max_retries} attempts: {file_link}")
    return None


def load_10k_xbrl(cik_num=None, years=None, download_dir=None):
    """
    Loads the XBRL files for a given CIK and list of years.

    Args:
        cik_num (str): The CIK number of the company.
        years (list or set): The list or set of years to load.
        download_dir (str, optional): Directory to download files (default: ./downloads).
        
    Returns:
        list: List of URLs to XBRL filings.
    """
    if not cik_num:
        print("CIK number is required.")
        return []

    download_dir = download_dir or os.getenv('DOWNLOAD_DIR', './downloads')
    url_to_all_10k = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik_num}&type=10-K&count=40"
    
    for attempt in range(5):
        try:
            response = requests.get(url_to_all_10k, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed to access {url_to_all_10k}: {e}")
            time.sleep(2 ** attempt) 
            continue

        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find('table', class_='tableFile2')

            if not table:
                return []

            full_links = []
            for row in table.find_all('tr')[1:]:
                cols = row.find_all('td')
    return []
