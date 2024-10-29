import xml.etree.ElementTree as ET
import json
instructions = {
    "formula_calculation": "The value must be calculated based on the exact numbers found in the source document. \
        The value must be consolidated from the main company, excluding any segment or scenario-specific data. \
        Ensure the correct context reference is used for the calculation (e.g., consolidated financials). \
        Provide the result either as a numeric value or a percentage, depending on the financial ratio.",
    "xbrl_tags": "The answer must be the exact consolidated tag found in the source document. \
            Also take any company-created or customized tags into consideration if they are relevant. \
            Provide the final XBRL tag as it appears in the source.",
    "value": "The value must be consolidated from the main company and should not include values from any segments or specific scenarios. \
        The answer must be the exact figure found in the source document. \
        Provide the exact value and format it as a monetary value in $ billion. Do not round the figure.",
    "formula_formatted_with_tags": "The formula must consist of the relevant XBRL tags found in the source document. \
                            Take any company-created or customized tags into consideration if applicable. \
                            Provide the full formula according to the structure of the specific financial ratio, \
                            using the exact XBRL tags as they appear in the source."
}

response_format = {
    "formula_calculation": "For numeric values: \"Answer: {number}\" For percentage values: \"Answer: \{number\}\%\"",
    "xbrl_tags": "Answer: {XBRL tag}",
    "value": "Answer: $[value] billion",
    "formula_formatted_with_tags": "Answer: {Complete formula with XBRL tags}"
}
def extract_xbrl_tags(queries):
    results = []
    i = 0
    for idx, query in enumerate(queries):
        if i == 10:
            break
        if query['category2'] != 'formula_calculation':
            continue
        
        doc_path = f'./DowJones30/{query["doc_path"]}'
        print(f"Processing file: {doc_path}")
        tags = query.get('id', [])

        if not tags:
            continue

        try:
            tree = ET.parse(doc_path)
            root = tree.getroot()
        except FileNotFoundError:
            print(f"File not found: {doc_path}")
            continue
        except ET.ParseError as e:
            print(f"XML Parsing Error in {doc_path}: {e}")
            continue

        # Create a set of tags for fast membership checking
        tag_set = set(tags)

        # First pass: Gather all elements with 'id' attribute
        id_elements = []
        for elem in root.iter():
            elem_id = elem.get('id')
            if elem_id:
                id_elements.append((elem_id, elem))

        extracted_data = []
        
        window_size = 100 // len(tags) if tags else 0

        for idx, (elem_id, elem) in enumerate(id_elements):
            if elem_id in tag_set:
                start = max(0, idx - window_size // 2)
                end = min(len(id_elements), idx + window_size // 2 + 1)

                for _, current_elem in id_elements[start:end]:
                    extracted_string = format_element_data(current_elem)
                    extracted_data.append(extracted_string)

        # Format output for the current query
        if extracted_data:
            result = {
                "id": idx + 1,
                "Query": query['query'],
                "Context": ''.join(extracted_data),
                "Additional Instructions": instructions[query['category2']],
                "Response Formats": response_format[query['category2']]
            }
            results.append(result)
            i+=1

    return results

def format_element_data(elem):
    return (f"file:{elem.get('contextRef')}.xml\n"
            f"<{elem.tag} contextRef=\"{elem.get('contextRef', 'None')}\" "
            f"decimals=\"{elem.get('decimals', 'None')}\" "
            f"id=\"{elem.get('id', 'None')}\" "
            f"unitRef=\"{elem.get('unitRef', 'None')}\">{elem.text.strip() if elem.text else 'None'}</{elem.tag}>\n")

# Load queries from JSON file
with open('./XBRL.json', 'r') as file:
    queries = json.load(file)

# Run the function and get results
formatted_results = extract_xbrl_tags(queries)

# Print the results as JSON
formatted_json = json.dumps(formatted_results, indent=4)

# Optionally, save the formatted JSON back to a file
with open('./formula_calculation.json', 'w') as outfile:
    outfile.write(formatted_json)
