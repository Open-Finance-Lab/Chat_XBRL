# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 16:58:28 2024

@author: carin
"""
'''
import requests

def get_file(url):
    webpage = requests.get(url)
    
    if response.status_code == 200:
        return response.text
    else:
        print("Failed to retrieve file")
        return ""
    
    
def parse_companies(text):
    #split the text by new lines
    lines = text.strip().splitlines()
    
    companies = []
    
    for line in lines:
        #find the first & second colons to split company name & CIK number
        first_colon = line.find(':')
        second_colon = line.find(':', first_colon + 1)
        
        if first_colon :
'''        
            
            
import requests

def fetch_file_from_url(url):
    # Send a GET request to the provided URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve file from {url}")
        return ""

def parse_companies(text):
    # Split the text by new lines
    lines = text.strip().splitlines()
    
    companies = []

    for line in lines:
        # Find the first and second colons to split company name and CIK number
        first_colon = line.find(':')
        second_colon = line.find(':', first_colon + 1)
        
        if first_colon != -1 and second_colon != -1:
            company_name = line[:first_colon].strip()
            cik_number = line[first_colon+1:second_colon].strip()
            companies.append((company_name, cik_number))

    # Sort companies by name
    companies.sort(key=lambda x: x[0].lower())

    return companies

def display_companies(companies):
    for company, cik in companies:
        print(f"Company: {company}, CIK: {cik}")

# URL to the txt file
url = "https://www.sec.gov/Archives/edgar/cik-lookup-data.txt"

# Fetch the content from the URL
file_content = fetch_file_from_url(url)

# Parse and display the companies if the content is not empty
if file_content:
    companies = parse_companies(file_content)
    display_companies(companies)
