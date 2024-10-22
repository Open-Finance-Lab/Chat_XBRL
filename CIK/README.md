Install python
Install pip
Navigate to directory
Ensure the CIK numbers extracted are valid
Write the extracted CIK numbers to a JSON output file

This task provides a Python-based tool that automates the process of parsing a file to extract Central Index Key (CIK) numbers for companies, browsing the SEC website, and retrieving the latest 10-K filings for those companies. The CIK numbers then identify companies that file with the SEC, and the tool leverages the EDGAR (Electronic Data Gathering, Analysis, and Retrieval) system to pull relevant 10-K filings.

The process involves:

Parsing a file to extract CIK numbers: Reads from a provided CSV file that contains CIK numbers.
Browsing the SEC website (EDGAR): Using the extracted CIK numbers, the tool navigates the SEC’s EDGAR database.
Retrieving 10-K filings: It fetches the most recent 10-K filings for the companies associated with the provided CIK numbers.
This project is useful for financial analysts, auditors, or any user interested in quickly retrieving the annual financial statements (10-Ks) of multiple companies for research purposes.


Clone your repo
Navigate to project directory
Install the necessary dependencies

1. Project Components:
Parsing the CIK File
The first step is parsing the input file to extract the list of CIK numbers. This is handled by the appropriate function.

2. SEC EDGAR Scraping
Once the CIK numbers are parsed, the script navigates to the SEC EDGAR website and searches for the relevant company filings. The requests library is used to perform the GET request to the SEC’s EDGAR search page.

3. Retrieving the 10-K Filings
The retrieved 10-K filings are saved to the specified output folder. The program checks if the folder exists, and if not, it creates the directory. The 10-K documents (HTML or TXT) are then saved with the company CIK as the file name and year. 


10/22/24
- Added functionality to process 100 queries instead of 40 queries
- Only extract XML files