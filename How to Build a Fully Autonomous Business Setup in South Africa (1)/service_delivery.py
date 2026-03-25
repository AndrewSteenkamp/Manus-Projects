"""
Service Delivery Automation
Autonomous execution of client projects
"""

import sys
sys.path.append('/home/ubuntu/autonomous_business')

from datetime import datetime
import json
from openai import OpenAI

class ServiceDelivery:
    """
    Automates service delivery for client projects
    Handles project execution, quality control, and client communication
    """
    
    def __init__(self):
        self.client = OpenAI()
        self.active_projects = {}
        self.completed_projects = []
        
    def execute_project(self, project):
        """
        Execute a client project autonomously
        """
        project_id = project["project_id"]
        self.active_projects[project_id] = project
        
        # Generate execution plan
        execution_plan = self.create_execution_plan(project)
        project["execution_plan"] = execution_plan
        
        # Start execution
        project["status"] = "in_progress"
        project["progress"] = 0
        
        return {
            "project_id": project_id,
            "execution_plan": execution_plan,
            "status": "Project execution started"
        }
    
    def create_execution_plan(self, project):
        """
        AI creates detailed execution plan
        """
        service_type = project["service_type"]
        
        prompt = f"""Create a detailed execution plan for this project:

Service Type: {service_type}
Client: {project['client_name']}

Break down into:
1. Specific tasks (step-by-step)
2. Required resources/tools
3. Time estimates
4. Quality checkpoints
5. Client communication points

Respond in JSON format with tasks array."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are a project execution expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4
            )
            
            plan = json.loads(response.choices[0].message.content)
            plan["created_at"] = datetime.now().isoformat()
            
            return plan
        except Exception as e:
            return {"error": str(e)}
    
    def execute_task(self, project_id, task_description):
        """
        Execute a specific task within a project
        """
        if project_id not in self.active_projects:
            return {"error": "Project not found"}
        
        project = self.active_projects[project_id]
        
        # AI determines how to execute the task
        execution_result = self.ai_execute_task(task_description, project)
        
        # Log task completion
        if "tasks_completed" not in project:
            project["tasks_completed"] = []
        
        project["tasks_completed"].append({
            "task": task_description,
            "result": execution_result,
            "completed_at": datetime.now().isoformat()
        })
        
        # Update progress
        total_tasks = len(project.get("execution_plan", {}).get("tasks", []))
        completed = len(project["tasks_completed"])
        project["progress"] = (completed / total_tasks * 100) if total_tasks > 0 else 0
        
        return execution_result
    
    def ai_execute_task(self, task, project):
        """
        AI determines how to execute a task and simulates execution
        """
        prompt = f"""Execute this task for a client project:

Task: {task}
Project Type: {project['service_type']}
Client: {project['client_name']}

Provide:
1. Execution approach
2. Key actions taken
3. Output/deliverable
4. Quality check result
5. Next steps

Respond in JSON format."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are an AI agent executing client project tasks."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6
            )
            
            result = json.loads(response.choices[0].message.content)
            result["status"] = "completed"
            result["timestamp"] = datetime.now().isoformat()
            
            return result
        except Exception as e:
            return {"error": str(e), "status": "failed"}
    
    def quality_check(self, project_id):
        """
        AI-powered quality assurance check
        """
        if project_id not in self.active_projects:
            return {"error": "Project not found"}
        
        project = self.active_projects[project_id]
        tasks_completed = project.get("tasks_completed", [])
        
        prompt = f"""Conduct quality assurance review:

Project Type: {project['service_type']}
Tasks Completed: {len(tasks_completed)}
Progress: {project.get('progress', 0)}%

Review:
1. Completeness
2. Quality of work
3. Client requirements met
4. Issues/concerns
5. Ready for delivery?

Respond in JSON format."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are a QA specialist reviewing project quality."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            qa_result = json.loads(response.choices[0].message.content)
            qa_result["timestamp"] = datetime.now().isoformat()
            
            project["qa_checks"] = project.get("qa_checks", [])
            project["qa_checks"].append(qa_result)
            
            return qa_result
        except Exception as e:
            return {"error": str(e)}
    
    def generate_client_update(self, project_id):
        """
        Generate automated client progress update
        """
        if project_id not in self.active_projects:
            return {"error": "Project not found"}
        
        project = self.active_projects[project_id]
        
        prompt = f"""Create a client progress update:

Client: {project['client_name']}
Project: {project['service_type']}
Progress: {project.get('progress', 0)}%
Tasks Completed: {len(project.get('tasks_completed', []))}

The update should:
1. Be professional and positive
2. Highlight completed work
3. Show progress clearly
4. Mention next steps
5. Invite feedback

Respond with the update message."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are a project manager updating clients."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            update = {
                "message": response.choices[0].message.content,
                "progress": project.get("progress", 0),
                "sent_at": datetime.now().isoformat()
            }
            
            project["client_updates"] = project.get("client_updates", [])
            project["client_updates"].append(update)
            
            return update
        except Exception as e:
            return {"error": str(e)}
    
    def complete_project(self, project_id):
        """
        Mark project as complete and generate final deliverables
        """
        if project_id not in self.active_projects:
            return {"error": "Project not found"}
        
        project = self.active_projects[project_id]
        
        # Final QA check
        final_qa = self.quality_check(project_id)
        
        # Generate final deliverable package
        deliverable = self.generate_final_deliverable(project)
        
        # Mark complete
        project["status"] = "completed"
        project["completed_at"] = datetime.now().isoformat()
        project["final_qa"] = final_qa
        project["deliverable"] = deliverable
        
        # Move to completed projects
        self.completed_projects.append(project)
        del self.active_projects[project_id]
        
        return {
            "project_id": project_id,
            "status": "completed",
            "deliverable": deliverable,
            "final_qa": final_qa
        }
    
    def generate_final_deliverable(self, project):
        """
        Generate final deliverable package for client
        """
        deliverable = {
            "project_id": project["project_id"],
            "client": project["client_name"],
            "service": project["service_type"],
            "completed_at": datetime.now().isoformat(),
            "summary": f"Project completed successfully with {len(project.get('tasks_completed', []))} tasks",
            "files": [],  # In production, would include actual files
            "documentation": "Complete project documentation",
            "support": "30-day support included"
        }
        
        return deliverable
    
    def handle_client_feedback(self, project_id, feedback):
        """
        Process client feedback and adjust if needed
        """
        if project_id not in self.active_projects:
            # Check completed projects
            project = next((p for p in self.completed_projects if p["project_id"] == project_id), None)
            if not project:
                return {"error": "Project not found"}
        else:
            project = self.active_projects[project_id]
        
        # AI analyzes feedback
        prompt = f"""Analyze client feedback:

Feedback: {feedback}
Project: {project['service_type']}

Determine:
1. Sentiment (positive/neutral/negative)
2. Action required (none/minor_adjustment/major_revision)
3. Specific changes needed
4. Response to client

Respond in JSON format."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are analyzing client feedback."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4
            )
            
            analysis = json.loads(response.choices[0].message.content)
            
            project["feedback"] = project.get("feedback", [])
            project["feedback"].append({
                "feedback": feedback,
                "analysis": analysis,
                "received_at": datetime.now().isoformat()
            })
            
            return analysis
        except Exception as e:
            return {"error": str(e)}
    
    def get_delivery_metrics(self):
        """
        Get service delivery performance metrics
        """
        total_projects = len(self.active_projects) + len(self.completed_projects)
        
        avg_progress = sum(p.get("progress", 0) for p in self.active_projects.values()) / len(self.active_projects) if self.active_projects else 0
        
        return {
            "active_projects": len(self.active_projects),
            "completed_projects": len(self.completed_projects),
            "total_projects": total_projects,
            "average_progress": f"{avg_progress:.1f}%",
            "completion_rate": f"{(len(self.completed_projects) / total_projects * 100):.1f}%" if total_projects > 0 else "0%"
        }


class ClientCommunication:
    """
    Automated client communication system
    """
    
    def __init__(self):
        self.client = OpenAI()
        self.communications = []
        
    def send_automated_message(self, client_info, message_type, context):
        """
        Send automated message to client
        
        message_type: welcome, update, invoice, completion, follow_up
        """
        prompt = f"""Create a {message_type} message for a client:

Client: {client_info.get('name', 'Client')}
Context: {json.dumps(context)}

The message should be:
1. Professional and friendly
2. Clear and concise
3. Include relevant details
4. Have appropriate call-to-action

Respond with just the message text."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are a professional client communications specialist."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            message = {
                "message_id": f"MSG-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
                "client": client_info,
                "type": message_type,
                "content": response.choices[0].message.content,
                "sent_at": datetime.now().isoformat()
            }
            
            self.communications.append(message)
            
            return message
        except Exception as e:
            return {"error": str(e)}
    
    def get_communication_history(self, client_id):
        """
        Get all communications for a client
        """
        return [c for c in self.communications if c["client"].get("client_id") == client_id]
