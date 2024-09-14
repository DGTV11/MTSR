import math

## User variables
# OLLAMA_LLM = "qwen2:1.5b"
OLLAMA_LLM = "gemma2:2b-instruct-q5_0"
# OLLAMA_LLM = "openhermes"

## System variables
CTX_WINDOW = 8192
MAX_SEARCH_DEPTH = 25
NUMBER_OF_NEW_NODES_PER_EXPANSION = 3
NUMBER_OF_REWARD_SAMPLES = 3
NUMBER_OF_TERMINAL_CHECK_SAMPLES = 3
TERMINAL_SCORE_THRESHOLD = 85
OVERSCORE_REDUCTION_CONSTANT = 5
UCT_E = 0.1
UCT_C = math.sqrt(2)

LLM_SYSTEM_PROMPT = r"Always assist with care, respect, and truth. Respond with utmost utility yet securely and in a conversational and friendly tone. Avoid harmful, unethical, prejudiced, or negative content. Ensure replies promote fairness and positivity. You are allowed to give feedback (even on your own responses) if required. You are also capable of refining your own responses if required."

EXPANSION_PROMPT = "Generate ONE and ONE and ONLY ONE reasoning step detailing ONE step of your strategy to respond to the initial query BASED on the initial query and the previous reasoning step(s) if any. You MUST not respond directly to the initial query! That reasoning step MUST be numbered from 1 onwards depending on how many previous reasoning steps there are."

FEEDBACK_PROMPT = 'Please give strict and direct feedback on your generated reasoning step. Do NOT give feedback on the initial query - ONLY give feedback on your response based on how well your generated reasoning step answers the initial query, "$QUERY". Do NOT give entirely positive feedback - you MUST find AS MANY things that CAN AND MUST be improved as possible (e.g. phrasing, content, factuality). Make sure that your feedback is SPECIFIC (i.e. identifying concrete phrases in or parts of the reasoning step to change) and ACTIONABLE (i.e. identifying concrete actions that would likely improve the reasoning step). ONLY give the feedback and your thought process behind it AND NOTHING ELSE (not even a revised reasoning step). You are capable of giving strict and direct feedback that is specific and actionable, and therefore MUST do so. DO NOT REFUSE TO GIVE FEEDBACK!!! Let\'s think step by step.'

REFINE_PROMPT = "Give me a revised reasoning step, incorporating all necessary improvements based on the feedback. Generate the reasoning step as if you are directly making a new reasoning step, without mentioning your feedback or your inital reasoning step AT ALL. DO NOT mention that you are giving a refined reasoning step AT ALL - you must pretend that this is your inital generated reasoning step, as you will FORGET the initial generated reasoning step and self-feedback in the next user query!"

EVALUATION_PROMPT = 'Analyse the generated reasoning step strictly and directly. Your analysis MUST be based on HOW COMPLETE the chain of thought made up of ALL of the generated reasoning steps is in augmenting the generation of a WELL-WRITTEN answer to the inital query, "$QUERY". Do NOT give entirely positive feedback - you MUST find AS MANY things that CAN AND MUST be improved as possible (e.g. phrasing, content, factuality). You are capable of giving strict and direct feedback that is specific and actionable, and therefore MUST do so. DO NOT REFUSE TO MAKE AN EVALUATION!!! After your reasoning, you ABSOLUTELY MUST output an INTEGER score between [-100,+100] (i.e. from -100 to +100) between <output> tags (e.g. <output>0</output> for a final score of 0). The <output> tags ABSOLUTELY MUST ONLY BE USED TO ENCLOSE THE FINAL OUTPUT!!! Prompt format: "[reasoning] Final score: <output>[score]</output> ". Let\'s think step by step.'
