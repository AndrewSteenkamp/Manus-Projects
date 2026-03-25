'''Base class for all AI agents.'''

class BaseAgent:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def execute_task(self, task):
        raise NotImplementedError("This method should be overridden by subclasses.")

