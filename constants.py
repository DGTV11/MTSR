import math


## User variables
# OLLAMA_LLM = "gemma2:2b-instruct-q5_0"

## System variables
MAX_NO_MAIN_REASONING_PHASES = 2
NUMBER_OF_NEW_NODES_PER_EXPANSION = 3
NUMBER_OF_SELF_REFINE_ITERATIONS = 1
NUMBER_OF_REWARD_SAMPLES = 3
# TERMINAL_SCORE_THRESHOLD = 85
DIMINISHING_RETURNS_THRESHOLD = 0.01
OVERSCORE_REDUCTION_CONSTANT = 5
UCT_E = 0.1
UCT_C = math.sqrt(2)
VERBOSE_MODE = True
SHOW_THOUGHTS_AFTER_EACH_STEP = True

# Helper functions
def clear_shell():
    if os_name == "nt":
        shell("cls")
    else:
        shell("clear")

def printd(string):
    if VERBOSE_MODE:
        print(string)

def clear_shelld():
    if VERBOSE_MODE:
        clear_shell()

wrap_chat_message = lambda role, content: {"role": role, "content": content}
