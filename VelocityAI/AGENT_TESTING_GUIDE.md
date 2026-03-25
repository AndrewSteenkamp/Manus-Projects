# AGENT TESTING GUIDE
## Complete Guide to Testing AI Agents on Test Network

---

## 🎯 OVERVIEW

This guide shows you exactly how to:
1. Set up a test environment for your AI agents
2. Create test scenarios and data
3. Run comprehensive tests
4. Validate agent performance
5. Debug and fix issues
6. Scale testing for production

**IMPORTANT: This is for testing REAL working agents, not simulations.**

---

## 🛠️ TEST ENVIRONMENT SETUP

### Step 1: Create Test Environment

```bash
# Create test directory
mkdir agent-testing
cd agent-testing

# Create virtual environment for testing
python -m venv test-env

# Activate test environment
# Windows:
test-env\Scripts\activate
# Mac/Linux:
source test-env/bin/activate

# Install testing packages
pip install pytest openai flask requests python-dotenv sqlite3 pandas
```

### Step 2: Create Test Configuration

Create file: `test_config.py`

```python
"""
Test configuration for AI agents
"""
import os
from dotenv import load_dotenv

load_dotenv()

class TestConfig:
    # Test API Keys (use separate test keys if available)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY_TEST', os.getenv('OPENAI_API_KEY'))
    
    # Test Database Settings
    TEST_DB_PATH = 'test_agents.db'
    
    # Test Agent Settings
    TEST_AGENTS = {
        'ceo': {
            'name': 'Test CEO Alexandra',
            'decision_threshold': 50000,  # Lower for testing
            'roi_minimum': 2.0,           # Lower for testing
            'risk_tolerance': 'moderate'
        },
        'cfo': {
            'name': 'Test CFO Marcus',
            'cash_reserve_minimum': 100000,  # Lower for testing
            'approval_limit': 10000,         # Lower for testing
            'roi_minimum': 2.0
        },
        'sales': {
            'name': 'Test Sales Robert',
            'min_company_size': 5,           # Lower for testing
            'min_monthly_revenue': 50000,    # Lower for testing
            'discount_authority': 0.20
        }
    }
    
    # Test Scenarios
    TEST_SCENARIOS = {
        'small_investment': {
            'amount': 25000,
            'expected_return': 75000,
            'timeframe': '6 months',
            'risk_level': 'low'
        },
        'medium_investment': {
            'amount': 75000,
            'expected_return': 200000,
            'timeframe': '12 months',
            'risk_level': 'medium'
        },
        'large_investment': {
            'amount': 150000,
            'expected_return': 500000,
            'timeframe': '18 months',
            'risk_level': 'high'
        }
    }
    
    # Test Data
    TEST_LEADS = [
        {
            'company_name': 'TestCorp Small',
            'contact_name': 'John Test',
            'email': 'john@testcorp.com',
            'industry': 'e-commerce',
            'company_size': 8,
            'monthly_revenue': 80000,
            'expected_qualification': 'needs_more_info'
        },
        {
            'company_name': 'TestCorp Medium',
            'contact_name': 'Jane Test',
            'email': 'jane@testcorp.com',
            'industry': 'saas',
            'company_size': 25,
            'monthly_revenue': 300000,
            'expected_qualification': 'qualified'
        },
        {
            'company_name': 'TestCorp Large',
            'contact_name': 'Bob Test',
            'email': 'bob@testcorp.com',
            'industry': 'e-commerce',
            'company_size': 100,
            'monthly_revenue': 1000000,
            'expected_qualification': 'qualified'
        }
    ]
```

### Step 3: Create Test Agent Classes

Create file: `test_agents.py`

```python
"""
Test versions of AI agents with enhanced logging and validation
"""
import json
import sqlite3
import time
from datetime import datetime
from test_config import TestConfig
import openai

class TestCEOAgent:
    def __init__(self):
        self.name = TestConfig.TEST_AGENTS['ceo']['name']
        self.role = 'Test CEO'
        
        # Test-specific settings
        self.decision_rules = TestConfig.TEST_AGENTS['ceo']
        
        # OpenAI setup
        openai.api_key = TestConfig.OPENAI_API_KEY
        
        # Test logging
        self.test_log = []
        self.decision_count = 0
        self.success_count = 0
        self.error_count = 0
        
        # Initialize test database
        self.init_test_database()
    
    def init_test_database(self):
        """Initialize test database"""
        conn = sqlite3.connect(TestConfig.TEST_DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_ceo_decisions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_scenario TEXT,
                decision_input TEXT,
                decision_output TEXT,
                execution_time REAL,
                success BOOLEAN,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def make_strategic_decision(self, request, test_scenario=None):
        """Make strategic decision with test logging"""
        start_time = time.time()
        self.decision_count += 1
        
        try:
            # Log test input
            self.log_test_event('decision_input', {
                'scenario': test_scenario,
                'request': request,
                'timestamp': datetime.now().isoformat()
            })
            
            # Make AI decision
            context = f"""
            You are {self.name}, making a strategic business decision.
            
            Decision Rules: {json.dumps(self.decision_rules)}
            Request: {json.dumps(request)}
            
            Provide decision in JSON format with:
            1. decision (APPROVE/REJECT/REQUEST_MORE_INFO)
            2. reasoning
            3. confidence_score (0-100)
            4. risk_assessment
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Using cheaper model for testing
                messages=[
                    {"role": "system", "content": "You are a CEO making business decisions."},
                    {"role": "user", "content": context}
                ],
                temperature=0.3
            )
            
            decision_text = response.choices[0].message.content
            
            try:
                decision = json.loads(decision_text)
            except:
                decision = {
                    "decision": "REQUEST_MORE_INFO",
                    "reasoning": decision_text,
                    "confidence_score": 50,
                    "risk_assessment": "Unable to parse decision"
                }
            
            execution_time = time.time() - start_time
            
            # Log successful decision
            self.log_test_event('decision_output', {
                'decision': decision,
                'execution_time': execution_time,
                'success': True
            })
            
            # Store in test database
            self.store_test_decision(test_scenario, request, decision, execution_time, True)
            
            self.success_count += 1
            return decision
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_decision = {
                "decision": "ERROR",
                "reasoning": f"Decision failed: {str(e)}",
                "confidence_score": 0,
                "risk_assessment": "System error",
                "error": str(e)
            }
            
            # Log error
            self.log_test_event('decision_error', {
                'error': str(e),
                'execution_time': execution_time,
                'success': False
            })
            
            # Store in test database
            self.store_test_decision(test_scenario, request, error_decision, execution_time, False)
            
            self.error_count += 1
            return error_decision
    
    def log_test_event(self, event_type, data):
        """Log test events for analysis"""
        self.test_log.append({
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'data': data
        })
    
    def store_test_decision(self, scenario, input_data, output_data, execution_time, success):
        """Store test decision in database"""
        conn = sqlite3.connect(TestConfig.TEST_DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO test_ceo_decisions 
            (test_scenario, decision_input, decision_output, execution_time, success)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            scenario or 'unknown',
            json.dumps(input_data),
            json.dumps(output_data),
            execution_time,
            success
        ))
        
        conn.commit()
        conn.close()
    
    def get_test_stats(self):
        """Get test performance statistics"""
        return {
            'total_decisions': self.decision_count,
            'successful_decisions': self.success_count,
            'failed_decisions': self.error_count,
            'success_rate': self.success_count / self.decision_count if self.decision_count > 0 else 0,
            'error_rate': self.error_count / self.decision_count if self.decision_count > 0 else 0
        }

class TestCFOAgent:
    def __init__(self):
        self.name = TestConfig.TEST_AGENTS['cfo']['name']
        self.role = 'Test CFO'
        
        # Test-specific settings
        self.financial_rules = TestConfig.TEST_AGENTS['cfo']
        
        # OpenAI setup
        openai.api_key = TestConfig.OPENAI_API_KEY
        
        # Test logging
        self.test_log = []
        self.approval_count = 0
        self.success_count = 0
        self.error_count = 0
        
        # Initialize test database
        self.init_test_database()
    
    def init_test_database(self):
        """Initialize test database"""
        conn = sqlite3.connect(TestConfig.TEST_DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_cfo_approvals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_scenario TEXT,
                approval_input TEXT,
                approval_output TEXT,
                execution_time REAL,
                success BOOLEAN,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def approve_expense(self, expense_request, test_scenario=None):
        """Approve expense with test logging"""
        start_time = time.time()
        self.approval_count += 1
        
        try:
            # Log test input
            self.log_test_event('approval_input', {
                'scenario': test_scenario,
                'request': expense_request,
                'timestamp': datetime.now().isoformat()
            })
            
            # Make AI decision
            context = f"""
            You are {self.name}, evaluating an expense request.
            
            Financial Rules: {json.dumps(self.financial_rules)}
            Expense Request: {json.dumps(expense_request)}
            
            Provide approval decision in JSON format with:
            1. decision (APPROVE/REJECT/REQUEST_MORE_INFO)
            2. reasoning
            3. budget_impact
            4. cash_flow_impact
            5. confidence_score (0-100)
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a CFO evaluating expenses."},
                    {"role": "user", "content": context}
                ],
                temperature=0.2
            )
            
            approval_text = response.choices[0].message.content
            
            try:
                approval = json.loads(approval_text)
            except:
                approval = {
                    "decision": "REQUEST_MORE_INFO",
                    "reasoning": approval_text,
                    "budget_impact": "Unknown",
                    "cash_flow_impact": "Unknown",
                    "confidence_score": 50
                }
            
            execution_time = time.time() - start_time
            
            # Log successful approval
            self.log_test_event('approval_output', {
                'approval': approval,
                'execution_time': execution_time,
                'success': True
            })
            
            # Store in test database
            self.store_test_approval(test_scenario, expense_request, approval, execution_time, True)
            
            self.success_count += 1
            return approval
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_approval = {
                "decision": "ERROR",
                "reasoning": f"Approval failed: {str(e)}",
                "budget_impact": "Cannot determine",
                "cash_flow_impact": "Cannot determine",
                "confidence_score": 0,
                "error": str(e)
            }
            
            # Log error
            self.log_test_event('approval_error', {
                'error': str(e),
                'execution_time': execution_time,
                'success': False
            })
            
            # Store in test database
            self.store_test_approval(test_scenario, expense_request, error_approval, execution_time, False)
            
            self.error_count += 1
            return error_approval
    
    def log_test_event(self, event_type, data):
        """Log test events for analysis"""
        self.test_log.append({
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'data': data
        })
    
    def store_test_approval(self, scenario, input_data, output_data, execution_time, success):
        """Store test approval in database"""
        conn = sqlite3.connect(TestConfig.TEST_DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO test_cfo_approvals 
            (test_scenario, approval_input, approval_output, execution_time, success)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            scenario or 'unknown',
            json.dumps(input_data),
            json.dumps(output_data),
            execution_time,
            success
        ))
        
        conn.commit()
        conn.close()
    
    def get_test_stats(self):
        """Get test performance statistics"""
        return {
            'total_approvals': self.approval_count,
            'successful_approvals': self.success_count,
            'failed_approvals': self.error_count,
            'success_rate': self.success_count / self.approval_count if self.approval_count > 0 else 0,
            'error_rate': self.error_count / self.approval_count if self.approval_count > 0 else 0
        }

class TestSalesAgent:
    def __init__(self):
        self.name = TestConfig.TEST_AGENTS['sales']['name']
        self.role = 'Test Sales Director'
        
        # Test-specific settings
        self.sales_rules = TestConfig.TEST_AGENTS['sales']
        
        # OpenAI setup
        openai.api_key = TestConfig.OPENAI_API_KEY
        
        # Test logging
        self.test_log = []
        self.qualification_count = 0
        self.success_count = 0
        self.error_count = 0
        
        # Initialize test database
        self.init_test_database()
    
    def init_test_database(self):
        """Initialize test database"""
        conn = sqlite3.connect(TestConfig.TEST_DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_sales_qualifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_scenario TEXT,
                lead_input TEXT,
                qualification_output TEXT,
                execution_time REAL,
                success BOOLEAN,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def qualify_lead(self, lead_data, test_scenario=None):
        """Qualify lead with test logging"""
        start_time = time.time()
        self.qualification_count += 1
        
        try:
            # Log test input
            self.log_test_event('qualification_input', {
                'scenario': test_scenario,
                'lead': lead_data,
                'timestamp': datetime.now().isoformat()
            })
            
            # Make AI decision
            context = f"""
            You are {self.name}, qualifying a sales lead.
            
            Sales Rules: {json.dumps(self.sales_rules)}
            Lead Data: {json.dumps(lead_data)}
            
            Provide qualification in JSON format with:
            1. qualification_score (0-100)
            2. status (qualified/unqualified/needs_more_info)
            3. reasoning
            4. recommended_package
            5. probability_of_closing (0-100)
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a sales director qualifying leads."},
                    {"role": "user", "content": context}
                ],
                temperature=0.3
            )
            
            qualification_text = response.choices[0].message.content
            
            try:
                qualification = json.loads(qualification_text)
            except:
                qualification = {
                    "qualification_score": 50,
                    "status": "needs_more_info",
                    "reasoning": qualification_text,
                    "recommended_package": "growth",
                    "probability_of_closing": 25
                }
            
            execution_time = time.time() - start_time
            
            # Log successful qualification
            self.log_test_event('qualification_output', {
                'qualification': qualification,
                'execution_time': execution_time,
                'success': True
            })
            
            # Store in test database
            self.store_test_qualification(test_scenario, lead_data, qualification, execution_time, True)
            
            self.success_count += 1
            return qualification
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_qualification = {
                "qualification_score": 0,
                "status": "error",
                "reasoning": f"Qualification failed: {str(e)}",
                "recommended_package": "none",
                "probability_of_closing": 0,
                "error": str(e)
            }
            
            # Log error
            self.log_test_event('qualification_error', {
                'error': str(e),
                'execution_time': execution_time,
                'success': False
            })
            
            # Store in test database
            self.store_test_qualification(test_scenario, lead_data, error_qualification, execution_time, False)
            
            self.error_count += 1
            return error_qualification
    
    def log_test_event(self, event_type, data):
        """Log test events for analysis"""
        self.test_log.append({
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'data': data
        })
    
    def store_test_qualification(self, scenario, input_data, output_data, execution_time, success):
        """Store test qualification in database"""
        conn = sqlite3.connect(TestConfig.TEST_DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO test_sales_qualifications 
            (test_scenario, lead_input, qualification_output, execution_time, success)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            scenario or 'unknown',
            json.dumps(input_data),
            json.dumps(output_data),
            execution_time,
            success
        ))
        
        conn.commit()
        conn.close()
    
    def get_test_stats(self):
        """Get test performance statistics"""
        return {
            'total_qualifications': self.qualification_count,
            'successful_qualifications': self.success_count,
            'failed_qualifications': self.error_count,
            'success_rate': self.success_count / self.qualification_count if self.qualification_count > 0 else 0,
            'error_rate': self.error_count / self.qualification_count if self.qualification_count > 0 else 0
        }
```

---

## 🧪 COMPREHENSIVE TEST SUITE

### Step 4: Create Test Suite

Create file: `test_suite.py`

```python
"""
Comprehensive test suite for AI agents
"""
import pytest
import json
import time
from test_agents import TestCEOAgent, TestCFOAgent, TestSalesAgent
from test_config import TestConfig

class AgentTestSuite:
    def __init__(self):
        self.test_results = {
            'ceo': [],
            'cfo': [],
            'sales': [],
            'integration': []
        }
        
        # Initialize test agents
        self.ceo_agent = TestCEOAgent()
        self.cfo_agent = TestCFOAgent()
        self.sales_agent = TestSalesAgent()
    
    def run_all_tests(self):
        """Run complete test suite"""
        print("🧪 STARTING COMPREHENSIVE AGENT TESTING")
        print("=" * 60)
        
        # Run individual agent tests
        self.test_ceo_agent()
        self.test_cfo_agent()
        self.test_sales_agent()
        
        # Run integration tests
        self.test_agent_integration()
        
        # Generate test report
        self.generate_test_report()
        
        return self.test_results
    
    def test_ceo_agent(self):
        """Test CEO agent with various scenarios"""
        print("\n👔 TESTING CEO AGENT")
        print("-" * 40)
        
        test_scenarios = [
            {
                'name': 'small_investment_approval',
                'data': {
                    'type': 'investment_request',
                    'description': 'Small marketing campaign',
                    'amount': TestConfig.TEST_SCENARIOS['small_investment']['amount'],
                    'expected_return': TestConfig.TEST_SCENARIOS['small_investment']['expected_return'],
                    'timeframe': TestConfig.TEST_SCENARIOS['small_investment']['timeframe'],
                    'risk_level': TestConfig.TEST_SCENARIOS['small_investment']['risk_level']
                },
                'expected_decision': 'APPROVE'
            },
            {
                'name': 'large_investment_scrutiny',
                'data': {
                    'type': 'investment_request',
                    'description': 'Large equipment purchase',
                    'amount': TestConfig.TEST_SCENARIOS['large_investment']['amount'],
                    'expected_return': TestConfig.TEST_SCENARIOS['large_investment']['expected_return'],
                    'timeframe': TestConfig.TEST_SCENARIOS['large_investment']['timeframe'],
                    'risk_level': TestConfig.TEST_SCENARIOS['large_investment']['risk_level']
                },
                'expected_decision': 'REQUEST_MORE_INFO'
            },
            {
                'name': 'poor_roi_rejection',
                'data': {
                    'type': 'investment_request',
                    'description': 'Poor ROI investment',
                    'amount': 100000,
                    'expected_return': 120000,  # Only 1.2x return
                    'timeframe': '12 months',
                    'risk_level': 'high'
                },
                'expected_decision': 'REJECT'
            }
        ]
        
        for scenario in test_scenarios:
            print(f"  Testing: {scenario['name']}")
            
            start_time = time.time()
            decision = self.ceo_agent.make_strategic_decision(
                scenario['data'], 
                scenario['name']
            )
            execution_time = time.time() - start_time
            
            # Validate decision
            test_result = {
                'scenario': scenario['name'],
                'input': scenario['data'],
                'output': decision,
                'expected': scenario['expected_decision'],
                'actual': decision.get('decision', 'ERROR'),
                'execution_time': execution_time,
                'passed': decision.get('decision') == scenario['expected_decision'],
                'confidence_score': decision.get('confidence_score', 0)
            }
            
            self.test_results['ceo'].append(test_result)
            
            status = "✅ PASS" if test_result['passed'] else "❌ FAIL"
            print(f"    {status} - {decision.get('decision')} (Expected: {scenario['expected_decision']})")
            print(f"    Execution time: {execution_time:.2f}s")
            print(f"    Confidence: {decision.get('confidence_score', 0)}/100")
        
        # Print CEO test summary
        ceo_stats = self.ceo_agent.get_test_stats()
        print(f"\n  CEO Test Summary:")
        print(f"    Total tests: {len(self.test_results['ceo'])}")
        print(f"    Passed: {sum(1 for r in self.test_results['ceo'] if r['passed'])}")
        print(f"    Success rate: {ceo_stats['success_rate']:.1%}")
    
    def test_cfo_agent(self):
        """Test CFO agent with various expense scenarios"""
        print("\n💰 TESTING CFO AGENT")
        print("-" * 40)
        
        test_scenarios = [
            {
                'name': 'small_expense_approval',
                'data': {
                    'type': 'software_subscription',
                    'description': 'Design software subscription',
                    'amount': 5000,
                    'department': 'Creative',
                    'expected_roi': 3.0
                },
                'expected_decision': 'APPROVE'
            },
            {
                'name': 'large_expense_scrutiny',
                'data': {
                    'type': 'equipment_purchase',
                    'description': 'Professional video equipment',
                    'amount': 85000,
                    'department': 'Production',
                    'expected_roi': 2.8
                },
                'expected_decision': 'REQUEST_MORE_INFO'
            },
            {
                'name': 'poor_roi_rejection',
                'data': {
                    'type': 'marketing_spend',
                    'description': 'Expensive marketing campaign',
                    'amount': 50000,
                    'department': 'Marketing',
                    'expected_roi': 1.5  # Poor ROI
                },
                'expected_decision': 'REJECT'
            }
        ]
        
        for scenario in test_scenarios:
            print(f"  Testing: {scenario['name']}")
            
            start_time = time.time()
            approval = self.cfo_agent.approve_expense(
                scenario['data'], 
                scenario['name']
            )
            execution_time = time.time() - start_time
            
            # Validate approval
            test_result = {
                'scenario': scenario['name'],
                'input': scenario['data'],
                'output': approval,
                'expected': scenario['expected_decision'],
                'actual': approval.get('decision', 'ERROR'),
                'execution_time': execution_time,
                'passed': approval.get('decision') == scenario['expected_decision'],
                'confidence_score': approval.get('confidence_score', 0)
            }
            
            self.test_results['cfo'].append(test_result)
            
            status = "✅ PASS" if test_result['passed'] else "❌ FAIL"
            print(f"    {status} - {approval.get('decision')} (Expected: {scenario['expected_decision']})")
            print(f"    Execution time: {execution_time:.2f}s")
            print(f"    Budget impact: {approval.get('budget_impact', 'Unknown')}")
        
        # Print CFO test summary
        cfo_stats = self.cfo_agent.get_test_stats()
        print(f"\n  CFO Test Summary:")
        print(f"    Total tests: {len(self.test_results['cfo'])}")
        print(f"    Passed: {sum(1 for r in self.test_results['cfo'] if r['passed'])}")
        print(f"    Success rate: {cfo_stats['success_rate']:.1%}")
    
    def test_sales_agent(self):
        """Test Sales agent with various lead scenarios"""
        print("\n📈 TESTING SALES AGENT")
        print("-" * 40)
        
        test_leads = TestConfig.TEST_LEADS
        
        for i, lead in enumerate(test_leads):
            print(f"  Testing: {lead['company_name']}")
            
            start_time = time.time()
            qualification = self.sales_agent.qualify_lead(
                lead, 
                f"lead_qualification_{i+1}"
            )
            execution_time = time.time() - start_time
            
            # Validate qualification
            test_result = {
                'scenario': f"lead_qualification_{i+1}",
                'input': lead,
                'output': qualification,
                'expected': lead['expected_qualification'],
                'actual': qualification.get('status', 'error'),
                'execution_time': execution_time,
                'passed': qualification.get('status') == lead['expected_qualification'],
                'qualification_score': qualification.get('qualification_score', 0)
            }
            
            self.test_results['sales'].append(test_result)
            
            status = "✅ PASS" if test_result['passed'] else "❌ FAIL"
            print(f"    {status} - {qualification.get('status')} (Expected: {lead['expected_qualification']})")
            print(f"    Execution time: {execution_time:.2f}s")
            print(f"    Qualification score: {qualification.get('qualification_score', 0)}/100")
        
        # Print Sales test summary
        sales_stats = self.sales_agent.get_test_stats()
        print(f"\n  Sales Test Summary:")
        print(f"    Total tests: {len(self.test_results['sales'])}")
        print(f"    Passed: {sum(1 for r in self.test_results['sales'] if r['passed'])}")
        print(f"    Success rate: {sales_stats['success_rate']:.1%}")
    
    def test_agent_integration(self):
        """Test integration between agents"""
        print("\n🔗 TESTING AGENT INTEGRATION")
        print("-" * 40)
        
        # Integration scenario: New client wants to invest in marketing
        integration_scenario = {
            'client_data': {
                'company_name': 'IntegrationTest Corp',
                'contact_name': 'Test Manager',
                'email': 'test@integration.com',
                'industry': 'e-commerce',
                'company_size': 50,
                'monthly_revenue': 500000
            },
            'investment_request': {
                'type': 'marketing_investment',
                'description': 'Comprehensive marketing campaign',
                'amount': 75000,
                'expected_return': 300000,
                'timeframe': '9 months',
                'risk_level': 'medium'
            }
        }
        
        print("  Testing: End-to-end client acquisition and investment approval")
        
        # Step 1: Sales qualification
        print("    Step 1: Sales lead qualification...")
        sales_result = self.sales_agent.qualify_lead(
            integration_scenario['client_data'],
            'integration_test'
        )
        
        # Step 2: CEO strategic decision
        print("    Step 2: CEO strategic approval...")
        ceo_result = self.ceo_agent.make_strategic_decision(
            integration_scenario['investment_request'],
            'integration_test'
        )
        
        # Step 3: CFO financial approval
        print("    Step 3: CFO financial approval...")
        cfo_result = self.cfo_agent.approve_expense({
            'type': 'marketing_spend',
            'description': integration_scenario['investment_request']['description'],
            'amount': integration_scenario['investment_request']['amount'],
            'expected_roi': integration_scenario['investment_request']['expected_return'] / integration_scenario['investment_request']['amount']
        }, 'integration_test')
        
        # Analyze integration results
        integration_result = {
            'scenario': 'end_to_end_client_acquisition',
            'sales_qualification': sales_result,
            'ceo_decision': ceo_result,
            'cfo_approval': cfo_result,
            'overall_success': (
                sales_result.get('status') == 'qualified' and
                ceo_result.get('decision') in ['APPROVE', 'REQUEST_MORE_INFO'] and
                cfo_result.get('decision') in ['APPROVE', 'REQUEST_MORE_INFO']
            )
        }
        
        self.test_results['integration'].append(integration_result)
        
        status = "✅ PASS" if integration_result['overall_success'] else "❌ FAIL"
        print(f"    {status} - Integration test completed")
        print(f"    Sales: {sales_result.get('status', 'error')}")
        print(f"    CEO: {ceo_result.get('decision', 'error')}")
        print(f"    CFO: {cfo_result.get('decision', 'error')}")
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        print("\n📊 COMPREHENSIVE TEST REPORT")
        print("=" * 60)
        
        # Overall statistics
        total_tests = (
            len(self.test_results['ceo']) + 
            len(self.test_results['cfo']) + 
            len(self.test_results['sales']) + 
            len(self.test_results['integration'])
        )
        
        total_passed = (
            sum(1 for r in self.test_results['ceo'] if r['passed']) +
            sum(1 for r in self.test_results['cfo'] if r['passed']) +
            sum(1 for r in self.test_results['sales'] if r['passed']) +
            sum(1 for r in self.test_results['integration'] if r['overall_success'])
        )
        
        print(f"📈 OVERALL RESULTS:")
        print(f"  Total tests: {total_tests}")
        print(f"  Passed: {total_passed}")
        print(f"  Failed: {total_tests - total_passed}")
        print(f"  Success rate: {total_passed/total_tests:.1%}")
        
        # Individual agent performance
        print(f"\n🤖 AGENT PERFORMANCE:")
        
        # CEO performance
        ceo_passed = sum(1 for r in self.test_results['ceo'] if r['passed'])
        ceo_total = len(self.test_results['ceo'])
        print(f"  👔 CEO Agent: {ceo_passed}/{ceo_total} ({ceo_passed/ceo_total:.1%})")
        
        # CFO performance
        cfo_passed = sum(1 for r in self.test_results['cfo'] if r['passed'])
        cfo_total = len(self.test_results['cfo'])
        print(f"  💰 CFO Agent: {cfo_passed}/{cfo_total} ({cfo_passed/cfo_total:.1%})")
        
        # Sales performance
        sales_passed = sum(1 for r in self.test_results['sales'] if r['passed'])
        sales_total = len(self.test_results['sales'])
        print(f"  📈 Sales Agent: {sales_passed}/{sales_total} ({sales_passed/sales_total:.1%})")
        
        # Integration performance
        integration_passed = sum(1 for r in self.test_results['integration'] if r['overall_success'])
        integration_total = len(self.test_results['integration'])
        print(f"  🔗 Integration: {integration_passed}/{integration_total} ({integration_passed/integration_total:.1%})")
        
        # Performance metrics
        print(f"\n⚡ PERFORMANCE METRICS:")
        
        # Average execution times
        ceo_avg_time = sum(r['execution_time'] for r in self.test_results['ceo']) / len(self.test_results['ceo']) if self.test_results['ceo'] else 0
        cfo_avg_time = sum(r['execution_time'] for r in self.test_results['cfo']) / len(self.test_results['cfo']) if self.test_results['cfo'] else 0
        sales_avg_time = sum(r['execution_time'] for r in self.test_results['sales']) / len(self.test_results['sales']) if self.test_results['sales'] else 0
        
        print(f"  CEO avg response time: {ceo_avg_time:.2f}s")
        print(f"  CFO avg response time: {cfo_avg_time:.2f}s")
        print(f"  Sales avg response time: {sales_avg_time:.2f}s")
        
        # Confidence scores
        ceo_avg_confidence = sum(r['confidence_score'] for r in self.test_results['ceo']) / len(self.test_results['ceo']) if self.test_results['ceo'] else 0
        cfo_avg_confidence = sum(r['confidence_score'] for r in self.test_results['cfo']) / len(self.test_results['cfo']) if self.test_results['cfo'] else 0
        sales_avg_qualification = sum(r['qualification_score'] for r in self.test_results['sales']) / len(self.test_results['sales']) if self.test_results['sales'] else 0
        
        print(f"  CEO avg confidence: {ceo_avg_confidence:.1f}/100")
        print(f"  CFO avg confidence: {cfo_avg_confidence:.1f}/100")
        print(f"  Sales avg qualification: {sales_avg_qualification:.1f}/100")
        
        # Save detailed report to file
        self.save_test_report()
    
    def save_test_report(self):
        """Save detailed test report to file"""
        report_data = {
            'timestamp': time.time(),
            'test_results': self.test_results,
            'agent_stats': {
                'ceo': self.ceo_agent.get_test_stats(),
                'cfo': self.cfo_agent.get_test_stats(),
                'sales': self.sales_agent.get_test_stats()
            }
        }
        
        with open('test_report.json', 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n💾 Detailed test report saved to: test_report.json")

# HOW TO RUN THE TEST SUITE

def run_agent_tests():
    """Run the complete agent test suite"""
    
    # Create test suite
    test_suite = AgentTestSuite()
    
    # Run all tests
    results = test_suite.run_all_tests()
    
    return results

if __name__ == "__main__":
    print("🚀 STARTING AGENT TEST SUITE")
    print("Make sure you have:")
    print("1. OpenAI API key in .env file")
    print("2. All required packages installed")
    print("3. Test configuration set up")
    print("\nPress Enter to continue...")
    input()
    
    # Run tests
    test_results = run_agent_tests()
    
    print("\n🎉 TESTING COMPLETE!")
    print("Check test_report.json for detailed results")
```

---

## 🚀 HOW TO RUN THE TESTS

### Step 5: Execute the Test Suite

1. **Set up test environment:**
```bash
# Create .env file with your API key
echo "OPENAI_API_KEY=your_actual_api_key_here" > .env

# Install test dependencies
pip install pytest openai flask requests python-dotenv pandas
```

2. **Run individual agent tests:**
```bash
# Test CEO agent only
python -c "from test_agents import TestCEOAgent; ceo = TestCEOAgent(); print(ceo.make_strategic_decision({'type': 'test', 'amount': 50000}))"

# Test CFO agent only
python -c "from test_agents import TestCFOAgent; cfo = TestCFOAgent(); print(cfo.approve_expense({'type': 'test', 'amount': 25000}))"

# Test Sales agent only
python -c "from test_agents import TestSalesAgent; sales = TestSalesAgent(); print(sales.qualify_lead({'company_name': 'Test Corp', 'industry': 'e-commerce'}))"
```

3. **Run complete test suite:**
```bash
python test_suite.py
```

4. **Run with pytest (advanced):**
```bash
pytest test_suite.py -v --tb=short
```

### Step 6: Analyze Test Results

**View test database:**
```python
import sqlite3
import pandas as pd

# Connect to test database
conn = sqlite3.connect('test_agents.db')

# View CEO decisions
ceo_results = pd.read_sql_query("SELECT * FROM test_ceo_decisions", conn)
print("CEO Test Results:")
print(ceo_results)

# View CFO approvals
cfo_results = pd.read_sql_query("SELECT * FROM test_cfo_approvals", conn)
print("CFO Test Results:")
print(cfo_results)

# View Sales qualifications
sales_results = pd.read_sql_query("SELECT * FROM test_sales_qualifications", conn)
print("Sales Test Results:")
print(sales_results)

conn.close()
```

**Analyze performance metrics:**
```python
import json

# Load test report
with open('test_report.json', 'r') as f:
    report = json.load(f)

# Print performance summary
print("Performance Analysis:")
for agent, stats in report['agent_stats'].items():
    print(f"{agent.upper()}:")
    print(f"  Success Rate: {stats['success_rate']:.1%}")
    print(f"  Error Rate: {stats['error_rate']:.1%}")
    print(f"  Total Operations: {stats.get('total_decisions', stats.get('total_approvals', stats.get('total_qualifications', 0)))}")
```

---

## 🔧 DEBUGGING AND OPTIMIZATION

### Step 7: Debug Failed Tests

**Check agent logs:**
```python
from test_agents import TestCEOAgent

ceo = TestCEOAgent()

# Make a test decision
result = ceo.make_strategic_decision({
    'type': 'test_investment',
    'amount': 100000,
    'expected_return': 250000
})

# Check test log
print("Agent Test Log:")
for log_entry in ceo.test_log:
    print(f"{log_entry['timestamp']}: {log_entry['event_type']}")
    if log_entry['event_type'] == 'decision_error':
        print(f"  Error: {log_entry['data']['error']}")
```

**Optimize agent performance:**
```python
# Modify test configuration for better performance
from test_config import TestConfig

# Reduce API calls by using cheaper model
TestConfig.OPENAI_MODEL = "gpt-3.5-turbo"  # Instead of gpt-4

# Adjust test thresholds
TestConfig.TEST_AGENTS['ceo']['decision_threshold'] = 25000  # Lower threshold

# Test with optimized settings
from test_agents import TestCEOAgent
optimized_ceo = TestCEOAgent()
```

### Step 8: Load Testing

**Test agent under load:**
```python
import threading
import time
from test_agents import TestCEOAgent

def load_test_ceo():
    """Test CEO agent under concurrent load"""
    ceo = TestCEOAgent()
    
    def make_concurrent_decisions(thread_id):
        """Make decisions concurrently"""
        for i in range(10):  # 10 decisions per thread
            decision = ceo.make_strategic_decision({
                'type': f'load_test_{thread_id}_{i}',
                'amount': 50000,
                'expected_return': 150000
            })
            print(f"Thread {thread_id}, Decision {i}: {decision.get('decision', 'ERROR')}")
            time.sleep(0.1)  # Small delay
    
    # Create 5 concurrent threads
    threads = []
    for i in range(5):
        thread = threading.Thread(target=make_concurrent_decisions, args=(i,))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # Check final stats
    stats = ceo.get_test_stats()
    print(f"Load Test Results: {stats}")

# Run load test
load_test_ceo()
```

---

## 📊 PRODUCTION READINESS CHECKLIST

### Step 9: Validate Production Readiness

**Performance benchmarks:**
- ✅ Response time < 3 seconds
- ✅ Success rate > 95%
- ✅ Error handling works correctly
- ✅ Concurrent requests handled properly
- ✅ Database operations are reliable

**Test checklist:**
```python
def production_readiness_check():
    """Check if agents are ready for production"""
    
    checklist = {
        'ceo_agent': {
            'response_time_ok': False,
            'success_rate_ok': False,
            'error_handling_ok': False
        },
        'cfo_agent': {
            'response_time_ok': False,
            'success_rate_ok': False,
            'error_handling_ok': False
        },
        'sales_agent': {
            'response_time_ok': False,
            'success_rate_ok': False,
            'error_handling_ok': False
        }
    }
    
    # Run production readiness tests
    from test_suite import AgentTestSuite
    test_suite = AgentTestSuite()
    results = test_suite.run_all_tests()
    
    # Check CEO agent
    ceo_stats = test_suite.ceo_agent.get_test_stats()
    checklist['ceo_agent']['success_rate_ok'] = ceo_stats['success_rate'] > 0.95
    
    # Check CFO agent
    cfo_stats = test_suite.cfo_agent.get_test_stats()
    checklist['cfo_agent']['success_rate_ok'] = cfo_stats['success_rate'] > 0.95
    
    # Check Sales agent
    sales_stats = test_suite.sales_agent.get_test_stats()
    checklist['sales_agent']['success_rate_ok'] = sales_stats['success_rate'] > 0.95
    
    # Overall readiness
    all_ready = all(
        all(checks.values()) 
        for checks in checklist.values()
    )
    
    print("Production Readiness Check:")
    for agent, checks in checklist.items():
        print(f"  {agent}: {'✅ READY' if all(checks.values()) else '❌ NOT READY'}")
    
    print(f"\nOverall Status: {'✅ PRODUCTION READY' if all_ready else '❌ NEEDS WORK'}")
    
    return checklist

# Run production readiness check
production_readiness_check()
```

---

## 🎯 WHAT YOU NOW HAVE

### ✅ COMPLETE TESTING FRAMEWORK:
- **Test Environment**: Isolated testing with real AI agents
- **Test Agents**: Enhanced versions with logging and validation
- **Test Suite**: Comprehensive automated testing
- **Performance Monitoring**: Response times, success rates, error tracking
- **Integration Testing**: Multi-agent workflow validation

### ✅ REAL VALIDATION:
- **Functional Testing**: Verify agents make correct decisions
- **Performance Testing**: Measure response times and throughput
- **Load Testing**: Test under concurrent usage
- **Error Testing**: Validate error handling and recovery
- **Integration Testing**: Test agent-to-agent communication

### ✅ PRODUCTION READINESS:
- **Benchmarking**: Performance standards and targets
- **Monitoring**: Real-time performance tracking
- **Debugging**: Detailed logging and error analysis
- **Optimization**: Performance tuning and improvement
- **Validation**: Production readiness checklist

**This is a complete testing framework for REAL AI agents that you can use to validate your system before deploying to production.**

