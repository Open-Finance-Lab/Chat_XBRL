PROJECT OVERVIEW
This project investigates the Model Openness Framework (MOF) and the use of XBRL (eXtensible Business Reporting Language) to benchmark large language models (LLMs) in their ability to analyze and extract meaningful insights from structured datasets. By leveraging these frameworks, the project evaluates how LLMs—such as those available through platforms like Hugging Face—process and interpret real-world financial documents and datasets.

A significant focus of this project is on the retrieval and handling of Central Index Key (CIK) numbers, an essential component for identifying and analyzing SEC (Securities and Exchange Commission) filings. The extracted data serves as a test case to explore the capabilities of LLMs in automating information extraction tasks from structured data formats.

The entire project was developed and executed using Google Colab, providing an accessible and scalable environment for computation and analysis without requiring specialized hardware.


CIK TASK
The CIK Retrieval Task is a core part of this project, focusing on extracting the CIK numbers of companies and organizing the data in a structured, JSON format. CIK numbers are unique identifiers assigned by the SEC to each entity filing disclosures, and they are crucial for efficiently accessing financial filings and reports.

Objectives of the CIK Task:
- Automate the retrieval of CIK numbers for all companies.
- Format the retrieved data into a structured and accessible format (JSON).
- Lay the groundwork for further analysis and benchmarking using the retrieved CIK data.
Technical Approach:
- Data Parsing: The task involved parsing a provided text file containing company names and their associated CIK numbers. This was achieved using  a Python script to ensure accuracy and consistency.
- Data Formatting: The extracted data was converted into a structured JSON format, making it easy to use in downstream tasks and enabling compatibility with various tools and platforms.
- Error Handling: Special attention was given to handle edge cases, such as missing or improperly formatted entries, ensuring the integrity of the final dataset.

PROGRESS
Completed Milestones

1. CIK Data Retrieval:

Successfully parsed the provided dataset of company names and CIK numbers using a custom Python script.
Extracted and verified the accuracy of all entries.

2. Data Formatting:

Organized the retrieved data into a JSON format. Each entry contains:
name: The name of the company.
cik: The associated CIK number for the company.

3. Validation:

Ensured that all retrieved CIK numbers match the corresponding company names.
Addressed and resolved any issues with missing or improperly formatted data during the parsing process.

4. Output:

Saved the processed data to a JSON file named parsed_companies.json, ready for further analysis and benchmarking.


