'''Finance agent for handling financial tasks.'''

from ..base_agent import BaseAgent

class FinanceAgent(BaseAgent):
    def __init__(self, name, role):
        super().__init__(name, role)

    def execute_task(self, task):
        if task == "generate_financial_report":
            return "Generating financial report..."
        elif task == "process_invoices":
            return "Processing invoices..."
        else:
            return f"Unknown task: {task}"

