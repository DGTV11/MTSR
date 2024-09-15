import math

## User variables
# OLLAMA_LLM = "qwen2:1.5b"
OLLAMA_LLM = "gemma2:2b-instruct-q5_0"
# OLLAMA_LLM = "openhermes"

## System variables
CTX_WINDOW = 8192
SEARCH_DEPTH_CAP = 50
NUMBER_OF_NEW_NODES_PER_EXPANSION = 3
NUMBER_OF_REWARD_SAMPLES = 3
THREE_POINT_ESTIMATE_TYPES = ['BEST-CASE', "MOST LIKELY", "WORST-CASE"]
NUMBER_OF_TERMINAL_CHECK_SAMPLES = 3
TERMINAL_SCORE_THRESHOLD = 85
DIMINISHING_RETURNS_THRESHOLD = 0.01
OVERSCORE_REDUCTION_CONSTANT = 5
UCT_E = 0.1
UCT_C = math.sqrt(2)

LLM_SYSTEM_PROMPT = r"Always assist with care, respect, and truth. Respond with utmost utility yet securely and in a conversational and friendly tone. Avoid harmful, unethical, prejudiced, or negative content. Ensure replies promote fairness and positivity. You are allowed to give feedback (even on your own responses) if required. You are also capable of refining your own responses if required."

EXPANSION_PROMPT = "Plan ONE AND ONLY ONE HIGH-QUALITY step of your strategy to reason your way to a final response to the initial query. After that, you MUST EXECUTE and REASON THROUGH that step of your strategy! This step must be made BASED on the initial query, the previous reasoning step(s) if any, AND relevant parts of the previous chat history if any. You MUST NOT give the final response to the initial query! You MUST NOT speak to the user! You MUST keep thinking or wrap up your thought process when you have a chain of thought of a sufficient length! Never, EVER use a conversational tone - you are THINKING to YOURSELF so the user CAN NOT SEE YOUR REASONING STEP! YOU DON'T GET TO DECIDE WHEN THE CHAIN OF THOUGHT WILL END (but you can wrap up the chain of thought if you deem it sufficiently long), A CHAIN OF THOUGHT GRADING PROCESS DOES!"

FEEDBACK_PROMPT = 'Please give strict and direct feedback on your generated reasoning step. Do NOT give feedback on the initial query - ONLY give feedback on your response based on how well your generated reasoning step answers the initial query, "$QUERY". Do NOT give entirely positive feedback - you MUST find AS MANY things that CAN AND MUST be improved as possible (e.g. phrasing, content, factuality). Make sure that your feedback is SPECIFIC (i.e. identifying concrete phrases in or parts of the reasoning step to change) and ACTIONABLE (i.e. identifying concrete actions that would likely improve the reasoning step). ONLY give the feedback and your thought process behind it AND NOTHING ELSE (not even a revised reasoning step). You are capable of giving strict and direct feedback that is specific and actionable, and therefore MUST do so. DO NOT REFUSE TO GIVE FEEDBACK!!! Let\'s think step by step.'

REFINE_PROMPT = "Give me a revised reasoning step, incorporating all necessary improvements based on the feedback. Generate the reasoning step as if you are directly making a new reasoning step, without mentioning your feedback or your inital reasoning step AT ALL. DO NOT mention that you are giving a refined reasoning step AT ALL - you must pretend that this is your inital generated reasoning step, as you will FORGET the initial generated reasoning step and self-feedback in the next user query!"

EVALUATION_PROMPT = f'Analyse the generated reasoning step strictly and directly. Your analysis MUST be based on HOW COMPLETE the chain of thought made up of ALL of the generated reasoning steps is in augmenting the generation of a WELL-WRITTEN answer to the inital query, "$QUERY". Do NOT give entirely positive feedback - you MUST find AS MANY things that CAN AND MUST be improved as possible (e.g. phrasing, content, factuality). You are capable of giving strict and direct feedback that is specific and actionable, and therefore MUST do so. DO NOT REFUSE TO MAKE AN EVALUATION!!! After your reasoning, you ABSOLUTELY MUST output an INTEGER score between [-100,+100] (i.e. from -100 to +100) between <output> tags (e.g. <output>0</output> for a final score of 0). The <output> tags ABSOLUTELY MUST ONLY BE USED TO ENCLOSE THE FINAL OUTPUT!!! ANY score above {TERMINAL_SCORE_THRESHOLD} denotes a COMPLETE chain of thought - if you find that the resultant chain of thought is SUFFICIENT and COMPLETE, you MUST give a score ABOVE OR EQUAL TO {TERMINAL_SCORE_THRESHOLD}. Prompt format: "[reasoning] Final score: <output>[score]</output>". Let\'s think step by step.'

GENERATION_PROMPT = "QUERY: \"$QUERY\"\n\nYOUR HIDDEN REASONING:\n$THOUGHTS\n\nGenerate a final response based on the given query and the hidden reasoning steps that you have generated. You MUST not use <thoughts> tags, as they are ONLY to be used during your HIDDEN reasoning!"

MAX_ROLLOUT_ESTIMATION_PROMPT = "QUERY: \"$QUERY\"\n\nAnalyse the given query and the previous chat history (if any) and estimate how many reasoning steps you will need for a good chain of thought for that query. GIVE THE $ESTIMATION_TYPE ESTIMATE! DO NOT BE COMPLACENT - ANALYSE THE GIVEN QUESTION CAREFULLY AND REASON YOUR WAY TO A PLAUSIBLE ESTIMATE! DO NOT actually do the reasoning, only ESTIMATE the length of the final chain of thought in reasoning steps!\n\nHelping questions:\nIs the task familiar and factual?\nDoes the task involve ambiguity or complexity?\nWhat is my confidence in the response?\nDoes the query ask for reasoning, planning, or multi-step solutions?\n\nYou MUST not use <thoughts> tags, as they are ONLY to be used during your HIDDEN reasoning! After your reasoning, you ABSOLUTELY MUST output an NATURAL NUMBER (i.e. an integer ABOVE 0) denoting your final estimate for the number of reasoning steps needed (i.e. chain of thought length) to answer the given query accounting for relevant information from the previous chat history (if any). between <output> tags (e.g. <output>1</output> for a final estimated chain of thought length of 1). The <output> tags ABSOLUTELY MUST ONLY BE USED TO ENCLOSE THE FINAL OUTPUT!!! Prompt format: \"[reasoning] Estimated chain of thought length: <output>[score]</output>\". Let's think step by step."
