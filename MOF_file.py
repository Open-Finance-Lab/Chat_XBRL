import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig
from huggingface_hub import login

json_file = '/path_to_file/samplemof.json'
df = pd.read_json(json_file)

# Display the first few rows of the dataframe
print(df.head())

#tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3.1-8B", token='')
#config = AutoConfig.from_pretrained("meta-llama/Meta-Llama-3.1-8B", token='')
#print(config)
#model = AutoModelForCausalLM.from_pretrained("meta-llama/Meta-Llama-3.1-8B", config=config, token='')
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-3B-Instruct", token= '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')
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-3B-Instruct",token='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')

device = 'cuda' if torch.cuda.is_available() else 'cpu'
model.to(device)

# 0-shot, answering questions every time in a size of 5
def generate_responses(questions, batch_size=5):
    responses = []
    tokenizer.pad_token = tokenizer.eos_token
    for i in range(0, len(questions), batch_size):
        batch_questions = questions[i:i + batch_size]
        inputs = tokenizer.batch_encode_plus(
            batch_questions,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        ).to('cuda')

        outputs = model.generate(
            input_ids=inputs['input_ids'],
            attention_mask=inputs['attention_mask'],
            max_length= 750,  # Set to the maximum length you need
            pad_token_id=tokenizer.eos_token_id,  # Set the end token
            no_repeat_ngram_size=2  # Optional: Prevent the generation of repeated 2-length n-grams
        )

        batch_responses = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
        responses.extend(batch_responses)

    return responses

df['evidence_text'] = generate_responses(df['Question'].tolist())

# Save the updated dataframe to a new CSV file
output_json_file = 'Llama-3.2-MOF.json'
df.to_json(output_json_file, index=False)

print(f"Responses have been generated and saved to {output_json_file}")

# Load and display the first few rows of the output CSV file for verification
output_df = pd.read_json(output_json_file)
print(output_df.head())
