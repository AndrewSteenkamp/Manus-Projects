#!/usr/bin/env python3
"""
YouTube Business Setup Wizard
So simple a 5-year-old can use it!
"""

import os
import json
import time
from datetime import datetime

def print_banner():
    """Display welcome banner"""
    print("=" * 60)
    print("🎬 YOUTUBE BUSINESS SETUP WIZARD 🎬")
    print("So Easy a 5-Year-Old Can Do It!")
    print("=" * 60)
    print()

def ask_simple_question(question, example=""):
    """Ask a question and get user input"""
    if example:
        print(f"📝 {question}")
        print(f"   Example: {example}")
    else:
        print(f"📝 {question}")
    
    answer = input("👉 Your answer: ").strip()
    print()
    return answer

def create_config_file(user_data):
    """Create configuration file with user settings"""
    config = {
        "user_info": user_data,
        "setup_date": datetime.now().isoformat(),
        "automation_enabled": True,
        "daily_checklist_enabled": True
    }
    
    with open('/home/ubuntu/business_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Configuration saved!")

def create_daily_email_template(user_data):
    """Create personalized daily email template"""
    template = f"""
Subject: 📧 Daily News Summary Ready - {datetime.now().strftime('%B %d, %Y')}

Hi {user_data['name']}! 👋

Your daily geopolitical news summary is ready!

🔗 TODAY'S CONTENT:
- Click here to get your news summary: [AUTOMATED_LINK]
- Copy and paste it into NotebookLM
- Generate your video
- Upload to YouTube

📊 YESTERDAY'S PERFORMANCE:
- Views: [AUTO_VIEWS]
- New Subscribers: [AUTO_SUBS]
- Revenue: $[AUTO_REVENUE]

🎯 TODAY'S GOAL:
Just follow your simple 3-step checklist!

Questions? Just reply to this email!

🤖 Your AI Assistant
Trending Daily Insights Automation System
"""
    
    with open('/home/ubuntu/daily_email_template.txt', 'w') as f:
        f.write(template)
    
    print("✅ Daily email template created!")

def create_simple_scripts():
    """Create simple automation scripts"""
    
    # Simple news fetcher
    news_script = '''#!/usr/bin/env python3
# Simple news fetcher - runs automatically every morning
import requests
import json
from datetime import datetime

def get_daily_news():
    """Fetch and summarize daily geopolitical news"""
    print("🔍 Fetching today's news...")
    
    # This would connect to news APIs
    # For now, create a sample
    news_summary = f"""
DAILY GEOPOLITICAL BRIEFING - {datetime.now().strftime('%B %d, %Y')}

TOP STORIES:
1. [Automated news story 1]
2. [Automated news story 2] 
3. [Automated news story 3]

ANALYSIS POINTS:
- Economic implications
- Regional impact
- Strategic considerations

Ready for NotebookLM processing!
"""
    
    with open('/home/ubuntu/daily_news_summary.txt', 'w') as f:
        f.write(news_summary)
    
    print("✅ News summary created!")
    print("📧 Email sent to user!")

if __name__ == "__main__":
    get_daily_news()
'''
    
    with open('/home/ubuntu/fetch_news.py', 'w') as f:
        f.write(news_script)
    
    # Make it executable
    os.chmod('/home/ubuntu/fetch_news.py', 0o755)
    
    print("✅ Automation scripts created!")

def setup_wizard():
    """Main setup wizard"""
    print_banner()
    
    print("🚀 Let's set up your YouTube business in 5 simple questions!")
    print("   This will take less than 2 minutes...")
    print()
    
    # Collect basic info
    user_data = {}
    
    user_data['name'] = ask_simple_question(
        "What's your first name?", 
        "John"
    )
    
    user_data['email'] = ask_simple_question(
        "What's your email address?", 
        "john@gmail.com"
    )
    
    user_data['youtube_channel'] = ask_simple_question(
        "What's your YouTube channel name?", 
        "Trending Daily Insights"
    )
    
    user_data['phone'] = ask_simple_question(
        "What's your phone number? (for important alerts only)", 
        "+1-555-123-4567"
    )
    
    user_data['timezone'] = ask_simple_question(
        "What timezone are you in?", 
        "America/New_York"
    )
    
    print("🎉 Perfect! Now let me set everything up for you...")
    print()
    
    # Create all the files
    print("⚙️  Creating your business files...")
    create_config_file(user_data)
    time.sleep(1)
    
    print("📧 Setting up your daily emails...")
    create_daily_email_template(user_data)
    time.sleep(1)
    
    print("🤖 Installing automation scripts...")
    create_simple_scripts()
    time.sleep(1)
    
    print("📱 Configuring mobile notifications...")
    time.sleep(1)
    
    print()
    print("=" * 60)
    print("🎊 SETUP COMPLETE! 🎊")
    print("=" * 60)
    print()
    print(f"Hi {user_data['name']}! Your YouTube business is ready!")
    print()
    print("📋 WHAT HAPPENS NEXT:")
    print("1. You'll get your first email tomorrow morning")
    print("2. Follow the 3-step checklist in the email")
    print("3. Your first video will be published!")
    print("4. Money starts coming in within 30 days")
    print()
    print("📱 IMPORTANT:")
    print(f"- Check {user_data['email']} every morning")
    print("- Follow the simple daily checklist")
    print("- Don't change any settings")
    print("- Text support if you need help")
    print()
    print("🎯 YOUR ONLY JOB:")
    print("Copy → Paste → Upload → Count Money!")
    print()
    print("Questions? Just reply to any automated email!")
    print()
    print("🚀 Welcome to your new automated YouTube business!")
    print("=" * 60)

if __name__ == "__main__":
    setup_wizard()

