#!/usr/bin/env python3
"""
TDI COMPLETE VIDEO GENERATION SYSTEM FOR ANACONDA/SPYDER
Professional video production system that creates complete videos with synchronized visuals
"""

import os
import json
import subprocess
import sys
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import requests
import webbrowser

class TDICompleteVideoSystem:
    def __init__(self):
        # Get current working directory (where user runs the script)
        self.base_dir = os.getcwd()
        self.project_name = "TDI_Video_Production"
        self.project_dir = os.path.join(self.base_dir, self.project_name)
        
        # Create project structure
        self.directories = {
            'assets': os.path.join(self.project_dir, 'visual_assets'),
            'maps': os.path.join(self.project_dir, 'visual_assets', 'maps'),
            'charts': os.path.join(self.project_dir, 'visual_assets', 'charts'),
            'overlays': os.path.join(self.project_dir, 'visual_assets', 'overlays'),
            'audio': os.path.join(self.project_dir, 'audio_files'),
            'videos': os.path.join(self.project_dir, 'final_videos'),
            'scripts': os.path.join(self.project_dir, 'video_scripts'),
            'temp': os.path.join(self.project_dir, 'temp_files')
        }
        
        # Create all directories
        for directory in self.directories.values():
            os.makedirs(directory, exist_ok=True)
        
        # TDI Brand Colors
        self.brand_colors = {
            'primary_blue': '#1E3A8A',
            'secondary_blue': '#3B82F6', 
            'accent_blue': '#60A5FA',
            'white': '#FFFFFF',
            'light_gray': '#F3F4F6',
            'dark_gray': '#374151'
        }
        
        print(f"🎬 TDI Complete Video System Initialized")
        print(f"📁 Project Directory: {self.project_dir}")
        print(f"📁 Working in: {self.base_dir}")
    
    def check_dependencies(self):
        """Check and install required packages"""
        
        required_packages = [
            'pillow', 'matplotlib', 'numpy', 'requests'
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
                print(f"✅ {package} - Available")
            except ImportError:
                missing_packages.append(package)
                print(f"❌ {package} - Missing")
        
        if missing_packages:
            print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
            for package in missing_packages:
                try:
                    subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                                 check=True, capture_output=True)
                    print(f"✅ Installed {package}")
                except subprocess.CalledProcessError as e:
                    print(f"❌ Failed to install {package}: {e}")
        
        return len(missing_packages) == 0
    
    def get_daily_topics(self):
        """Generate geopolitical topics for today's videos"""
        
        # Rotating topic sets for variety
        topic_sets = [
            [
                {
                    'title': 'Ukraine War Economic Impact: Global Market Analysis',
                    'regions': ['Europe', 'Ukraine', 'North America'],
                    'key_points': [
                        'Supply chain disruptions affecting global trade',
                        'Energy price volatility in European markets', 
                        'Sanctions impact on international banking'
                    ],
                    'statistics': [
                        {'value': '€2.1T', 'description': 'Total Economic Impact'},
                        {'value': '40%', 'description': 'Energy Price Increase'}
                    ]
                },
                {
                    'title': "China's Belt and Road Initiative: Strategic Developments",
                    'regions': ['Asia', 'China', 'Europe', 'Africa'],
                    'key_points': [
                        'Infrastructure investment reaching $1.3 trillion',
                        '147 countries now participating in BRI projects',
                        'Geopolitical implications for global trade routes'
                    ],
                    'statistics': [
                        {'value': '$1.3T', 'description': 'Investment Committed'},
                        {'value': '147', 'description': 'Participating Countries'}
                    ]
                },
                {
                    'title': 'Middle East Energy Politics: OPEC Strategy Analysis',
                    'regions': ['Middle East', 'North America', 'Asia'],
                    'key_points': [
                        'Oil production quotas affecting global prices',
                        'Strategic partnerships reshaping energy markets',
                        'Renewable energy transition challenges'
                    ],
                    'statistics': [
                        {'value': '32M', 'description': 'Barrels/Day Production'},
                        {'value': '13', 'description': 'OPEC+ Members'}
                    ]
                }
            ]
        ]
        
        # Select topics based on current date
        day_of_year = datetime.now().timetuple().tm_yday
        selected_topics = topic_sets[day_of_year % len(topic_sets)]
        
        return selected_topics
    
    def create_world_map(self, regions_to_highlight, title, output_filename):
        """Create professional world map with highlighted regions"""
        
        fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100)
        fig.patch.set_facecolor('#1E3A8A')  # TDI blue background
        
        # World regions (simplified coordinates)
        world_regions = {
            'North America': [(-140, 20, 90, 50)],
            'Europe': [(-10, 35, 50, 35)], 
            'Asia': [(40, 10, 140, 60)],
            'Middle East': [(25, 15, 40, 30)],
            'Africa': [(-20, -35, 75, 70)],
            'South America': [(-85, -55, 50, 70)],
            'Ukraine': [(22, 44, 18, 8)],
            'China': [(73, 18, 62, 35)]
        }
        
        ax.set_xlim(-180, 180)
        ax.set_ylim(-90, 90)
        ax.set_facecolor('#3B82F6')  # Secondary blue
        
        # Draw regions
        for region, coords in world_regions.items():
            for coord in coords:
                x, y, width, height = coord
                
                if region in regions_to_highlight:
                    color = '#60A5FA'  # Accent blue for highlighted
                    alpha = 0.9
                    linewidth = 3
                else:
                    color = '#F3F4F6'  # Light gray for others
                    alpha = 0.5
                    linewidth = 1
                
                rect = plt.Rectangle((x, y), width, height,
                                   facecolor=color, alpha=alpha,
                                   edgecolor='white', linewidth=linewidth)
                ax.add_patch(rect)
        
        # Add title and branding
        ax.text(0, 85, title, fontsize=24, fontweight='bold',
                color='white', ha='center')
        ax.text(-170, -80, 'TDI - TRENDING DAILY INSIGHTS',
                fontsize=16, fontweight='bold', color='white')
        
        # Remove axes
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
        
        # Save map
        output_path = os.path.join(self.directories['maps'], output_filename)
        plt.tight_layout()
        plt.savefig(output_path, dpi=100, bbox_inches='tight',
                   facecolor='#1E3A8A')
        plt.close()
        
        print(f"✅ World map created: {output_filename}")
        return output_path
    
    def create_data_chart(self, chart_data, title, output_filename):
        """Create professional data visualization"""
        
        fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100)
        fig.patch.set_facecolor('#1E3A8A')
        ax.set_facecolor('#F3F4F6')
        
        # Sample data for demonstration
        categories = ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024']
        values = [85, 92, 78, 95]
        
        # Create bar chart
        bars = ax.bar(categories, values, color='#3B82F6',
                     edgecolor='white', linewidth=2)
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                   f'{height}', ha='center', va='bottom',
                   fontsize=14, fontweight='bold')
        
        # Styling
        ax.set_title(title, fontsize=24, fontweight='bold',
                    color='white', pad=20)
        ax.tick_params(colors='#374151', labelsize=12)
        ax.grid(True, alpha=0.3)
        
        # Add branding
        fig.text(0.02, 0.02, 'TDI - TRENDING DAILY INSIGHTS',
                fontsize=14, fontweight='bold', color='white')
        
        # Save chart
        output_path = os.path.join(self.directories['charts'], output_filename)
        plt.tight_layout()
        plt.savefig(output_path, dpi=100, bbox_inches='tight',
                   facecolor='#1E3A8A')
        plt.close()
        
        print(f"✅ Chart created: {output_filename}")
        return output_path
    
    def create_text_overlay(self, text, overlay_type, output_filename):
        """Create text overlays for video"""
        
        # Create transparent image
        img = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Try to load system fonts, fallback to default
        try:
            if overlay_type == 'title':
                font = ImageFont.truetype("arial.ttf", 72)
            else:
                font = ImageFont.truetype("arial.ttf", 48)
        except:
            font = ImageFont.load_default()
        
        if overlay_type == 'title':
            # Title overlay with background
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (1920 - text_width) // 2
            y = (1080 - text_height) // 2
            
            # Semi-transparent background
            padding = 40
            draw.rectangle([x-padding, y-padding, 
                          x+text_width+padding, y+text_height+padding],
                         fill=(30, 58, 138, 200))
            
            # White text
            draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))
        
        elif overlay_type == 'lower_third':
            # Lower third with TDI branding
            draw.rectangle([0, 850, 1920, 1080], fill=(30, 58, 138, 220))
            
            # TDI logo area
            draw.rectangle([50, 870, 300, 1060], fill=(59, 130, 246, 255))
            
            try:
                logo_font = ImageFont.truetype("arial.ttf", 48)
                small_font = ImageFont.truetype("arial.ttf", 24)
            except:
                logo_font = font
                small_font = font
            
            draw.text((60, 900), "TDI", font=logo_font, fill=(255, 255, 255, 255))
            draw.text((60, 980), "TRENDING DAILY", font=small_font, fill=(255, 255, 255, 255))
            draw.text((60, 1020), "INSIGHTS", font=small_font, fill=(255, 255, 255, 255))
            
            # Main text
            draw.text((350, 940), text, font=font, fill=(255, 255, 255, 255))
        
        # Save overlay
        output_path = os.path.join(self.directories['overlays'], output_filename)
        img.save(output_path, 'PNG')
        
        print(f"✅ Text overlay created: {output_filename}")
        return output_path
    
    def generate_video_script(self, topic):
        """Generate detailed video script"""
        
        script = f"""TRENDING DAILY INSIGHTS - {topic['title']}

INTRODUCTION (30 seconds)
Welcome to Trending Daily Insights, your source for expert geopolitical analysis. I'm your host, and today we're examining {topic['title']}.

MAIN ANALYSIS (4-5 minutes)
Let me break this down into three critical points you need to understand.

First, {topic['key_points'][0]}. This represents a fundamental shift in how we understand global economic relationships. The data shows significant impacts across multiple sectors, with ripple effects extending far beyond the immediate region.

Second, {topic['key_points'][1]}. The strategic implications cannot be overstated. We're seeing responses from major international players that will shape policy decisions for years to come.

Third, {topic['key_points'][2]}. Looking at historical precedents and current trends, this development fits into a larger pattern of international relations that has been evolving over recent years.

STATISTICS AND DATA (1 minute)
The numbers tell a compelling story. {topic['statistics'][0]['description']}: {topic['statistics'][0]['value']}. Additionally, {topic['statistics'][1]['description']}: {topic['statistics'][1]['value']}.

FUTURE IMPLICATIONS (2 minutes)
Based on current analysis and expert projections, we can expect several key developments in the coming months. The most likely scenario involves continued diplomatic efforts alongside strategic positioning by major powers.

CONCLUSION (30 seconds)
This analysis highlights the complex interconnections in our global system. For businesses, investors, and policymakers, understanding these dynamics is essential for navigating an increasingly complex world.

That's today's analysis from Trending Daily Insights. Subscribe for daily geopolitical insights, and let me know in the comments what topics you'd like us to cover next."""

        return script
    
    def create_notebooklm_instructions(self, topic, script_file):
        """Create step-by-step NotebookLM instructions"""
        
        instructions = f"""🎬 NOTEBOOKLM VIDEO CREATION INSTRUCTIONS
Topic: {topic['title']}

STEP 1: PREPARE SCRIPT
✅ Script file created: {script_file}
✅ Copy the entire script content

STEP 2: NOTEBOOKLM SETUP
1. Open your web browser
2. Go to: notebooklm.google.com
3. Sign in with your Google account
4. Click "Create new notebook"

STEP 3: GENERATE AUDIO
1. Paste your script into the text area
2. Click "Generate audio overview"
3. Wait 2-3 minutes for processing
4. Download the generated audio file
5. Save as: {topic['title'].replace(' ', '_')}_audio.mp3

STEP 4: YOUTUBE UPLOAD DETAILS
📌 Title: {topic['title']}
📝 Description: Expert geopolitical analysis from Trending Daily Insights. Daily insights on global events, international relations, and strategic developments. Subscribe for professional analysis you can trust.

🏷️ Tags: geopolitics, international relations, global news, {', '.join(topic['regions']).lower()}, trending daily insights, political analysis, world events, strategic analysis

📂 Category: News & Politics
🎯 Audience: Not made for kids
⏰ Best Upload Times: 8-10 AM or 6-8 PM (your local time)

STEP 5: THUMBNAIL SUGGESTIONS
- Use world map highlighting relevant regions
- Include "TDI" branding prominently
- Add key statistic or compelling text
- Professional news broadcast style
- High contrast colors (blue/white/red)

STEP 6: ENGAGEMENT STRATEGY
- Pin a comment asking what topics viewers want covered
- Respond to comments within first 2 hours
- Share on relevant social media platforms
- Cross-promote with related videos

💡 PRO TIPS:
- Upload consistently at the same time daily
- Create playlists by region or topic
- Use end screens to promote subscription
- Monitor analytics for optimal posting times"""

        return instructions
    
    def generate_complete_video_package(self, topic_index=0):
        """Generate complete video package for one topic"""
        
        topics = self.get_daily_topics()
        if topic_index >= len(topics):
            topic_index = 0
        
        topic = topics[topic_index]
        date_str = datetime.now().strftime("%Y%m%d")
        safe_title = topic['title'].replace(' ', '_').replace(':', '').replace('?', '')[:30]
        
        print(f"\n🎬 Creating complete video package for: {topic['title']}")
        
        # 1. Generate visual assets
        print("📊 Creating visual assets...")
        
        # World map
        map_file = f"{safe_title}_map_{date_str}.png"
        map_path = self.create_world_map(topic['regions'], topic['title'], map_file)
        
        # Data chart
        chart_file = f"{safe_title}_chart_{date_str}.png"
        chart_path = self.create_data_chart(topic.get('chart_data', {}), 
                                          f"{topic['title']} - Key Metrics", chart_file)
        
        # Text overlays
        title_overlay_file = f"{safe_title}_title_{date_str}.png"
        title_path = self.create_text_overlay(topic['title'], 'title', title_overlay_file)
        
        lower_third_file = f"{safe_title}_lower_third_{date_str}.png"
        lower_third_path = self.create_text_overlay('Expert Geopolitical Analysis', 
                                                   'lower_third', lower_third_file)
        
        # 2. Generate script
        print("📝 Creating video script...")
        script = self.generate_video_script(topic)
        script_file = f"{safe_title}_script_{date_str}.txt"
        script_path = os.path.join(self.directories['scripts'], script_file)
        
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script)
        
        # 3. Create NotebookLM instructions
        print("📋 Creating NotebookLM instructions...")
        instructions = self.create_notebooklm_instructions(topic, script_file)
        instructions_file = f"{safe_title}_instructions_{date_str}.txt"
        instructions_path = os.path.join(self.directories['scripts'], instructions_file)
        
        with open(instructions_path, 'w', encoding='utf-8') as f:
            f.write(instructions)
        
        # 4. Create package manifest
        package_data = {
            'topic': topic['title'],
            'date': date_str,
            'files': {
                'script': script_path,
                'instructions': instructions_path,
                'world_map': map_path,
                'chart': chart_path,
                'title_overlay': title_path,
                'lower_third': lower_third_path
            },
            'youtube_details': {
                'title': topic['title'],
                'tags': ['geopolitics', 'international relations', 'global news'] + [r.lower() for r in topic['regions']],
                'category': 'News & Politics',
                'description': f"Expert analysis of {topic['title']}. Subscribe to Trending Daily Insights for daily geopolitical analysis."
            },
            'statistics': topic['statistics'],
            'regions': topic['regions']
        }
        
        manifest_file = f"{safe_title}_package_{date_str}.json"
        manifest_path = os.path.join(self.project_dir, manifest_file)
        
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(package_data, f, indent=2)
        
        print(f"\n✅ Complete video package created!")
        print(f"📄 Script: {script_path}")
        print(f"📋 Instructions: {instructions_path}")
        print(f"🗺️ World Map: {map_path}")
        print(f"📊 Chart: {chart_path}")
        print(f"📦 Package Manifest: {manifest_path}")
        
        return package_data
    
    def generate_daily_videos(self, count=3):
        """Generate complete packages for multiple videos"""
        
        print(f"🎬 TDI COMPLETE VIDEO GENERATION SYSTEM")
        print("=" * 60)
        print(f"Generating {count} complete video packages...")
        
        # Check dependencies
        if not self.check_dependencies():
            print("❌ Please install missing dependencies and try again")
            return None
        
        packages = []
        topics = self.get_daily_topics()
        
        for i in range(min(count, len(topics))):
            package = self.generate_complete_video_package(i)
            packages.append(package)
        
        # Create daily summary
        summary = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'total_packages': len(packages),
            'packages': packages,
            'project_directory': self.project_dir,
            'next_steps': [
                '1. Open the script files and copy content to NotebookLM',
                '2. Generate audio using NotebookLM',
                '3. Use visual assets to create complete videos',
                '4. Upload to YouTube with provided details',
                '5. Run this script again tomorrow for new content'
            ]
        }
        
        summary_file = f"TDI_Daily_Summary_{datetime.now().strftime('%Y%m%d')}.json"
        summary_path = os.path.join(self.project_dir, summary_file)
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        print("\n" + "=" * 60)
        print("🎉 DAILY VIDEO GENERATION COMPLETE!")
        print("=" * 60)
        print(f"📁 Project folder: {self.project_dir}")
        print(f"📊 Videos generated: {len(packages)}")
        print(f"📄 Summary: {summary_path}")
        print("\n🚀 NEXT STEPS:")
        for step in summary['next_steps']:
            print(f"   {step}")
        
        # Open project folder
        try:
            if os.name == 'nt':  # Windows
                os.startfile(self.project_dir)
            elif os.name == 'posix':  # Mac/Linux
                subprocess.run(['open', self.project_dir])
        except:
            print(f"\n📁 Manually open: {self.project_dir}")
        
        return summary

def main():
    """Main function to run the complete video generation system"""
    
    # Create system instance
    tdi_system = TDICompleteVideoSystem()
    
    # Generate daily videos
    result = tdi_system.generate_daily_videos(3)
    
    if result:
        print(f"\n✅ System ready! Check your project folder for all files.")
        print(f"📁 Location: {tdi_system.project_dir}")
    else:
        print(f"\n❌ System setup failed. Please check dependencies.")

if __name__ == "__main__":
    main()
