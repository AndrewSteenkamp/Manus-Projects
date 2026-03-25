#!/usr/bin/env python3
"""
Complete System Test - AI-Powered UGC Advertising Agency
Comprehensive testing of all agents and system components
"""

import os
import sys
import json
import time
import logging
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(__file__))

# Import all agents and services
from agents.ceo_agent import CEOAgent
from agents.cfo_agent import CFOAgent
from agents.sales_agent import SalesAgent
from agents.creative_agent import CreativeAgent
from services.ai_helper import AIHelper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SystemTester:
    """Comprehensive system testing for the AI-Powered UGC Agency."""
    
    def __init__(self):
        """Initialize the system tester."""
        self.test_results = {
            "timestamp": datetime.now().isoformat(),
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "agent_tests": {},
            "integration_tests": {},
            "performance_metrics": {}
        }
        
        logger.info("🧪 Initializing Complete System Test Suite")
    
    def run_all_tests(self):
        """Run all system tests."""
        logger.info("🚀 Starting Complete System Test Suite")
        
        # Test AI Helper
        self.test_ai_helper()
        
        # Test individual agents
        self.test_ceo_agent()
        self.test_cfo_agent()
        self.test_sales_agent()
        self.test_creative_agent()
        
        # Test agent integration
        self.test_agent_integration()
        
        # Test complete workflow
        self.test_complete_workflow()
        
        # Generate final report
        self.generate_test_report()
        
        return self.test_results
    
    def test_ai_helper(self):
        """Test AI Helper functionality."""
        logger.info("🤖 Testing AI Helper...")
        
        try:
            # Test initialization
            ai_helper = AIHelper()
            self.record_test("ai_helper_init", True)
            
            # Test connection
            connection_test = ai_helper.test_connection()
            self.record_test("ai_helper_connection", connection_test)
            
            # Test response generation
            response = ai_helper.generate_response("Hello, are you working?")
            response_test = len(response) > 0
            self.record_test("ai_helper_response", response_test)
            
            # Test cost info
            cost_info = ai_helper.get_cost_info()
            cost_test = isinstance(cost_info, str) and len(cost_info) > 0
            self.record_test("ai_helper_cost", cost_test)
            
            logger.info(f"✅ AI Helper tests completed: {ai_helper.provider}")
            
        except Exception as e:
            logger.error(f"❌ AI Helper test failed: {str(e)}")
            self.record_test("ai_helper_error", False, str(e))
    
    def test_ceo_agent(self):
        """Test CEO Agent functionality."""
        logger.info("🎯 Testing CEO Agent...")
        
        try:
            # Initialize CEO
            ceo = CEOAgent()
            self.record_test("ceo_init", True)
            
            # Test strategic decision making
            decision_context = {
                "decision_type": "market_expansion",
                "opportunity": "Enter European market",
                "investment_required": 50000,
                "expected_roi": "200% in 12 months"
            }
            
            decision = ceo.make_strategic_decision(decision_context)
            decision_test = "decision" in decision and "reasoning" in decision
            self.record_test("ceo_strategic_decision", decision_test)
            
            # Test budget approval
            budget_request = {
                "amount": 15000,
                "purpose": "Marketing campaign expansion",
                "department": "Marketing",
                "expected_roi": "300%"
            }
            
            approval = ceo.approve_budget(budget_request)
            approval_test = "approved" in approval and "reasoning" in approval
            self.record_test("ceo_budget_approval", approval_test)
            
            # Test performance dashboard
            dashboard = ceo.get_performance_dashboard()
            dashboard_test = "kpis" in dashboard and "timestamp" in dashboard
            self.record_test("ceo_dashboard", dashboard_test)
            
            # Test quarterly objectives
            objectives = ceo.set_quarterly_objectives()
            objectives_test = "objectives" in objectives
            self.record_test("ceo_objectives", objectives_test)
            
            logger.info(f"✅ CEO Agent tests completed: {ceo.name}")
            
        except Exception as e:
            logger.error(f"❌ CEO Agent test failed: {str(e)}")
            self.record_test("ceo_error", False, str(e))
    
    def test_cfo_agent(self):
        """Test CFO Agent functionality."""
        logger.info("💰 Testing CFO Agent...")
        
        try:
            # Initialize CFO
            cfo = CFOAgent()
            self.record_test("cfo_init", True)
            
            # Update financial data
            financial_data = {
                "monthly_revenue": 150000,
                "monthly_expenses": 25000,
                "client_acquisition_cost": 500,
                "customer_lifetime_value": 15000
            }
            
            cfo.update_financial_data(financial_data)
            self.record_test("cfo_data_update", True)
            
            # Test financial analysis
            analysis = cfo.analyze_financial_performance()
            analysis_test = "performance_assessment" in analysis
            self.record_test("cfo_financial_analysis", analysis_test)
            
            # Test expense approval
            expense_request = {
                "amount": 5000,
                "category": "marketing",
                "purpose": "Social media advertising campaign",
                "expected_roi": "300%"
            }
            
            approval = cfo.approve_expense(expense_request)
            approval_test = "approved" in approval
            self.record_test("cfo_expense_approval", approval_test)
            
            # Test financial report
            report = cfo.generate_financial_report()
            report_test = "executive_summary" in report and "revenue_analysis" in report
            self.record_test("cfo_financial_report", report_test)
            
            # Test revenue forecast
            forecast = cfo.forecast_revenue(6)
            forecast_test = "monthly_projections" in forecast
            self.record_test("cfo_revenue_forecast", forecast_test)
            
            logger.info(f"✅ CFO Agent tests completed: {cfo.name}")
            
        except Exception as e:
            logger.error(f"❌ CFO Agent test failed: {str(e)}")
            self.record_test("cfo_error", False, str(e))
    
    def test_sales_agent(self):
        """Test Sales Agent functionality."""
        logger.info("📈 Testing Sales Agent...")
        
        try:
            # Initialize Sales Agent
            sales = SalesAgent()
            self.record_test("sales_init", True)
            
            # Test lead generation
            target_criteria = {
                "industry": "E-commerce",
                "company_size": "50-200 employees",
                "revenue": "$1M-$10M"
            }
            
            leads = sales.generate_leads(target_criteria)
            leads_test = isinstance(leads, list) and len(leads) > 0
            self.record_test("sales_lead_generation", leads_test)
            
            # Test lead qualification
            if leads:
                qualification = sales.qualify_lead(leads[0])
                qualification_test = "qualification_score" in qualification
                self.record_test("sales_lead_qualification", qualification_test)
                
                # Test proposal generation
                proposal = sales.generate_proposal(leads[0])
                proposal_test = "recommended_package" in proposal
                self.record_test("sales_proposal_generation", proposal_test)
            
            # Test outreach campaign
            campaign_config = {
                "name": "Test Campaign",
                "target_audience": "E-commerce businesses",
                "message_type": "email_sequence"
            }
            
            campaign = sales.create_outreach_campaign(campaign_config)
            campaign_test = "id" in campaign and "status" in campaign
            self.record_test("sales_outreach_campaign", campaign_test)
            
            # Test sales dashboard
            dashboard = sales.get_sales_dashboard()
            dashboard_test = "sales_metrics" in dashboard and "total_leads" in dashboard
            self.record_test("sales_dashboard", dashboard_test)
            
            # Test pipeline management
            pipeline = sales.manage_sales_pipeline()
            pipeline_test = "pipeline_analysis" in pipeline
            self.record_test("sales_pipeline_management", pipeline_test)
            
            logger.info(f"✅ Sales Agent tests completed: {sales.name}")
            
        except Exception as e:
            logger.error(f"❌ Sales Agent test failed: {str(e)}")
            self.record_test("sales_error", False, str(e))
    
    def test_creative_agent(self):
        """Test Creative Agent functionality."""
        logger.info("🎨 Testing Creative Agent...")
        
        try:
            # Initialize Creative Agent
            creative = CreativeAgent()
            self.record_test("creative_init", True)
            
            # Test UGC video package creation
            project_brief = {
                "client_name": "Test Client",
                "product_name": "Test Product",
                "product_category": "Health & Supplements",
                "video_count": 3,
                "target_audience": "Health-conscious adults 25-45",
                "key_benefits": ["Improved energy", "Better focus", "Natural ingredients"],
                "brand_voice": "Trustworthy, scientific, approachable"
            }
            
            video_package = creative.create_ugc_video_package(project_brief)
            package_test = "id" in video_package and "package" in video_package
            self.record_test("creative_video_package", package_test)
            
            # Test script generation
            script_requirements = {
                "product_name": "Test Product",
                "video_style": "testimonial",
                "duration": "30 seconds",
                "platform": "instagram_reels",
                "key_message": "Improved energy and focus"
            }
            
            script = creative.generate_video_script(script_requirements)
            script_test = "script" in script and "id" in script
            self.record_test("creative_script_generation", script_test)
            
            # Test creative strategy
            campaign_brief = {
                "brand_name": "Test Brand",
                "goal": "increase_conversions",
                "target_audience": "Health-conscious consumers",
                "budget": 50000
            }
            
            strategy = creative.develop_creative_strategy(campaign_brief)
            strategy_test = "strategy" in strategy and "id" in strategy
            self.record_test("creative_strategy_development", strategy_test)
            
            # Test creative dashboard
            dashboard = creative.get_creative_dashboard()
            dashboard_test = "creative_metrics" in dashboard and "active_projects" in dashboard
            self.record_test("creative_dashboard", dashboard_test)
            
            # Test quality management
            content_review = {
                "content_id": "TEST-001",
                "content_type": "video_script",
                "content": {"script": "Test script content"},
                "brand_guidelines": {"voice": "Professional", "tone": "Friendly"}
            }
            
            quality_review = creative.manage_creative_quality(content_review)
            quality_test = "quality_score" in quality_review and "approval_status" in quality_review
            self.record_test("creative_quality_management", quality_test)
            
            logger.info(f"✅ Creative Agent tests completed: {creative.name}")
            
        except Exception as e:
            logger.error(f"❌ Creative Agent test failed: {str(e)}")
            self.record_test("creative_error", False, str(e))
    
    def test_agent_integration(self):
        """Test integration between agents."""
        logger.info("🔗 Testing Agent Integration...")
        
        try:
            # Initialize all agents
            ceo = CEOAgent()
            cfo = CFOAgent()
            sales = SalesAgent()
            creative = CreativeAgent()
            
            # Test cross-agent workflow
            # 1. Sales generates leads
            target_criteria = {"industry": "E-commerce", "revenue": "$1M+"}
            leads = sales.generate_leads(target_criteria)
            
            # 2. CFO approves marketing budget
            budget_request = {
                "amount": 10000,
                "purpose": "Lead generation campaign",
                "department": "marketing"
            }
            budget_approval = cfo.approve_expense(budget_request)
            
            # 3. Creative creates content for qualified leads
            if leads:
                project_brief = {
                    "client_name": leads[0].get("company_name", "Test Client"),
                    "product_name": "Test Product",
                    "video_count": 2
                }
                video_package = creative.create_ugc_video_package(project_brief)
            
            # 4. CEO makes strategic decision
            decision_context = {
                "decision_type": "campaign_approval",
                "budget_approved": budget_approval.get("approved", False),
                "leads_generated": len(leads),
                "content_created": True
            }
            strategic_decision = ceo.make_strategic_decision(decision_context)
            
            integration_test = (
                len(leads) > 0 and
                "approved" in budget_approval and
                "package" in video_package and
                "decision" in strategic_decision
            )
            
            self.record_test("agent_integration_workflow", integration_test)
            
            logger.info("✅ Agent Integration tests completed")
            
        except Exception as e:
            logger.error(f"❌ Agent Integration test failed: {str(e)}")
            self.record_test("integration_error", False, str(e))
    
    def test_complete_workflow(self):
        """Test complete end-to-end workflow."""
        logger.info("🔄 Testing Complete Workflow...")
        
        try:
            # Simulate complete client acquisition and fulfillment workflow
            start_time = time.time()
            
            # Step 1: Initialize agency
            ceo = CEOAgent()
            cfo = CFOAgent()
            sales = SalesAgent()
            creative = CreativeAgent()
            
            # Step 2: Generate and qualify leads
            leads = sales.generate_leads({"industry": "E-commerce"})
            qualified_leads = []
            
            for lead in leads[:3]:  # Test first 3 leads
                qualification = sales.qualify_lead(lead)
                if qualification.get("qualification_score", 0) >= 70:
                    qualified_leads.append(lead)
            
            # Step 3: Create proposals for qualified leads
            proposals = []
            for lead in qualified_leads:
                proposal = sales.generate_proposal(lead)
                proposals.append(proposal)
            
            # Step 4: Get budget approval for operations
            total_operational_cost = len(qualified_leads) * 1000  # $1K per client
            budget_request = {
                "amount": total_operational_cost,
                "purpose": "Client fulfillment operations",
                "department": "operations"
            }
            
            budget_approval = cfo.approve_expense(budget_request)
            
            # Step 5: Create video packages for approved clients
            video_packages = []
            if budget_approval.get("approved"):
                for lead in qualified_leads:
                    project_brief = {
                        "client_name": lead.get("company_name", "Test Client"),
                        "product_name": lead.get("product_name", "Test Product"),
                        "video_count": 3
                    }
                    
                    video_package = creative.create_ugc_video_package(project_brief)
                    video_packages.append(video_package)
            
            # Step 6: CEO strategic review
            workflow_context = {
                "decision_type": "workflow_completion",
                "leads_generated": len(leads),
                "qualified_leads": len(qualified_leads),
                "proposals_created": len(proposals),
                "budget_approved": budget_approval.get("approved", False),
                "video_packages_created": len(video_packages)
            }
            
            strategic_review = ceo.make_strategic_decision(workflow_context)
            
            end_time = time.time()
            workflow_duration = end_time - start_time
            
            # Evaluate workflow success
            workflow_success = (
                len(leads) > 0 and
                len(qualified_leads) > 0 and
                len(proposals) > 0 and
                budget_approval.get("approved", False) and
                len(video_packages) > 0 and
                strategic_review.get("decision") in ["APPROVE", "MODIFY"]
            )
            
            self.record_test("complete_workflow", workflow_success)
            
            # Record performance metrics
            self.test_results["performance_metrics"] = {
                "workflow_duration_seconds": workflow_duration,
                "leads_generated": len(leads),
                "qualified_leads": len(qualified_leads),
                "conversion_rate": len(qualified_leads) / max(1, len(leads)) * 100,
                "proposals_created": len(proposals),
                "video_packages_created": len(video_packages),
                "budget_approved": budget_approval.get("approved", False),
                "total_operational_cost": total_operational_cost
            }
            
            logger.info(f"✅ Complete Workflow test completed in {workflow_duration:.2f} seconds")
            
        except Exception as e:
            logger.error(f"❌ Complete Workflow test failed: {str(e)}")
            self.record_test("workflow_error", False, str(e))
    
    def record_test(self, test_name, passed, error_message=None):
        """Record test result."""
        self.test_results["tests_run"] += 1
        
        if passed:
            self.test_results["tests_passed"] += 1
            logger.info(f"✅ {test_name}: PASSED")
        else:
            self.test_results["tests_failed"] += 1
            logger.error(f"❌ {test_name}: FAILED")
            if error_message:
                logger.error(f"   Error: {error_message}")
        
        # Store detailed test result
        category = test_name.split("_")[0]
        if category not in self.test_results:
            self.test_results[category] = {}
        
        self.test_results[category][test_name] = {
            "passed": passed,
            "timestamp": datetime.now().isoformat(),
            "error": error_message if not passed else None
        }
    
    def generate_test_report(self):
        """Generate comprehensive test report."""
        logger.info("📊 Generating Test Report...")
        
        # Calculate success rate
        success_rate = (self.test_results["tests_passed"] / 
                       max(1, self.test_results["tests_run"])) * 100
        
        # Create summary
        summary = {
            "overall_status": "PASSED" if success_rate >= 80 else "FAILED",
            "success_rate": success_rate,
            "tests_run": self.test_results["tests_run"],
            "tests_passed": self.test_results["tests_passed"],
            "tests_failed": self.test_results["tests_failed"],
            "timestamp": self.test_results["timestamp"]
        }
        
        self.test_results["summary"] = summary
        
        # Save detailed report
        report_filename = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(report_filename, 'w') as f:
                json.dump(self.test_results, f, indent=2)
            
            logger.info(f"📄 Test report saved: {report_filename}")
            
        except Exception as e:
            logger.error(f"Failed to save test report: {str(e)}")
        
        # Print summary
        print("\n" + "="*60)
        print("🧪 AI-POWERED UGC AGENCY - SYSTEM TEST RESULTS")
        print("="*60)
        print(f"Overall Status: {summary['overall_status']}")
        print(f"Success Rate: {summary['success_rate']:.1f}%")
        print(f"Tests Run: {summary['tests_run']}")
        print(f"Tests Passed: {summary['tests_passed']}")
        print(f"Tests Failed: {summary['tests_failed']}")
        print(f"Test Duration: {datetime.now().isoformat()}")
        
        if "performance_metrics" in self.test_results:
            metrics = self.test_results["performance_metrics"]
            print(f"\n📊 PERFORMANCE METRICS:")
            print(f"Workflow Duration: {metrics.get('workflow_duration_seconds', 0):.2f}s")
            print(f"Leads Generated: {metrics.get('leads_generated', 0)}")
            print(f"Qualified Leads: {metrics.get('qualified_leads', 0)}")
            print(f"Conversion Rate: {metrics.get('conversion_rate', 0):.1f}%")
            print(f"Video Packages Created: {metrics.get('video_packages_created', 0)}")
        
        print("="*60)
        
        return self.test_results


def main():
    """Run the complete system test."""
    print("🚀 Starting AI-Powered UGC Agency System Test")
    print("This will test all agents and system components...")
    
    tester = SystemTester()
    results = tester.run_all_tests()
    
    # Return appropriate exit code
    success_rate = results["summary"]["success_rate"]
    exit_code = 0 if success_rate >= 80 else 1
    
    print(f"\n🎯 System test completed with {success_rate:.1f}% success rate")
    
    return exit_code


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
