import xml.etree.ElementTree as ET
import json

def extract_xbrl_tags(queries, max_queries=10):
    results = []
    processed_queries = 0

    for query in queries:
        if processed_queries >= max_queries:
            break

        doc_path = f'./DowJones30/{query["doc_path"]}'
        print(f"Processing file: {doc_path}")
        tags = query.get('id', [])

        if not tags:
            print(f"No tags found for query: {query['query']}")
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

        tag_set = set(tags)
        id_elements = [(elem.get('id'), elem) for elem in root.iter() if elem.get('id')]

        extracted_data = []
        window_size = max(1, 100 // len(tags))

        for idx, (elem_id, elem) in enumerate(id_elements):
            if elem_id in tag_set:
                start = max(0, idx - window_size // 2)
                end = min(len(id_elements), idx + window_size // 2 + 1)

                for _, current_elem in id_elements[start:end]:
                    extracted_data.append(format_element_data(current_elem))

        if extracted_data:
            result = {
                "id": processed_queries + 1,
                "query": query['query'],
                "text": ''.join(extracted_data),
                "answer": f"Answer: {tag_set.pop()}" if tag_set else "Answer: Not Found"
            }
            results.append(result)
            processed_queries += 1

    return results

def format_element_data(elem):
    return (
        f"file:{elem.get('contextRef', 'None')}.xml\n"
        f"<{elem.tag} contextRef=\"{elem.get('contextRef', 'None')}\" "
        f"decimals=\"{elem.get('decimals', 'None')}\" "
        f"id=\"{elem.get('id', 'None')}\" "
        f"unitRef=\"{elem.get('unitRef', 'None')}\">"
        f"{elem.text.strip() if elem.text else 'None'}</{elem.tag}>\n"
    )

if __name__ == "__main__":
    with open('./XBRLBench-use.json', 'r') as file:
        queries = json.load(file)

    formatted_results = extract_xbrl_tags(queries)

    formatted_json = json.dumps(formatted_results, indent=4)

    with open('./Updated_XBRL.json', 'w') as outfile:
        outfile.write(formatted_json)
