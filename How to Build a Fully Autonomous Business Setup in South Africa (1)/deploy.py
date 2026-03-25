#!/usr/bin/env python3
"""
Deployment script for Autonomous AI-Powered Business
This script helps you get the application running quickly
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_requirements():
    """Install required packages"""
    try:
        print("📦 Installing requirements...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        return False

def run_application():
    """Run the Flask application"""
    try:
        print("🚀 Starting the application...")
        print("📱 Open your browser and go to: http://127.0.0.1:5000")
        print("🛑 Press Ctrl+C to stop the application")
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Application stopped")

def main():
    """Main deployment function"""
    print("🤖 Autonomous AI-Powered Business Deployment")
    print("=" * 50)
    
    if not check_python_version():
        return
    
    if not install_requirements():
        return
    
    run_application()

if __name__ == "__main__":
    main()
