import json
import os
from tqdm import tqdm

original_file_path = './XBRLBench-use.json'
base_dir = './DowJones30/'
context_length = 1000  # Maximum characters to extract in total
prompt_file_path = './prompts.json'

with open(original_file_path, 'r') as f:
    data = json.loads(f.read())
with open(prompt_file_path, 'r') as f:
    prompt_data = json.loads(f.read())

category_to_prompt = {item["category"]: item["prompt"] for item in prompt_data}

# Given document path, id list, and maximum length for context
# Return a string containing the coresponding text section from the file
# If len(ids)=2 and context_length = 1000, we locate the two lines containing the id
# and look 250 line before and after the founded 2 lines (total 1000 lines)
def extract_context_characters(doc_path, ids, context_length):
    full_path = os.path.join(base_dir, doc_path)
    if not os.path.exists(full_path):
        print(f"File {full_path} does not exist.")
        return ""

    with open(full_path, 'r') as xml_file:
        content = xml_file.read()

    total_chars = len(content)
    split_context = context_length // len(ids)

    extracted_text = []

    for idx, target_id in enumerate(ids):
        id_position = content.find(target_id)

        if id_position == -1:
            print(f"ID {target_id} not found in {full_path}")
            continue

        context_before = split_context // 2
        context_after = split_context // 2

        if idx == len(ids) - 1:
            remaining_chars = context_length - len(extracted_text)
            context_before = remaining_chars // 2
            context_after = remaining_chars // 2

        start = max(0, id_position - context_before)
        end = min(total_chars, id_position + len(target_id) + context_after)
        extracted_text.append(content[start:end])

    return ''.join(extracted_text)


result_data = []
progress_bar = tqdm(total=20360, desc="Processing Entries", unit="entry")

for i, entry in enumerate(data):
    # Break on first 100 for testing
    if i >= 100:
        break

    ids = entry['id']
    doc_path = entry['doc_path']
    query = entry['query']
    answer = entry['answer']

    # Append prompts based on category1 and category2
    if entry['category1'] in category_to_prompt:
        query += f" {category_to_prompt[entry['category1']]}"
    if entry['category2'] in category_to_prompt:
        query += f" {category_to_prompt[entry['category2']]}"

    # Extract text based on the ID(s) from the corresponding XML file
    extracted_text = extract_context_characters(doc_path, ids, context_length)

    # Add file reference at the beginning of the text
    file_reference = f"file:{doc_path.split('/')[-1]}\n"
    full_text = file_reference + extracted_text

    new_entry = {
        "id": i + 1,
        "query": query,
        "text": full_text,
        "answer": answer
    }

    result_data.append(new_entry)
    progress_bar.update(1)

progress_bar.close()


output_file_path = './datasets/result_dataset.json'
with open(output_file_path, 'w') as outfile:
    json.dump(result_data, outfile, indent=4)

print(f"Result saved to {output_file_path}")
