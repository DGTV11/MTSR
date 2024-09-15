import curses
import configparser
import os
import requests

import openai
import ollama

# Sample configurations for different APIs
apis = {
    'OpenAI': {'needs_model': True, 'needs_key': True},
    'Groq': {'needs_model': True, 'needs_key': True},
    'Ollama': {'needs_model': True, 'needs_key': False}
}

CONFIG_FILE = 'config.ini'

def load_config():
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
    return config

def save_config(api, model, api_key):
    config = configparser.ConfigParser()
    config[api] = {
        'model': str(model),  # Convert model to string
        'api_key': str(api_key)  # Convert api_key to string
    }
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

def get_user_input(prompt, stdscr, y, x):
    curses.echo()
    max_y, max_x = stdscr.getmaxyx()
    
    # Ensure coordinates are within the terminal bounds
    if y >= max_y or x >= max_x:
        stdscr.addstr(0, 0, "Error: Coordinates out of bounds.")
        stdscr.refresh()
        return ""
    
    try:
        stdscr.addstr(y, x, prompt)
        stdscr.refresh()
        return stdscr.getstr(y, x + len(prompt)).decode()
    except curses.error as e:
        stdscr.addstr(y, x, f"Error: {e}")
        stdscr.refresh()
        return ""

def select_api(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Select API (Use arrow keys and Enter to select):")
    stdscr.refresh()

    choices = list(apis.keys())
    current_selection = 0

    while True:
        for idx, api in enumerate(choices):
            if idx == current_selection:
                stdscr.addstr(idx + 1, 0, f"> {api}", curses.A_REVERSE)
            else:
                stdscr.addstr(idx + 1, 0, f"  {api}")
        
        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP:
            current_selection = (current_selection - 1) % len(choices)
        elif key == curses.KEY_DOWN:
            current_selection = (current_selection + 1) % len(choices)
        elif key == ord('\n'):
            return choices[current_selection]

def select_model(stdscr, models):
    stdscr.clear()
    stdscr.addstr(0, 0, "Select Model (Use arrow keys and Enter to select):")
    stdscr.refresh()

    current_selection = 0

    while True:
        for idx, model in enumerate(models):
            if idx == current_selection:
                stdscr.addstr(idx + 1, 0, f"> {model}", curses.A_REVERSE)
            else:
                stdscr.addstr(idx + 1, 0, f"  {model}")
        
        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP:
            current_selection = (current_selection - 1) % len(models)
        elif key == curses.KEY_DOWN:
            current_selection = (current_selection + 1) % len(models)
        elif key == ord('\n'):
            return models[current_selection]

def fetch_openai_models(api_key):
    openai.api_key = api_key
    models = openai.Model.list()
    return [model['id'] for model in models['data']]

def fetch_groq_models(api_key):
    # Placeholder for Groq API model fetching
    return ['gemma2-9b-it', 'gemma-7b-it', 'llama-3.1-70b-versatile', 'llama-3.1-8b-instant', 'mixtral-8x7b-32768']  # Sample models for now

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

def main(stdscr):
    config = load_config()
    curses.curs_set(1)  # Show cursor
    api_choice = select_api(stdscr)

    saved_model = config.get(api_choice, 'model', fallback=None)
    saved_api_key = config.get(api_choice, 'api_key', fallback=None)

    current_model = saved_model or "None"
    current_api_key = saved_api_key or "None"

    stdscr.clear()
    stdscr.addstr(0, 0, f"Selected API: {api_choice}")
    stdscr.addstr(1, 0, f"Current Model: {current_model}")
    stdscr.addstr(2, 0, f"Current API Key: {current_api_key}")

    stdscr.refresh()

    if apis[api_choice]['needs_key']:
        api_key = get_user_input("Enter API key: ", stdscr, 5, 0)
    else:
        api_key = None

    # Fetch available models for the selected API
    if apis[api_choice]['needs_model']:
        models = get_models_for_api(api_choice, api_key)
        model = select_model(stdscr, models)
    else:
        model = "N/A"

    save_config(api_choice, model, api_key)

    stdscr.clear()
    stdscr.addstr(0, 0, "Configuration saved successfully!")
    stdscr.addstr(1, 0, f"API: {api_choice}")
    stdscr.addstr(2, 0, f"Model: {model}")
    stdscr.addstr(3, 0, f"API Key: {api_key}")
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
