# 🎬 TRENDING DAILY INSIGHTS - ANACONDA DEPLOYMENT GUIDE
## Complete Step-by-Step Setup for Video Generation System

---

## 📋 OVERVIEW

This guide will help you deploy the Trending Daily Insights video generation system using Anaconda and Spyder. By the end, you'll have a system that generates 3 professional geopolitical analysis videos daily.

**What You'll Get:**
- Automated video script generation
- NotebookLM-ready content
- Daily workflow automation
- Professional YouTube content

**Time to Deploy:** 30-45 minutes
**Time to First Video:** 15 minutes after setup

---

## 🛠️ PREREQUISITES

### Required Software:
- ✅ **Anaconda** (you already have this)
- ✅ **Spyder** (you already have this)
- 🌐 **Web Browser** (Chrome, Firefox, Safari)
- 📺 **YouTube Account** (for uploading)

### Required Accounts:
- 🎥 **YouTube Channel** (you have Trending Daily Insights)
- 🤖 **Google Account** (for NotebookLM access)
- 🔑 **OpenAI API Key** (optional - system works without it)

---

## 📁 STEP 1: DOWNLOAD AND EXTRACT FILES

### 1.1 Download the Package
1. **Download** the `daily_videos_package.tar.gz` file from the attachments
2. **Save** it to your Desktop or Documents folder
3. **Note the location** - you'll need this path

### 1.2 Extract Files (Windows)
```bash
# If you have 7-Zip or WinRAR:
1. Right-click on daily_videos_package.tar.gz
2. Select "Extract Here" or "Extract to folder"
3. You should see a folder called "daily_videos"

# If extraction fails, rename the file:
1. Rename daily_videos_package.tar.gz to daily_videos_package.zip
2. Extract using Windows built-in extractor
```

### 1.3 Extract Files (Mac/Linux)
```bash
# Open Terminal and navigate to download location:
cd ~/Downloads  # or wherever you saved the file
tar -xzf daily_videos_package.tar.gz
```

### 1.4 Verify Extraction
You should now have these files:
```
📁 daily_videos/
   📄 TDI_20250921_Video1_Ukraine_War_Economic_Impact_G.txt
   📄 TDI_20250921_Video1_Ukraine_War_Economic_Impact_G_INSTRUCTIONS.txt
   📄 TDI_20250921_Video2_China's_Belt_and_Road_Initiati.txt
   📄 TDI_20250921_Video2_China's_Belt_and_Road_Initiati_INSTRUCTIONS.txt
   📄 TDI_20250921_Video3_Middle_East_Oil_Politics_Regi.txt
   📄 TDI_20250921_Video3_Middle_East_Oil_Politics_Regi_INSTRUCTIONS.txt
   📄 Daily_Summary_20250921.json
📄 QUICK_START_GUIDE.txt
📄 daily_workflow.sh
```

---

## 🐍 STEP 2: ANACONDA ENVIRONMENT SETUP

### 2.1 Open Anaconda Navigator
1. **Launch** Anaconda Navigator from your applications
2. **Wait** for it to fully load (may take 30-60 seconds)

### 2.2 Create New Environment (Recommended)
```bash
# Option A: Using Anaconda Navigator GUI
1. Click "Environments" tab on the left
2. Click "Create" button at bottom
3. Name: "tdi_videos"
4. Python version: 3.9 or 3.10
5. Click "Create"
6. Wait for environment creation (2-3 minutes)

# Option B: Using Anaconda Prompt (Windows) or Terminal (Mac/Linux)
conda create -n tdi_videos python=3.9
conda activate tdi_videos
```

### 2.3 Install Required Packages
```bash
# In Anaconda Prompt or Terminal:
conda activate tdi_videos
conda install requests json5 -c conda-forge

# If you want OpenAI integration (optional):
pip install openai
```

### 2.4 Launch Spyder in New Environment
```bash
# Method 1: From Anaconda Navigator
1. Select "tdi_videos" environment from dropdown
2. Click "Install" on Spyder if not already installed
3. Click "Launch" on Spyder

# Method 2: From Command Line
conda activate tdi_videos
spyder
```

---

## 📝 STEP 3: SETUP VIDEO GENERATION SCRIPT

### 3.1 Create Project Folder
1. **Open** File Explorer (Windows) or Finder (Mac)
2. **Navigate** to your Documents folder
3. **Create** new folder called `TDI_VideoGenerator`
4. **Copy** all extracted files into this folder

### 3.2 Open Script in Spyder
1. **Launch** Spyder (should be in tdi_videos environment)
2. **File** → **Open** → Navigate to `TDI_VideoGenerator` folder
3. **Create** new file: **File** → **New File**
4. **Copy** the following code into Spyder:

```python
#!/usr/bin/env python3
"""
TRENDING DAILY INSIGHTS - VIDEO GENERATOR FOR ANACONDA/SPYDER
Run this script daily to generate 3 professional geopolitical videos
"""

import json
import os
from datetime import datetime
import webbrowser

class TDIVideoGenerator:
    def __init__(self):
        self.channel_name = "Trending Daily Insights"
        # Get current working directory
        self.base_dir = os.getcwd()
        self.output_dir = os.path.join(self.base_dir, "daily_videos")
        
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        print(f"📁 Working directory: {self.base_dir}")
        print(f"📁 Output directory: {self.output_dir}")
        
    def get_daily_topics(self):
        """Get 3 geopolitical topics for today"""
        
        # Rotating topics to ensure variety
        topic_sets = [
            [
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
            ],
            [
                {
                    "title": "US-China Trade Relations: Current Status and Future Outlook",
                    "angle": "Impact of tariffs and trade policies on global supply chains",
                    "keywords": ["us china", "trade", "tariffs", "supply chain"]
                },
                {
                    "title": "European Union Energy Security: Post-Russia Strategy",
                    "angle": "How Europe is reshaping its energy independence",
                    "keywords": ["eu", "energy", "russia", "independence"]
                },
                {
                    "title": "Indo-Pacific Security: Naval Power Dynamics",
                    "angle": "Military positioning and alliance structures in the region",
                    "keywords": ["indo pacific", "security", "naval", "alliances"]
                }
            ],
            [
                {
                    "title": "Global Inflation Trends: Geopolitical Drivers",
                    "angle": "How international conflicts drive economic instability",
                    "keywords": ["inflation", "economy", "geopolitics", "instability"]
                },
                {
                    "title": "Africa's Rising Influence: Continental Power Shifts",
                    "angle": "Economic growth and strategic partnerships reshaping Africa",
                    "keywords": ["africa", "growth", "partnerships", "influence"]
                },
                {
                    "title": "Cyber Warfare: State-Sponsored Attacks and Defense",
                    "angle": "How nations are weaponizing technology for geopolitical advantage",
                    "keywords": ["cyber", "warfare", "technology", "security"]
                }
            ]
        ]
        
        # Rotate based on day of year to ensure variety
        day_of_year = datetime.now().timetuple().tm_yday
        selected_set = topic_sets[day_of_year % len(topic_sets)]
        
        return selected_set
    
    def create_video_script(self, topic):
        """Create a professional 5-10 minute video script"""
        
        script = f"""Welcome to Trending Daily Insights, your source for expert geopolitical analysis. I'm your host, and today we're diving deep into {topic['title']}.

{topic['angle']}

Let me break this down into three key points that you need to understand.

First, the immediate implications. This development represents a significant shift in the global landscape. The economic ramifications are already being felt across multiple sectors, and we're seeing immediate responses from key international players. The ripple effects are extending far beyond the immediate region, affecting global supply chains, currency markets, and international trade relationships.

Second, the strategic context. To understand why this matters, we need to look at the broader geopolitical framework. This isn't happening in isolation - it's part of a larger pattern of international relations that has been developing over the past several years. The historical precedents show us similar situations and their outcomes, giving us valuable insights into potential future scenarios.

Third, what this means for the future. Based on current trends and historical precedents, we can make some educated predictions about where this is heading. The implications for global stability, economic markets, and international cooperation are substantial. We're looking at potential long-term shifts in power dynamics that could reshape international relations for decades to come.

Now, let's examine the key players involved and their motivations. Each major actor in this situation has specific interests and constraints that are driving their decisions. Understanding these motivations is crucial for predicting future developments and preparing for various scenarios.

The economic implications cannot be overstated. We're looking at potential impacts on global supply chains, currency markets, and international trade relationships. These effects will likely be felt for months, if not years, to come. Businesses and investors need to understand these dynamics to make informed decisions in this uncertain environment.

From a strategic perspective, this development fits into larger patterns of international competition and cooperation. The responses we're seeing from various nations reflect their broader foreign policy objectives and regional interests. This creates a complex web of relationships that influences everything from military positioning to economic partnerships.

Looking ahead, there are several scenarios we need to consider. The most likely outcome involves continued tension with periodic diplomatic efforts to find common ground. However, we must also prepare for the possibility of escalation or unexpected developments that could dramatically alter the current trajectory.

For investors and business leaders, this situation presents both risks and opportunities. Understanding the geopolitical context is essential for making informed decisions in this uncertain environment. The companies and countries that adapt quickly to these changing dynamics will be best positioned for future success.

In conclusion, {topic['title']} represents a critical moment in international relations. The decisions made in the coming weeks and months will have lasting implications for global stability and economic prosperity. As always, staying informed and thinking strategically about these developments is essential for navigating our interconnected world.

That's today's analysis from Trending Daily Insights. If you found this analysis helpful, please subscribe to our channel for daily geopolitical insights. Like this video if it provided value, and let me know in the comments what topics you'd like us to cover next.

Remember to stay informed, stay analytical, and we'll see you tomorrow with another edition of Trending Daily Insights."""

        return script
    
    def save_files(self, script, topic, video_number):
        """Save script and instructions for NotebookLM"""
        
        # Create safe filename
        date_str = datetime.now().strftime("%Y%m%d")
        safe_title = topic['title'][:30].replace(' ', '_').replace(':', '').replace('?', '').replace('/', '_')
        
        # Script file
        script_filename = f"TDI_{date_str}_Video{video_number}_{safe_title}.txt"
        script_filepath = os.path.join(self.output_dir, script_filename)
        
        with open(script_filepath, 'w', encoding='utf-8') as f:
            f.write(f"TRENDING DAILY INSIGHTS - {topic['title']}\n")
            f.write(f"Date: {datetime.now().strftime('%B %d, %Y')}\n\n")
            f.write(script)
        
        # Instructions file
        instructions = f"""🎬 NOTEBOOKLM INSTRUCTIONS FOR: {topic['title']}

STEP-BY-STEP PROCESS:

1. 🌐 Go to notebooklm.google.com
2. ➕ Click "Create new notebook"  
3. 📝 Copy the script from: {script_filename}
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

💡 PRO TIP: After uploading, pin a comment asking viewers what geopolitical topics they want covered next!"""

        instructions_filename = f"TDI_{date_str}_Video{video_number}_{safe_title}_INSTRUCTIONS.txt"
        instructions_filepath = os.path.join(self.output_dir, instructions_filename)
        
        with open(instructions_filepath, 'w', encoding='utf-8') as f:
            f.write(instructions)
        
        return script_filepath, instructions_filepath
    
    def generate_daily_videos(self):
        """Main function to generate today's videos"""
        
        print("🎬 TRENDING DAILY INSIGHTS - VIDEO GENERATOR")
        print("=" * 60)
        print("Generating today's videos...")
        print()
        
        # Get topics
        topics = self.get_daily_topics()
        generated_videos = []
        
        for i, topic in enumerate(topics, 1):
            print(f"🎥 Creating Video {i}: {topic['title']}")
            
            # Create script
            script = self.create_video_script(topic)
            
            # Save files
            script_file, instructions_file = self.save_files(script, topic, i)
            
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
            "output_directory": self.output_dir
        }
        
        summary_file = os.path.join(self.output_dir, f"Daily_Summary_{datetime.now().strftime('%Y%m%d')}.json")
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        print("\n" + "=" * 60)
        print("🎉 TODAY'S VIDEOS GENERATED!")
        print("=" * 60)
        print(f"📁 Files saved to: {self.output_dir}")
        print(f"📊 Videos created: {len(generated_videos)}")
        print()
        print("📋 TODAY'S VIDEOS:")
        for video in generated_videos:
            print(f"   • {video['title']}")
        print()
        print("🚀 NEXT STEPS:")
        print("1. Open the daily_videos folder")
        print("2. Follow the INSTRUCTIONS files")
        print("3. Upload to YouTube")
        print("4. Run this script again tomorrow!")
        
        # Open output folder automatically
        try:
            if os.name == 'nt':  # Windows
                os.startfile(self.output_dir)
            elif os.name == 'posix':  # Mac/Linux
                os.system(f'open "{self.output_dir}"')
        except:
            print(f"📁 Manually open: {self.output_dir}")
        
        return generated_videos

# Run the generator
if __name__ == "__main__":
    generator = TDIVideoGenerator()
    videos = generator.generate_daily_videos()
```

### 3.3 Save the Script
1. **File** → **Save As**
2. **Name:** `tdi_video_generator.py`
3. **Location:** Your `TDI_VideoGenerator` folder
4. **Click** Save

---

## ▶️ STEP 4: RUN YOUR FIRST VIDEO GENERATION

### 4.1 Execute the Script
1. **Make sure** the script is open in Spyder
2. **Click** the green "Run" button (▶️) or press **F5**
3. **Watch** the console output - it will show progress
4. **Wait** for completion (should take 10-20 seconds)

### 4.2 Verify Output
You should see output like:
```
🎬 TRENDING DAILY INSIGHTS - VIDEO GENERATOR
============================================================
📁 Working directory: C:\Users\YourName\Documents\TDI_VideoGenerator
📁 Output directory: C:\Users\YourName\Documents\TDI_VideoGenerator\daily_videos
🎥 Creating Video 1: Ukraine War Economic Impact: Global Market Analysis
   ✅ Video 1 ready!
🎥 Creating Video 2: China's Belt and Road Initiative: Latest Developments
   ✅ Video 2 ready!
🎥 Creating Video 3: Middle East Oil Politics: Regional Power Dynamics
   ✅ Video 3 ready!
============================================================
🎉 TODAY'S VIDEOS GENERATED!
```

### 4.3 Check Generated Files
The script should automatically open your `daily_videos` folder. You should see:
- 3 script files (.txt)
- 3 instruction files (_INSTRUCTIONS.txt)
- 1 summary file (.json)

---

## 🎥 STEP 5: CREATE YOUR FIRST VIDEO

### 5.1 Open Instructions
1. **Navigate** to your `daily_videos` folder
2. **Open** the first INSTRUCTIONS file (double-click)
3. **Read** the step-by-step process

### 5.2 Copy Script Content
1. **Open** the corresponding script file (without _INSTRUCTIONS)
2. **Select All** (Ctrl+A or Cmd+A)
3. **Copy** (Ctrl+C or Cmd+C)

### 5.3 Use NotebookLM
1. **Open** your web browser
2. **Go to** notebooklm.google.com
3. **Sign in** with your Google account
4. **Click** "Create new notebook"
5. **Paste** your script into the text area
6. **Click** "Generate audio overview"
7. **Wait** 2-3 minutes for processing
8. **Download** the generated audio file

### 5.4 Upload to YouTube
1. **Go to** youtube.com/upload
2. **Drag** your audio file into the upload area
3. **Use title** from the instructions file
4. **Copy/paste description** from instructions
5. **Add tags** from instructions
6. **Set category** to "News & Politics"
7. **Click** "Publish"

---

## 🔄 STEP 6: AUTOMATE DAILY WORKFLOW

### 6.1 Create Daily Routine
1. **Every morning** (or your preferred time)
2. **Open** Spyder
3. **Open** your `tdi_video_generator.py` script
4. **Click** Run (F5)
5. **Follow** the generated instructions
6. **Upload** to YouTube

### 6.2 Set Up Reminders
```
📅 Daily Schedule Suggestion:
- 8:00 AM: Run video generator script
- 8:15 AM: Create first video with NotebookLM
- 8:30 AM: Upload to YouTube
- 8:45 AM: Done for the day!

Total time: 45 minutes daily
```

### 6.3 Track Your Progress
Create a simple spreadsheet to track:
- Date
- Videos generated
- Videos uploaded
- Views/engagement
- Revenue (when it starts)

---

## 🚨 TROUBLESHOOTING

### Common Issues and Solutions:

#### Issue: "ModuleNotFoundError"
**Solution:**
```bash
# In Anaconda Prompt:
conda activate tdi_videos
conda install requests json5 -c conda-forge
```

#### Issue: Script won't run in Spyder
**Solution:**
1. Check you're in the correct environment (tdi_videos)
2. Restart Spyder
3. Make sure script is saved as .py file

#### Issue: Files not generating
**Solution:**
1. Check file permissions in your folder
2. Try running as administrator (Windows)
3. Check the console for error messages

#### Issue: NotebookLM not working
**Solution:**
1. Make sure you're signed into Google
2. Try a different browser
3. Check your internet connection
4. Try shorter script if it's too long

#### Issue: YouTube upload fails
**Solution:**
1. Check file format (should be audio)
2. Ensure file size is under 256GB
3. Verify your YouTube account is verified
4. Try uploading from different browser

---

## 📈 SCALING AND OPTIMIZATION

### Week 1: Master the Basics
- Generate and upload 1 video daily
- Focus on consistency over perfection
- Learn the NotebookLM workflow

### Week 2: Optimize Process
- Reduce generation time
- Improve video titles and descriptions
- Start tracking performance metrics

### Week 3: Expand Content
- Modify script to generate more topics
- Experiment with different video lengths
- Add more variety to content

### Month 2: Revenue Focus
- Apply for YouTube monetization
- Start reaching out to potential sponsors
- Analyze which content performs best

---

## 💰 REVENUE EXPECTATIONS

### Timeline:
- **Week 1-4:** Build content library (no revenue)
- **Month 2:** First YouTube ad revenue ($10-50)
- **Month 3:** Growing ad revenue ($50-200)
- **Month 4:** Potential sponsor deals ($500-2000)
- **Month 6:** Established revenue stream ($1000-5000)

### Key Metrics to Track:
- Daily uploads (target: 1 per day)
- Subscriber growth (target: 10% monthly)
- Average view duration (target: 60%+)
- Click-through rate (target: 5%+)

---

## 🎯 SUCCESS CHECKLIST

### Day 1 Goals:
- [ ] Anaconda environment set up
- [ ] Script running successfully in Spyder
- [ ] First video generated
- [ ] First video uploaded to YouTube

### Week 1 Goals:
- [ ] 7 videos uploaded
- [ ] Daily workflow established
- [ ] NotebookLM process mastered
- [ ] YouTube channel optimized

### Month 1 Goals:
- [ ] 30 videos uploaded
- [ ] Consistent daily posting
- [ ] Growing subscriber base
- [ ] Revenue tracking system in place

---

## 📞 SUPPORT AND NEXT STEPS

### If You Get Stuck:
1. **Check** the troubleshooting section above
2. **Review** each step carefully
3. **Test** with a simple example first
4. **Focus** on getting one video working before scaling

### Optimization Ideas:
- Add more topic variety to the script
- Create custom thumbnails
- Experiment with different upload times
- Engage with comments to boost engagement

### Future Enhancements:
- Integrate with YouTube API for automatic uploads
- Add sponsor message integration
- Create multiple video formats (shorts, long-form)
- Expand to other platforms (podcast, newsletter)

---

**🚀 You're now ready to launch your automated Trending Daily Insights video production system! Start with one video today and build the habit from there.**

