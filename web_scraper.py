import aiohttp
import asyncio 
from lxml import html 
from utils import load_yaml, save_yaml, update_yaml_with_classification_and_badges 
import logging 
import json 

# Configure logging to display messages in a standardized format.
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def fetch(session, url):
    """
    Makes an asynchronous HTTP GET request to fetch the content of a URL.

    Args:
        session (aiohttp.ClientSession): An active client session for making requests.
        url (str): The URL to fetch.

    Returns:
        str or None: The response text if successful, or None if the request fails.
    """
    try:
        async with session.get(url) as response:
            response.raise_for_status()  # Raise an exception for HTTP errors.
            logging.info(f"Fetched content from {url}")
            return await response.text()
    except aiohttp.ClientError as e:
        logging.error(f"Request failed for {url}: {e}")
        return None

async def scrape_classification_and_badges(url):
    """
    Scrapes classification and badge data from a given URL.

    Args:
        url (str): The URL to scrape data from.

    Returns:
        tuple: A tuple containing the classification (str) and badges (list of str).
    """
    async with aiohttp.ClientSession() as session:
        html_content = await fetch(session, url)
        if not html_content:
            return None, None

        # Parse the HTML content and extract classification and badges.
        tree = html.fromstring(html_content)
        classification = tree.xpath("//a[contains(text(), 'Classification')]/text()")
        badges = tree.xpath("//div[@class='badge-class']/text()")

        # Process and clean up the extracted data.
        classification = classification[0].strip() if classification else "No Classification Found"
        badges = [badge.strip() for badge in badges] if badges else []

        return classification, badges

async def scrape_multiple_pages(base_url, page_count):
    """
    Scrapes multiple pages from a base URL for classification and badge data.

    Args:
        base_url (str): The base URL to scrape from.
        page_count (int): The number of pages to scrape.

    Returns:
        list: A list of tuples containing classification and badges for each page.
    """
    tasks = [
        scrape_classification_and_badges(f"{base_url}&page={page}")
        for page in range(page_count)
    ]
    return await asyncio.gather(*tasks)  # Run all scraping tasks concurrently.

def export_to_json(data, output_file):
    """
    Exports data to a JSON file.

    Args:
        data (list): The data to export.
        output_file (str): The path to the JSON file to write to.
    """
    try:
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=4)  # Write data with pretty formatting.
        logging.info(f"Exported data to {output_file}")
    except Exception as e:
        logging.error(f"Failed to export data to JSON: {e}")

async def main(yaml_file, base_url, output_file, page_count=5):
    """
    Main function to orchestrate the scraping process, update YAML, and export results.

    Args:
        yaml_file (str): Path to the YAML file to load and update.
        base_url (str): Base URL for scraping data.
        output_file (str): Path to the JSON file for exporting results.
        page_count (int): Number of pages to scrape. Default is 5.
    """
    # Load YAML data for updating with scraped information.
    yaml_data = load_yaml(yaml_file)

    logging.info("Starting the web scraping process.")
    # Scrape classification and badge data from multiple pages.
    results = await scrape_multiple_pages(base_url, page_count)

    # Update the YAML data with the scraped results.
    for classification, badges in results:
        if classification or badges:
            update_yaml_with_classification_and_badges(yaml_data, classification, badges)

    # Save the updated YAML data back to the file.
    save_yaml(yaml_data, yaml_file)
    logging.info(f"Updated YAML file: {yaml_file}")

    # Export the scraped results to a JSON file for additional usage.
    export_to_json(results, output_file)

# Configure the file paths and URL for the scraping task.
yaml_file_path = 'models_Amber.yml'
website_url = 'https://mot.isitopen.ai/?page=0'
output_file = 'scraped_results.json'

# Run the asynchronous main function.
asyncio.run(main(yaml_file_path, website_url, output_file))
