import requests
from bs4 import BeautifulSoup
import yaml

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
    classification_tag = soup.find('a', href='/models?page=2&sort=desc&order=Classification')  # Replace with actual selector
    if classification_tag:
        classification = classification_tag.get_text(strip=True)
    else:
        print("Classification data not found.")
    return classification

def scrape_badges(url):
    """Scrapes multiple badge data from the given URL."""
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all badges; adjust the selector as needed based on HTML structure
    badges = []
    badge_tags = soup.find_all('your-selector-for-badge')  # Replace with actual selector
    for badge_tag in badge_tags:
        badge_text = badge_tag.get_text(strip=True)
        badges.append(badge_text)
    
    if not badges:
        print("Badge data not found.")
    return badges

def update_yaml_with_classification_and_badges(yaml_data, classification, badges):
    """Adds the classification and badges data to the 'release' section."""
    if 'release' in yaml_data:
        yaml_data['release']['classification'] = classification
        yaml_data['release']['badges'] = badges
    else:
        print("Release section not found in YAML data.")

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
