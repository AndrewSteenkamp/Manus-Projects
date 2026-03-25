#!/usr/bin/env python3
"""
YouTube Upload Automation
This script automates the process of uploading videos to YouTube
with optimized titles, descriptions, and metadata.
"""

import os
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path

class YouTubeUploader:
    def __init__(self, channel_config: Dict[str, Any]):
        """
        Initialize the YouTube uploader
        
        Args:
            channel_config (Dict): Configuration for the YouTube channel
        """
        self.channel_config = channel_config
        self.niche = channel_config.get('niche', 'General')
        self.channel_name = channel_config.get('channel_name', 'Daily Insights')
        self.upload_schedule = channel_config.get('upload_schedule', '09:00')
        
    def generate_optimized_title(self, script_metadata: Dict[str, Any]) -> str:
        """
        Generate an SEO-optimized title for the video
        
        Args:
            script_metadata (Dict): Metadata from the script generation
            
        Returns:
            str: Optimized YouTube title
        """
        date_str = datetime.now().strftime('%B %d')
        niche = script_metadata.get('niche', self.niche)
        trending_count = len(script_metadata.get('trending_topics', []))
        
        # Title templates based on content
        title_templates = [
            f"🔥 {niche} News Today ({date_str}) - {trending_count} Major Updates You Can't Miss",
            f"Daily {niche} Briefing: {date_str} | Top {trending_count} Trends Explained",
            f"{niche} Insights {date_str}: What's Trending Now + Market Analysis",
            f"Breaking: {trending_count} {niche} Updates That Will Impact Your Strategy ({date_str})",
            f"Your Daily {niche} Edge - {date_str} | Industry News & Analysis"
        ]
        
        # Choose template based on trending topics
        if trending_count >= 5:
            title = title_templates[0]  # Emphasize multiple updates
        elif trending_count >= 3:
            title = title_templates[1]  # Standard briefing format
        else:
            title = title_templates[2]  # Focus on insights
        
        # Ensure title is under 100 characters for optimal display
        if len(title) > 100:
            title = title[:97] + "..."
        
        return title
    
    def generate_optimized_description(self, script_metadata: Dict[str, Any], script_content: str) -> str:
        """
        Generate an SEO-optimized description for the video
        
        Args:
            script_metadata (Dict): Metadata from the script generation
            script_content (str): The full script content
            
        Returns:
            str: Optimized YouTube description
        """
        niche = script_metadata.get('niche', self.niche)
        date_str = datetime.now().strftime('%B %d, %Y')
        trending_topics = script_metadata.get('trending_topics', [])
        
        description = f"""🎯 Your daily {niche} briefing for {date_str}

In today's episode, we break down the most important {niche} developments that could impact your success. Our team has analyzed hundreds of sources to bring you only what matters.

🔥 What's Covered Today:
"""
        
        # Add trending topics
        for i, topic in enumerate(trending_topics[:7], 1):
            description += f"{i}. {topic}\n"
        
        description += f"""
⏰ Timestamps:
00:00 - Introduction & Overview
01:30 - Top Story Analysis
03:45 - Market Implications
05:30 - Key Takeaways

💡 Why This Matters:
The {niche} landscape is evolving rapidly. These daily briefings help you stay ahead of trends, identify opportunities, and make informed decisions.

🔔 Never Miss an Update:
Subscribe and hit the notification bell for daily {niche} insights delivered every morning at {self.upload_schedule}.

📊 Sources & Research:
Our analysis is based on data from industry leaders, market reports, and trending discussions across multiple platforms.

🎯 For {niche} Professionals:
Whether you're a beginner or expert, these insights are designed to give you a competitive edge in the {niche} space.

---

#Daily{niche} #{niche}News #{niche}Insights #TrendingNow #MarketAnalysis #Industry{niche} #{niche}Updates #BusinessIntelligence

📧 Business Inquiries: contact@{self.channel_name.lower().replace(' ', '')}.com
🌐 Website: www.{self.channel_name.lower().replace(' ', '')}.com

Disclaimer: This content is for educational purposes only and should not be considered as professional advice. Always do your own research before making any decisions.
"""
        
        return description
    
    def generate_tags(self, script_metadata: Dict[str, Any]) -> List[str]:
        """
        Generate relevant tags for the video
        
        Args:
            script_metadata (Dict): Metadata from the script generation
            
        Returns:
            List[str]: List of relevant tags
        """
        niche = script_metadata.get('niche', self.niche)
        trending_topics = script_metadata.get('trending_topics', [])
        
        # Base tags
        tags = [
            niche.lower(),
            f"{niche.lower()} news",
            f"{niche.lower()} insights",
            f"daily {niche.lower()}",
            "trending",
            "analysis",
            "market update",
            "industry news",
            "business intelligence",
            "professional development"
        ]
        
        # Add trending topic tags
        for topic in trending_topics[:5]:
            tags.append(topic.lower())
            tags.append(f"{topic.lower()} {niche.lower()}")
        
        # Add date-based tags
        today = datetime.now()
        tags.extend([
            today.strftime("%B %Y").lower(),
            today.strftime("%Y").lower(),
            "latest news",
            "breaking news"
        ])
        
        # Remove duplicates and limit to 500 characters total
        unique_tags = list(dict.fromkeys(tags))
        
        # YouTube has a 500 character limit for tags
        final_tags = []
        char_count = 0
        for tag in unique_tags:
            if char_count + len(tag) + 1 <= 500:  # +1 for comma
                final_tags.append(tag)
                char_count += len(tag) + 1
            else:
                break
        
        return final_tags
    
    def create_thumbnail_suggestions(self, script_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create suggestions for thumbnail design
        
        Args:
            script_metadata (Dict): Metadata from the script generation
            
        Returns:
            Dict: Thumbnail design suggestions
        """
        niche = script_metadata.get('niche', self.niche)
        trending_count = len(script_metadata.get('trending_topics', []))
        
        suggestions = {
            "main_text": f"{trending_count} {niche.upper()} UPDATES",
            "subtitle": datetime.now().strftime('%B %d'),
            "color_scheme": {
                "AI": {"primary": "#FF6B35", "secondary": "#004E89", "accent": "#FFFFFF"},
                "crypto": {"primary": "#F7931A", "secondary": "#000000", "accent": "#FFFFFF"},
                "business": {"primary": "#1E3A8A", "secondary": "#FFFFFF", "accent": "#EF4444"},
                "tech": {"primary": "#10B981", "secondary": "#1F2937", "accent": "#FFFFFF"}
            }.get(niche, {"primary": "#3B82F6", "secondary": "#1F2937", "accent": "#FFFFFF"}),
            "elements": [
                "Trending arrow icon",
                "Clock/time icon for 'daily'",
                "Professional headshot or avatar",
                "Background: subtle pattern or gradient"
            ],
            "text_style": "Bold, sans-serif font (Impact or Montserrat)",
            "dimensions": "1280x720 pixels",
            "file_format": "PNG or JPG"
        }
        
        return suggestions
    
    def schedule_upload(self, video_path: str, script_metadata: Dict[str, Any], upload_time: str = None) -> Dict[str, Any]:
        """
        Prepare upload configuration for scheduled publishing
        
        Args:
            video_path (str): Path to the video file
            script_metadata (Dict): Metadata from the script generation
            upload_time (str): Time to schedule upload (HH:MM format)
            
        Returns:
            Dict: Upload configuration
        """
        if not upload_time:
            upload_time = self.upload_schedule
        
        # Calculate next upload time
        now = datetime.now()
        upload_hour, upload_minute = map(int, upload_time.split(':'))
        
        next_upload = now.replace(hour=upload_hour, minute=upload_minute, second=0, microsecond=0)
        if next_upload <= now:
            next_upload += timedelta(days=1)
        
        upload_config = {
            "video_path": video_path,
            "title": self.generate_optimized_title(script_metadata),
            "description": self.generate_optimized_description(script_metadata, ""),
            "tags": self.generate_tags(script_metadata),
            "category_id": "25",  # News & Politics
            "privacy_status": "public",
            "scheduled_publish_time": next_upload.isoformat(),
            "thumbnail_suggestions": self.create_thumbnail_suggestions(script_metadata),
            "end_screen_config": {
                "subscribe_button": True,
                "related_videos": 2,
                "playlist_promotion": True
            },
            "cards": [
                {
                    "type": "video",
                    "time": 30,
                    "message": "Watch yesterday's briefing"
                },
                {
                    "type": "playlist",
                    "time": 180,
                    "message": f"More {script_metadata.get('niche', self.niche)} insights"
                }
            ]
        }
        
        return upload_config
    
    def create_upload_instructions(self, upload_config: Dict[str, Any]) -> str:
        """
        Create step-by-step upload instructions
        
        Args:
            upload_config (Dict): Upload configuration
            
        Returns:
            str: Detailed upload instructions
        """
        instructions = f"""# YouTube Upload Instructions

## Video Information
- **File**: {upload_config['video_path']}
- **Scheduled Time**: {upload_config['scheduled_publish_time']}
- **Category**: News & Politics

## Step-by-Step Upload Process:

### 1. Upload Video
1. Go to YouTube Studio (studio.youtube.com)
2. Click "CREATE" → "Upload videos"
3. Select video file: `{upload_config['video_path']}`
4. Wait for upload to complete

### 2. Video Details
**Title** (copy exactly):
```
{upload_config['title']}
```

**Description** (copy exactly):
```
{upload_config['description']}
```

### 3. Thumbnail
- Upload custom thumbnail using these specifications:
  - **Main Text**: {upload_config['thumbnail_suggestions']['main_text']}
  - **Subtitle**: {upload_config['thumbnail_suggestions']['subtitle']}
  - **Colors**: {upload_config['thumbnail_suggestions']['color_scheme']}
  - **Dimensions**: {upload_config['thumbnail_suggestions']['dimensions']}

### 4. Audience & Visibility
- **Audience**: Not made for kids
- **Visibility**: {upload_config['privacy_status'].title()}
- **Schedule**: {upload_config['scheduled_publish_time']}

### 5. Tags
Add these tags (comma-separated):
```
{', '.join(upload_config['tags'])}
```

### 6. End Screen & Cards
- **End Screen**: Add subscribe button and 2 related videos
- **Cards**: 
  - Card 1 (30s): Link to previous day's video
  - Card 2 (3m): Link to channel playlist

### 7. Final Steps
1. Review all information
2. Click "SCHEDULE" (not "PUBLISH")
3. Confirm scheduled time
4. Save as draft if needed

## Post-Upload Checklist:
- [ ] Video scheduled successfully
- [ ] Thumbnail uploaded and looks good
- [ ] Title and description are complete
- [ ] Tags are added
- [ ] End screen configured
- [ ] Cards added
- [ ] Scheduled for correct time

## Analytics to Monitor:
- Click-through rate (aim for >10%)
- Average view duration (aim for >50%)
- Subscriber growth
- Engagement rate (likes, comments, shares)
"""
        
        return instructions
    
    def save_upload_package(self, upload_config: Dict[str, Any], output_dir: str = None) -> str:
        """
        Save the complete upload package
        
        Args:
            upload_config (Dict): Upload configuration
            output_dir (str): Output directory
            
        Returns:
            str: Path to the upload package directory
        """
        if not output_dir:
            output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'uploads')
        
        # Create timestamped directory
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        package_dir = os.path.join(output_dir, f"upload_{timestamp}")
        os.makedirs(package_dir, exist_ok=True)
        
        # Save upload configuration
        config_file = os.path.join(package_dir, "upload_config.json")
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(upload_config, f, indent=2, default=str)
        
        # Save upload instructions
        instructions = self.create_upload_instructions(upload_config)
        instructions_file = os.path.join(package_dir, "upload_instructions.md")
        with open(instructions_file, 'w', encoding='utf-8') as f:
            f.write(instructions)
        
        # Save thumbnail specifications
        thumbnail_specs = json.dumps(upload_config['thumbnail_suggestions'], indent=2)
        thumbnail_file = os.path.join(package_dir, "thumbnail_specs.json")
        with open(thumbnail_file, 'w', encoding='utf-8') as f:
            f.write(thumbnail_specs)
        
        print(f"✅ Upload package saved to: {package_dir}")
        return package_dir

def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='YouTube Upload Automation')
    parser.add_argument('--video', required=True, help='Path to video file')
    parser.add_argument('--metadata', required=True, help='Path to script metadata JSON')
    parser.add_argument('--config', required=True, help='Path to channel configuration JSON')
    
    args = parser.parse_args()
    
    # Load configurations
    with open(args.config, 'r') as f:
        channel_config = json.load(f)
    
    with open(args.metadata, 'r') as f:
        script_metadata = json.load(f)
    
    # Create uploader and process
    uploader = YouTubeUploader(channel_config)
    upload_config = uploader.schedule_upload(args.video, script_metadata)
    package_path = uploader.save_upload_package(upload_config)
    
    print(f"Upload package created at: {package_path}")

if __name__ == "__main__":
    main()

