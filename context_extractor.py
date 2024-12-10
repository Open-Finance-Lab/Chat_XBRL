import json
import os
from tqdm import tqdm

def extract_context_characters(doc_path, ids, context_length, base_dir="./DowJones30/"):
    """ Extracts a text section from a file based on IDs and context length."""
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

def process_dataset(original_file_path, prompt_file_path, output_file_path, base_dir="./DowJones30/", context_length=1000):
    """ Processes the dataset and generates a result JSON file."""
    with open(original_file_path, 'r') as f:
        data = json.load(f)
  with open(prompt_file_path, 'r') as f:
        prompt_data = json.load(f)

    category_to_prompt = {item["category"]: item["prompt"] for item in prompt_data}
    result_data = []
    progress_bar = tqdm(total=len(data), desc="Processing Entries", unit="entry")

    for i, entry in enumerate(data):
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
        extracted_text = extract_context_characters(doc_path, ids, context_length, base_dir)

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

    with open(output_file_path, 'w') as outfile:
        json.dump(result_data, outfile, indent=4)

    print(f"Result saved to {output_file_path}")

if __name__ == "__main__":
    original_file_path = './datasets/20360QA.json'
    prompt_file_path = './datasets/prompts.json'
    output_file_path = './datasets/result_dataset.json'

    process_dataset(original_file_path, prompt_file_path, output_file_path)
