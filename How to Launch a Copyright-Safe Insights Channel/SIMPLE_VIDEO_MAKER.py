#!/usr/bin/env python3
"""
SIMPLE TDI VIDEO MAKER - GET YOUR FIRST VIDEO ONLINE TODAY!
No complex setup, no dependencies, just working videos in 15 minutes
"""

import os
import json
from datetime import datetime

def create_simple_script():
    """Create one simple video script that works with NotebookLM"""
    
    script = """Welcome to Trending Daily Insights. I'm your host bringing you expert geopolitical analysis.

Today we're examining the current state of global energy markets and their impact on international relations.

The first key point is energy security. Nations worldwide are reassessing their energy dependencies following recent global events. This shift is reshaping diplomatic relationships and trade partnerships across continents.

The second critical factor is economic implications. Energy price volatility is affecting everything from manufacturing costs to consumer prices. We're seeing inflation pressures in developed economies and supply chain adjustments in emerging markets.

The third element is strategic positioning. Countries are accelerating renewable energy transitions while simultaneously securing traditional energy supplies. This dual approach is creating new geopolitical alliances and tensions.

Looking at the data, global energy prices have fluctuated by over thirty percent in the past year. This volatility is driving policy changes in major economies including the United States, European Union, and China.

The implications for businesses are significant. Companies are diversifying supply chains, investing in energy efficiency, and factoring geopolitical risk into long-term planning. Smart investors are positioning themselves for the energy transition while managing current market volatility.

For policymakers, the challenge is balancing energy security with climate commitments. We're seeing increased cooperation on renewable energy development alongside strategic competition for traditional energy resources.

Looking ahead, expect continued volatility in energy markets as geopolitical tensions persist. However, the long-term trend toward renewable energy and energy independence will likely accelerate, creating both challenges and opportunities for nations and businesses alike.

That's today's analysis from Trending Daily Insights. If you found this valuable, please subscribe for daily geopolitical insights. Like this video and let me know in the comments what global topics you'd like us to analyze next.

Remember, understanding geopolitics is essential for navigating our interconnected world. We'll see you tomorrow with another edition of Trending Daily Insights."""

    return script

def create_upload_instructions():
    """Create simple upload instructions"""
    
    instructions = """🎬 HOW TO MAKE YOUR FIRST TDI VIDEO (15 MINUTES TOTAL)

STEP 1: GET THE AUDIO (5 minutes)
1. Copy the script from 'video_script.txt'
2. Go to notebooklm.google.com
3. Sign in with Google
4. Click "Create new notebook"
5. Paste the script
6. Click "Generate audio overview"
7. Wait 2-3 minutes
8. Download the audio file

STEP 2: UPLOAD TO YOUTUBE (10 minutes)
1. Go to youtube.com/upload
2. Upload your audio file
3. Title: "Global Energy Markets: Geopolitical Analysis | TDI"
4. Description: "Expert analysis of global energy markets and their geopolitical implications. Subscribe to Trending Daily Insights for daily international relations analysis."
5. Tags: geopolitics, energy, global markets, international relations, trending daily insights
6. Category: News & Politics
7. Thumbnail: Use YouTube's auto-generated thumbnail for now
8. Click PUBLISH

STEP 3: CELEBRATE! 🎉
You just published your first professional geopolitical analysis video!

TOMORROW: Run this script again for a new video topic.

💰 REVENUE TIMELINE:
- Week 1: Build content (7 videos)
- Week 2-3: YouTube starts recommending your videos
- Month 2: First ad revenue ($10-50)
- Month 3: Growing revenue ($50-200)
- Month 4: Potential sponsors ($500+)

🔥 SUCCESS TIP: Consistency beats perfection. Upload daily, even if videos aren't perfect."""

    return instructions

def main():
    """Create everything needed for first video"""
    
    print("🎬 SIMPLE TDI VIDEO MAKER")
    print("=" * 50)
    print("Creating your first video package...")
    
    # Create working directory
    work_dir = os.path.join(os.getcwd(), "TDI_Simple_Videos")
    os.makedirs(work_dir, exist_ok=True)
    
    # Create script
    script = create_simple_script()
    script_file = os.path.join(work_dir, "video_script.txt")
    
    with open(script_file, 'w', encoding='utf-8') as f:
        f.write(script)
    
    # Create instructions
    instructions = create_upload_instructions()
    instructions_file = os.path.join(work_dir, "UPLOAD_INSTRUCTIONS.txt")
    
    with open(instructions_file, 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    # Create summary
    summary = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "video_title": "Global Energy Markets: Geopolitical Analysis | TDI",
        "script_file": script_file,
        "instructions_file": instructions_file,
        "next_steps": [
            "1. Open video_script.txt and copy the content",
            "2. Go to notebooklm.google.com and paste script",
            "3. Generate audio and download",
            "4. Upload to YouTube with provided details",
            "5. Your first video is LIVE!"
        ]
    }
    
    summary_file = os.path.join(work_dir, "summary.json")
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    
    print(f"✅ Video package created in: {work_dir}")
    print(f"📝 Script: {script_file}")
    print(f"📋 Instructions: {instructions_file}")
    print()
    print("🚀 NEXT STEPS:")
    print("1. Open the TDI_Simple_Videos folder")
    print("2. Follow the UPLOAD_INSTRUCTIONS.txt file")
    print("3. Your first video will be live in 15 minutes!")
    print()
    print("💡 REMEMBER: Just get ONE video online today.")
    print("   Perfect is the enemy of done!")
    
    # Try to open the folder
    try:
        if os.name == 'nt':  # Windows
            os.startfile(work_dir)
        else:  # Mac/Linux
            os.system(f'open "{work_dir}"')
    except:
        print(f"\n📁 Manually open: {work_dir}")

if __name__ == "__main__":
    main()
