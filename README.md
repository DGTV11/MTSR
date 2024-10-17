# MTSR
**M**CTSr + **T**oT + **S**elf-**R**eflection (yea i didn't know XoT existed when I started this) 

## Installation
1) Install Python 3.10+ and Ollama

2) Install Python dependencies
```sh
pip install -r requirements.txt
```

3) Install an Ollama model (recommended model: `gemma2:2b-instruct-q5_0`)

## Usage
1) Do initial configuration
```sh
python3 config.py
```

2) Run OllamaSelfRefine
```sh
python3 main.py
```

## TODO
- Implement json mode (title, thought, next_action) like in g1
    - e.g. next_action: reason, final_response, stop

## Related works
- Ding, Ruomeng, et al. ‘Everything of Thoughts: Defying the Law of Penrose Triangle for Thought Generation’. arXiv [Cs.AI], 7 Nov. 2023, http://arxiv.org/abs/2311.04254. arXiv.

## References
- Madaan, Aman, et al. 'Self-Refine: Iterative Refinement with Self-Feedback'. arXiv [Cs.CL], 2023, http://arxiv.org/abs/2303.17651. arXiv.
- Zhang, Di, et al. 'Accessing GPT-4 Level Mathematical Olympiad Solutions via Monte Carlo Tree Self-Refine with LLaMa-3 8B'. arXiv [Cs.AI], 11 June 2024, http://arxiv.org/abs/2406.07394. arXiv.
- Saravia, Elvis. 'Prompt Engineering Guide'. https://github.com/dair-ai/Prompt-Engineering-Guide, 12 2022.
- ChatGPT. "Combining Research and Prompting" OpenAI, 14 Sept. 2024, https://chatgpt.com/share/66e4f655-8774-8005-bb25-5c6b6846b657.
- ChatGPT. "Importance vs Greedy Sampling" OpenAI, 14 Sept. 2024, https://chatgpt.com/share/66e53529-7408-8005-9feb-0c04c823c4de.
- Yao, Shunyu, et al. 'Tree of Thoughts: Deliberate Problem Solving with Large Language Models'. arXiv [Cs.CL], 17 May 2023, http://arxiv.org/abs/2305.10601. arXiv.
- ChatGPT. "API Configuration and Models" OpenAI, 15 Sept. 2024, https://chatgpt.com/share/66e6c8c8-5e00-8005-b092-4a3fbf492765.
