'''
import requests
from bs4 import BeautifulSoup
import json
import time
import random

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.126 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:112.0) Gecko/20100101 Firefox/112.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:114.0) Gecko/20100101 Firefox/114.0",
]

    try:
        # Randomize the User-Agent
        headers = {"User-Agent": random.choice(user_agents)}
        

# Timer with a fixed delay of 2 seconds
time.sleep(2)  # Delay for 2 seconds before the next action

# Timer with a random delay between 2 and 5 seconds
time.sleep(random.uniform(2, 5))  # Randomized delay between 2 and 5 seconds

'''
#Example: 
import requests
from bs4 import BeautifulSoup
import json
import time
import random

# URL of the website containing the table
table_url = "https://example.com/table"  # Replace with the actual URL of the table

# Path to the metadata file
metadata_file_path = "metadata.json"

# List of User-Agent strings to rotate
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.126 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:112.0) Gecko/20100101 Firefox/112.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:114.0) Gecko/20100101 Firefox/114.0",
]

# Function to perform the scraping
def scrape_table_and_update_metadata():
    try:
        # Randomize the User-Agent
        headers = {"User-Agent": random.choice(user_agents)}

        # Step 1: Fetch the webpage
        print("Fetching the webpage...")
        response = requests.get(table_url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        # Step 2: Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # Step 3: Find the table element
        table = soup.find("table")
        if not table:  # If no table is found
            raise ValueError("No table found on the webpage. Please check the URL or structure of the page.")

        # Step 4: Extract classification and badge data from the table
        rows = table.find_all("tr")  # Find all table rows
        extracted_data = []  # List to store the extracted classification and badge values

        # Assuming the table headers include columns like "Name", "Organization", "Classification", "Badge"
        header_row = rows[0]
        headers = [header.get_text(strip=True) for header in header_row.find_all("th")]

        # Find the indices for "Classification" and "Badge" columns
        try:
            classification_index = headers.index("Classification")
            badge_index = headers.index("Badge")
        except ValueError as e:
            raise ValueError("Could not find 'Classification' or 'Badge' columns in the table headers.") from e

        # Loop through all rows (skip the header row)
        for row in rows[1:]:
            cells = row.find_all("td")  # Find all columns in the row
            if len(cells) > max(classification_index, badge_index):  # Ensure the row has enough columns
                classification = cells[classification_index].get_text(strip=True)
                badge = cells[badge_index].get_text(strip=True)
                extracted_data.append({"classification": classification, "badge": badge})

        # Step 5: Print the extracted data for verification
        print("Extracted Data:", extracted_data)

        # Step 6: Read and update the metadata file
        try:
            with open(metadata_file_path, "r") as file:
                metadata = json.load(file)  # Load the metadata JSON
        except FileNotFoundError:
            print(f"Metadata file '{metadata_file_path}' not found. Creating a new file.")
            metadata = {}  # Create an empty metadata dictionary if the file doesn't exist

        # Update the metadata
        if extracted_data:
            metadata["classification"] = extracted_data[0].get("classification", "N/A")
            metadata["badge"] = extracted_data[0].get("badge", "N/A")

        # Step 7: Write the updated metadata back to the file
        with open(metadata_file_path, "w") as file:
            json.dump(metadata, file, indent=4)
            print(f"Metadata updated and saved to '{metadata_file_path}'.")

        # Add a delay to avoid overwhelming the server
        print("Pausing before the next request...")
        time.sleep(random.uniform(2, 5))  # Pause for 2-5 seconds (randomized)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
    except ValueError as e:
        print(f"Error processing the webpage: {e}")
    except json.JSONDecodeError:
        print("Error: Failed to parse the metadata JSON file. Ensure it is valid JSON.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Run the scraper
scrape_table_and_update_metadata()


