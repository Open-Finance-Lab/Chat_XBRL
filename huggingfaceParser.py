import requests
import os
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("BeautifulSoup not found.")

try:
    import yaml
except ImportError:
    print("PyYAML not found.")

# Function to scrape the website for LLM classifications and badges
def scrape_llm_data(url):
    # List to store the scraped data for each LLM
    llm_data = []
    
    # Send an HTTP GET request to the provided URL
    response = requests.get(url)
    
    # Check if the response is successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all table rows containing model data
        rows = soup.find_all('tr', class_='model-row')
        
        # Iterate through each row to extract model details
        for row in rows:
            llm_name = row.find('td', class_='model-name').text.strip()  # Extract model name
            classification = row.find('td', class_='classification').text.strip()  # Extract classification
            badge = row.find('td', class_='badge-number').text.strip()  # Extract badge number
            
            # Append the extracted data to the list
            llm_data.append({'name': llm_name, 'classification': classification, 'badge_number': badge})
    else:
        # Print an error message if the request fails
        print(f"Failed to fetch data from {url}, status code: {response.status_code}")
    
    # Return the list of scraped data
    return llm_data

# Function to update the YAML file
def update_yaml_file(file_path, classification, badge_number):
    try:
        # Open the YAML file for reading
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)  # Load the YAML content into a Python dictionary

        # Initialize an empty dictionary if the file is empty
        if not data:
            data = {}

        # Update the dictionary with the classification and badge number
        data['classification'] = classification
        data['badge_number'] = badge_number

        # Write the updated dictionary back to the YAML file
        with open(file_path, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)
        print(f"Successfully updated {file_path}")
    except Exception as e:
        # Print an error message if the update fails
        print(f"Failed to update {file_path}: {e}")

# Main logic
if __name__ == "__main__":
    # URL of the webpage to scrape
    base_url = "https://mot.isitopen.ai/models?page=0&sort=desc&order=Classification"
    
    # Scrape data from the webpage
    llm_data = scrape_llm_data(base_url)

    # Directory containing YAML files
    yaml_directory = "./models"

    # Check if the directory exists
    if not os.path.exists(yaml_directory):
        print(f"Directory {yaml_directory} does not exist. Please create it and add YAML files.")
    else:
        # Iterate through the scraped data
        for llm in llm_data:
            # Construct the file name for each YAML file based on the model name
            file_name = f"{llm['name'].replace(' ', '_')}.yml"
            file_path = os.path.join(yaml_directory, file_name)

            # Check if the YAML file exists
            if os.path.exists(file_path):
                # Update the YAML file with the classification and badge number
                update_yaml_file(file_path, llm['classification'], llm['badge_number'])
            else:
                # Print a message if the YAML file is not found
                print(f"YAML file for {llm['name']} not found at {file_path}.")
