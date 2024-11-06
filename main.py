import sys
from os import system as shell
from os import name as os_name
import re
import time
import datetime

from llm import *

from constants import *
from prompts import *
from tree import search

wrap_chat_message = lambda role, content: {"role": role, "content": content}

global_chat_history = [wrap_chat_message("system", LLM_SYSTEM_PROMPT)]


def clear_shell():
    if os_name == "nt":
        shell("cls")
    else:
        shell("clear")


"""
def clear_shell():
    pass
"""

clear_shell()
while True:
    print("user (press Ctrl+D to finish) >")
    user_message = sys.stdin.read()
    global_chat_history.append(wrap_chat_message("user", user_message))

    start_time = time.time()

    # Reasoning phase list generation
    clear_shell()
    estimations = []
    for i, estimation_type in enumerate(THREE_POINT_ESTIMATE_TYPES):
        print(
            f"Getting main reasoning phase count estimate {i+1}/{len(THREE_POINT_ESTIMATE_TYPES)} ({estimation_type.lower()} estimate)"
        )

        tmp_chat_history = global_chat_history[:-1] + [
            wrap_chat_message(
                "user",
                MAX_ROLLOUT_ESTIMATION_PROMPT.replace(
                    "$QUERY",
                    global_chat_history[-1]["content"].replace(
                        "$ESTIMATION_TYPE", estimation_type
                    ),
                ),
            )
        ]

        j = 0
        res = []
        while not res:
            j += 1
            print(f"Attempt no. {j}")
            evaluation_raw_txt = chat(
                model="reasoning",
                messages=tmp_chat_history,
            )[
                "message"
            ]["content"]
            reg_str = r"<output>(\d+)</output>"
            res = re.findall(reg_str, evaluation_raw_txt)
            if not res:
                continue
            single_estimation = max(int(res[-1]), 1)
            estimations.append(single_estimation)

    reasoning_phases = generate_reasoning_phases(
        min(
            ((estimations[0] + 4 * estimations[1] + estimations[2]) // 6),
            MAX_NO_MAIN_REASONING_PHASES,
        )
    )

    # Thinking
    thoughts = ""
    for step in search(global_chat_history, reasoning_phases):
        clear_shell()
        if step["finished"]:
            thoughts = step["thoughts"]
            # match step["reason"]:
            #     case 1:
            #         finished_reason = "definite search completion"
            #     case 2:
            #         finished_reason = "diminishing returns"
            #     case 3:
            #         finished_reason = "maximum search depth reached"
            print(
                # f'Finished reasoning with a Q value of {step["q_value"]} because of {finished_reason}.'
                f'Finished reasoning with a Q value of {step["q_value"]}.'
            )
            print(f"Thoughts:\n\n{thoughts}\n\nResponse:")
        else:
            print(f'Current best node has a Q value of {step["q_value"]}')
            print(f'Thoughts:\n{step["thoughts"]}')

    # Response
    tmp_chat_history = global_chat_history[:-1] + [
        wrap_chat_message(
            "user",
            GENERATION_PROMPT.replace(
                "$QUERY", global_chat_history[-1]["content"]
            ).replace("$THOUGHTS", thoughts),
        )
    ]
    response = chat(
        model="response",
        messages=tmp_chat_history,
    )[
        "message"
    ]["content"]
    print(response)
    global_chat_history.append(wrap_chat_message("assistant", response))

    end_time = time.time()
    time_taken = end_time - start_time

    clear_shell()
    for i, message in enumerate(global_chat_history, start=1):
        if message["role"] == "system":
            continue

        if i < len(global_chat_history):
            print(f"{message['role']} > {message['content']}")
        else:
            print(
                f"{message['role']} (with thoughts) > {thoughts}\n\n{message['content']}"
            )
    print(
        # f'=============================\nFinished reasoning with a Q value of {step["q_value"]} in {str(datetime.timedelta(seconds=time_taken))} because of {finished_reason}.'
        f'=============================\nFinished reasoning with a Q value of {step["q_value"]} in {str(datetime.timedelta(seconds=time_taken))}.'
    )
