#!/usr/bin/env python3
"""
TRENDING DAILY INSIGHTS - SIMPLE VIDEO GENERATOR
Core Product: Generate videos for your YouTube channel TODAY

This script does ONE thing: Takes news topics and creates ready-to-upload videos
No complex business setup - just video production
"""

import requests
import json
import os
from datetime import datetime
import openai
from openai import OpenAI

class SimpleVideoGenerator:
    def __init__(self):
        self.client = OpenAI()
        self.channel_name = "Trending Daily Insights"
        self.output_dir = "/home/ubuntu/daily_videos"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def get_daily_topics(self):
        """Get 3 simple geopolitical topics for today"""
        
        prompt = """
        Generate 3 geopolitical topics for today's Trending Daily Insights videos.
        
        Requirements:
        - Current/relevant topics (Ukraine, China, Middle East, Economics)
        - Each topic should be 5-10 minutes of content
        - Include specific angle/perspective
        - Make them engaging for YouTube audience
        
        Format as JSON:
        {
            "topics": [
                {
                    "title": "Video title",
                    "angle": "Specific perspective/angle",
                    "keywords": ["keyword1", "keyword2", "keyword3"]
                }
            ]
        }
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a geopolitical content strategist for YouTube."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            # Extract JSON from response
            start = content.find('{')
            end = content.rfind('}') + 1
            json_content = content[start:end]
            
            topics_data = json.loads(json_content)
            return topics_data['topics']
            
        except Exception as e:
            print(f"Error getting topics: {e}")
            # Fallback topics
            return [
                {
                    "title": "Ukraine War Update: Latest Developments",
                    "angle": "Economic impact on global markets",
                    "keywords": ["ukraine", "war", "economy"]
                },
                {
                    "title": "China's Economic Strategy: What's Next?",
                    "angle": "Impact on US-China relations",
                    "keywords": ["china", "economy", "trade"]
                },
                {
                    "title": "Middle East Tensions: Regional Analysis",
                    "angle": "Oil prices and global implications",
                    "keywords": ["middle east", "oil", "geopolitics"]
                }
            ]
    
    def create_video_script(self, topic):
        """Create a 5-10 minute video script for the topic"""
        
        prompt = f"""
        Write a 5-10 minute video script for Trending Daily Insights YouTube channel.
        
        Topic: {topic['title']}
        Angle: {topic['angle']}
        Keywords: {', '.join(topic['keywords'])}
        
        Script Requirements:
        - Professional but accessible tone
        - Clear structure: Intro, 3 main points, conclusion
        - Include specific facts and analysis
        - Add calls to action (subscribe, like, comment)
        - Mention "Trending Daily Insights" 2-3 times
        - 800-1200 words (5-10 minutes when spoken)
        
        Format:
        [INTRO]
        Welcome to Trending Daily Insights...
        
        [MAIN CONTENT]
        Today we're analyzing...
        
        [CONCLUSION]
        That's today's analysis from Trending Daily Insights...
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert geopolitical analyst and YouTube content creator."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error creating script: {e}")
            return f"""
            [INTRO]
            Welcome to Trending Daily Insights, your source for expert geopolitical analysis.
            
            [MAIN CONTENT]
            Today we're examining {topic['title']}. {topic['angle']}
            
            This development has significant implications for global markets and international relations.
            
            [CONCLUSION]
            That's today's analysis from Trending Daily Insights. Subscribe for daily geopolitical insights.
            """
    
    def save_script_for_notebooklm(self, script, topic, video_number):
        """Save script in format ready for NotebookLM"""
        
        # Clean script for NotebookLM
        clean_script = script.replace("[INTRO]", "").replace("[MAIN CONTENT]", "").replace("[CONCLUSION]", "")
        clean_script = clean_script.strip()
        
        # Create filename
        date_str = datetime.now().strftime("%Y%m%d")
        filename = f"TDI_{date_str}_Video{video_number}_{topic['title'][:30].replace(' ', '_').replace(':', '')}.txt"
        filepath = os.path.join(self.output_dir, filename)
        
        # Save script
        with open(filepath, 'w') as f:
            f.write(f"TRENDING DAILY INSIGHTS - {topic['title']}\n")
            f.write(f"Date: {datetime.now().strftime('%B %d, %Y')}\n\n")
            f.write(clean_script)
        
        # Create NotebookLM instructions
        instructions = f"""
        NOTEBOOKLM INSTRUCTIONS FOR: {topic['title']}
        
        1. Go to notebooklm.google.com
        2. Create new notebook
        3. Copy and paste the script below:
        
        {clean_script}
        
        4. Click "Generate audio overview"
        5. Wait 2-3 minutes
        6. Download the audio file
        7. Upload to YouTube with title: "{topic['title']}"
        
        YOUTUBE UPLOAD DETAILS:
        Title: {topic['title']}
        Description: Expert geopolitical analysis from Trending Daily Insights. Subscribe for daily insights on global events.
        Tags: {', '.join(topic['keywords'])}, geopolitics, analysis, trending daily insights
        """
        
        instructions_file = filepath.replace('.txt', '_INSTRUCTIONS.txt')
        with open(instructions_file, 'w') as f:
            f.write(instructions)
        
        return filepath, instructions_file
    
    def generate_daily_videos(self):
        """Generate today's videos - the core product"""
        
        print("🎬 TRENDING DAILY INSIGHTS - VIDEO GENERATOR")
        print("=" * 50)
        print("Generating today's videos...")
        print()
        
        # Get topics
        print("📋 Getting today's topics...")
        topics = self.get_daily_topics()
        
        generated_videos = []
        
        for i, topic in enumerate(topics, 1):
            print(f"\n🎥 Creating Video {i}: {topic['title']}")
            
            # Create script
            print("   ✍️  Writing script...")
            script = self.create_video_script(topic)
            
            # Save for NotebookLM
            print("   💾 Saving for NotebookLM...")
            script_file, instructions_file = self.save_script_for_notebooklm(script, topic, i)
            
            video_data = {
                "video_number": i,
                "title": topic['title'],
                "angle": topic['angle'],
                "keywords": topic['keywords'],
                "script_file": script_file,
                "instructions_file": instructions_file,
                "status": "ready_for_notebooklm"
            }
            
            generated_videos.append(video_data)
            print(f"   ✅ Video {i} ready!")
        
        # Save summary
        summary = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "total_videos": len(generated_videos),
            "videos": generated_videos,
            "next_steps": [
                "Open each INSTRUCTIONS file",
                "Follow NotebookLM steps for each video",
                "Upload generated audio to YouTube",
                "Repeat tomorrow for new videos"
            ]
        }
        
        summary_file = os.path.join(self.output_dir, f"Daily_Summary_{datetime.now().strftime('%Y%m%d')}.json")
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print("\n" + "=" * 50)
        print("🎉 TODAY'S VIDEOS GENERATED!")
        print("=" * 50)
        print(f"📁 Location: {self.output_dir}")
        print(f"📊 Videos Created: {len(generated_videos)}")
        print()
        print("🚀 NEXT STEPS:")
        print("1. Go to the daily_videos folder")
        print("2. Open each INSTRUCTIONS file")
        print("3. Follow the NotebookLM steps")
        print("4. Upload to YouTube")
        print("5. Run this script again tomorrow")
        print()
        print("📋 TODAY'S VIDEOS:")
        for video in generated_videos:
            print(f"   • {video['title']}")
        
        return generated_videos

def create_simple_daily_workflow():
    """Create the simplest possible daily workflow"""
    
    workflow_script = '''#!/bin/bash
# DAILY VIDEO WORKFLOW - Run this every morning

echo "🌅 Starting daily video generation..."

# Generate today's videos
python3 simple_video_generator.py

echo "✅ Videos generated!"
echo "📋 Next: Check daily_videos folder and follow instructions"
echo "🎬 Upload to YouTube when ready"
'''
    
    with open('/home/ubuntu/daily_workflow.sh', 'w') as f:
        f.write(workflow_script)
    
    os.chmod('/home/ubuntu/daily_workflow.sh', 0o755)
    print("✅ Daily workflow script created: daily_workflow.sh")

if __name__ == "__main__":
    generator = SimpleVideoGenerator()
    videos = generator.generate_daily_videos()
    create_simple_daily_workflow()
    
    print("\n🎯 CORE PRODUCT READY!")
    print("You can now generate videos daily with: ./daily_workflow.sh")

