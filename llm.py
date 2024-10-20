import logging
import configparser
import os

import openai

CONFIG_FILE = "config.ini"
LOG_FILE = "llm-out.log"

logger = logging.getLogger(__name__)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

apis = {
    "OpenAI": {"endpoint": "https://api.openai.com/v1/"},
    "Groq": {"endpoint": "https://api.groq.com/openai/v1/"},
    "Ollama": {"endpoint": "http://localhost:11434/v1/"},
}


def load_config():
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
    return config


def get_api_config():
    config = load_config()
    config_obj = {}

    for api_name in map(lambda s: s + "_reasoning", apis.keys()):
        if api_name in config:
            config_obj["reasoning"] = {
                "endpoint": apis[api_name.replace("_reasoning", "")]["endpoint"],
                "model": config.get(api_name, "model", fallback=None),
                "api_key": config.get(api_name, "api_key", fallback=None),
            }
            break
    else:
        return None

    for api_name in map(lambda s: s + "_response", apis.keys()):
        if api_name in config:
            config_obj["response"] = {
                "endpoint": apis[api_name.replace("_response", "")]["endpoint"],
                "model": config.get(api_name, "model", fallback=None),
                "api_key": config.get(api_name, "api_key", fallback=None),
            }
            break
    else:
        return None

    return config_obj


API_CONFIG = get_api_config()


# Main Chat Function
def chat(model, messages):
    """
    model -> 'reasoning' or 'response'
    """
    if API_CONFIG is None:
        raise ValueError("API configuration not found.")

    openai.base_url = API_CONFIG[model]["endpoint"]
    openai.api_key = API_CONFIG[model]["api_key"]

    # Get full response without streaming
    response = openai.chat.completions.create(
        model=API_CONFIG[model]["model"], messages=messages
    )

    # Logging
    logger.info(
        f"{model} gave a response of: {response.choices[0].message.content if response.choices else None}"
    )

    # Return the full message content
    return {
        "message": {
            "role": "assistant",
            "content": (
                response.choices[0].message.content if response.choices else None
            ),
        }
    }
