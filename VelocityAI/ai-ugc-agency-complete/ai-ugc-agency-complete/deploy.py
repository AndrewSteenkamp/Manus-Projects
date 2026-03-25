#!/usr/bin/env python3
"""
AI-Powered UGC Advertising Agency - Automated Deployment Script
One-click deployment and setup for the complete autonomous agency system
"""

import os
import sys
import subprocess
import json
import time
from datetime import datetime
from pathlib import Path

class AgencyDeployer:
    """Automated deployment system for the AI-Powered UGC Agency."""
    
    def __init__(self):
        """Initialize the deployment system."""
        self.project_root = Path(__file__).parent
        self.deployment_log = []
        self.start_time = datetime.now()
        
        print("🚀 AI-Powered UGC Advertising Agency")
        print("🤖 Automated Deployment System")
        print("="*50)
    
    def log(self, message, status="INFO"):
        """Log deployment messages."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {status}: {message}"
        self.deployment_log.append(log_entry)
        
        # Color coding for terminal output
        colors = {
            "INFO": "\033[94m",    # Blue
            "SUCCESS": "\033[92m", # Green
            "WARNING": "\033[93m", # Yellow
            "ERROR": "\033[91m",   # Red
            "RESET": "\033[0m"     # Reset
        }
        
        color = colors.get(status, colors["RESET"])
        print(f"{color}{log_entry}{colors['RESET']}")
    
    def check_python_version(self):
        """Check Python version compatibility."""
        self.log("Checking Python version...")
        
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            self.log(f"Python {version.major}.{version.minor} detected. Python 3.8+ required.", "ERROR")
            return False
        
        self.log(f"Python {version.major}.{version.minor}.{version.micro} - Compatible ✓", "SUCCESS")
        return True
    
    def install_dependencies(self):
        """Install required Python packages."""
        self.log("Installing Python dependencies...")
        
        try:
            # Check if requirements.txt exists
            requirements_file = self.project_root / "requirements.txt"
            if not requirements_file.exists():
                self.log("requirements.txt not found", "ERROR")
                return False
            
            # Install packages
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log("Dependencies installed successfully ✓", "SUCCESS")
                return True
            else:
                self.log(f"Failed to install dependencies: {result.stderr}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"Error installing dependencies: {str(e)}", "ERROR")
            return False
    
    def setup_environment(self):
        """Set up environment variables."""
        self.log("Setting up environment configuration...")
        
        env_file = self.project_root / ".env"
        env_example = self.project_root / ".env.example"
        
        # Create .env from .env.example if it doesn't exist
        if not env_file.exists() and env_example.exists():
            try:
                with open(env_example, 'r') as f:
                    env_content = f.read()
                
                with open(env_file, 'w') as f:
                    f.write(env_content)
                
                self.log(".env file created from template", "SUCCESS")
                self.log("⚠️  Please edit .env file with your API keys", "WARNING")
                
            except Exception as e:
                self.log(f"Error creating .env file: {str(e)}", "ERROR")
                return False
        
        # Check for required environment variables
        required_vars = ["AI_PROVIDER"]
        missing_vars = []
        
        if env_file.exists():
            try:
                with open(env_file, 'r') as f:
                    env_content = f.read()
                
                for var in required_vars:
                    if f"{var}=" not in env_content or f"{var}=" in env_content and not env_content.split(f"{var}=")[1].split('\n')[0].strip():
                        missing_vars.append(var)
                
                if missing_vars:
                    self.log(f"Missing environment variables: {', '.join(missing_vars)}", "WARNING")
                    self.log("Please configure your .env file before running the system", "WARNING")
                else:
                    self.log("Environment configuration complete ✓", "SUCCESS")
                
            except Exception as e:
                self.log(f"Error reading .env file: {str(e)}", "ERROR")
                return False
        
        return True
    
    def create_directories(self):
        """Create necessary directories."""
        self.log("Creating project directories...")
        
        directories = [
            "data",
            "logs", 
            "uploads",
            "exports",
            "backups"
        ]
        
        try:
            for directory in directories:
                dir_path = self.project_root / directory
                dir_path.mkdir(exist_ok=True)
            
            self.log("Project directories created ✓", "SUCCESS")
            return True
            
        except Exception as e:
            self.log(f"Error creating directories: {str(e)}", "ERROR")
            return False
    
    def test_system_components(self):
        """Test all system components."""
        self.log("Testing system components...")
        
        try:
            # Test AI Helper
            sys.path.append(str(self.project_root))
            from services.ai_helper import AIHelper
            
            ai_helper = AIHelper()
            connection_test = ai_helper.test_connection()
            
            if connection_test:
                self.log("AI Helper connection test passed ✓", "SUCCESS")
            else:
                self.log("AI Helper connection test failed", "WARNING")
                self.log("Check your API keys in .env file", "WARNING")
            
            # Test agent imports
            from agents.ceo_agent import CEOAgent
            from agents.cfo_agent import CFOAgent
            from agents.sales_agent import SalesAgent
            from agents.creative_agent import CreativeAgent
            
            self.log("All agent modules imported successfully ✓", "SUCCESS")
            
            # Test web application
            from web.app import app
            self.log("Web application imported successfully ✓", "SUCCESS")
            
            return True
            
        except ImportError as e:
            self.log(f"Import error: {str(e)}", "ERROR")
            return False
        except Exception as e:
            self.log(f"System test error: {str(e)}", "ERROR")
            return False
    
    def run_comprehensive_test(self):
        """Run the comprehensive system test."""
        self.log("Running comprehensive system test...")
        
        try:
            # Import and run the test suite
            from test_complete_system import SystemTester
            
            tester = SystemTester()
            results = tester.run_all_tests()
            
            success_rate = results["summary"]["success_rate"]
            
            if success_rate >= 80:
                self.log(f"System test passed: {success_rate:.1f}% success rate ✓", "SUCCESS")
                return True
            else:
                self.log(f"System test failed: {success_rate:.1f}% success rate", "WARNING")
                self.log("Some components may not be fully functional", "WARNING")
                return False
                
        except Exception as e:
            self.log(f"Error running system test: {str(e)}", "ERROR")
            return False
    
    def start_web_server(self):
        """Start the web server."""
        self.log("Starting web server...")
        
        try:
            # Check if server is already running
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', 5000))
            sock.close()
            
            if result == 0:
                self.log("Web server already running on port 5000", "WARNING")
                return True
            
            # Start the server
            self.log("Starting Flask web server on http://localhost:5000", "INFO")
            self.log("Press Ctrl+C to stop the server", "INFO")
            
            # Import and run the app
            from web.app import app
            app.run(host='0.0.0.0', port=5000, debug=False)
            
            return True
            
        except KeyboardInterrupt:
            self.log("Web server stopped by user", "INFO")
            return True
        except Exception as e:
            self.log(f"Error starting web server: {str(e)}", "ERROR")
            return False
    
    def generate_deployment_report(self):
        """Generate deployment report."""
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        report = {
            "deployment_timestamp": self.start_time.isoformat(),
            "completion_timestamp": end_time.isoformat(),
            "duration_seconds": duration.total_seconds(),
            "deployment_log": self.deployment_log,
            "system_info": {
                "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                "platform": sys.platform,
                "project_root": str(self.project_root)
            }
        }
        
        # Save report
        report_file = self.project_root / f"deployment_report_{self.start_time.strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)
            
            self.log(f"Deployment report saved: {report_file.name}", "SUCCESS")
            
        except Exception as e:
            self.log(f"Error saving deployment report: {str(e)}", "ERROR")
        
        return report
    
    def deploy(self):
        """Run the complete deployment process."""
        self.log("Starting AI-Powered UGC Agency deployment...")
        
        steps = [
            ("Python Version Check", self.check_python_version),
            ("Install Dependencies", self.install_dependencies),
            ("Environment Setup", self.setup_environment),
            ("Create Directories", self.create_directories),
            ("Test System Components", self.test_system_components),
            ("Run Comprehensive Test", self.run_comprehensive_test)
        ]
        
        failed_steps = []
        
        for step_name, step_function in steps:
            self.log(f"Step: {step_name}", "INFO")
            
            try:
                success = step_function()
                if success:
                    self.log(f"✅ {step_name} completed successfully", "SUCCESS")
                else:
                    self.log(f"❌ {step_name} failed", "ERROR")
                    failed_steps.append(step_name)
            except Exception as e:
                self.log(f"❌ {step_name} failed with error: {str(e)}", "ERROR")
                failed_steps.append(step_name)
        
        # Generate deployment report
        report = self.generate_deployment_report()
        
        # Final status
        print("\n" + "="*60)
        print("🎉 AI-POWERED UGC AGENCY DEPLOYMENT COMPLETE")
        print("="*60)
        
        if not failed_steps:
            print("✅ All deployment steps completed successfully!")
            print("\n🚀 NEXT STEPS:")
            print("1. Edit your .env file with API keys")
            print("2. Run: python web/app.py")
            print("3. Open: http://localhost:5000")
            print("4. Start generating UGC videos for clients!")
            
            # Offer to start the server
            try:
                start_server = input("\nStart web server now? (y/n): ").lower().strip()
                if start_server == 'y':
                    self.start_web_server()
            except KeyboardInterrupt:
                print("\nDeployment completed. Run 'python web/app.py' to start the server.")
        else:
            print(f"❌ {len(failed_steps)} deployment steps failed:")
            for step in failed_steps:
                print(f"   - {step}")
            print("\nPlease review the deployment log and fix any issues.")
        
        print("="*60)
        
        return len(failed_steps) == 0


def main():
    """Main deployment function."""
    deployer = AgencyDeployer()
    success = deployer.deploy()
    
    # Return appropriate exit code
    return 0 if success else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
