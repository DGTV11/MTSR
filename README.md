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

## Notes
Thwrw was some AI assistance in the creation of this repository

## TODO
- Implement json mode (title, thought, next_action) like in g1
    - e.g. next_action: reason, final_response, stop

## Related works
- Ding, Ruomeng, et al. ‘Everything of Thoughts: Defying the Law of Penrose Triangle for Thought Generation’. arXiv [Cs.AI], 7 Nov. 2023, http://arxiv.org/abs/2311.04254. arXiv.

## References
- Madaan, Aman, et al. 'Self-Refine: Iterative Refinement with Self-Feedback'. arXiv [Cs.CL], 2023, http://arxiv.org/abs/2303.17651. arXiv.
- Zhang, Di, et al. 'Accessing GPT-4 Level Mathematical Olympiad Solutions via Monte Carlo Tree Self-Refine with LLaMa-3 8B'. arXiv [Cs.AI], 11 June 2024, http://arxiv.org/abs/2406.07394. arXiv.
- Saravia, Elvis. 'Prompt Engineering Guide'. https://github.com/dair-ai/Prompt-Engineering-Guide, 12 2022.
- Yao, Shunyu, et al. 'Tree of Thoughts: Deliberate Problem Solving with Large Language Models'. arXiv [Cs.CL], 17 May 2023, http://arxiv.org/abs/2305.10601. arXiv.