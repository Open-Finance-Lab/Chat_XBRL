This program takes in a YML file and extracts the name, producer, classification, last updated, and badge. It then converts the model data to a data frame. 

The initial issue with this code was that classification and badge were outputting as null and empty. The resolution for this bug was that there was no classification or badge key in the YML file. A solution to this was to input classification in each YML file. This was tedious and required me to go through every YML file. A second solution was to create a web scraping program to extract the classifcation and badges to put onto the data frame. While this took more logic and code, it was entirely more efficient for future classifications and badges. 

This entire pipeline was integrated with the Model Openness Tool (MOT) on Hugging Face. I took the initial code from MOT, refactored it, and added error handling and automated data population for missing fields, effectively eliminating the bugs that had previously caused missing or inaccurate data. The enhancements ensure that the extracted data is complete and accurate, making it readily usable for evaluation and display in MOT applications. This approach not only saves time but also enhances the reliability of the data extraction process, helping to maintain consistent model metadata across the framework.


Web Scraper Implementation:
Features
Web Scraping: Retrieves specific data (classification and badge) from a given website.
YAML Manipulation: Parses an existing YAML file and updates specific fields within it.
Error Logging: Includes error handling for common issues like missing data fields and network errors.
Modular Structure: Organized functions for scraping classification and badge separately, making it easy to customize for other websites or data types.
Requirements
Python 3.7+
Libraries:
requests
PyYAML
BeautifulSoup4
To install required libraries, run:

bash
Copy code
pip install requests pyyaml beautifulsoup4
Installation
Clone this repository:

bash
Copy code
git clone https://github.com/your-username/YAML-Web-Scraper.git
Navigate into the directory:

bash
Copy code
cd YAML-Web-Scraper
Install dependencies (see Requirements above).

Usage
To run the scraper, specify the path to your YAML file and the URL from which to scrape data.

bash
Copy code
python scraper.py
Replace scraper.py with the filename of your script if different.

Command-Line Usage
Open your terminal.

Run:

bash
Copy code
python scraper.py path/to/your_file.yml https://example-website.com
Sample Command
bash
Copy code
python scraper.py sample.yml https://mot.isitopen.ai/?page=0
File Structure
Your project directory should contain:

graphql
Copy code
YAML-Web-Scraper/
│
├── scraper.py        # The main script containing all functions
├── sample.yml        # An example YAML file (for testing purposes)
└── README.md         # This documentation file
Functions Overview
1. load_yaml(file_path)
Loads the YAML file specified by the file_path. Uses yaml.safe_load to parse the YAML content into a Python dictionary.

Parameters: file_path - Path to the YAML file.
Returns: Parsed YAML content as a dictionary.
2. save_yaml(data, file_path)
Saves the updated YAML data back to the file.

Parameters:
data: YAML data to save.
file_path: Path to save the updated YAML file.
3. scrape_classification(url)
Scrapes classification data from the provided URL using BeautifulSoup. This function isolates and retrieves the classification text based on HTML selectors (adjust your-selector-for-classification as needed).

Parameters: url - The URL to scrape classification data from.
Returns: Classification data as a string.
4. scrape_badge(url)
Scrapes badge data from the provided URL using BeautifulSoup. This function isolates and retrieves the badge text based on HTML selectors (adjust your-selector-for-badge as needed).

Parameters: url - The URL to scrape badge data from.
Returns: Badge data as a string.
5. update_yaml_with_classification_and_badge(yaml_data, classification, badge)
Adds classification and badge data to the release section of the YAML dictionary.

Parameters:
yaml_data: The YAML data dictionary.
classification: The classification string to add.
badge: The badge string to add.
6. main(yaml_file, url)
Coordinates the entire scraping and YAML updating process.

Parameters:
yaml_file: Path to the YAML file to update.
url: The URL to scrape data from.
Customization
The scraper’s behavior can be customized based on the HTML structure of the target website.

Update HTML Selectors: Replace 'your-selector-for-classification' and 'your-selector-for-badge' in scrape_classification and scrape_badge functions with the actual HTML selectors (CSS or XPath) needed to locate the classification and badge elements on the webpage.

Use Chrome or Firefox Developer Tools to inspect the HTML and identify these selectors.
Add New Fields: To add additional fields, create a new scraping function similar to scrape_classification or scrape_badge, update update_yaml_with_classification_and_badge to handle new data, and modify the YAML structure as needed.

Example YAML File
An example input YAML file (sample.yml) should follow this structure:

yaml
Copy code
framework:
  name: 'Model Openness Framework'
  version: '1.0'
  date: '2024-12-15'
release:
  name: 'AraGPT2'
  version: '1.5B'
  date: '2024-10-03'
  type: 'language'
  architecture: 'transformer decoder'
  producer: 'American University of Beirut'
  components:
    - name: 'Model architecture'
      description: 'Well-commented code for model architecture'
      license_name: 'Pending evaluation'
  # Additional components...
After running the script, if classification and badge are successfully retrieved, the YAML file will include:

yaml
Copy code
release:
  classification: 'The classification retrieved from the website'
  badge: 'The badge retrieved from the website'
Error Handling
The script includes basic error handling:

Network Errors: If there’s an issue connecting to the URL, requests will raise an HTTP error. Ensure the target URL is reachable.
Missing Data: If classification or badge data is not found, the functions will return empty strings and print an error message.
YAML Structure Issues: If the expected release section is missing, the update_yaml_with_classification_and_badge function will print an error message. Ensure your YAML file follows the expected structure.
Contributing
We welcome contributions! To contribute:

Fork the repository.
Create a feature branch (git checkout -b feature-branch).
Commit your changes (git commit -m "Add new feature").
Push to your branch (git push origin feature-branch).
Open a Pull Request.