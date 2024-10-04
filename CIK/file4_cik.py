# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 17:30:42 2024

@author: willi
"""

import re

# Function to parse and extract CIK numbers and write to a new file
def parse_cik_numbers(input_file, output_file):
    # Open the input file and read the content
    with open(input_file, 'r') as file:
        text = file.read()

    # Define a regular expression pattern to match the CIK number (10-digit numbers) enclosed by colons
    cik_pattern = r":(\d{10}):"

    # Find all matches for the pattern in the text
    cik_numbers = re.findall(cik_pattern, text)

    # Open the output file and write the extracted CIK numbers, each on a new line
    with open(output_file, 'w') as output:
        for cik in cik_numbers:
            output.write(cik + '\n')

    print(f"Extracted {len(cik_numbers)} CIK numbers written to {output_file}")

# Example usage
input_file = 'cik-lookup-data-4.txt'  # Your input file path
output_file = 'output.txt'      # The output file where CIK numbers will be written
parse_cik_numbers(input_file, output_file)