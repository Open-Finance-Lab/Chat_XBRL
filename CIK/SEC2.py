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
