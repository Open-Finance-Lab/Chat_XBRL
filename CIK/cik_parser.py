import json  # Importing the JSON module to handle JSON formatting and writing.

def parse_data_from_file(file_path):
    """
    Reads a file containing company names and CIKs, processes each line to extract 
    the name and CIK values, and returns a list of dictionaries with the parsed data.

    Args:
        file_path (str): The path to the input text file containing data in 'name:CIK' format.

    Returns:
        list: A list of dictionaries, each containing 'name' and 'cik' keys.
    """
    # Open the file in read mode with 'latin-1' encoding.
    with open(file_path, 'r', encoding='latin-1') as file:
        lines = file.readlines()  # Read all lines from the file.

    parsed_data = []  # Initialize an empty list to store the parsed data.

    # Loop through each line in the file.
    for line in lines:
        if ':' in line:  # Check if the line contains a colon ':' to separate name and CIK.
            parts = line.split(':', 1)  # Split the line into two parts: name and CIK.
            name = parts[0].strip()  # Extract and clean the name (remove leading/trailing spaces).
            cik = parts[1].strip().rstrip(':')  # Extract and clean the CIK (remove trailing colon, if any).
            # Add the parsed data as a dictionary to the list.
            parsed_data.append({"name": name, "cik": cik})
    
    return parsed_data  # Return the list of parsed dictionaries.

# Define the input file path containing the raw data.
input_file_path = "cik-lookup-data.txt"

# Call the function to parse the data from the input file.
parsed_data = parse_data_from_file(input_file_path)

# Convert the parsed data into a formatted JSON string with indentation for readability.
json_output = json.dumps(parsed_data, indent=4)

# Define the output file path where the JSON data will be saved.
output_file_path = "parsed_companies.json"

# Open the output file in write mode and write the JSON string to it.
with open(output_file_path, "w") as json_file:
    json_file.write(json_output)  # Write the JSON-formatted data to the file.
