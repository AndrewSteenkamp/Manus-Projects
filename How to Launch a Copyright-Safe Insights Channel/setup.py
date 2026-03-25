#!/usr/bin/env python3
"""
Setup script for Autonomous YouTube Agent
Handles installation, configuration, and initial setup
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def install_dependencies():
    """Install required Python packages."""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)

def create_config():
    """Create initial configuration files."""
    print("⚙️ Creating configuration files...")
    
    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)
    
    # Main agent configuration
    agent_config = {
        "agent_settings": {
            "name": "TrendingDailyInsights_Agent",
            "version": "1.0.0",
            "autonomous_mode": True,
            "daily_schedule": "08:00",
            "timezone": "UTC"
        },
        "channel_config": {
            "channel_id": "REPLACE_WITH_YOUR_CHANNEL_ID",
            "niche": "Geopolitical Analysis",
            "target_audience": "Geopolitics enthusiasts, investors, policy makers",
            "content_style": "Professional analysis with expert insights"
        },
        "research_config": {
            "primary_sources": [
                "reuters.com",
                "apnews.com",
                "ft.com",
                "defensenews.com",
                "foreignaffairs.com"
            ],
            "keywords": [
                "Ukraine war",
                "geopolitical analysis", 
                "military strategy",
                "international relations",
                "economic warfare",
                "sanctions analysis"
            ],
            "expert_sources": [
                "Scott Ritter",
                "John Mearsheimer", 
                "Michael Hudson",
                "Douglas MacGregor"
            ]
        },
        "content_config": {
            "video_length": "8-12 minutes",
            "daily_topics": 3,
            "analysis_depth": "expert-level",
            "voice_style": "professional, authoritative"
        },
        "automation_config": {
            "auto_research": True,
            "auto_script_generation": True,
            "auto_video_creation": True,
            "auto_upload": True,
            "auto_optimization": True
        },
        "performance_config": {
            "target_views": 1000,
            "target_ctr": 0.08,
            "target_retention": 0.6,
            "optimization_frequency": "weekly"
        }
    }
    
    with open(config_dir / "agent_config.json", "w") as f:
        json.dump(agent_config, f, indent=2)
    
    # API keys template
    api_keys_template = {
        "youtube": {
            "api_key": "YOUR_YOUTUBE_API_KEY",
            "client_id": "YOUR_YOUTUBE_CLIENT_ID", 
            "client_secret": "YOUR_YOUTUBE_CLIENT_SECRET"
        },
        "notebooklm": {
            "api_key": "YOUR_NOTEBOOKLM_API_KEY"
        },
        "news_apis": {
            "newsapi_key": "YOUR_NEWSAPI_KEY",
            "reuters_key": "YOUR_REUTERS_KEY"
        },
        "openai": {
            "api_key": "YOUR_OPENAI_API_KEY"
        }
    }
    
    with open(config_dir / "api_keys_template.json", "w") as f:
        json.dump(api_keys_template, f, indent=2)
    
    print("✅ Configuration files created")
    print("📝 Please edit config/api_keys_template.json with your actual API keys")
    print("📝 Then rename it to api_keys.json")

def create_systemd_service():
    """Create systemd service file for Linux deployment."""
    service_content = """[Unit]
Description=Autonomous YouTube Agent
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/autonomous_youtube_agent
ExecStart=/usr/bin/python3 autonomous_agent_system.py --daemon
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
    
    with open("youtube-agent.service", "w") as f:
        f.write(service_content)
    
    print("✅ Systemd service file created: youtube-agent.service")

def create_startup_scripts():
    """Create startup scripts for different platforms."""
    
    # Linux/Mac startup script
    linux_script = """#!/bin/bash
cd "$(dirname "$0")"
python3 autonomous_agent_system.py --daemon
"""
    
    with open("start_agent.sh", "w") as f:
        f.write(linux_script)
    os.chmod("start_agent.sh", 0o755)
    
    # Windows startup script
    windows_script = """@echo off
cd /d "%~dp0"
python autonomous_agent_system.py --daemon
pause
"""
    
    with open("start_agent.bat", "w") as f:
        f.write(windows_script)
    
    print("✅ Startup scripts created")

def setup_directories():
    """Create necessary directories."""
    directories = ["logs", "output", "cache", "templates", "assets"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print("✅ Directory structure created")

def main():
    """Main setup function."""
    print("🤖 Autonomous YouTube Agent Setup")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Run setup steps
    setup_directories()
    install_dependencies()
    create_config()
    create_systemd_service()
    create_startup_scripts()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit config/api_keys_template.json with your API keys")
    print("2. Rename it to config/api_keys.json")
    print("3. Update config/agent_config.json with your channel details")
    print("4. Run: python autonomous_agent_system.py --dev-mode (for testing)")
    print("5. Run: python autonomous_agent_system.py --daemon (for production)")
    print("\n📖 See agent_deployment_guide.md for detailed instructions")

if __name__ == "__main__":
    main()

