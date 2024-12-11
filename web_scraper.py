import aiohttp
import asyncio
from lxml import html
from utils import load_yaml, save_yaml, update_yaml_with_classification_and_badges  # Import from utils
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def fetch(session, url):
    """Asynchronous fetch for making concurrent requests."""
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            logging.info(f"Fetched content from {url}")
            return await response.text()
    except aiohttp.ClientError as e:
        logging.error(f"Request failed for {url}: {e}")
        return None

async def scrape_classification_and_badges(url):
    """Scrapes classification and badges from a URL."""
    async with aiohttp.ClientSession() as session:
        html_content = await fetch(session, url)
        if not html_content:
            return None, None
        
        tree = html.fromstring(html_content)

        # Adjust XPath/CSS selectors based on the website structure
        classification = tree.xpath("//a[contains(text(), 'Classification')]/text()")
        badges = tree.xpath("//div[@class='badge-class']/text()")
        
        classification = classification[0].strip() if classification else "No Classification Found"
        badges = [badge.strip() for badge in badges] if badges else []

        return classification, badges

async def scrape_multiple_pages(base_url, page_count):
    """Scrapes multiple pages for classification and badges."""
    tasks = []
    for page in range(page_count):
        url = f"{base_url}&page={page}"
        tasks.append(scrape_classification_and_badges(url))
    
    results = await asyncio.gather(*tasks)
    return results

def export_to_json(data, output_file):
    """Exports scraped data to a JSON file."""
    try:
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=4)
        logging.info(f"Exported data to {output_file}")
    except Exception as e:
        logging.error(f"Failed to export data to JSON: {e}")

async def main(yaml_file, base_url, output_file, page_count=5):
    # Load YAML data
    yaml_data = load_yaml(yaml_file)

    # Scrape data
    logging.info("Starting the web scraping process.")
    results = await scrape_multiple_pages(base_url, page_count)

    # Update YAML with scraped data
    for classification, badges in results:
        if classification or badges:
            update_yaml_with_classification_and_badges(yaml_data, classification, badges)

    # Save updated YAML
    save_yaml(yaml_data, yaml_file)
    logging.info(f"Updated YAML file: {yaml_file}")

    # Export results to JSON for additional insight
    export_to_json(results, output_file)

# Usage
yaml_file_path = 'models_Amber.yml'
website_url = 'https://mot.isitopen.ai/?page=0'
output_file = 'scraped_results.json'
asyncio.run(main(yaml_file_path, website_url, output_file))
