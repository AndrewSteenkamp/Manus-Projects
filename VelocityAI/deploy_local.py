#!/usr/bin/env python3
"""
Complete Local Deployment Script
Automatically sets up everything you need
"""

import os
import subprocess
import sys

def check_python():
    """Check Python version"""
    print("🐍 Checking Python version...")
    
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        print("Please install Python 3.8 or higher")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_packages():
    """Install required packages"""
    print("📦 Installing required packages...")
    
    packages = [
        'flask',
        'python-dotenv', 
        'requests',
        'anthropic',
        'google-generativeai',
        'huggingface_hub'
    ]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✅ Installed {package}")
        except subprocess.CalledProcessError:
            print(f"⚠️  Failed to install {package} (continuing anyway)")
    
    return True

def create_env_file():
    """Create .env file with API key placeholders"""
    print("🔑 Creating .env file...")
    
    env_content = """# UGC Video Generator - API Keys
# Choose ONE provider and add its API key

# OPTION 1: FREE - Hugging Face (Recommended)
# Sign up at: https://huggingface.co/
# Get token from: https://huggingface.co/settings/tokens
HF_API_KEY=your_huggingface_token_here

# OPTION 2: FREE - Google Gemini
# Get key from: https://makersuite.google.com/app/apikey
GOOGLE_API_KEY=your_google_api_key_here

# OPTION 3: CHEAP - Anthropic Claude
# Sign up at: https://console.anthropic.com/
ANTHROPIC_API_KEY=your_anthropic_key_here

# Set your preferred provider
AI_PROVIDER=huggingface
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ .env file created")
    print("📝 Please edit .env file and add your API key")
    return True

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    
    directories = ['ugc_videos', 'templates']
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created {directory}/")
    
    return True

def test_system():
    """Test the system"""
    print("🧪 Testing system...")
    
    try:
        # Test AI helper
        from ai_helper import AIHelper
        
        helper = AIHelper(provider="huggingface")
        print(f"✅ AI Helper initialized with {helper.provider}")
        
        # Test video generator
        from ugc_video_generator_local import UGCVideoGenerator
        
        generator = UGCVideoGenerator(ai_provider="huggingface")
        print("✅ UGC Video Generator initialized")
        
        return True
        
    except Exception as e:
        print(f"❌ System test failed: {str(e)}")
        return False

def main():
    """Main deployment function"""
    print("🚀 UGC VIDEO GENERATOR - LOCAL DEPLOYMENT")
    print("=" * 60)
    
    # Check Python
    if not check_python():
        return False
    
    # Install packages
    if not install_packages():
        return False
    
    # Create directories
    if not create_directories():
        return False
    
    # Create .env file
    if not create_env_file():
        return False
    
    # Test system
    if not test_system():
        print("⚠️  System test failed, but basic setup is complete")
    
    print("\n🎉 DEPLOYMENT COMPLETE!")
    print("=" * 60)
    
    print("\n📋 NEXT STEPS:")
    print("1. Edit .env file and add your API key")
    print("2. Run: python ugc_video_generator_local.py")
    print("3. Or run web interface: python ugc_web_interface_local.py")
    
    print("\n💰 COST COMPARISON:")
    print("OpenAI GPT-4: $0.03 per request")
    print("Hugging Face: FREE (1000 requests/month)")
    print("Google Gemini: FREE (60 requests/minute)")
    print("Anthropic Claude: $0.006 per request (5x cheaper)")
    
    print("\n🎯 RECOMMENDED: Start with Hugging Face (free)")
    
    return True

if __name__ == "__main__":
    main()

