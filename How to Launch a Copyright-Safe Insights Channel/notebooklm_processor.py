#!/usr/bin/env python3
"""
NotebookLM Content Processor
This script automates the process of converting research reports into
video scripts and managing NotebookLM workflows.
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
import requests
from pathlib import Path

class NotebookLMProcessor:
    def __init__(self, api_key: str = None):
        """
        Initialize the NotebookLM processor
        
        Args:
            api_key (str): API key for NotebookLM (if available)
        """
        self.api_key = api_key or os.getenv('NOTEBOOKLM_API_KEY')
        self.base_url = "https://notebooklm.google.com/api/v1"  # Hypothetical API endpoint
        
    def create_video_script(self, research_report: str, niche: str, target_length: int = 300) -> Dict[str, Any]:
        """
        Convert a research report into a video script
        
        Args:
            research_report (str): The daily research report content
            niche (str): The niche/topic
            target_length (int): Target script length in words
            
        Returns:
            Dict containing the script and metadata
        """
        print("📝 Creating video script from research report...")
        
        # Extract key information from the research report
        lines = research_report.split('\n')
        trending_topics = []
        top_stories = []
        
        in_trending = False
        in_stories = False
        
        for line in lines:
            if "🔥 Trending Topics" in line:
                in_trending = True
                in_stories = False
                continue
            elif "📈 Top Stories" in line:
                in_trending = False
                in_stories = True
                continue
            elif line.startswith("###") or line.startswith("---"):
                in_trending = False
                in_stories = False
                continue
                
            if in_trending and line.strip().startswith("- "):
                trending_topics.append(line.strip()[2:])
            elif in_stories and line.strip().startswith("#### "):
                story_title = line.strip()[5:].split('.', 1)[-1].strip()
                top_stories.append(story_title)
        
        # Generate script structure
        script_data = {
            "title": f"Daily {niche} Insights - {datetime.now().strftime('%B %d, %Y')}",
            "intro": self._generate_intro(niche, trending_topics),
            "main_content": self._generate_main_content(top_stories[:5], niche),
            "outro": self._generate_outro(niche),
            "metadata": {
                "niche": niche,
                "date": datetime.now().strftime('%Y-%m-%d'),
                "trending_topics": trending_topics,
                "story_count": len(top_stories),
                "estimated_duration": "5-7 minutes"
            }
        }
        
        # Combine into full script
        full_script = f"{script_data['intro']}\n\n{script_data['main_content']}\n\n{script_data['outro']}"
        script_data['full_script'] = full_script
        script_data['word_count'] = len(full_script.split())
        
        return script_data
    
    def _generate_intro(self, niche: str, trending_topics: List[str]) -> str:
        """Generate an engaging intro for the video"""
        date_str = datetime.now().strftime('%B %d, %Y')
        
        intro = f"""Welcome to your daily {niche} insights for {date_str}. I'm here to cut through the noise and bring you the most important developments that matter to your success.

Today we're covering {len(trending_topics)} major trends that are shaping the {niche} landscape right now."""
        
        if trending_topics:
            intro += f" We'll dive deep into {', '.join(trending_topics[:3])}"
            if len(trending_topics) > 3:
                intro += f" and {len(trending_topics) - 3} other key developments"
            intro += "."
        
        intro += f"\n\nLet's jump right in because these insights could change how you approach {niche} this week."
        
        return intro
    
    def _generate_main_content(self, stories: List[str], niche: str) -> str:
        """Generate the main content section"""
        content = ""
        
        for i, story in enumerate(stories, 1):
            content += f"""
## Story {i}: {story}

This development is significant because it represents a shift in how {niche} professionals are approaching their strategies. Here's what you need to know:

The key takeaway is that this trend is accelerating, and early adopters are already seeing results. If you're in the {niche} space, this is something you can't afford to ignore.

What this means for you: Consider how this development might impact your current approach and whether there are opportunities to adapt your strategy accordingly."""
            
            if i < len(stories):
                content += "\n\n---\n"
        
        return content
    
    def _generate_outro(self, niche: str) -> str:
        """Generate a compelling outro with call to action"""
        outro = f"""That wraps up today's {niche} insights. These developments are moving fast, and staying informed is your competitive advantage.

If you found this valuable, make sure to subscribe and hit the notification bell so you never miss a daily briefing. Tomorrow, we'll be covering the latest developments in {niche}, including some exclusive insights you won't find anywhere else.

What story from today resonated most with you? Drop a comment below and let me know your thoughts.

Until tomorrow, stay ahead of the curve."""
        
        return outro
    
    def optimize_for_notebooklm(self, script: str) -> str:
        """
        Optimize the script for NotebookLM video generation
        
        Args:
            script (str): The raw script content
            
        Returns:
            str: Optimized script for NotebookLM
        """
        print("🔧 Optimizing script for NotebookLM...")
        
        # Add clear section breaks for slide generation
        optimized = script.replace("## Story", "\n[SLIDE BREAK]\n\n## Story")
        
        # Add timing cues
        optimized = optimized.replace("Let's jump right in", "[PAUSE] Let's jump right in")
        optimized = optimized.replace("Here's what you need to know:", "[PAUSE] Here's what you need to know:")
        optimized = optimized.replace("What this means for you:", "[EMPHASIS] What this means for you:")
        
        # Add visual cues for NotebookLM
        optimized = f"[TITLE SLIDE]\n{optimized}"
        optimized += "\n\n[END SLIDE]"
        
        return optimized
    
    def create_notebooklm_instructions(self, script_data: Dict[str, Any]) -> str:
        """
        Create instructions for using the script with NotebookLM
        
        Args:
            script_data (Dict): The script data with metadata
            
        Returns:
            str: Instructions for NotebookLM usage
        """
        instructions = f"""# NotebookLM Video Generation Instructions

## Script Information
- **Title**: {script_data['title']}
- **Niche**: {script_data['metadata']['niche']}
- **Date**: {script_data['metadata']['date']}
- **Estimated Duration**: {script_data['metadata']['estimated_duration']}
- **Word Count**: {script_data['word_count']} words

## Steps to Generate Video in NotebookLM:

1. **Create New Notebook**
   - Go to notebooklm.google.com
   - Click "Create new notebook"
   - Name it: "{script_data['title']}"

2. **Add Script as Source**
   - Click "Add source"
   - Select "Copy and paste text"
   - Paste the optimized script below

3. **Generate Video Overview**
   - Click on "Video overview" in the notebook
   - Wait for processing (usually 2-5 minutes)
   - Review the generated video

4. **Download and Customize**
   - Download the video file
   - Add custom branding if needed
   - Upload to YouTube with optimized title and description

## Optimized Script for NotebookLM:

{script_data['full_script']}

## Suggested YouTube Optimization:

**Title**: {script_data['title']} | Top {len(script_data['metadata']['trending_topics'])} Trends You Need to Know

**Description**: 
Today's {script_data['metadata']['niche']} briefing covers the most important developments in the industry. We analyze {len(script_data['metadata']['trending_topics'])} trending topics and break down what they mean for your success.

🔥 Trending Topics Covered:
{chr(10).join([f"• {topic}" for topic in script_data['metadata']['trending_topics'][:5]])}

**Tags**: {script_data['metadata']['niche']}, daily news, industry insights, trending, analysis, {', '.join(script_data['metadata']['trending_topics'][:3])}
"""
        
        return instructions
    
    def save_script_package(self, script_data: Dict[str, Any], output_dir: str = None) -> str:
        """
        Save the complete script package to files
        
        Args:
            script_data (Dict): The script data
            output_dir (str): Output directory path
            
        Returns:
            str: Path to the saved package directory
        """
        if not output_dir:
            output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts')
        
        # Create timestamped directory
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        niche = script_data['metadata']['niche']
        package_dir = os.path.join(output_dir, f"{niche}_{timestamp}")
        os.makedirs(package_dir, exist_ok=True)
        
        # Save script file
        script_file = os.path.join(package_dir, "script.txt")
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script_data['full_script'])
        
        # Save optimized script
        optimized_script = self.optimize_for_notebooklm(script_data['full_script'])
        optimized_file = os.path.join(package_dir, "script_optimized.txt")
        with open(optimized_file, 'w', encoding='utf-8') as f:
            f.write(optimized_script)
        
        # Save instructions
        instructions = self.create_notebooklm_instructions(script_data)
        instructions_file = os.path.join(package_dir, "notebooklm_instructions.md")
        with open(instructions_file, 'w', encoding='utf-8') as f:
            f.write(instructions)
        
        # Save metadata
        metadata_file = os.path.join(package_dir, "metadata.json")
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(script_data['metadata'], f, indent=2)
        
        print(f"✅ Script package saved to: {package_dir}")
        return package_dir
    
    def process_research_report(self, report_path: str, niche: str) -> str:
        """
        Complete workflow: process research report into NotebookLM-ready package
        
        Args:
            report_path (str): Path to the research report file
            niche (str): The niche/topic
            
        Returns:
            str: Path to the generated script package
        """
        print(f"🔄 Processing research report: {report_path}")
        
        # Read the research report
        with open(report_path, 'r', encoding='utf-8') as f:
            research_content = f.read()
        
        # Generate script
        script_data = self.create_video_script(research_content, niche)
        
        # Save complete package
        package_path = self.save_script_package(script_data)
        
        print("✅ Research report processed successfully!")
        return package_path

def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='NotebookLM Content Processor')
    parser.add_argument('--report', required=True, help='Path to research report file')
    parser.add_argument('--niche', required=True, help='The niche/topic')
    
    args = parser.parse_args()
    
    processor = NotebookLMProcessor()
    package_path = processor.process_research_report(args.report, args.niche)
    
    print(f"Script package created at: {package_path}")

if __name__ == "__main__":
    main()

