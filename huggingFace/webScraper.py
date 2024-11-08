import requests
from bs4 import BeautifulSoup
import yaml
import re

def load_yaml(file_path):
    """Loads the YAML file."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def save_yaml(data, file_path):
    """Saves the updated data back to the YAML file."""
    with open(file_path, 'w') as file:
        yaml.dump(data, file, sort_keys=False)

def scrape_classification(url):
    """Scrapes the classification data from the given URL."""
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the classification data; adjust the selector as needed based on HTML structure
    classification = ""
    classification_tag = soup.find('your-selector-for-classification')
    if classification_tag:
        classification = classification_tag.get_text(strip=True)
    else:
        print("Classification data not found.")
    return classification

def update_yaml_with_classification(yaml_data, classification):
    """Adds the classification data to the 'release' section."""
    if 'release' in yaml_data:
        yaml_data['release']['classification'] = classification
    else:
        print("Release section not found in YAML data.")

def main(yaml_file, url):
    # Load the YAML data
    yaml_data = load_yaml(yaml_file)
    
    # Scrape the classification data from the website
    classification = scrape_classification(url)
    if classification:
        # Update YAML with the classification
        update_yaml_with_classification(yaml_data, classification)
        
        # Save the updated YAML data
        save_yaml(yaml_data, yaml_file)
        print(f"Updated YAML file with classification: {classification}")
    else:
        print("No classification data found to update YAML.")

# Usage
yaml_file_path = 'your_file.yml'
website_url = 'https://mot.isitopen.ai/?page=0'
main(yaml_file_path, website_url)
