#parse companies function

import json

def parse_txt_to_json(input_file, output_file):
    data = []

    with open(input_file, 'r') as file:
        for line in file:
            # Split the line on the colon, but only on the first colon
            parts = line.split(':')
            if len(parts) > 1:
                company_name = parts[0].strip()  # Company name is before the first colon
                cik_number = parts[1].strip()    # CIK number is between the colons
                # Add the parsed data as a dictionary to the list
                data.append({
                    "company": company_name,
                    "CIK": cik_number
                })

    # Write the resulting data to a JSON file
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Example usage
input_file = 'input_data.txt'
output_file = 'output_data.json'
parse_txt_to_json(input_file, output_file)

