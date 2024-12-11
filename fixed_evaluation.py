import xml.etree.ElementTree as ET  # For parsing XML files.
import json  # For handling JSON data.

def extract_xbrl_tags(queries):
    """
    Processes a list of queries to extract specific XBRL tags from XML files.

    Args:
        queries (list): A list of dictionaries, where each dictionary contains:
                        - 'doc_path' (str): The path to the XML document.
                        - 'id' (list): A list of tag IDs to extract.

    Returns:
        list: A list of results, where each result is a dictionary containing:
              - 'id' (int): A unique identifier for the query.
              - 'query' (str): The query string.
              - 'text' (str): Extracted XML content for the specified tags.
              - 'answer' (str): A representative answer from the extracted tags.
    """
    results = []  # List to store the extracted results.
    i = 0  # Counter for result IDs.

    for idx, query in enumerate(queries):
        doc_path = f'./DowJones30/{query["doc_path"]}'  # Construct the full file path.
        print(f"Processing file: {doc_path}")
        tags = query.get('id', [])  # Retrieve the list of tags to extract.

        # Skip queries with no tags.
        if not tags:
            continue

        try:
            # Parse the XML file and get its root element.
            tree = ET.parse(doc_path)
            root = tree.getroot()
        except FileNotFoundError:
            # Handle case where the file does not exist.
            print(f"File not found: {doc_path}")
            continue
        except ET.ParseError as e:
            # Handle XML parsing errors.
            print(f"XML Parsing Error in {doc_path}: {e}")
            continue

        # Create a set of tags for fast membership checking.
        tag_set = set(tags)

        # Gather all elements with an 'id' attribute.
        id_elements = []
        for elem in root.iter():
            elem_id = elem.get('id')
            if elem_id:  # Only include elements with a valid 'id' attribute.
                id_elements.append((elem_id, elem))

        extracted_data = []  # List to store extracted content for the current query.
        
        # Calculate the window size for surrounding context.
        window_size = 100 // len(tags) if tags else 0

        # Extract data for each tag in the tag set.
        for idx, (elem_id, elem) in enumerate(id_elements):
            if elem_id in tag_set:
                # Determine the range of elements to include for context.
                start = max(0, idx - window_size // 2)
                end = min(len(id_elements), idx + window_size // 2 + 1)

                # Collect formatted data for elements in the context window.
                for _, current_elem in id_elements[start:end]:
                    extracted_string = format_element_data(current_elem)
                    extracted_data.append(extracted_string)

        # Format the output for the current query.
        if extracted_data:
            result = {
                "id": idx + 1,  # Unique result ID.
                "query": query['query'],  # The original query string.
                "text": ''.join(extracted_data),  # Concatenated extracted content.
                "answer": f"Answer:{tag_set.pop()}"  # Use one tag as a sample answer.
            }
            results.append(result)

    return results  # Return all extracted results.

def format_element_data(elem):
    """
    Formats the data of an XML element for output.

    Args:
        elem (Element): The XML element to format.

    Returns:
        str: A formatted string containing the element's tag, attributes, and text content.
    """
    return (f"file:{elem.get('contextRef')}.xml\n"
            f"<{elem.tag} contextRef=\"{elem.get('contextRef', 'None')}\" "
            f"decimals=\"{elem.get('decimals', 'None')}\" "
            f"id=\"{elem.get('id', 'None')}\" "
            f"unitRef=\"{elem.get('unitRef', 'None')}\">{elem.text.strip() if elem.text else 'None'}</{elem.tag}>\n")

# Load queries from a JSON file.
with open('./XBRL.json', 'r') as file:
    queries = json.load(file)

# Process the queries to extract XBRL tags.
formatted_results = extract_xbrl_tags(queries)

# Convert the results to a JSON string with pretty formatting.
formatted_json = json.dumps(formatted_results, indent=4)

# Save the formatted JSON results to a file.
with open('./Updated_XBRL.json', 'w') as outfile:
    outfile.write(formatted_json)
