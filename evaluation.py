import xml.etree.ElementTree as ET  # Importing the XML library for parsing XML documents.
import json  # Importing JSON library to handle JSON data.

def extract_xbrl_tags(queries):
    """
    Processes a list of queries to extract specific XBRL tags from XML documents, 
    formats the extracted data, and returns it as a structured result.

    Args:
        queries (list): A list of dictionaries containing 'doc_path' (path to the XML file)
                        and 'id' (list of tags to extract) for each query.

    Returns:
        list: A list of results for each query. Each result includes:
              - 'id': Index of the query.
              - 'query': The original query string.
              - 'text': The concatenated extracted data from the specified tags.
              - 'answer': An example answer using one of the tags.
    """
    results = []  # List to store results for all queries.
    i = 0  # Counter for assigning IDs to results.

    for idx, query in enumerate(queries):
        doc_path = f'./DowJones30/{query["doc_path"]}'  # Construct the file path for the XML document.
        print(f"Processing file: {doc_path}")
        tags = query.get('id', [])  # Retrieve the tags to search for.

        # Skip queries with no tags.
        if not tags:
            continue

        try:
            # Parse the XML document and get its root element.
            tree = ET.parse(doc_path)
            root = tree.getroot()
        except FileNotFoundError:
            # Handle case where the file is not found.
            print(f"File not found: {doc_path}")
            continue
        except ET.ParseError as e:
            # Handle XML parsing errors.
            print(f"XML Parsing Error in {doc_path}: {e}")
            continue

        # Create a set of tags for quick lookup.
        tag_set = set(tags)

        # First pass: Collect all elements with an 'id' attribute.
        id_elements = []
        for elem in root.iter():
            elem_id = elem.get('id')
            if elem_id:  # Only process elements with an 'id' attribute.
                id_elements.append((elem_id, elem))

        extracted_data = []  # List to store formatted data for the current query.
        
        # Calculate a window size for surrounding context based on the number of tags.
        window_size = 100 // len(tags) if tags else 0

        # Loop through elements with IDs and extract relevant data based on the tag set.
        for idx, (elem_id, elem) in enumerate(id_elements):
            if elem_id in tag_set:
                # Determine the range of surrounding elements to include in the output.
                start = max(0, idx - window_size // 2)
                end = min(len(id_elements), idx + window_size // 2 + 1)

                # Collect formatted data for elements in the determined range.
                for _, current_elem in id_elements[start:end]:
                    extracted_string = format_element_data(current_elem)
                    extracted_data.append(extracted_string)

        # Format the output for the current query.
        if extracted_data:
            result = {
                "id": idx + 1,  # Unique ID for this query result.
                "query": query['query'],  # The original query text.
                "text": ''.join(extracted_data),  # Concatenated extracted data.
                "answer": f"Answer:{tag_set.pop()}"  # Use one tag as a sample answer.
            }
            results.append(result)  # Add the result to the overall results list.

    return results  # Return all formatted results.

def format_element_data(elem):
    """
    Formats an XML element's data into a structured string with relevant attributes and content.

    Args:
        elem (Element): An XML element object.

    Returns:
        str: A formatted string representation of the element's data.
    """
    return (f"file:{elem.get('contextRef')}.xml\n"
            f"<{elem.tag} contextRef=\"{elem.get('contextRef', 'None')}\" "
            f"decimals=\"{elem.get('decimals', 'None')}\" "
            f"id=\"{elem.get('id', 'None')}\" "
            f"unitRef=\"{elem.get('unitRef', 'None')}\">{elem.text.strip() if elem.text else 'None'}</{elem.tag}>\n")

# Load queries from a JSON file.
with open('./XBRL.json', 'r') as file:
    queries = json.load(file)

# Process the queries and extract XBRL tags.
formatted_results = extract_xbrl_tags(queries)

# Convert the results into a JSON string with pretty printing.
formatted_json = json.dumps(formatted_results, indent=4)

# Save the formatted JSON results to a file.
with open('./Updated_XBRL.json', 'w') as outfile:
    outfile.write(formatted_json)
