import xml.etree.ElementTree as ET
from collections import defaultdict

def extract_xbrl_tags(queries):
    for query in queries:
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

        # Create a map of prefixes to their target numbers
        tag_map = defaultdict(list)
        for tag in tags:
            prefix, number = tag.split('-')
            tag_map[prefix].append(number)

        # First pass: Gather all elements with 'id' attribute
        id_elements = []
        for elem in root.iter():
            elem_id = elem.get('id')
            if elem_id and '-' in elem_id:
                prefix, number = elem_id.split('-', 1)
                if prefix in tag_map:
                    id_elements.append((prefix, int(number), elem))

        id_elements.sort(key=lambda x: x[1])

        extracted_data = []
        
        window_size = 100 // len(tags)

        for idx, (prefix, number, elem) in enumerate(id_elements):
            if str(number) in tag_map[prefix]:
                start = max(0, idx - window_size // 2)
                end = min(len(id_elements), idx + window_size // 2 + 1)

                for _, _, current_elem in id_elements[start:end]:
                    extracted_string = format_element_data(current_elem)
                    extracted_data.append(extracted_string)

        if extracted_data:
            query['query'] += "\n\nExtracted XML Data:\n" + ''.join(extracted_data)

def format_element_data(elem):
    return (f"Tag: {elem.tag}, "
            f"Value: {elem.text.strip() if elem.text else 'None'}, "
            f"contextRef: {elem.get('contextRef', 'None')}, "
            f"decimals: {elem.get('decimals', 'None')}, "
            f"id: {elem.get('id', 'None')}, "
            f"unitRef: {elem.get('unitRef', 'None')}\n")

# test
queries = [
    {
        "id": [
            "f-57"
        ],
        "contextID": [
            "c-1"
        ],
        "doc_path": "amgn-20231231/amgn-20231231_htm.xml",
        "category1": "xbrl_data_extraction",
        "category2": "xbrl_tags",
        "query": "What is the US GAAP XBRL tag for Cost of Goods Sold as reported by Amgen Inc for the Fiscal Year ending in FY 2023? (Response format: XBRL tag, e.g., 'Answer: us-gaap:Depreciation')",
        "answer": "Answer:us-gaap:CostOfGoodsAndServicesSold",
        "raw_answer": "us-gaap:CostOfGoodsAndServicesSold",
        "xbrl_tag": [
            "us-gaap:CostOfGoodsAndServicesSold"
        ],
        "ticker": "AMGN",
        "template": "What is the US GAAP XBRL tag for {financial concept} as reported by {company name} for the {time period - noun} ending in {fiscal year/quarter}? (Response format: XBRL tag, e.g., 'Answer: us-gaap:Depreciation')",
        "{financial concept}": "Cost of Goods Sold",
        "{fiscal year/quarter}": "FY 2023",
        "{company name}": "Amgen Inc",
        "{time period - noun}": "Fiscal Year"
    }
]

# Run the function
extract_xbrl_tags(queries)

# Print the updated queries with appended XML data
for query in queries:
    print(query['query'])