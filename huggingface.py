import json
import pandas as pd
from huggingface_hub import HfApi, hf_hub_download
import numpy as np
import os
from requests.exceptions import HTTPError
import time

# Check if the Data folder exists, if not create it
if not os.path.exists("/home/user/HF-Models/"):
    os.makedirs("/home/user/HF-Models/")

# 1. Collect data
print('### 1/3: Calling API for models on HF Hub')
start_time = time.time()
api = HfApi() # token=token
models = list(api.list_models())
model_count = len(models)

# Filter models with X or more downloads
filtered_models = [model for model in models if model.likes and model.likes >= 100]
filtered_models_count = len(filtered_models)
end_time = time.time()
collect_time = end_time - start_time
print(f"Time taken to collect data for {filtered_models_count} / {model_count}  models: {collect_time:.2f} seconds")

# 2. Wrangle data into a pandas dataframe
print(f'### 2/3: Wrangling data for {filtered_models_count} models')
start_time = time.time()
data = []
for model in filtered_models:
    try:
        # Get all available information about the model
        model_info = api.model_info(model.modelId)
        
        # Extract the desired information
        model_id = model.modelId
        name = model_id.split('/')[1] if '/' in model_id else model_id
        organization = model_id.split('/')[0] if '/' in model_id else np.nan
        likes = model.likes
        license = next((tag.split(":")[1] for tag in model.tags if "license:" in tag), np.nan)
        datasets = [tag.split(':')[1] for tag in model.tags if tag.startswith('dataset:')] if any(tag.startswith('dataset:') for tag in model.tags) else 'Dataset not provided'

        # Check for 'transformers', 'diffusers', or none in the tags
        if 'transformers' in model.tags:
            architecture = 'Transformers'
        elif 'diffusers' in model.tags:
            architecture = 'Diffusion'
        else:
            architecture = ''
        
        url = f"https://huggingface.co/{model_id}"
        arxiv = next((f"https://arxiv.org/abs/{tag.split(':')[1]}" for tag in model.tags if tag.startswith('arxiv:')), 'Not Included')
        
        # Download the readme file
        try:
            readme_path = hf_hub_download(repo_id=model_id, filename="README.md")
            with open(readme_path, 'r') as file:
                model_card_content = file.read()
            model_card = 'Model Card Provided'
        except Exception:
            model_card_content = np.nan
            model_card = 'None'
        
        # Check for the specified tags and add them to the 'Supporting Libraries and Tools' list
        supporting_libraries = [tag for tag in model.tags if tag in ['pytorch', 'tensorslow', 'jax', 'transformers', 'safetensors', 'tensorboard', 'peft', 'diffusers', 'gguf', 'onnx', 'keras', 'adapters', 'flair', 'transformers.js', 'mlx', 'spacy', 'espnet', 'fastai', 'coreml', 'nemo', 'rust', 'joblib', 'bertopic', 'tfite', 'openvino', 'scikit-learn', 'openclip', 'paddlepaddle', 'fairseq', 'graphcore']]
        
        # Prepare a row to add to the list
        row_to_add = pd.Series({
            'Name': name,
            'Description': model_card_content,
            'Version/Parameters': np.nan,
            'Organization': organization,
            'Model Type': np.nan,
            'Architecture': architecture,
            'Training Treatment': np.nan,
            'Base Model': np.nan,
            'Model Architecture': license,
            'Data Preprocessing Code': np.nan,
            'Training Code': np.nan,
            'Inference Code': np.nan,
            'Evaluation Code': np.nan,
            'Supporting Libraries and Tools': supporting_libraries,
            'Datasets': datasets,
            'Model Parameters (Final)': np.nan,
            'Model Metadata': np.nan,
            'Model Parameters (Intermediate)': np.nan,
            'Evaluation Data': np.nan,
            'Sample Model Outputs': np.nan,
            'Evaluation Results': np.nan,
            'Model Card': model_card,
            'Data Card': np.nan,
            'Technical Report': np.nan,
            'Research Paper': arxiv,
            'Github Repo URL': np.nan,
            'HuggingFace Model URL': url,
            'Likes': likes
        })
        
        # Append the row to the list
        data.append(row_to_add)
    except Exception as e:
        print(f"Error processing model {model.modelId}: {str(e)}")
        continue

end_time = time.time()
wrangle_time = end_time - start_time
print(f"Time taken to wrangle data: {wrangle_time:.2f} seconds \n")

# Convert the list to a DataFrame
df = pd.DataFrame(data)
df = df.sort_values('Likes', ascending=False)

# 3. Save CSV file
df.to_csv('/home/user/HF-Models/hf-models-data-mot.csv', index=False)
print(f'### 3/3: Saved data for {filtered_models_count} models with at least 100 likes')
