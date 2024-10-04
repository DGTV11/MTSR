import configparser
import os
from os import name as os_name
from os import system as shell
import requests
import openai
import ollama

apis = {
    'OpenAI': {'needs_model': True, 'needs_key': True},
    'Groq': {'needs_model': True, 'needs_key': True},
    'Ollama': {'needs_model': True, 'needs_key': False}
}

CONFIG_FILE = 'config.ini'

def clear_shell():
    if os_name == "nt":
        shell("cls")
    else:
        shell("clear")

def load_config():
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
    return config

def save_config(api, model, api_key, model_type):
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
    config[f"{api}_{model_type}"] = {
        'model': str(model),  # Convert model to string
        'api_key': str(api_key)  # Convert api_key to string
    }
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

def select_api():
    print("Select API:")
    choices = list(apis.keys())
    for idx, api in enumerate(choices):
        print(f"{idx + 1}. {api}")
    
    while True:
        choice = input("Enter the number corresponding to the API: ")
        if choice.isdigit() and 1 <= int(choice) <= len(choices):
            return choices[int(choice) - 1]
        else:
            print("Invalid choice. Please select a valid option.")

def select_model(models):
    print("Select Model:")
    for idx, model in enumerate(models):
        print(f"{idx + 1}. {model}")
    
    while True:
        choice = input("Enter the number corresponding to the model: ")
        if choice.isdigit() and 1 <= int(choice) <= len(models):
            return models[int(choice) - 1]
        else:
            print("Invalid choice. Please select a valid model.")

def fetch_openai_models(api_key):
    openai.api_key = api_key
    models = openai.models.list()
    return [model['id'] for model in models['data']]

def fetch_groq_models(api_key):
    return ['gemma2-9b-it', 'gemma-7b-it', 'llama-3.1-70b-versatile', 'llama-3.1-8b-instant', 'mixtral-8x7b-32768']

def fetch_ollama_models():
    return list(map(lambda m: m['name'], ollama.list()['models']))

def get_models_for_api(api_choice, api_key):
    if api_choice == 'OpenAI':
        return fetch_openai_models(api_key)
    elif api_choice == 'Groq':
        return fetch_groq_models(api_key)
    elif api_choice == 'Ollama':
        return fetch_ollama_models()
    else:
        return []

def main():
    config = load_config()

    # Configure Reasoning Model
    clear_shell()
    print("\n--- Configure Reasoning Model ---")
    reasoning_api_choice = select_api()

    # Fetch saved API key and model for reasoning
    saved_reasoning_model = config.get(f"{reasoning_api_choice}_reasoning", 'model', fallback=None)
    saved_reasoning_api_key = config.get(f"{reasoning_api_choice}_reasoning", 'api_key', fallback=None)

    print(f"Selected API: {reasoning_api_choice}")
    print(f"Current Reasoning Model: {saved_reasoning_model or 'None'}")
    print(f"Current Reasoning API Key: {saved_reasoning_api_key or 'None'}")

    # Input API key if needed
    if apis[reasoning_api_choice]['needs_key']:
        reasoning_api_key = input("Enter API key (or press Enter to keep current): ") or saved_reasoning_api_key
    else:
        reasoning_api_key = None

    print('\n\n')

    # Fetch models and select one if applicable
    if apis[reasoning_api_choice]['needs_model']:
        reasoning_models = get_models_for_api(reasoning_api_choice, reasoning_api_key)
        reasoning_model = select_model(reasoning_models)
    else:
        reasoning_model = "N/A"

    # Save reasoning model configuration
    save_config(reasoning_api_choice, reasoning_model, reasoning_api_key, model_type="reasoning")

    # Configure Response Model
    clear_shell()
    print("\n--- Configure Response Model ---")
    response_api_choice = select_api()

    # Fetch saved API key and model for response
    saved_response_model = config.get(f"{response_api_choice}_response", 'model', fallback=None)
    saved_response_api_key = config.get(f"{response_api_choice}_response", 'api_key', fallback=None)

    print(f"Selected API: {response_api_choice}")
    print(f"Current Response Model: {saved_response_model or 'None'}")
    print(f"Current Response API Key: {saved_response_api_key or 'None'}")

    # Input API key if needed
    if apis[response_api_choice]['needs_key']:
        response_api_key = input("Enter API key (or press Enter to keep current): ") or saved_response_api_key
    else:
        response_api_key = None

    print('\n\n')

    # Fetch models and select one if applicable
    if apis[response_api_choice]['needs_model']:
        response_models = get_models_for_api(response_api_choice, response_api_key)
        response_model = select_model(response_models)
    else:
        response_model = "N/A"

    # Save response model configuration
    save_config(response_api_choice, response_model, response_api_key, model_type="response")

    print("\nConfiguration saved successfully!")
    print(f"Reasoning Model - API: {reasoning_api_choice}, Model: {reasoning_model}, API Key: {reasoning_api_key}")
    print(f"Response Model - API: {response_api_choice}, Model: {response_model}, API Key: {response_api_key}")

if __name__ == "__main__":
    main()

