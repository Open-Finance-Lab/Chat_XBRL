import yaml

def load_yaml(file_path):
    """Loads the YAML file."""
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"YAML file not found at {file_path}. Creating a new one.")
        return {}

def save_yaml(data, file_path):
    """Saves the updated data back to the YAML file."""
    with open(file_path, 'w') as file:
        yaml.dump(data, file, sort_keys=False)

def update_yaml_with_classification_and_badges(yaml_data, classification, badges):
    """Adds the classification and badges data to the 'release' section."""
    if 'release' not in yaml_data:
        yaml_data['release'] = {}
    yaml_data['release']['classification'] = classification
    yaml_data['release']['badges'] = badges
