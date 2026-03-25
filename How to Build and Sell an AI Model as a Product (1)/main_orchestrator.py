#!/usr/bin/env python3
"""
Main Orchestrator for Siener AI Autonomous System
Coordinates and manages all autonomous agents to run the business automatically
"""

import asyncio
import json
import logging
import schedule
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any
import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.agent_orchestrator import AgentOrchestrator, Task, TaskPriority
from agents.marketing_agent import MarketingAgent
from agents.engineering_agent import EngineeringAgent
from agents.product_agent import ProductAgent
from agents.operations_agent import OperationsAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/siener-ai/orchestrator.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class SienerAIOrchestrator:
    """Main orchestrator that manages all autonomous agents"""
    
    def __init__(self):
        self.orchestrator = AgentOrchestrator()
        self.agents = {}
        self.running = False
        self.scheduler_thread = None
        
        # Business configuration
        self.business_config = {
            'company_name': 'Siener AI',
            'director_email': os.getenv('DIRECTOR_EMAIL', 'director@siener-ai.com'),
            'business_hours': {'start': 8, 'end': 18},  # 8 AM to 6 PM
            'timezone': 'UTC',
            'auto_scaling': True,
            'alert_thresholds': {
                'system_health': 70,
                'response_time': 2000,
                'error_rate': 5.0
            }
        }
        
    async def initialize(self):
        """Initialize all autonomous agents"""
        logger.info("Initializing Siener AI Autonomous System...")
        
        try:
            # Initialize agents
            self.agents['marketing'] = MarketingAgent()
            self.agents['engineering'] = EngineeringAgent()
            self.agents['product'] = ProductAgent()
            self.agents['operations'] = OperationsAgent()
            
            # Register agents with orchestrator
            for agent_name, agent in self.agents.items():
                await self.orchestrator.register_agent(agent)
                logger.info(f"Registered {agent_name} agent")
                
            # Setup automated schedules
            self.setup_automated_schedules()
            
            logger.info("Siener AI Autonomous System initialized successfully")
            
        except Exception as e:
            logger.error(f"Initialization failed: {str(e)}")
            raise
            
    def setup_automated_schedules(self):
        """Setup automated task schedules"""
        logger.info("Setting up automated schedules...")
        
        # Daily operations
        schedule.every().day.at("08:00").do(self.schedule_daily_operations)
        schedule.every().day.at("18:00").do(self.schedule_end_of_day_operations)
        
        # Hourly monitoring
        schedule.every().hour.do(self.schedule_hourly_monitoring)
        
        # Marketing activities
        schedule.every().day.at("09:00").do(self.schedule_daily_marketing)
        schedule.every().monday.at("10:00").do(self.schedule_weekly_marketing)
        
        # Product analysis
        schedule.every().day.at("10:00").do(self.schedule_daily_product_analysis)
        schedule.every().week.do(self.schedule_weekly_product_review)
        
        # Engineering maintenance
        schedule.every().day.at("02:00").do(self.schedule_daily_maintenance)
        schedule.every().sunday.at("03:00").do(self.schedule_weekly_maintenance)
        
        # Business reporting
        schedule.every().day.at("07:00").do(self.schedule_daily_reporting)
        schedule.every().monday.at("08:00").do(self.schedule_weekly_reporting)
        
        logger.info("Automated schedules configured")
        
    async def start(self):
        """Start the autonomous system"""
        logger.info("Starting Siener AI Autonomous System...")
        
        self.running = True
        
        # Start the scheduler in a separate thread
        self.scheduler_thread = threading.Thread(target=self.run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        # Start initial tasks
        await self.run_startup_tasks()
        
        # Main orchestrator loop
        await self.run_main_loop()
        
    def run_scheduler(self):
        """Run the task scheduler"""
        logger.info("Task scheduler started")
        
        while self.running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
            
        logger.info("Task scheduler stopped")
        
    async def run_startup_tasks(self):
        """Run initial startup tasks"""
        logger.info("Running startup tasks...")
        
        try:
            # System health check
            health_task = Task(
                task_id="startup_health_check",
                agent_type="engineering",
                action="monitor_system_health",
                parameters={
                    'check_apis': True,
                    'check_database': True,
                    'check_performance': True,
                    'auto_fix': True
                },
                priority=TaskPriority.HIGH
            )
            await self.orchestrator.execute_task(health_task)
            
            # Initial market analysis
            market_task = Task(
                task_id="startup_market_analysis",
                agent_type="product",
                action="generate_market_analysis",
                parameters={
                    'markets': ['SPY', 'QQQ', 'IWM', 'GLD', 'BTC-USD'],
                    'analysis_depth': 'comprehensive',
                    'include_predictions': True
                },
                priority=TaskPriority.MEDIUM
            )
            await self.orchestrator.execute_task(market_task)
            
            # Marketing system initialization
            marketing_task = Task(
                task_id="startup_marketing_init",
                agent_type="marketing",
                action="initialize_campaigns",
                parameters={
                    'platforms': ['social_media', 'content_marketing', 'email'],
                    'target_audience': 'financial_professionals',
                    'budget_allocation': {'social_media': 40, 'content': 35, 'email': 25}
                },
                priority=TaskPriority.MEDIUM
            )
            await self.orchestrator.execute_task(marketing_task)
            
            logger.info("Startup tasks completed successfully")
            
        except Exception as e:
            logger.error(f"Startup tasks failed: {str(e)}")
            
    async def run_main_loop(self):
        """Main orchestrator loop"""
        logger.info("Main orchestrator loop started")
        
        while self.running:
            try:
                # Process pending tasks
                await self.orchestrator.process_pending_tasks()
                
                # Monitor agent health
                await self.monitor_agent_health()
                
                # Check for urgent issues
                await self.check_urgent_issues()
                
                # Sleep for a short interval
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"Main loop error: {str(e)}")
                await asyncio.sleep(60)  # Wait longer on error
                
        logger.info("Main orchestrator loop stopped")
        
    async def monitor_agent_health(self):
        """Monitor the health of all agents"""
        try:
            for agent_name, agent in self.agents.items():
                if hasattr(agent, 'get_health_status'):
                    health = await agent.get_health_status()
                    if not health.get('healthy', True):
                        logger.warning(f"Agent {agent_name} health issue: {health}")
                        await self.handle_agent_health_issue(agent_name, health)
                        
        except Exception as e:
            logger.error(f"Agent health monitoring failed: {str(e)}")
            
    async def handle_agent_health_issue(self, agent_name: str, health_info: Dict[str, Any]):
        """Handle agent health issues"""
        try:
            # Create incident response task
            incident_task = Task(
                task_id=f"agent_health_incident_{agent_name}_{int(time.time())}",
                agent_type="operations",
                action="handle_incident_response",
                parameters={
                    'incident_type': 'agent_health',
                    'affected_agent': agent_name,
                    'health_info': health_info,
                    'auto_resolve': True
                },
                priority=TaskPriority.HIGH
            )
            
            await self.orchestrator.execute_task(incident_task)
            
        except Exception as e:
            logger.error(f"Failed to handle agent health issue: {str(e)}")
            
    async def check_urgent_issues(self):
        """Check for urgent business issues that need immediate attention"""
        try:
            # Check system health
            health_task = Task(
                task_id=f"urgent_health_check_{int(time.time())}",
                agent_type="engineering",
                action="monitor_system_health",
                parameters={
                    'check_apis': True,
                    'check_database': True,
                    'check_performance': True,
                    'auto_fix': False  # Don't auto-fix during urgent checks
                },
                priority=TaskPriority.HIGH
            )
            
            health_result = await self.orchestrator.execute_task(health_task)
            
            # Check for critical issues
            if health_result and health_result.get('overall_health') == 'critical':
                await self.handle_critical_system_issue(health_result)
                
        except Exception as e:
            logger.error(f"Urgent issue check failed: {str(e)}")
            
    async def handle_critical_system_issue(self, health_info: Dict[str, Any]):
        """Handle critical system issues"""
        try:
            logger.critical("Critical system issue detected!")
            
            # Create high-priority incident response
            incident_task = Task(
                task_id=f"critical_incident_{int(time.time())}",
                agent_type="operations",
                action="handle_incident_response",
                parameters={
                    'incident_type': 'critical_system',
                    'health_info': health_info,
                    'notify_director': True,
                    'auto_resolve': True
                },
                priority=TaskPriority.CRITICAL
            )
            
            await self.orchestrator.execute_task(incident_task)
            
        except Exception as e:
            logger.error(f"Failed to handle critical system issue: {str(e)}")
            
    # Scheduled task methods
    def schedule_daily_operations(self):
        """Schedule daily operations tasks"""
        asyncio.create_task(self.run_daily_operations())
        
    def schedule_end_of_day_operations(self):
        """Schedule end of day operations"""
        asyncio.create_task(self.run_end_of_day_operations())
        
    def schedule_hourly_monitoring(self):
        """Schedule hourly monitoring tasks"""
        asyncio.create_task(self.run_hourly_monitoring())
        
    def schedule_daily_marketing(self):
        """Schedule daily marketing tasks"""
        asyncio.create_task(self.run_daily_marketing())
        
    def schedule_weekly_marketing(self):
        """Schedule weekly marketing tasks"""
        asyncio.create_task(self.run_weekly_marketing())
        
    def schedule_daily_product_analysis(self):
        """Schedule daily product analysis"""
        asyncio.create_task(self.run_daily_product_analysis())
        
    def schedule_weekly_product_review(self):
        """Schedule weekly product review"""
        asyncio.create_task(self.run_weekly_product_review())
        
    def schedule_daily_maintenance(self):
        """Schedule daily maintenance tasks"""
        asyncio.create_task(self.run_daily_maintenance())
        
    def schedule_weekly_maintenance(self):
        """Schedule weekly maintenance tasks"""
        asyncio.create_task(self.run_weekly_maintenance())
        
    def schedule_daily_reporting(self):
        """Schedule daily reporting"""
        asyncio.create_task(self.run_daily_reporting())
        
    def schedule_weekly_reporting(self):
        """Schedule weekly reporting"""
        asyncio.create_task(self.run_weekly_reporting())
        
    # Task execution methods
    async def run_daily_operations(self):
        """Run daily operations tasks"""
        logger.info("Running daily operations...")
        
        tasks = [
            # System health check
            Task(
                task_id=f"daily_health_check_{datetime.now().strftime('%Y%m%d')}",
                agent_type="engineering",
                action="monitor_system_health",
                parameters={
                    'check_apis': True,
                    'check_database': True,
                    'check_performance': True,
                    'auto_fix': True
                },
                priority=TaskPriority.HIGH
            ),
            
            # Business metrics monitoring
            Task(
                task_id=f"daily_metrics_{datetime.now().strftime('%Y%m%d')}",
                agent_type="operations",
                action="monitor_business_metrics",
                parameters={
                    'include_revenue': True,
                    'include_customers': True,
                    'include_performance': True
                },
                priority=TaskPriority.MEDIUM
            )
        ]
        
        for task in tasks:
            await self.orchestrator.execute_task(task)
            
    async def run_end_of_day_operations(self):
        """Run end of day operations"""
        logger.info("Running end of day operations...")
        
        # Generate daily report
        report_task = Task(
            task_id=f"daily_report_{datetime.now().strftime('%Y%m%d')}",
            agent_type="operations",
            action="generate_daily_report",
            parameters={
                'include_metrics': True,
                'include_revenue': True,
                'include_customer_data': True,
                'send_to_director': True
            },
            priority=TaskPriority.HIGH
        )
        
        await self.orchestrator.execute_task(report_task)
        
        # System backup
        backup_task = Task(
            task_id=f"daily_backup_{datetime.now().strftime('%Y%m%d')}",
            agent_type="engineering",
            action="backup_system",
            parameters={
                'backup_database': True,
                'backup_files': True,
                'backup_configs': True
            },
            priority=TaskPriority.MEDIUM
        )
        
        await self.orchestrator.execute_task(backup_task)
        
    async def run_hourly_monitoring(self):
        """Run hourly monitoring tasks"""
        # Quick health check
        health_task = Task(
            task_id=f"hourly_health_{datetime.now().strftime('%Y%m%d_%H')}",
            agent_type="operations",
            action="perform_health_check",
            parameters={
                'check_uptime': True,
                'check_response_times': True,
                'check_error_rates': True,
                'alert_if_issues': True
            },
            priority=TaskPriority.MEDIUM
        )
        
        await self.orchestrator.execute_task(health_task)
        
    async def run_daily_marketing(self):
        """Run daily marketing tasks"""
        logger.info("Running daily marketing tasks...")
        
        tasks = [
            # Create and publish content
            Task(
                task_id=f"daily_content_{datetime.now().strftime('%Y%m%d')}",
                agent_type="marketing",
                action="create_and_publish_content",
                parameters={
                    'content_types': ['social_media', 'blog_post'],
                    'platforms': ['twitter', 'linkedin', 'website'],
                    'topics': ['market_analysis', 'ai_insights', 'financial_trends']
                },
                priority=TaskPriority.MEDIUM
            ),
            
            # Analyze campaign performance
            Task(
                task_id=f"daily_campaign_analysis_{datetime.now().strftime('%Y%m%d')}",
                agent_type="marketing",
                action="analyze_campaign_performance",
                parameters={
                    'campaigns': 'all_active',
                    'optimize_budget': True,
                    'adjust_targeting': True
                },
                priority=TaskPriority.MEDIUM
            )
        ]
        
        for task in tasks:
            await self.orchestrator.execute_task(task)
            
    async def run_weekly_marketing(self):
        """Run weekly marketing tasks"""
        logger.info("Running weekly marketing tasks...")
        
        # Weekly marketing strategy review
        strategy_task = Task(
            task_id=f"weekly_marketing_strategy_{datetime.now().strftime('%Y%W')}",
            agent_type="marketing",
            action="review_marketing_strategy",
            parameters={
                'analyze_performance': True,
                'update_targeting': True,
                'plan_next_week': True,
                'budget_optimization': True
            },
            priority=TaskPriority.MEDIUM
        )
        
        await self.orchestrator.execute_task(strategy_task)
        
    async def run_daily_product_analysis(self):
        """Run daily product analysis"""
        logger.info("Running daily product analysis...")
        
        tasks = [
            # Market analysis
            Task(
                task_id=f"daily_market_analysis_{datetime.now().strftime('%Y%m%d')}",
                agent_type="product",
                action="generate_market_analysis",
                parameters={
                    'markets': ['SPY', 'QQQ', 'IWM', 'GLD', 'BTC-USD'],
                    'analysis_depth': 'standard',
                    'include_predictions': True
                },
                priority=TaskPriority.MEDIUM
            ),
            
            # User behavior analysis
            Task(
                task_id=f"daily_user_analysis_{datetime.now().strftime('%Y%m%d')}",
                agent_type="product",
                action="analyze_user_behavior",
                parameters={
                    'analyze_engagement': True,
                    'analyze_conversion': True,
                    'identify_improvements': True
                },
                priority=TaskPriority.MEDIUM
            )
        ]
        
        for task in tasks:
            await self.orchestrator.execute_task(task)
            
    async def run_weekly_product_review(self):
        """Run weekly product review"""
        logger.info("Running weekly product review...")
        
        # Comprehensive product insights
        insights_task = Task(
            task_id=f"weekly_product_insights_{datetime.now().strftime('%Y%W')}",
            agent_type="product",
            action="generate_product_insights",
            parameters={
                'analyze_user_feedback': True,
                'competitive_analysis': True,
                'feature_performance': True,
                'roadmap_updates': True
            },
            priority=TaskPriority.MEDIUM
        )
        
        await self.orchestrator.execute_task(insights_task)
        
    async def run_daily_maintenance(self):
        """Run daily maintenance tasks"""
        logger.info("Running daily maintenance...")
        
        # Performance optimization
        optimization_task = Task(
            task_id=f"daily_optimization_{datetime.now().strftime('%Y%m%d')}",
            agent_type="engineering",
            action="optimize_performance",
            parameters={
                'optimize_database': True,
                'optimize_api_responses': True,
                'clean_logs': True
            },
            priority=TaskPriority.LOW
        )
        
        await self.orchestrator.execute_task(optimization_task)
        
    async def run_weekly_maintenance(self):
        """Run weekly maintenance tasks"""
        logger.info("Running weekly maintenance...")
        
        tasks = [
            # Comprehensive system maintenance
            Task(
                task_id=f"weekly_maintenance_{datetime.now().strftime('%Y%W')}",
                agent_type="engineering",
                action="perform_system_maintenance",
                parameters={
                    'update_dependencies': True,
                    'security_scan': True,
                    'performance_audit': True,
                    'cleanup_old_data': True
                },
                priority=TaskPriority.MEDIUM
            ),
            
            # Security audit
            Task(
                task_id=f"weekly_security_audit_{datetime.now().strftime('%Y%W')}",
                agent_type="engineering",
                action="security_scan",
                parameters={
                    'scan_vulnerabilities': True,
                    'check_access_logs': True,
                    'update_security_policies': True
                },
                priority=TaskPriority.HIGH
            )
        ]
        
        for task in tasks:
            await self.orchestrator.execute_task(task)
            
    async def run_daily_reporting(self):
        """Run daily reporting"""
        logger.info("Running daily reporting...")
        
        # Already handled in end_of_day_operations
        pass
        
    async def run_weekly_reporting(self):
        """Run weekly reporting"""
        logger.info("Running weekly reporting...")
        
        # Weekly business intelligence report
        bi_task = Task(
            task_id=f"weekly_business_intelligence_{datetime.now().strftime('%Y%W')}",
            agent_type="operations",
            action="generate_business_intelligence",
            parameters={
                'time_period': 'weekly',
                'include_trends': True,
                'include_forecasts': True,
                'include_recommendations': True,
                'send_to_director': True
            },
            priority=TaskPriority.MEDIUM
        )
        
        await self.orchestrator.execute_task(bi_task)
        
    async def stop(self):
        """Stop the autonomous system"""
        logger.info("Stopping Siener AI Autonomous System...")
        
        self.running = False
        
        # Wait for scheduler thread to stop
        if self.scheduler_thread and self.scheduler_thread.is_alive():
            self.scheduler_thread.join(timeout=10)
            
        # Stop orchestrator
        await self.orchestrator.stop()
        
        logger.info("Siener AI Autonomous System stopped")
        
    async def get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        try:
            agent_statuses = {}
            for agent_name, agent in self.agents.items():
                agent_statuses[agent_name] = {
                    'status': agent.status.value,
                    'last_activity': agent.last_activity.isoformat() if agent.last_activity else None,
                    'tasks_completed': getattr(agent, 'tasks_completed', 0)
                }
                
            return {
                'system_running': self.running,
                'agents': agent_statuses,
                'orchestrator_status': await self.orchestrator.get_status(),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to get system status: {str(e)}")
            return {'error': str(e)}

async def main():
    """Main entry point"""
    orchestrator = SienerAIOrchestrator()
    
    try:
        # Initialize the system
        await orchestrator.initialize()
        
        # Start the autonomous system
        await orchestrator.start()
        
    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
    except Exception as e:
        logger.error(f"System error: {str(e)}")
    finally:
        # Stop the system
        await orchestrator.stop()

if __name__ == "__main__":
    # Create log directory
    os.makedirs('/var/log/siener-ai', exist_ok=True)
    
    # Run the main orchestrator
    asyncio.run(main())

