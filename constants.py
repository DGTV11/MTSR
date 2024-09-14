## User variables
# OLLAMA_LLM = "qwen2:1.5b"
OLLAMA_LLM = "gemma2:2b-instruct-q5_0"
# OLLAMA_LLM = "openhermes"

## System variables
LLM_SYSTEM_PROMPT = r"Always assist with care, respect, and truth. Respond with utmost utility yet securely and in a conversational and friendly tone. Avoid harmful, unethical, prejudiced, or negative content. Ensure replies promote fairness and positivity. You are allowed to give feedback (even on your own responses) if required. You are also capable of refining your own responses if required."

FEEDBACK_PROMPT = "Please give strict and direct feedback on your previous response. Do NOT give feedback on the initial query - ONLY give feedback on your response based on how well your previous response answers the initial query, \"$QUERY\". Do NOT give entirely positive feedback - you MUST find AS MANY things that CAN AND MUST be improved as possible (e.g. phrasing, content, factuality). Make sure that your feedback is SPECIFIC (i.e. identifying concrete phrases in/parts of the output to change) and ACTIONABLE (i.e. identifying concrete actions that would likely improve the response). ONLY give the feedback and your thought process behind it AND NOTHING ELSE (not even a revised response). You are capable of giving strict and direct feedback that is specific and actionable, and therefore MUST do so. DO NOT REFUSE TO GIVE FEEDBACK!!! Let's think step by step."

REFINE_PROMPT = "Give me a revised response to the initial query \"$QUERY\", incorporating all necessary improvements based on the feedback. Address the query as if you are responding to it directly, without mentioning your feedback or your inital response AT ALL. DO NOT mention that you are giving a refined response AT ALL - you must pretend that this is your inital response, as you will FORGET the initial response and self-feedback in the next user query!"


