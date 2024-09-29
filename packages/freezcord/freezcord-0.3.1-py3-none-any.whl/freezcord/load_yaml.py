import yaml

def load_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        file = yaml.safe_load(file)
    return file