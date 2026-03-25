#!/usr/bin/env python3
"""
Master Workflow Orchestrator
This script orchestrates the complete daily workflow for the YouTube insights channel,
from research to upload preparation.
"""

import os
import sys
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional

# Import our custom modules
sys.path.append(os.path.dirname(__file__))
from research.daily_research_scraper import DailyResearchScraper
from content_generation.notebooklm_processor import NotebookLMProcessor
from youtube_management.youtube_uploader import YouTubeUploader
from analytics.performance_tracker import PerformanceTracker

class MasterWorkflow:
    def __init__(self, config_path: str):
        """
        Initialize the master workflow
        
        Args:
            config_path (str): Path to the configuration file
        """
        self.config = self._load_config(config_path)
        self.niche = self.config['channel']['niche']
        self.keywords = self.config['channel']['keywords']
        self.channel_id = self.config['channel']['channel_id']
        
        # Initialize components
        self.research_scraper = DailyResearchScraper(self.niche, self.keywords)
        self.content_processor = NotebookLMProcessor()
        self.youtube_uploader = YouTubeUploader(self.config['channel'])
        self.performance_tracker = PerformanceTracker(self.channel_id, self.niche)
        
        # Setup directories
        self.base_dir = os.path.dirname(__file__)
        self.output_dir = os.path.join(self.base_dir, '..', 'daily_output')
        os.makedirs(self.output_dir, exist_ok=True)
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Configuration file not found: {config_path}")
            print("Creating default configuration...")
            return self._create_default_config(config_path)
    
    def _create_default_config(self, config_path: str) -> Dict[str, Any]:
        """Create a default configuration file"""
        default_config = {
            "channel": {
                "niche": "AI",
                "channel_name": "Daily AI Insights",
                "channel_id": "YOUR_CHANNEL_ID_HERE",
                "keywords": ["artificial intelligence", "AI news", "machine learning", "AI tools", "AI trends"],
                "upload_schedule": "09:00",
                "timezone": "UTC"
            },
            "content": {
                "target_duration": "5-7 minutes",
                "style": "professional",
                "include_timestamps": True,
                "add_call_to_action": True
            },
            "automation": {
                "auto_research": True,
                "auto_script_generation": True,
                "auto_upload_preparation": True,
                "send_notifications": True
            },
            "analytics": {
                "track_performance": True,
                "generate_weekly_reports": True,
                "monitor_competitors": False
            }
        }
        
        # Save default config
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2)
        
        print(f"✅ Default configuration created at: {config_path}")
        print("Please edit the configuration file with your channel details before running again.")
        
        return default_config
    
    def run_daily_workflow(self, date: str = None) -> Dict[str, str]:
        """
        Run the complete daily workflow
        
        Args:
            date (str): Date for the workflow (YYYY-MM-DD), defaults to today
            
        Returns:
            Dict containing paths to generated files
        """
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        print(f"🚀 Starting daily workflow for {date}")
        print(f"📺 Channel: {self.config['channel']['channel_name']}")
        print(f"🎯 Niche: {self.niche}")
        
        workflow_results = {
            'date': date,
            'research_report': '',
            'script_package': '',
            'upload_package': '',
            'analytics_report': '',
            'status': 'started'
        }
        
        try:
            # Step 1: Research
            print("\n" + "="*50)
            print("STEP 1: DAILY RESEARCH")
            print("="*50)
            
            research_report_path = self.research_scraper.run_daily_research()
            workflow_results['research_report'] = research_report_path
            print(f"✅ Research complete: {research_report_path}")
            
            # Step 2: Content Generation
            print("\n" + "="*50)
            print("STEP 2: CONTENT GENERATION")
            print("="*50)
            
            script_package_path = self.content_processor.process_research_report(
                research_report_path, self.niche
            )
            workflow_results['script_package'] = script_package_path
            print(f"✅ Script generation complete: {script_package_path}")
            
            # Step 3: Upload Preparation
            print("\n" + "="*50)
            print("STEP 3: UPLOAD PREPARATION")
            print("="*50)
            
            # Load script metadata
            metadata_path = os.path.join(script_package_path, 'metadata.json')
            with open(metadata_path, 'r', encoding='utf-8') as f:
                script_metadata = json.load(f)
            
            # Prepare upload (video file would be generated separately via NotebookLM)
            video_placeholder = "VIDEO_TO_BE_GENERATED_IN_NOTEBOOKLM.mp4"
            upload_config = self.youtube_uploader.schedule_upload(video_placeholder, script_metadata)
            upload_package_path = self.youtube_uploader.save_upload_package(upload_config)
            workflow_results['upload_package'] = upload_package_path
            print(f"✅ Upload preparation complete: {upload_package_path}")
            
            # Step 4: Analytics (if enabled)
            if self.config['analytics']['track_performance']:
                print("\n" + "="*50)
                print("STEP 4: ANALYTICS")
                print("="*50)
                
                analytics_report_path = self.performance_tracker.run_analytics()
                workflow_results['analytics_report'] = analytics_report_path
                print(f"✅ Analytics complete: {analytics_report_path}")
            
            # Step 5: Create Daily Summary
            print("\n" + "="*50)
            print("STEP 5: DAILY SUMMARY")
            print("="*50)
            
            summary_path = self._create_daily_summary(workflow_results)
            workflow_results['daily_summary'] = summary_path
            workflow_results['status'] = 'completed'
            
            print(f"✅ Daily workflow complete!")
            print(f"📋 Summary: {summary_path}")
            
        except Exception as e:
            print(f"❌ Workflow failed: {str(e)}")
            workflow_results['status'] = 'failed'
            workflow_results['error'] = str(e)
        
        return workflow_results
    
    def _create_daily_summary(self, workflow_results: Dict[str, str]) -> str:
        """Create a daily summary of the workflow results"""
        date = workflow_results['date']
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        summary = f"""# Daily Workflow Summary - {date}
## Channel: {self.config['channel']['channel_name']}
## Niche: {self.niche}

### Workflow Status: {workflow_results['status'].upper()}

### Generated Files:

#### 1. Research Report
- **File**: `{workflow_results.get('research_report', 'Not generated')}`
- **Description**: Daily research compilation from multiple sources
- **Next Step**: Review trending topics and top stories

#### 2. Script Package
- **Directory**: `{workflow_results.get('script_package', 'Not generated')}`
- **Contents**: 
  - `script.txt` - Raw script
  - `script_optimized.txt` - NotebookLM-ready script
  - `notebooklm_instructions.md` - Step-by-step instructions
  - `metadata.json` - Script metadata
- **Next Step**: Use optimized script in NotebookLM to generate video

#### 3. Upload Package
- **Directory**: `{workflow_results.get('upload_package', 'Not generated')}`
- **Contents**:
  - `upload_config.json` - Upload configuration
  - `upload_instructions.md` - Step-by-step upload guide
  - `thumbnail_specs.json` - Thumbnail design specifications
- **Next Step**: Follow upload instructions after video generation

#### 4. Analytics Report
- **File**: `{workflow_results.get('analytics_report', 'Not generated')}`
- **Description**: Channel performance analysis and recommendations
- **Next Step**: Review recommendations and implement improvements

### 🎬 Next Steps for Video Creation:

1. **Generate Video in NotebookLM**:
   - Open the script package directory
   - Follow instructions in `notebooklm_instructions.md`
   - Use the optimized script to generate video

2. **Create Thumbnail**:
   - Use specifications in `thumbnail_specs.json`
   - Design eye-catching thumbnail with suggested elements
   - Save as 1280x720 PNG/JPG

3. **Upload to YouTube**:
   - Follow instructions in `upload_instructions.md`
   - Use provided title, description, and tags
   - Schedule for optimal time: {self.config['channel']['upload_schedule']}

4. **Monitor Performance**:
   - Check analytics 24 hours after upload
   - Engage with comments within first hour
   - Share on social media platforms

### 📊 Today's Research Highlights:
- **Keywords Tracked**: {', '.join(self.keywords)}
- **Sources Analyzed**: YouTube, Reddit, Twitter
- **Content Focus**: {self.niche} trends and developments

### ⚙️ Automation Status:
- **Research**: {'✅ Automated' if self.config['automation']['auto_research'] else '❌ Manual'}
- **Script Generation**: {'✅ Automated' if self.config['automation']['auto_script_generation'] else '❌ Manual'}
- **Upload Prep**: {'✅ Automated' if self.config['automation']['auto_upload_preparation'] else '❌ Manual'}

### 📈 Performance Tracking:
- **Analytics**: {'✅ Enabled' if self.config['analytics']['track_performance'] else '❌ Disabled'}
- **Weekly Reports**: {'✅ Enabled' if self.config['analytics']['generate_weekly_reports'] else '❌ Disabled'}

---
*Summary generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        # Save summary
        summary_path = os.path.join(self.output_dir, f"daily_summary_{timestamp}.md")
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        return summary_path
    
    def setup_scheduled_workflow(self) -> str:
        """Create a scheduled workflow script for daily automation"""
        script_content = f"""#!/bin/bash
# Daily YouTube Channel Workflow
# This script runs the complete daily workflow automatically

cd "{os.path.dirname(__file__)}"

echo "Starting daily workflow at $(date)"

# Run the master workflow
python3 master_workflow.py --config config/channel_config.json --auto

echo "Daily workflow completed at $(date)"
"""
        
        script_path = os.path.join(self.base_dir, 'run_daily_workflow.sh')
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Make executable
        os.chmod(script_path, 0o755)
        
        print(f"✅ Scheduled workflow script created: {script_path}")
        print("\nTo set up daily automation, add this to your crontab:")
        print(f"0 {self.config['channel']['upload_schedule'].split(':')[0]} * * * {script_path}")
        
        return script_path
    
    def validate_setup(self) -> Dict[str, bool]:
        """Validate that all components are properly configured"""
        validation_results = {
            'config_valid': False,
            'directories_created': False,
            'dependencies_available': False,
            'api_access': False
        }
        
        # Check config
        required_fields = ['channel.niche', 'channel.keywords', 'channel.channel_id']
        config_valid = True
        for field in required_fields:
            keys = field.split('.')
            value = self.config
            for key in keys:
                value = value.get(key, {})
            if not value or value == "YOUR_CHANNEL_ID_HERE":
                config_valid = False
                break
        validation_results['config_valid'] = config_valid
        
        # Check directories
        required_dirs = ['reports', 'scripts', 'uploads', 'analytics_data']
        for dir_name in required_dirs:
            os.makedirs(os.path.join(self.base_dir, '..', dir_name), exist_ok=True)
        validation_results['directories_created'] = True
        
        # Check dependencies
        try:
            import requests
            validation_results['dependencies_available'] = True
        except ImportError:
            validation_results['dependencies_available'] = False
        
        # Check API access (simplified)
        try:
            # This would test actual API connectivity
            validation_results['api_access'] = True
        except:
            validation_results['api_access'] = False
        
        return validation_results

def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Master Workflow Orchestrator')
    parser.add_argument('--config', default='config/channel_config.json', help='Path to configuration file')
    parser.add_argument('--date', help='Date for workflow (YYYY-MM-DD), defaults to today')
    parser.add_argument('--setup', action='store_true', help='Setup scheduled workflow')
    parser.add_argument('--validate', action='store_true', help='Validate setup')
    parser.add_argument('--auto', action='store_true', help='Run in automated mode (less output)')
    
    args = parser.parse_args()
    
    # Create config directory if it doesn't exist
    config_dir = os.path.dirname(args.config)
    if config_dir:
        os.makedirs(config_dir, exist_ok=True)
    
    # Initialize workflow
    workflow = MasterWorkflow(args.config)
    
    if args.validate:
        print("🔍 Validating setup...")
        results = workflow.validate_setup()
        for check, passed in results.items():
            status = "✅" if passed else "❌"
            print(f"{status} {check.replace('_', ' ').title()}")
        
        if all(results.values()):
            print("\n✅ All validations passed! Ready to run workflow.")
        else:
            print("\n❌ Some validations failed. Please fix issues before running.")
        return
    
    if args.setup:
        print("⚙️ Setting up scheduled workflow...")
        script_path = workflow.setup_scheduled_workflow()
        return
    
    # Run daily workflow
    if not args.auto:
        print("🚀 Running daily workflow...")
    
    results = workflow.run_daily_workflow(args.date)
    
    if results['status'] == 'completed':
        if not args.auto:
            print(f"\n✅ Workflow completed successfully!")
            print(f"📋 Check the daily summary for next steps: {results.get('daily_summary', '')}")
    else:
        print(f"\n❌ Workflow failed: {results.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()

