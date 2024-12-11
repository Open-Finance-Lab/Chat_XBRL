import json

def parse_data_from_file(file_path):
    with open(file_path, 'r', encoding='latin-1') as file:
        lines = file.readlines()  
        
    parsed_data = []
    for line in lines:
        if ':' in line:
            parts = line.split(':', 1)
            name = parts[0].strip()
            cik = parts[1].strip().rstrip(':') 
            parsed_data.append({"name": name, "cik": cik})
    
    return parsed_data

input_file_path = "cik-lookup-data.txt" 

parsed_data = parse_data_from_file(input_file_path)

json_output = json.dumps(parsed_data, indent=4)

output_file_path = "parsed_companies.json"

with open(output_file_path, "w") as json_file:
    json_file.write(json_output)
