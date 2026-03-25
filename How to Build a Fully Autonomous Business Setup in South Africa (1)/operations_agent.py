'''Operations agent for handling operational tasks.'''

from ..base_agent import BaseAgent

class OperationsAgent(BaseAgent):
    def __init__(self, name, role):
        super().__init__(name, role)

    def execute_task(self, task):
        if task == "plan_project":
            return "Planning a new project..."
        elif task == "allocate_resources":
            return "Allocating resources..."
        else:
            return f"Unknown task: {task}"

