import json
import os
from langchain_community.llms import Ollama

def load_prompt(prompt_name):
    prompt_path = os.path.join(os.path.dirname(__file__), 'prompts', prompt_name)
    with open(prompt_path, 'r') as file:
        return file.read()

def load_config(config_name):
    config_path = os.path.join(os.path.dirname(__file__), 'configs', config_name)
    with open(config_path, 'r') as file:
        return json.load(file)

def initialize_model(config_name, prompt_name):
    config = load_config(config_name)
    prompt = load_prompt(prompt_name)
    
    return Ollama(
        base_url=config['base_url'],
        model=config['model'],
        system=prompt,
        temperature=config['temperature'],
        tfs_z=config['tfs_z'],
        metadata=config['metadata'],
        format=config['format']
    )
