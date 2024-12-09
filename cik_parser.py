import requests
import json

#The goal of this parser is to take the input file produce an output json file to be used by the webscraper
#The result looks like the following:         "CIK": "0001993586", "company_name": "KERSHAW DAVID"
#The reason this was picked was because the 10K XBRL extraction file takes cik and name in order to make specific files. 

def extract_cik_from_txt(file_path):
    ciks = []
    with open(file_path, 'r') as file:
        for line in file:
            # Split the line by the colon and get the last part
            parts = line.strip().split(':')
            if len(parts) > 1:
                company_name = parts[0].strip()
                cik = parts[1].strip()  # Get the CIK part and remove whitespace
                if cik.isdigit():  # Check if the CIK is numeric
                    ciks.append({"CIK" : cik,
                                 "company_name" : company_name})
    return ciks

def write_ciks_to_json(cik_numbers, output_file):
    with open(output_file, 'w') as json_file:
        json.dump(cik_numbers, json_file, indent=4)  # Write CIK numbers to JSON with indentation

def main(txt_file, output_file):
    cik_numbers = extract_cik_from_txt(txt_file)
    write_ciks_to_json(cik_numbers, output_file)  # Write to JSON file
    print(f"Extracted CIK numbers written to {output_file}")

if __name__ == "__main__":
    #generalize the input json file. the input file needs to be in the same folder as this code. 

    txt_file_path = input("Enter the JSON FILE: ").strip()
    txt_file_path += '.txt'  # Update with your file path
    output_file_path = './cik_numbers.json'  # Output JSON file 
    main(txt_file_path, output_file_path)
