import sys
import re
import time
import datetime

from llm import *

from constants import *
from prompts import *
from tree import search

global_chat_history = [wrap_chat_message("system", LLM_SYSTEM_PROMPT)]


"""
def clear_shell():
    pass
"""


def mtsr(messages):
    if messages[-1]["role"] != "user":
        raise ValueError("Last message must be a user message")

    start_time = time.time()

    # Reasoning phase list generation
    estimations = []
    for i, estimation_type in enumerate(THREE_POINT_ESTIMATE_TYPES):
        printd(
            f"Getting main reasoning phase count estimate {i+1}/{len(THREE_POINT_ESTIMATE_TYPES)} ({estimation_type.lower()} estimate)"
        )

        tmp_chat_history = messages[:-1] + [
            wrap_chat_message(
                "user",
                NO_OF_MAIN_REASONING_STEPS_ESTIMATION_PROMPT.replace(
                    "$QUERY", messages[-1]["content"]
                ).replace("$ESTIMATION_TYPE", estimation_type),
            )
        ]

        j = 0
        res = []
        while not res:
            j += 1
            printd(f"Attempt no. {j}")
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
    for step in search(messages, reasoning_phases):
        clear_shelld()
        if step["finished"]:
            printd(f'Finished reasoning with a Q value of {step["q_value"]}.')

            printd(f'Thoughts:\n{step["thoughts"]}')
        else:
            printd(f'Current best node has a Q value of {step["q_value"]}')
            printd(f'Thoughts:\n{step["thoughts"]}')

    # Response
    tmp_chat_history = global_chat_history[:-1] + [
        wrap_chat_message(
            "user",
            GENERATION_PROMPT.replace("$QUERY", messages[-1]["content"]).replace(
                "$THOUGHTS", thoughts
            ),
        )
    ]
    response = chat(
        model="response",
        messages=tmp_chat_history,
    )[
        "message"
    ]["content"]

    end_time = time.time()

    return messages + [wrap_chat_message("assistant", response)], thoughts, step["q_value"], end_time - start_time


if __name__ == "__main__":
    clear_shell()
    while True:
        print("user (press Ctrl+D to finish) >")
        user_message = sys.stdin.read()
        global_chat_history.append(wrap_chat_message("user", user_message))

        clear_shell()

        global_chat_history, thoughts, final_q_value, time_taken = mtsr(global_chat_history)

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
            f'=============================\nFinished reasoning with a Q value of {final_q_value} in {str(datetime.timedelta(seconds=time_taken))}.'
        )
