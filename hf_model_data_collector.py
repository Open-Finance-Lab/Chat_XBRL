import json
import pandas as pd
from huggingface_hub import HfApi, hf_hub_download
import numpy as np
import os
from requests.exceptions import HTTPError
import time

def collect_model_data(min_likes=100, output_folder="/home/user/HF-Models/"):
    """ Collects and processes model data from Hugging Face Hub."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    print('### 1/3: Calling API for models on HF Hub')
    start_time = time.time()
    api = HfApi()
    models = list(api.list_models())
    filtered_models = [model for model in models if model.likes and model.likes >= min_likes]
    collect_time = time.time() - start_time
    print(f"Time taken to collect data for {len(filtered_models)} models: {collect_time:.2f} seconds")

    print(f'### 2/3: Wrangling data for {len(filtered_models)} models')
    data = []
    for model in filtered_models:
        try:
            model_info = api.model_info(model.modelId)
            model_id = model.modelId
            name = model_id.split('/')[1] if '/' in model_id else model_id
            organization = model_id.split('/')[0] if '/' in model_id else np.nan
            likes = model.likes
            license = next((tag.split(":")[1] for tag in model.tags if "license:" in tag), np.nan)
            datasets = [tag.split(':')[1] for tag in model.tags if tag.startswith('dataset:')] or 'Dataset not provided'
            architecture = 'Transformers' if 'transformers' in model.tags else ('Diffusion' if 'diffusers' in model.tags else '')
            url = f"https://huggingface.co/{model_id}"
            arxiv = next((f"https://arxiv.org/abs/{tag.split(':')[1]}" for tag in model.tags if tag.startswith('arxiv:')), 'Not Included')
            
            try:
                readme_path = hf_hub_download(repo_id=model_id, filename="README.md")
                with open(readme_path, 'r') as file:
                    model_card_content = file.read()
                model_card = 'Model Card Provided'
            except Exception:
                model_card_content = np.nan
                model_card = 'None'

            supporting_libraries = [
                tag for tag in model.tags if tag in [
                    'pytorch', 'tensorslow', 'jax', 'transformers', 'safetensors', 'tensorboard', 'peft',
                    'diffusers', 'gguf', 'onnx', 'keras', 'adapters', 'flair', 'transformers.js', 'mlx',
                    'spacy', 'espnet', 'fastai', 'coreml', 'nemo', 'rust', 'joblib', 'bertopic', 'tfite',
                    'openvino', 'scikit-learn', 'openclip', 'paddlepaddle', 'fairseq', 'graphcore'
                ]
            ]

            row_to_add = {
                'Name': name,
                'Description': model_card_content,
                'Organization': organization,
                'Architecture': architecture,
                'License': license,
                'Datasets': datasets,
                'Supporting Libraries': supporting_libraries,
                'Model Card': model_card,
                'Research Paper': arxiv,
                'HuggingFace Model URL': url,
                'Likes': likes
            }
            data.append(row_to_add)
        except Exception as e:
            print(f"Error processing model {model.modelId}: {str(e)}")
            continue

    df = pd.DataFrame(data).sort_values('Likes', ascending=False)
    output_file = os.path.join(output_folder, 'hf-models-data.csv')
    df.to_csv(output_file, index=False)
    print(f'### 3/3: Saved data for {len(filtered_models)} models with at least {min_likes} likes')

if __name__ == "__main__":
    collect_model_data()
