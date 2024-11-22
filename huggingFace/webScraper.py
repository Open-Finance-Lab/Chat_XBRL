import requests
from bs4 import BeautifulSoup
from utils import load_yaml, save_yaml, update_yaml_with_classification_and_badges  # Import from utils

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
