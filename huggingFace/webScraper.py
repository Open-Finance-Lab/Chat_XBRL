import requests
from bs4 import BeautifulSoup
import yaml

def load_yaml(file_path):
    """Loads the YAML file."""
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"YAML file not found at {file_path}. Creating a new one.")
        return {}

def save_yaml(data, file_path):
    """Saves the updated data back to the YAML file."""
    with open(file_path, 'w') as file:
        yaml.dump(data, file, sort_keys=False)

def scrape_classification(url):
    """Scrapes the classification data from the given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Adjust the selector based on actual website structure
        classification_tag = soup.find('a', href=True, text='Classification')  # Example selector
        if classification_tag:
            return classification_tag.get_text(strip=True)
        else:
            print("Classification data not found.")
            return ""
    except requests.RequestException as e:
        print(f"Error fetching classification: {e}")
        return ""

def scrape_badges(url):
    """Scrapes multiple badge data from the given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Adjust the selector based on actual website structure
        badges = []
        badge_tags = soup.select('.badge-class')  # Example CSS selector
        for badge_tag in badge_tags:
            badges.append(badge_tag.get_text(strip=True))
        
        if not badges:
            print("Badge data not found.")
        return badges
    except requests.RequestException as e:
        print(f"Error fetching badges: {e}")
        return []

def update_yaml_with_classification_and_badges(yaml_data, classification, badges):
    """Adds the classification and badges data to the 'release' section."""
    if 'release' not in yaml_data:
        yaml_data['release'] = {}
    yaml_data['release']['classification'] = classification
    yaml_data['release']['badges'] = badges

def main(yaml_file, url):
    # Load the YAML data
    yaml_data = load_yaml(yaml_file)
    
    # Scrape the classification and badges data from the website
    classification = scrape_classification(url)
    badges = scrape_badges(url)
    
    # Update YAML with the classification and badges
    if classification or badges:
        update_yaml_with_classification_and_badges(yaml_data, classification, badges)
        
        # Save the updated YAML data
        save_yaml(yaml_data, yaml_file)
        print(f"Updated YAML file with classification: {classification} and badges: {badges}")
    else:
        print("No classification or badge data found to update YAML.")

# Usage
yaml_file_path = 'models_Amber.yml'
website_url = 'https://mot.isitopen.ai/?page=0'
main(yaml_file_path, website_url)
