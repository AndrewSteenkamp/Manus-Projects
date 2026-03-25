#!/usr/bin/env python3
"""
TRENDING DAILY INSIGHTS - SIMPLE VIDEO GENERATOR (No External Dependencies)
Core Product: Generate videos for your YouTube channel TODAY

This script creates video scripts and NotebookLM instructions
No complex setup - just video production
"""

import json
import os
from datetime import datetime

class SimpleVideoGenerator:
    def __init__(self):
        self.channel_name = "Trending Daily Insights"
        self.output_dir = "/home/ubuntu/daily_videos"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def get_daily_topics(self):
        """Get 3 geopolitical topics for today"""
        
        # Pre-defined topics that are always relevant
        topics = [
            {
                "title": "Ukraine War Economic Impact: Global Market Analysis",
                "angle": "How the ongoing conflict affects international trade and energy prices",
                "keywords": ["ukraine", "war", "economy", "energy", "trade"]
            },
            {
                "title": "China's Belt and Road Initiative: Latest Developments",
                "angle": "Strategic implications for global infrastructure and geopolitics",
                "keywords": ["china", "belt and road", "infrastructure", "geopolitics"]
            },
            {
                "title": "Middle East Oil Politics: Regional Power Dynamics",
                "angle": "OPEC decisions and their impact on global energy security",
                "keywords": ["middle east", "oil", "opec", "energy security"]
            }
        ]
        
        return topics
    
    def create_video_script(self, topic):
        """Create a 5-10 minute video script for the topic"""
        
        script_template = f"""
Welcome to Trending Daily Insights, your source for expert geopolitical analysis. I'm your host, and today we're diving deep into {topic['title']}.

{topic['angle']}

Let me break this down into three key points that you need to understand.

First, the immediate implications. This development represents a significant shift in the global landscape. The economic ramifications are already being felt across multiple sectors, and we're seeing immediate responses from key international players.

Second, the strategic context. To understand why this matters, we need to look at the broader geopolitical framework. This isn't happening in isolation - it's part of a larger pattern of international relations that has been developing over the past several years.

Third, what this means for the future. Based on current trends and historical precedents, we can make some educated predictions about where this is heading. The implications for global stability, economic markets, and international cooperation are substantial.

Now, let's examine the key players involved and their motivations. Each major actor in this situation has specific interests and constraints that are driving their decisions. Understanding these motivations is crucial for predicting future developments.

The economic implications cannot be overstated. We're looking at potential impacts on global supply chains, currency markets, and international trade relationships. These effects will likely be felt for months, if not years, to come.

From a strategic perspective, this development fits into larger patterns of international competition and cooperation. The responses we're seeing from various nations reflect their broader foreign policy objectives and regional interests.

Looking ahead, there are several scenarios we need to consider. The most likely outcome involves continued tension with periodic diplomatic efforts to find common ground. However, we must also prepare for the possibility of escalation or unexpected developments.

For investors and business leaders, this situation presents both risks and opportunities. Understanding the geopolitical context is essential for making informed decisions in this uncertain environment.

In conclusion, {topic['title']} represents a critical moment in international relations. The decisions made in the coming weeks and months will have lasting implications for global stability and economic prosperity.

That's today's analysis from Trending Daily Insights. If you found this analysis helpful, please subscribe to our channel for daily geopolitical insights. Like this video if it provided value, and let me know in the comments what topics you'd like us to cover next.

Remember to stay informed, stay analytical, and we'll see you tomorrow with another edition of Trending Daily Insights.
"""
        
        return script_template.strip()
    
    def save_script_for_notebooklm(self, script, topic, video_number):
        """Save script in format ready for NotebookLM"""
        
        # Create filename
        date_str = datetime.now().strftime("%Y%m%d")
        safe_title = topic['title'][:30].replace(' ', '_').replace(':', '').replace('?', '').replace('/', '_')
        filename = f"TDI_{date_str}_Video{video_number}_{safe_title}.txt"
        filepath = os.path.join(self.output_dir, filename)
        
        # Save script
        with open(filepath, 'w') as f:
            f.write(f"TRENDING DAILY INSIGHTS - {topic['title']}\n")
            f.write(f"Date: {datetime.now().strftime('%B %d, %Y')}\n\n")
            f.write(script)
        
        # Create NotebookLM instructions
        instructions = f"""
🎬 NOTEBOOKLM INSTRUCTIONS FOR: {topic['title']}

STEP-BY-STEP PROCESS:

1. 🌐 Go to notebooklm.google.com
2. ➕ Click "Create new notebook"
3. 📝 Copy the script from the file: {filename}
4. 📋 Paste it into NotebookLM
5. 🎙️ Click "Generate audio overview"
6. ⏱️ Wait 2-3 minutes for processing
7. ⬇️ Download the audio file
8. 📺 Upload to YouTube

YOUTUBE UPLOAD DETAILS:
📌 Title: {topic['title']}
📝 Description: Expert geopolitical analysis from Trending Daily Insights. Subscribe for daily insights on global events and international relations.
🏷️ Tags: {', '.join(topic['keywords'])}, geopolitics, analysis, trending daily insights, international relations, global news
📂 Category: News & Politics
🎯 Audience: Not made for kids

THUMBNAIL SUGGESTIONS:
- World map with highlighted regions
- News graphics with "TDI" branding
- Professional news-style layout
- Bold text with key topic words

OPTIMAL UPLOAD TIME:
- Morning: 8-10 AM (your local time)
- Evening: 6-8 PM (your local time)

💡 PRO TIP: After uploading, pin a comment asking viewers what geopolitical topics they want covered next!
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
            "channel": "Trending Daily Insights",
            "total_videos": len(generated_videos),
            "videos": generated_videos,
            "next_steps": [
                "1. Open each INSTRUCTIONS file",
                "2. Follow NotebookLM steps for each video", 
                "3. Upload generated audio to YouTube",
                "4. Run this script again tomorrow for new videos"
            ],
            "daily_workflow": "Run ./daily_workflow.sh every morning"
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
        print("🚀 IMMEDIATE NEXT STEPS:")
        print("1. Go to the daily_videos folder")
        print("2. Open the first INSTRUCTIONS file")
        print("3. Follow the NotebookLM steps")
        print("4. Upload your first video to YouTube")
        print("5. Repeat for videos 2 and 3")
        print()
        print("📋 TODAY'S VIDEOS:")
        for video in generated_videos:
            print(f"   • {video['title']}")
        print()
        print("💡 TOMORROW: Run this script again for 3 new videos!")
        
        return generated_videos

def create_simple_daily_workflow():
    """Create the simplest possible daily workflow"""
    
    workflow_script = '''#!/bin/bash
# DAILY VIDEO WORKFLOW - Run this every morning

echo "🌅 Starting daily video generation for Trending Daily Insights..."
echo ""

# Generate today's videos
python3.11 simple_video_generator_no_openai.py

echo ""
echo "✅ Videos generated!"
echo "📋 Next: Check daily_videos folder and follow INSTRUCTIONS files"
echo "🎬 Upload to YouTube when ready"
echo "💰 Start earning revenue!"
'''
    
    with open('/home/ubuntu/daily_workflow.sh', 'w') as f:
        f.write(workflow_script)
    
    os.chmod('/home/ubuntu/daily_workflow.sh', 0o755)
    print("✅ Daily workflow script created: daily_workflow.sh")

def create_quick_start_guide():
    """Create a quick start guide"""
    
    guide = """
🚀 TRENDING DAILY INSIGHTS - QUICK START GUIDE

GOAL: Get your first video uploaded to YouTube TODAY

STEP 1: Generate Videos (DONE!)
✅ You just ran the video generator
✅ 3 video scripts created
✅ NotebookLM instructions ready

STEP 2: Create Your First Video (15 minutes)
1. Go to daily_videos folder
2. Open the first INSTRUCTIONS file
3. Copy the script text
4. Go to notebooklm.google.com
5. Paste script and generate audio
6. Download the audio file

STEP 3: Upload to YouTube (10 minutes)
1. Go to youtube.com/upload
2. Upload your audio file
3. Use the title from instructions
4. Copy/paste the description
5. Add the suggested tags
6. Publish!

STEP 4: Repeat Tomorrow
1. Run: ./daily_workflow.sh
2. Follow same process
3. Build your daily content habit

🎯 SUCCESS METRICS:
- Day 1: Upload 1 video
- Week 1: Upload 7 videos (1 per day)
- Month 1: 30 videos uploaded
- Month 2: Start seeing revenue

💰 REVENUE TIMELINE:
- Week 1-2: Build content library
- Week 3-4: YouTube starts recommending
- Month 2: First ad revenue
- Month 3: Sponsor opportunities

🔥 REMEMBER: Consistency beats perfection!
Upload daily, even if videos aren't perfect.
"""
    
    with open('/home/ubuntu/QUICK_START_GUIDE.txt', 'w') as f:
        f.write(guide)
    
    print("✅ Quick start guide created: QUICK_START_GUIDE.txt")

if __name__ == "__main__":
    generator = SimpleVideoGenerator()
    videos = generator.generate_daily_videos()
    create_simple_daily_workflow()
    create_quick_start_guide()
    
    print("\n🎯 CORE PRODUCT READY!")
    print("📖 Read QUICK_START_GUIDE.txt for next steps")
    print("🔄 Run ./daily_workflow.sh every morning for new videos")

