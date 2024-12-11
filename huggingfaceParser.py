import requests
from bs4 import BeautifulSoup
import yaml
import os

# Function to scrape the website for LLM classifications and badges
def scrape_llm_data(url):
    llm_data = []
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.find_all('tr', class_='model-row')
        for row in rows:
            llm_name = row.find('td', class_='model-name').text.strip()
            classification = row.find('td', class_='classification').text.strip()
            badge = row.find('td', class_='badge-number').text.strip()
            llm_data.append({'name': llm_name, 'classification': classification, 'badge_number': badge})
    return llm_data

# Function to update the YAML file
def update_yaml_file(file_path, classification, badge_number):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)

    # Add classification and badge to the YAML structure
    data['classification'] = classification
    data['badge_number'] = badge_number

    # Save the updated YAML
    with open(file_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

# Main logic
if __name__ == "__main__":
    base_url = "https://mot.isitopen.ai/models?page=0&sort=desc&order=Classification"
    llm_data = scrape_llm_data(base_url)

    # Directory containing YAML files
    yaml_directory = "./models"

    for llm in llm_data:
        file_name = f"{llm['name'].replace(' ', '_')}.yml"
        file_path = os.path.join(yaml_directory, file_name)

        if os.path.exists(file_path):
            update_yaml_file(file_path, llm['classification'], llm['badge_number'])
            print(f"Updated {file_name} with classification and badge.")
        else:
            print(f"YAML file for {llm['name']} not found.")