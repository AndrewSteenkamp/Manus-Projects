'''Legal agent for handling legal tasks.'''

from ..base_agent import BaseAgent

class LegalAgent(BaseAgent):
    def __init__(self, name, role):
        super().__init__(name, role)

    def execute_task(self, task):
        if task == "draft_contract":
            return "Drafting a standard contract..."
        elif task == "review_nda":
            return "Reviewing Non-Disclosure Agreement..."
        else:
            return f"Unknown task: {task}"

