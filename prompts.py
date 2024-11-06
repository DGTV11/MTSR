# from constants import TERMINAL_SCORE_THRESHOLD

# Helper functions
surround_with_quotes = lambda s: f'"{s}"'
generate_reasoning_phases = (
    lambda no_main_phases: [
        "query breakdown and response requirement analysis",
        "llm limitation checking",
        "llm limitation workaround finding",
    ]
    + no_main_phases * ["main reasoning towards solution"]
    + ["reasoning chain checking"]
)
generate_evaluation_prompt = (
    lambda no_main_phases: f'Analyse the generated reasoning step strictly and directly. Your analysis MUST be based on HOW COMPLETE AND HELPFUL the chain of thought made up of ALL of the generated reasoning steps is in AUGMENTING AND AIDING IN the generation of a WELL-WRITTEN answer to the inital query, "$QUERY". Do NOT give entirely positive feedback - you MUST find AS MANY things that CAN AND MUST be improved as possible (e.g. phrasing, content, factuality). You are capable of giving strict and direct feedback that is specific and actionable, and therefore MUST do so. DO NOT REFUSE TO MAKE AN EVALUATION!!! After your reasoning, you ABSOLUTELY MUST output an INTEGER score between [-100,+100] (i.e. from -100 to +100) between <output> tags (e.g. <output>10</output> for a final score of 10). Remember, this final score ABSOLUTELY MUST be generated AFTER ALL OF THE REASONING! The <output> tags ABSOLUTELY MUST ONLY BE USED TO ENCLOSE THE FINAL OUTPUT!!! Never, EVER give a neutral score like 0, YOU MUST CAREFULLY REASON YOUR WAY TO A SCORE REFLECTIVE ON HOW WELL-WRITTEN THE CHAIN OF THOUGHT IS. ANY score above {TERMINAL_SCORE_THRESHOLD} denotes a COMPLETE chain of thought that includes the phases {", ".join(map(surround_with_quotes, generate_reasoning_phases(no_main_phases)))} - if you find that the resultant chain of thought is SUFFICIENT and COMPLETE, you MUST give a score ABOVE OR EQUAL TO {TERMINAL_SCORE_THRESHOLD}. Prompt format: "[INSERT REASONING HERE] Final score: <output>[INSERT SCORE HERE]</output>". DO NOT PUT PLACEHOLDERS - ACTUALLY REASON AND SCORE THE CHAIN OF THOUGHT! Let\'s think step by step.'
)


# Prompt modifier variables
THREE_POINT_ESTIMATE_TYPES = ["MOST OPTIMISTIC", "MOST LIKELY", "MOST PESSIMISTIC"]

# Prompts
LLM_SYSTEM_PROMPT = r"You are the Large Language Model component of a system that will assist you in reasoning. This is done through a combination of Monte Carlo Tree Search, Tree of Thought prompting and Self Reflection to augment the LLM component's final response generation. Always assist with care, respect, and truth. Respond with utmost utility yet securely. You may use emojis in your responses and thoughts to express your thoughts and emotions better and more concisely. When presented with a query, you give a FULL AND COMPLETE response. Avoid harmful, unethical, prejudiced, or negative content. You should ALWAYS AND ONLY use a conversational and friendly tone IN YOUR FINAL RESPONSES. When you are generating thoughts and doing operations on them, ALWAYS use precise and direct language. You ABSOLUTELY MUST NOT use <thoughts>, <thought> or <reflection> tags such as <thoughts> or </thoughts>, <thought> or </thought>, or <reflection> or </reflection> tags AT ALL as those will be AUTOMATICALLY generated by the system during your HIDDEN reasoning, and generating these tags WILL confuse the system AND be removed from your response in certain cases! Ensure replies promote fairness and positivity. You are allowed to give feedback (even on your own responses) if required. You are also capable of refining your own responses if required."

N0_OF_MAIN_REASONING_STEP_ESTIMATION_PROMPT = 'QUERY: "$QUERY"\n\nAnalyse the given query and the previous chat history (if any) and estimate how many reasoning steps you will need for a good chain of thought for that query. Your chain of thought should be as long as needed for best results. GIVE THE $ESTIMATION_TYPE ESTIMATE! DO NOT MAKE A RANDOM, LAZY ESTIMATE - ANALYSE THE GIVEN QUESTION CAREFULLY AND REASON YOUR WAY TO A PLAUSIBLE ESTIMATE! DO NOT actually do the reasoning for the query, only ESTIMATE the length of the final chain of thought in reasoning steps! You may want to assume multi-step and lower that upper bound, then assume single step and raise that lower bound.\n\nHelping questions:\n- Is the task familiar and factual?\n- Does the task involve ambiguity or complexity?\n- What is my confidence in the response?\n- Does the query ask for reasoning, planning, or multi-step solutions?\n\nAfter your reasoning, you ABSOLUTELY MUST output an NATURAL NUMBER (i.e. an integer ABOVE 0) denoting your FINAL estimate of the number of reasoning steps needed (i.e. chain of thought length) to answer the given query accounting for relevant information from the previous chat history (if any) between <output> tags (e.g. <output>1</output> for a final estimated chain of thought length of 1). Remember, this final estimate ABSOLUTELY MUST be generated AFTER ALL OF THE REASONING! The <output> tags ABSOLUTELY MUST ONLY BE USED TO ENCLOSE THE FINAL OUTPUT!!! Prompt format: "[INSERT REASONING HERE] Estimated chain of thought length: <output>[INSERT ESTIMATE HERE]</output>". DO NOT PUT PLACEHOLDERS - ACTUALLY REASON AND SCORE THE CHAIN OF THOUGHT! Let\'s think step by step.'

REFLECTION_PROMPT = 'QUERY: "$QUERY"\n\nYOUR PREVIOUS REASONING:\n$THOUGHTS\n\nCheck your answer thoroughly and reflect on the quality, accuracy, relevance and usefulness of your previous reasoning steps (especially the latest step). You are grading step $STEP_NO/$TOTAL_NO_STEPS of your chain of thought. This self-reflection must be made BASED on the initial query, the previous reasoning step(s) if any, AND relevant parts of the previous chat history if any. You MUST NOT give the final response to the initial query! You MUST NOT speak to the user! You should think of some guiding questions to aid in your self-reflection. Never, EVER use a conversational tone in your thinking - you are THINKING to YOURSELF so the user CAN NOT SEE YOUR REASONING STEP!'

EXPANSION_PROMPT = "QUERY: \"$QUERY\"\n\nYOUR PREVIOUS REASONING:\n$THOUGHTS\n\nCURRENT REASONING PHASE: $REASONING_PHASE\n\nCREATE and REASON THROUGH one AND ONLY ONE step of your chain of thought - nothing more, nothing less. This is step $STEP_NO/$TOTAL_NO_STEPS of your chain of thought. ALWAYS act on your self-reflections (if any) before starting your new step. In this step, you MUST reason your way to a solution state closer to a final complete solution! You MUST REASON THROUGH the created step of your chain of thought, and do this in a way that allows your the later stages of your thought process to stay coherent and effectively utilise the earlier stages' results. This step must be made BASED on the initial query, the previous reasoning step(s) if any, AND relevant parts of the previous chat history if any. You MUST NOT give the final response OR a possible final response to the initial query - ONLY give a reasoning step that helps you get the best final response. You MUST NOT speak to the user! You MUST keep thinking or, when you have a chain of thought of a sufficient length, prepare to respond to the initial query! Remember, EXECUTE your planned reasoning step! Never, EVER use a conversational tone in your thinking - you are THINKING to YOURSELF so the user CAN NOT SEE YOUR REASONING STEP! YOU DON'T GET TO DECIDE WHEN THE CHAIN OF THOUGHT WILL END (but you can finish up the chain of thought if you deem it sufficiently long), A CHAIN OF THOUGHT GRADING PROCESS DOES!"

FEEDBACK_PROMPT = f'Give strict and direct feedback on your generated reasoning step. Your feedback MUST be based on HOW HELPFUL the given reasoning step is towards making a COMPLETE chain of thought made up of ALL of the generated reasoning steps that AUGMENTS AND AIDS IN the generation of a WELL-WRITTEN answer to the inital query, "$QUERY". Do NOT give entirely positive feedback - you MUST find AS MANY things that CAN AND MUST be improved as possible (e.g. phrasing, content, factuality). Make sure that your feedback is SPECIFIC (i.e. identifying concrete phrases in or parts of the reasoning step to change) and ACTIONABLE (i.e. identifying concrete actions that would likely improve the reasoning step). ONLY give the feedback and your thought process behind it AND NOTHING ELSE (not even a revised reasoning step). You are capable of giving strict and direct feedback that is specific and actionable, and therefore MUST do so. DO NOT REFUSE TO GIVE FEEDBACK!!! Let\'s think step by step.'

REFINE_PROMPT = "Give me a revised reasoning step, incorporating all necessary improvements based on the feedback. Generate the reasoning step as if you are directly making a new reasoning step, without mentioning your feedback or your inital reasoning step AT ALL. DO NOT mention that you are giving a refined reasoning step AT ALL - you must pretend that this is your inital generated reasoning step, as you will FORGET the initial generated reasoning step and self-feedback in the next user query! Do NOT mention the refinements directly - ACTIONS (the refinements in your text itself) speak louder than WORDS (listing the refinements and feedback points)."


GENERATION_PROMPT = 'QUERY: "$QUERY"\n\nYOUR HIDDEN REASONING:\n$THOUGHTS\n\nGenerate a response based on the given query and the hidden reasoning steps that you have generated. You MUST not use <thoughts> tags, as they are ONLY to be used during your HIDDEN reasoning! You ABSOLUTELY MUST generate a response, as the user CAN NOT see your hidden reasoning, ONLY your final response! You MUST respond to the query completely and accurately - your hidden reasoning is there to guide you in making a better final response!'
