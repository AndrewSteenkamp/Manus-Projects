"""
Design Module Manager
Manages the complete design team and coordinates all design operations for Socrates AI
"""

import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    COMPLETED = "completed"
    BLOCKED = "blocked"

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class DesignTask:
    id: str
    title: str
    description: str
    assignee: str
    status: TaskStatus
    priority: Priority
    due_date: datetime
    created_date: datetime
    dependencies: List[str]
    deliverables: List[str]
    feedback: List[Dict[str, Any]]
    estimated_hours: int
    actual_hours: int = 0

@dataclass
class TeamMember:
    name: str
    role: str
    specialties: List[str]
    current_workload: int
    max_capacity: int
    skills_rating: Dict[str, int]  # skill: rating (1-10)
    availability: Dict[str, bool]  # day: available

class DesignModuleManager:
    def __init__(self):
        self.team_members = self._initialize_team()
        self.active_tasks = []
        self.completed_tasks = []
        self.design_system = DesignSystemManager()
        self.collaboration_hub = CollaborationHub()
        
    def _initialize_team(self) -> Dict[str, TeamMember]:
        """Initialize the design team with world-class specialists"""
        return {
            "ui_designer": TeamMember(
                name="UI Design Specialist",
                role="ui_designer",
                specialties=["visual_design", "interface_design", "design_systems", "prototyping"],
                current_workload=0,
                max_capacity=40,  # hours per week
                skills_rating={
                    "figma": 10,
                    "sketch": 9,
                    "adobe_creative_suite": 10,
                    "design_systems": 10,
                    "prototyping": 9,
                    "visual_hierarchy": 10,
                    "color_theory": 10,
                    "typography": 10,
                    "responsive_design": 9,
                    "accessibility": 8
                },
                availability={"monday": True, "tuesday": True, "wednesday": True, 
                            "thursday": True, "friday": True, "saturday": False, "sunday": False}
            ),
            "ux_researcher": TeamMember(
                name="UX Research Specialist",
                role="ux_researcher", 
                specialties=["user_research", "usability_testing", "data_analysis", "behavioral_psychology"],
                current_workload=0,
                max_capacity=40,
                skills_rating={
                    "user_interviews": 10,
                    "usability_testing": 10,
                    "survey_design": 9,
                    "data_analysis": 9,
                    "persona_development": 10,
                    "journey_mapping": 9,
                    "a_b_testing": 8,
                    "analytics": 8,
                    "behavioral_psychology": 9,
                    "research_methodology": 10
                },
                availability={"monday": True, "tuesday": True, "wednesday": True,
                            "thursday": True, "friday": True, "saturday": False, "sunday": False}
            ),
            "brand_guardian": TeamMember(
                name="Brand Design Specialist",
                role="brand_guardian",
                specialties=["brand_identity", "visual_identity", "brand_strategy", "marketing_design"],
                current_workload=0,
                max_capacity=40,
                skills_rating={
                    "brand_strategy": 10,
                    "logo_design": 10,
                    "visual_identity": 10,
                    "brand_guidelines": 9,
                    "marketing_materials": 9,
                    "brand_consistency": 10,
                    "storytelling": 9,
                    "market_positioning": 8,
                    "competitive_analysis": 8,
                    "brand_evolution": 9
                },
                availability={"monday": True, "tuesday": True, "wednesday": True,
                            "thursday": True, "friday": True, "saturday": False, "sunday": False}
            ),
            "visual_storyteller": TeamMember(
                name="Visual Storytelling Specialist",
                role="visual_storyteller",
                specialties=["illustration", "infographics", "data_visualization", "motion_graphics"],
                current_workload=0,
                max_capacity=40,
                skills_rating={
                    "illustration": 10,
                    "infographic_design": 10,
                    "data_visualization": 9,
                    "motion_graphics": 8,
                    "storytelling": 10,
                    "after_effects": 8,
                    "chart_design": 9,
                    "icon_design": 9,
                    "presentation_design": 9,
                    "visual_communication": 10
                },
                availability={"monday": True, "tuesday": True, "wednesday": True,
                            "thursday": True, "friday": True, "saturday": False, "sunday": False}
            )
        }
    
    async def assign_task(self, task_data: Dict[str, Any]) -> DesignTask:
        """Intelligently assign tasks based on team member expertise and availability"""
        
        # Analyze task requirements
        required_skills = self._analyze_task_requirements(task_data)
        
        # Find best team member for the task
        best_assignee = self._find_best_assignee(required_skills, task_data.get('priority', Priority.MEDIUM))
        
        # Create task
        task = DesignTask(
            id=f"design_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            title=task_data['title'],
            description=task_data['description'],
            assignee=best_assignee,
            status=TaskStatus.PENDING,
            priority=Priority(task_data.get('priority', 2)),
            due_date=datetime.fromisoformat(task_data['due_date']),
            created_date=datetime.now(),
            dependencies=task_data.get('dependencies', []),
            deliverables=task_data.get('deliverables', []),
            feedback=[],
            estimated_hours=task_data.get('estimated_hours', 8)
        )
        
        # Update team member workload
        self.team_members[best_assignee].current_workload += task.estimated_hours
        
        # Add to active tasks
        self.active_tasks.append(task)
        
        # Notify team and other modules
        await self._notify_task_assignment(task)
        
        return task
    
    def _analyze_task_requirements(self, task_data: Dict[str, Any]) -> List[str]:
        """Analyze task to determine required skills"""
        title = task_data['title'].lower()
        description = task_data['description'].lower()
        
        skill_keywords = {
            'ui_design': ['interface', 'ui', 'button', 'form', 'layout', 'component'],
            'ux_research': ['research', 'user', 'testing', 'survey', 'interview', 'analysis'],
            'brand_design': ['brand', 'logo', 'identity', 'guidelines', 'marketing'],
            'visual_storytelling': ['illustration', 'infographic', 'chart', 'visualization', 'story']
        }
        
        required_skills = []
        text = f"{title} {description}"
        
        for skill, keywords in skill_keywords.items():
            if any(keyword in text for keyword in keywords):
                required_skills.append(skill)
        
        return required_skills or ['ui_design']  # Default to UI design
    
    def _find_best_assignee(self, required_skills: List[str], priority: Priority) -> str:
        """Find the best team member for the task based on skills and availability"""
        scores = {}
        
        for member_id, member in self.team_members.items():
            score = 0
            
            # Skill match score
            for skill in required_skills:
                if skill in member.specialties:
                    score += 10
                # Check individual skill ratings
                for member_skill, rating in member.skills_rating.items():
                    if skill in member_skill:
                        score += rating
            
            # Availability score (prefer less loaded members)
            availability_score = max(0, member.max_capacity - member.current_workload)
            score += availability_score
            
            # Priority adjustment
            if priority == Priority.CRITICAL:
                score *= 1.5
            elif priority == Priority.HIGH:
                score *= 1.2
            
            scores[member_id] = score
        
        # Return member with highest score
        return max(scores, key=scores.get)
    
    async def _notify_task_assignment(self, task: DesignTask):
        """Notify team member and other modules about task assignment"""
        notification = {
            'type': 'task_assignment',
            'module': 'design',
            'task_id': task.id,
            'assignee': task.assignee,
            'title': task.title,
            'priority': task.priority.name,
            'due_date': task.due_date.isoformat(),
            'timestamp': datetime.now().isoformat()
        }
        
        # Send to collaboration hub
        await self.collaboration_hub.broadcast_notification(notification)
    
    async def update_task_status(self, task_id: str, status: TaskStatus, notes: str = ""):
        """Update task status and notify stakeholders"""
        task = self._find_task(task_id)
        if not task:
            return False
        
        old_status = task.status
        task.status = status
        
        # Add status update to feedback
        task.feedback.append({
            'type': 'status_update',
            'old_status': old_status.value,
            'new_status': status.value,
            'notes': notes,
            'timestamp': datetime.now().isoformat()
        })
        
        # If completed, move to completed tasks
        if status == TaskStatus.COMPLETED:
            self.active_tasks.remove(task)
            self.completed_tasks.append(task)
            
            # Update team member workload
            assignee = self.team_members[task.assignee]
            assignee.current_workload = max(0, assignee.current_workload - task.estimated_hours)
        
        # Notify other modules
        await self._notify_status_update(task, old_status, status)
        
        return True
    
    def _find_task(self, task_id: str) -> Optional[DesignTask]:
        """Find task by ID in active tasks"""
        for task in self.active_tasks:
            if task.id == task_id:
                return task
        return None
    
    async def _notify_status_update(self, task: DesignTask, old_status: TaskStatus, new_status: TaskStatus):
        """Notify other modules about task status changes"""
        notification = {
            'type': 'task_status_update',
            'module': 'design',
            'task_id': task.id,
            'title': task.title,
            'old_status': old_status.value,
            'new_status': new_status.value,
            'assignee': task.assignee,
            'timestamp': datetime.now().isoformat()
        }
        
        await self.collaboration_hub.broadcast_notification(notification)
    
    def get_team_status(self) -> Dict[str, Any]:
        """Get comprehensive team status report"""
        return {
            'team_members': {
                member_id: {
                    'name': member.name,
                    'role': member.role,
                    'current_workload': member.current_workload,
                    'capacity_utilization': (member.current_workload / member.max_capacity) * 100,
                    'specialties': member.specialties,
                    'availability': member.availability
                }
                for member_id, member in self.team_members.items()
            },
            'active_tasks': len(self.active_tasks),
            'completed_tasks': len(self.completed_tasks),
            'tasks_by_status': {
                status.value: len([t for t in self.active_tasks if t.status == status])
                for status in TaskStatus
            },
            'tasks_by_priority': {
                priority.value: len([t for t in self.active_tasks if t.priority == priority])
                for priority in Priority
            }
        }
    
    async def daily_standup(self) -> Dict[str, Any]:
        """Generate daily standup report"""
        today = datetime.now().date()
        
        # Tasks due today
        due_today = [t for t in self.active_tasks if t.due_date.date() == today]
        
        # Overdue tasks
        overdue = [t for t in self.active_tasks if t.due_date.date() < today]
        
        # Blocked tasks
        blocked = [t for t in self.active_tasks if t.status == TaskStatus.BLOCKED]
        
        # Team workload
        team_workload = {
            member_id: {
                'current_tasks': len([t for t in self.active_tasks if t.assignee == member_id]),
                'workload_hours': member.current_workload,
                'capacity_percentage': (member.current_workload / member.max_capacity) * 100
            }
            for member_id, member in self.team_members.items()
        }
        
        standup_report = {
            'date': today.isoformat(),
            'due_today': [{'id': t.id, 'title': t.title, 'assignee': t.assignee} for t in due_today],
            'overdue_tasks': [{'id': t.id, 'title': t.title, 'assignee': t.assignee, 'days_overdue': (today - t.due_date.date()).days} for t in overdue],
            'blocked_tasks': [{'id': t.id, 'title': t.title, 'assignee': t.assignee} for t in blocked],
            'team_workload': team_workload,
            'total_active_tasks': len(self.active_tasks),
            'completion_rate': len(self.completed_tasks) / (len(self.completed_tasks) + len(self.active_tasks)) * 100 if (self.completed_tasks or self.active_tasks) else 0
        }
        
        # Send to collaboration hub
        await self.collaboration_hub.share_standup_report('design', standup_report)
        
        return standup_report

class DesignSystemManager:
    """Manages the design system and ensures consistency across all designs"""
    
    def __init__(self):
        self.components = {}
        self.tokens = {}
        self.guidelines = {}
        
    def update_component(self, component_name: str, component_data: Dict[str, Any]):
        """Update a design system component"""
        self.components[component_name] = {
            **component_data,
            'last_updated': datetime.now().isoformat(),
            'version': self.components.get(component_name, {}).get('version', 0) + 1
        }
    
    def get_component(self, component_name: str) -> Optional[Dict[str, Any]]:
        """Get a design system component"""
        return self.components.get(component_name)
    
    def validate_design_consistency(self, design_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate design against design system guidelines"""
        issues = []
        
        # Check color usage
        if 'colors' in design_data:
            for color in design_data['colors']:
                if color not in self.tokens.get('colors', {}):
                    issues.append(f"Color {color} not in design system")
        
        # Check typography
        if 'fonts' in design_data:
            for font in design_data['fonts']:
                if font not in self.tokens.get('typography', {}):
                    issues.append(f"Font {font} not in design system")
        
        return {
            'is_consistent': len(issues) == 0,
            'issues': issues,
            'recommendations': self._generate_recommendations(issues)
        }
    
    def _generate_recommendations(self, issues: List[str]) -> List[str]:
        """Generate recommendations based on consistency issues"""
        recommendations = []
        for issue in issues:
            if 'Color' in issue:
                recommendations.append("Use colors from the approved design system palette")
            elif 'Font' in issue:
                recommendations.append("Use typography from the design system type scale")
        return recommendations

class CollaborationHub:
    """Manages communication and collaboration with other modules"""
    
    def __init__(self):
        self.connected_modules = []
        self.message_queue = []
        
    async def broadcast_notification(self, notification: Dict[str, Any]):
        """Broadcast notification to all connected modules"""
        # In a real implementation, this would send to message queue or webhook
        self.message_queue.append({
            **notification,
            'broadcast_time': datetime.now().isoformat()
        })
        
        # Log for debugging
        print(f"[DESIGN MODULE] Broadcasting: {notification['type']} - {notification.get('title', 'N/A')}")
    
    async def share_standup_report(self, module_name: str, report: Dict[str, Any]):
        """Share daily standup report with other modules"""
        await self.broadcast_notification({
            'type': 'standup_report',
            'module': module_name,
            'report': report
        })
    
    async def request_collaboration(self, target_module: str, request_data: Dict[str, Any]):
        """Request collaboration from another module"""
        collaboration_request = {
            'type': 'collaboration_request',
            'from_module': 'design',
            'to_module': target_module,
            'request': request_data,
            'timestamp': datetime.now().isoformat()
        }
        
        await self.broadcast_notification(collaboration_request)
        
        return collaboration_request

# Example usage and testing
async def main():
    """Example usage of the Design Module Manager"""
    
    # Initialize the design module manager
    design_manager = DesignModuleManager()
    
    # Create some example tasks
    tasks = [
        {
            'title': 'Design Socrates AI Dashboard UI',
            'description': 'Create the main dashboard interface for the Socrates AI platform with charts, metrics, and navigation',
            'due_date': (datetime.now() + timedelta(days=5)).isoformat(),
            'priority': 3,
            'estimated_hours': 16,
            'deliverables': ['Figma designs', 'Component specifications', 'Responsive layouts']
        },
        {
            'title': 'Conduct User Research for Trading Interface',
            'description': 'Research user needs and behaviors for the trading analysis interface',
            'due_date': (datetime.now() + timedelta(days=3)).isoformat(),
            'priority': 4,
            'estimated_hours': 12,
            'deliverables': ['User interviews', 'Research report', 'Personas']
        },
        {
            'title': 'Create Brand Guidelines for Socrates AI',
            'description': 'Develop comprehensive brand guidelines including logo usage, colors, typography',
            'due_date': (datetime.now() + timedelta(days=7)).isoformat(),
            'priority': 2,
            'estimated_hours': 20,
            'deliverables': ['Brand guide document', 'Logo variations', 'Color palette']
        }
    ]
    
    # Assign tasks
    assigned_tasks = []
    for task_data in tasks:
        task = await design_manager.assign_task(task_data)
        assigned_tasks.append(task)
        print(f"Assigned task '{task.title}' to {task.assignee}")
    
    # Get team status
    team_status = design_manager.get_team_status()
    print(f"\nTeam Status:")
    print(f"Active tasks: {team_status['active_tasks']}")
    print(f"Team utilization:")
    for member_id, status in team_status['team_members'].items():
        print(f"  {status['name']}: {status['capacity_utilization']:.1f}% capacity")
    
    # Simulate task progress
    if assigned_tasks:
        first_task = assigned_tasks[0]
        await design_manager.update_task_status(first_task.id, TaskStatus.IN_PROGRESS, "Started working on dashboard designs")
        print(f"\nUpdated task '{first_task.title}' to IN_PROGRESS")
    
    # Generate daily standup
    standup = await design_manager.daily_standup()
    print(f"\nDaily Standup Report:")
    print(f"Due today: {len(standup['due_today'])} tasks")
    print(f"Overdue: {len(standup['overdue_tasks'])} tasks")
    print(f"Completion rate: {standup['completion_rate']:.1f}%")

if __name__ == "__main__":
    asyncio.run(main())

