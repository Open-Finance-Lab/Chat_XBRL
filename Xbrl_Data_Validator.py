import xml.etree.ElementTree as ET
import json

def validate_xbrl_data(file_path, required_fields):
    """ Validates XBRL data in a given XML file. """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        validation_results = []

        for elem in root.iter():
            elem_id = elem.get('id')
            if elem_id:
                missing_fields = [field for field in required_fields if elem.get(field) is None]
                
                if missing_fields:
                    validation_results.append({
                        "element_id": elem_id,
                        "missing_fields": missing_fields
                    })

        return validation_results
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except ET.ParseError as e:
        print(f"XML Parsing Error in {file_path}: {e}")
        return []

# Example usage
if __name__ == "__main__":
    # Load queries from JSON file
    with open('./XBRLquestions.json', 'r') as file:
        queries = json.load(file)

    required_fields = ['contextRef', 'decimals', 'unitRef']
    
    for query in queries:
        doc_path = f'./DowJones30/{query["doc_path"]}'
        print(f"Validating file: {doc_path}")
        validation_results = validate_xbrl_data(doc_path, required_fields)

        if validation_results:
            print(f"Validation issues found in {doc_path}:")
            print(json.dumps(validation_results, indent=4))
        else:
            print(f"No validation issues found in {doc_path}")
