from os import system as shell
from os import name as os_name

import ollama

from constants import *

wrap_chat_message = lambda role, content: {"role": role, "content": content}

global_chat_history = [wrap_chat_message("system", LLM_SYSTEM_PROMPT)]

def self_refine_inference(chat_history, model_name):
    # Get initial response (1)
    stream = ollama.chat(model=model_name, messages=chat_history, stream=True)

    assistant_message_content = ""
    for chunk in stream:
        chunk_content = chunk["message"]["content"]
        assistant_message_content += chunk_content
        yield chunk_content

    chat_history.append(wrap_chat_message("assistant", assistant_message_content))
    yield 1

    # Get feedback (2)
    chat_history.append(wrap_chat_message("user", FEEDBACK_PROMPT.replace('$QUERY', user_message)))
    stream = ollama.chat(model=model_name, messages=chat_history, stream=True)

    assistant_message_content = ""
    for chunk in stream:
        chunk_content = chunk["message"]["content"]
        assistant_message_content += chunk_content
        yield chunk_content

    chat_history.append(wrap_chat_message("assistant", assistant_message_content))

    yield 2
    # Get final response (3)
    chat_history.append(wrap_chat_message("user", REFINE_PROMPT.replace('$QUERY', user_message)))
    stream = ollama.chat(model=model_name, messages=chat_history, stream=True)

    assistant_message_content = ""
    for chunk in stream:
        chunk_content = chunk["message"]["content"]
        assistant_message_content += chunk_content
        yield chunk_content

    yield 3

    for _ in range(4):
        chat_history.pop()
    chat_history.append(wrap_chat_message("assistant", assistant_message_content))
    yield chat_history

if os_name == 'nt':
    shell("cls")
else:
    shell("clear")
while True:
    user_message = input("user > ")
    global_chat_history.append(wrap_chat_message("user", user_message))

    inference_stream = self_refine_inference(global_chat_history, OLLAMA_LLM)

    print("GETTING INITIAL RESPONSE...")

    for chunk in inference_stream:
        if type(chunk) is int:
            break
        print(chunk, end="", flush=True)

    print()
    print("GETTING FEEDBACK...")

    for chunk in inference_stream:
        if type(chunk) is int:
            break
        print(chunk, end="", flush=True)

    print()
    print("GETTING FINAL RESPONSE...")

    for chunk in inference_stream:
        if type(chunk) is int:
            break
        print(chunk, end="", flush=True)

    global_chat_history = next(inference_stream)
    if os_name == 'nt':
        shell("cls")
    else:
        shell("clear")
    for message in global_chat_history:
        if message["role"] == "system":
            continue
        print(f"{message['role']} > {message['content']}")
