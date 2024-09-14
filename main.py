from os import system as shell
from os import name as os_name

import ollama

from constants import *
from tree import search

wrap_chat_message = lambda role, content: {"role": role, "content": content}

global_chat_history = [wrap_chat_message("system", LLM_SYSTEM_PROMPT)]

def clear_shell():
    if os_name == "nt":
        shell("cls")
    else:
        shell("clear")

while True:
    user_message = input("user > ")
    global_chat_history.append(wrap_chat_message("user", user_message))

    # Thinking
    thoughts = ""
    for step in search(global_chat_history, OLLAMA_LLM):
        clear_shell()
        if step['finished']:
            thoughts = step["thoughts"]
            match step["finished"]:
                case 1:
                    finished_reason = "definite search completion"
                case 2:
                    finished_reason = "diminishing returns"
                case 3:
                    finished_reason = "maximum search depth reached"
            print(f'Finished reasoning with a Q value of {step["q_value"]} because of {finished_reason}.')
            print(f'Thoughts:\n\n{thoughts}\n\n')
        else:
            print(f'Best node has a Q value of {step["q_value"]}')
            print(f'Thoughts:\n{step["thoughts"]}\n\nResponse:')

    tmp_chat_history = (
        global_chat_history[:-1] + [
            wrap_chat_message("user", f"QUERY: \"{global_chat_history[-1]['content']}\"\n\nYOUR REASONING:\n{thoughts}\n\nGenerate a final response based on the given query and the reasoning steps that you have generated.")
        ]
    )
    response = ""
    for chunk in ollama.chat(model=self.model_name, messages=tmp_chat_history, stream=True, options={'num_ctx': CTX_WINDOW}):
        response += chunk['message']['content']
        print(chunk['message']['content'], end="", flush=True)
    global_chat_history.append(wrap_chat_message("assistant", thoughts+'\n\n'+response))

    clear_shell()
    for message in global_chat_history:
        if message["role"] == "system":
            continue
        print(f"{message['role']} > {message['content']}")
