import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig
from huggingface_hub import login

     

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B", token= '')
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-1B",token='')
     

device = 'cuda' if torch.cuda.is_available() else 'cpu'
model.to(device)

def ask_question(question, context, instructions, tokenizer, model):
    # Format the prompt with context and instructions
    prompt = f"Context: {context}\n\nInstructions: {instructions}\n\nQuestion: {question}\nAnswer:"
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    # Generate a response (rest of the function remains the same)
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=50)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    answer = response.split("Answer:")[-1].strip()
    return answer
     

def generate_responses(json_data, batch_size=5):
    responses = []
    tokenizer.pad_token = tokenizer.eos_token

    # Prompt format for clarity
    for item in json_data:
        # if i >= batch_size:
        #     break
        answer = ask_question(item['Query'], item['Context'], item.get('Additional Instructions'), tokenizer, model)
        responses.append({
            "query": item['Query'],
            # "input": item['Context'],
            "response": answer
        })

    return responses

json_file = "/formula_calculation.json"
df = pd.read_json(json_file)
json_data = df.to_dict(orient='records')

# Convert json_data to a Pandas DataFrame
json_data = pd.DataFrame(json_data)

first_item = json_data.iloc[0]  # Get the first row as a Series

answer = ask_question(
    first_item['Query'],
    first_item['Context'],
    first_item.get('Additional Instructions'),
    tokenizer,
    model
)
print("Query: ", first_item['Query'])
# print("Context", first_item['Context'])
print("Additional Instructions: ", first_item['Additional Instructions'])
print("Answer:  ", answer)

json_file = "/formula_calculation.json"
df = pd.read_json(json_file)
json_data = df.to_dict(orient='records')

# Generate responses and save
output_data = generate_responses(json_data)

with open('generated_responses.json', 'w') as f:
    json.dump(output_data, f, indent=2)

print("Responses have been saved to 'generated_responses.json'")
