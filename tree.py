import re, math
from collections import deque

import ollama

from constants import *

wrap_chat_message = lambda role, content: {"role": role, "content": content}

class ThoughtNode:
    def __init__(self, previous_chat_history=None, model_name=None, parent=None):
        self.previous_chat_history = previous_chat_history
        self.model_name = model_name

        self.parent = parent
        self.children = []

        self.reasoning_step = ""

        self.q_value = 0
        self.n_value = 0
        self.uct_value = 0

        self.is_search_finished = False

    @property
    def previous_agent_thoughts(self):
        previous_reasoning_steps = deque()

        node_parent = self.parent
        while node_parent:
            previous_reasoning_steps.appendleft(node_parent.reasoning_step)
            node_parent = node_parent.parent
            
        return f'<thoughts>\n{"\n\n".join(previous_reasoning_steps)}\n</thoughts>'

    @property
    def agent_thoughts(self):
        reasoning_steps = deque()

        node = self
        while node:
            reasoning_steps.appendleft(node.reasoning_step)
            node = node.parent
            
        return f'<thoughts>\n{"\n\n".join(reasoning_steps)}\n</thoughts>'

    @property
    def agent_thoughts_list(self):
        reasoning_steps = deque()

        node = self
        while node:
            reasoning_steps.appendleft(node.reasoning_step)
            node = node.parent
            
        return list(reasoning_steps)

    @property
    def q_values(self):
        values = deque()

        node = self
        while node:
            values.appendleft(node.q_value)
            node = node.parent
            
        return list(values)

    def expand_node(self):
        for i in range(NUMBER_OF_NEW_NODES_PER_EXPANSION):
            # Create new node
            new_node = ThoughtNode(self.previous_chat_history, self.model_name, self)
            # Generate next reasoning step
            tmp_chat_history = self.previous_chat_history+[wrap_chat_message('assistant', self.previous_agent_thoughts), wrap_chat_message('user', EXPANSION_PROMPT)]
            tmp_chat_history.append(ollama.chat(model=self.model_name, messages=tmp_chat_history, options={'num_ctx': CTX_WINDOW})['message']['content'])
            
            # Refine next reasoning step
            initial_query = self.previous_chat_history[-1]['content']

            ## Get feedback
            tmp_chat_history.append(wrap_chat_message("user", FEEDBACK_PROMPT.replace('$QUERY', initial_query)))
            assistant_message_content = ollama.chat(model=model_name, messages=tmp_chat_history, options={'num_ctx': CTX_WINDOW})["message"]["content"]
            tmp_chat_history.append(wrap_chat_message("assistant", assistant_message_content))

            ## Refine reasoning step
            tmp_chat_history.append(wrap_chat_message("user", REFINE_PROMPT.replace('$QUERY', initial_query)))
            assistant_message_content = ollama.chat(model=model_name, messages=tmp_chat_history, options={'num_ctx': CTX_WINDOW})["message"]["content"]
            new_node.reasoning_step = assistant_message_content

            # Evaluate reasoning step
            tmp_chat_history = self.previous_chat_history+[wrap_chat_message('assistant', self.previous_agent_thoughts), wrap_chat_message('user', EXPANSION_PROMPT), wrap_chat_message('assistant', new_node.reasoning_step), wrap_chat_message('user', EVALUATION_PROMPT.replace('$QUERY', initial_query))]
            r = []
            for i in range(NUMBER_OF_REWARD_SAMPLES):
                while True:
                    evaluation_raw_txt = ollama.chat(model=self.model_name, messages=tmp_chat_history, options={'num_ctx': CTX_WINDOW})['message']['content']
                   get list inside deque # regex to extract required strings
                    reg_str = "<output>(.*?)</output>"
                    res = re.findall(reg_str, evaluation_raw_txt)
                    if not res:
                        continue
                    try:
                        single_r = min(max(int(res[-1]), -100), 100)
                        single_r -= OVERSCORE_REDUCTION_CONSTANT*(single_r > 95)
                        r.append(single_r)
                    except:
                        continue

            new_node.q_value = 0.5*(min(r)+(sum(r)/NUMBER_OF_REWARD_SAMPLES))
            new_node.n_value = NUMBER_OF_REWARD_SAMPLES

            # Check if node is terminal
            ## Check for definite search completion
            new_node.is_search_finished = 1*(new_node.q_value >= TERMINAL_SCORE_THRESHOLD)
            if not new_node.is_search_finished: ## Check for diminishing returns
                if len(self.q_values) < 2:
                    new_node.is_search_finished = False  # Not enough data to determine diminishing returns
                
                # Calculate the improvements between consecutive Q-values
                improvements = [q_values[i] - q_values[i-1] for i in range(1, len(q_values))]
                
                # Check if improvements are below the threshold
                new_node.is_search_finished = 2*all(abs(improvement) < threshold for improvement in improvements)
            if not new_node.is_search_finished: ## Check for max search depth
                new_node.is_search_finished = 3*(len(new_node.agent_thoughts_list)>=MAX_SEARCH_DEPTH)
                
            # Append node to children
            self.children.append(new_node)

            # Check if expansion should stop early
            if new_node.q_value > self.q_value:
                break

    def backpropagate(self):
        parent_node = self

        while parent_node:
            parent_node.q_value = 0.5*(parent_node.q_value+max(map(lambda c: c.q_value, parent_node.children)))
            parent_node = parent_node.parent

    def uct_update_children(self):
        for child in self.children:
            child.uct_value = self.q_value + UCT_C * math.sqrt(math.log(self.n_value+1)/(child.n_value+UCT_E))

    def select(self):
        return max(self.children, key=lambda c: c.uct_value)

def search(previous_chat_history, model_name):
    current_node = ThoughtNode(previous_chat_history, model_name)

    while not current_node.is_search_finished:
        yield {'finished': False, 'thoughts': current_node.agent_thoughts, 'q_value': current_node.q_value}
        current_node.expand_node()
        current_node.backpropagate()
        current_node.uct_update_children()
        current_node = current_node.select()

    return {'finished': True, 'reason': current_node.is_search_finished, 'thoughts': current_node.agent_thoughts, 'q_value': current_node.q_value}
