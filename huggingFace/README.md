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

Updates to the Web Scraper
The web scraper has undergone significant updates to improve its functionality, reliability, and compatibility with the target website’s structure. Initially, the script included placeholder selectors for scraping data, which made it non-functional for real-world usage. These placeholders have been replaced with accurate and dynamic CSS selectors and attributes that align with the actual HTML structure of the target website. This ensures that the scraper can successfully extract both classification and badge data without errors.

Furthermore, error handling has been greatly enhanced throughout the script. Previously, there was minimal handling for scenarios where HTTP requests failed or when specific elements on the page were missing. The updated script now includes detailed error messages for situations such as network failures, invalid responses, or changes in the website’s layout. This not only prevents the script from crashing but also provides clear feedback to the user, making debugging and maintenance significantly easier.

In terms of YAML file integration, the script was updated to handle a wider range of scenarios. For instance, if the specified YAML file does not exist, the script will now create a new file and initialize it with the required structure. If the file exists but lacks a "release" section, the script dynamically adds this section before updating it with the scraped data. This ensures seamless operation regardless of the starting state of the YAML file. Additionally, the data-saving process has been optimized to retain the original file structure and formatting wherever possible, improving both usability and clarity for future edits.

To improve user experience, detailed logging has been introduced. This includes messages indicating whether the classification or badge data was successfully found, whether it was updated in the YAML file, or if no relevant data was retrieved from the website. These logs provide valuable insights into the scraper’s operations and make it easier to track what the script has accomplished during execution. Moreover, they help identify areas where additional adjustments might be needed, especially if the target website’s structure changes in the future.

Finally, the script has been designed with adaptability in mind. The selectors and scraping logic are modular, making it easier to adjust them for changes in the target website’s structure. For example, the classification and badge scraping functions can be updated independently to accommodate new element identifiers or attributes. These improvements, combined with better error handling and YAML integration, ensure that the web scraper is robust, user-friendly, and capable of delivering consistent results even in the face of evolving requirements.

By addressing previous limitations and adding new features, this update transforms the web scraper into a powerful, reliable, and maintainable tool that is ready for production use.


11/22/24 Update
Documentation for Modular Web Scraper Update
Introduction
This documentation explains the updates made to a Python web scraper to improve its modularity and maintainability. By separating utility functions into a dedicated file and importing them into the main script, the updated structure adheres to the principles of modular design, enabling easier reuse, testing, and scalability.

Updated Structure
Files Created/Modified
utils.py
Contains utility functions for YAML file operations and data updating. This file centralizes common functionalities that can be reused in other projects.

Main Script (main.py)
Handles web scraping and integrates functionalities from utils.py. It focuses on the program's core logic.

Breakdown of Changes
1. Utility Functions in utils.py
The utils.py file encapsulates commonly used operations related to YAML files and updating data. This separation reduces redundancy and enhances readability.

Functions in utils.py
load_yaml(file_path)
Purpose: Loads data from a YAML file, creating a new YAML file if one doesn't exist.
Parameters:

file_path (str): Path to the YAML file.
Returns:
(dict): The parsed YAML data or an empty dictionary if the file doesn't exist.
Example Usage:

python
Copy code
yaml_data = load_yaml('example.yml')
save_yaml(data, file_path)
Purpose: Saves data to a YAML file.
Parameters:

data (dict): Data to be written to the file.
file_path (str): Path to the YAML file.
Returns: None.
Example Usage:

python
Copy code
save_yaml(yaml_data, 'example.yml')
update_yaml_with_classification_and_badges(yaml_data, classification, badges)
Purpose: Updates a YAML dictionary with classification and badge data.
Parameters:

yaml_data (dict): The YAML data to be updated.
classification (str): Classification data to add.
badges (list): List of badge data to add.
Returns: None (updates the yaml_data object in-place).
Example Usage:

python
Copy code
update_yaml_with_classification_and_badges(yaml_data, "Class A", ["Badge 1", "Badge 2"])
2. Main Script (main.py)
The main script imports the utility functions from utils.py to perform YAML operations and focuses on web scraping. The main script handles:

Fetching data from a URL.
Processing the data.
Updating the YAML file with new information.
Changes Made to main.py
Import Utility Functions:
The following import statement is added at the top of the main script:

python
Copy code
from utils import load_yaml, save_yaml, update_yaml_with_classification_and_badges
Core Scraping Functions: These functions are retained in the main script as they directly handle the logic for web scraping:

scrape_classification(url): Scrapes the classification data from a specified URL.
scrape_badges(url): Scrapes badge data from a specified URL.
Main Function: The main() function coordinates the loading of YAML data, web scraping, and updating the YAML file using the imported utility functions.



1. Integration of Web Scraper
New Function: scrape_model_data
Purpose: Simulates scraping data from the web for machine learning models.
Implementation:
Generates a placeholder dataset to represent scraped data.
Returns a pandas.DataFrame with the same structure as the YAML data.
Example Output:
python
Copy code
[{"Name": "Scraped Model 1", "Organization": "Org A", ...}]
Modification: get_combined_data
Purpose: Combines local YAML data with the scraped web data.
Implementation:
Calls load_all_models(directory) to load YAML data.
Calls scrape_model_data() to get scraped data.
Merges the two datasets using pd.concat.
2. Refresh Functionality
New Function: refresh_data
Purpose: Allows dynamic reloading of YAML and scraped data.
Implementation:
Reloads data using get_combined_data.
Resets the pagination to display the first page.
Updates the table with the refreshed data.
3. Pagination and Search Capabilities
Preserved Functionality
filter_data: Filters data based on user inputs for Name and Organization.
paginate_data: Handles data slicing for the current page based on page size and number.
Event Handlers: All pagination buttons (Next, Previous, and Go to Page) remain unchanged.
4. Changes in User Interface
Addition: Refresh Button
UI Element: A "🔄 Refresh Data" button was added.
Functionality: Links to the refresh_data function. Reloads both YAML and scraped data, resets the table to the first page, and updates pagination controls.
Pagination Controls Enhanced
Preserved: Buttons (Previous, Next, Go to Page) and page numbering display.
Updated: Automatically refreshes pagination limits when new data is loaded.
5. Data Handling Enhancements
Unified Data Source: global_df
Modification: global_df now contains both YAML and scraped data.
Impact: Ensures seamless integration of multiple data sources for filtering and pagination.
Dynamic Updates:
Reloading the table is efficient and does not affect user interaction.
6. Changes to Event Functions
The following events were updated to support the new dynamic global_df:

Search Functionality
Functions Affected:
on_search_change
on_prev
on_next
on_go
Impact: These functions now operate on the refreshed global_df.
Refresh Integration
Button: refresh_button
Linked Function: refresh_data
Output:
Updates table data (table_output).
Resets pagination (total_pages_text, page number).
Code Design Benefits
Modular: New functionality integrates cleanly without disrupting the original structure.
Scalable: The script can handle more data sources or scrapers in the future.
User-Friendly: Improved UI with dynamic data refresh options.
Conclusion
The updated script now provides:

Dynamic Data Refreshing: Seamlessly integrates YAML and scraped data.
Preserved Features: Retains the search, pagination, and filtering functionalities.
Improved Scalability: Allows future data source additions without significant changes.

New web scraper changes and functionalities:
Features
1. Concurrency with asyncio
The scraper uses asynchronous programming with aiohttp and asyncio, allowing concurrent HTTP requests. This significantly improves performance, especially when scraping multiple pages.

2. Advanced HTML Parsing
The lxml library is used for HTML parsing with support for XPath, making data extraction more flexible and robust compared to traditional CSS selectors.

3. Error Handling
Robust error-handling mechanisms ensure graceful recovery from network issues and missing data. Errors are logged for debugging purposes.

4. Structured Logging
Logging is configured to provide timestamped, clear, and informative messages. This aids in monitoring and debugging.

5. Multi-Page Scraping
The scraper can handle pagination, making it suitable for websites that divide data across multiple pages.

6. YAML Configuration Updates
Scraped data is seamlessly integrated into an existing YAML file using helper functions (load_yaml, save_yaml, update_yaml_with_classification_and_badges).

7. Data Export
Scraped results are exported to a JSON file for further analysis or backup.

Prerequisites
Ensure the following dependencies are installed:

Python 3.8+
Libraries: aiohttp, lxml, pyyaml
Install dependencies using:

bash
Copy code
pip install aiohttp lxml pyyaml