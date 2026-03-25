# YouTube Daily Insights Channel - Automation Tools

This directory contains all the automation tools needed to run a successful daily insights YouTube channel using AI and NotebookLM.

## 🚀 Quick Start

1. **Configure your channel**:
   ```bash
   python3 master_workflow.py --validate
   ```

2. **Run daily workflow**:
   ```bash
   python3 master_workflow.py --config config/channel_config.json
   ```

3. **Set up automation**:
   ```bash
   python3 master_workflow.py --setup
   ```

## 📁 Directory Structure

```
automation_tools/
├── research/
│   └── daily_research_scraper.py    # Automated research gathering
├── content_generation/
│   └── notebooklm_processor.py      # Script generation for NotebookLM
├── youtube_management/
│   └── youtube_uploader.py          # Upload optimization and scheduling
├── analytics/
│   └── performance_tracker.py       # Performance analysis and insights
├── master_workflow.py               # Main orchestrator
└── README.md                        # This file
```

## 🔧 Individual Tools

### 1. Daily Research Scraper
**File**: `research/daily_research_scraper.py`

Automatically gathers trending content from multiple sources:
- YouTube videos in your niche
- Reddit discussions
- Twitter trends
- Compiles into structured daily report

**Usage**:
```bash
python3 research/daily_research_scraper.py --niche "AI" --keywords "artificial intelligence" "machine learning" "AI tools"
```

**Output**: Daily research report in Markdown format

### 2. NotebookLM Processor
**File**: `content_generation/notebooklm_processor.py`

Converts research reports into video scripts optimized for NotebookLM:
- Generates engaging intro/outro
- Structures content for slide-based videos
- Creates NotebookLM instructions
- Optimizes for video generation

**Usage**:
```bash
python3 content_generation/notebooklm_processor.py --report path/to/report.md --niche "AI"
```

**Output**: Complete script package with NotebookLM instructions

### 3. YouTube Uploader
**File**: `youtube_management/youtube_uploader.py`

Prepares optimized upload packages:
- SEO-optimized titles and descriptions
- Relevant tags and categories
- Thumbnail design specifications
- Upload scheduling instructions

**Usage**:
```bash
python3 youtube_management/youtube_uploader.py --video video.mp4 --metadata metadata.json --config channel_config.json
```

**Output**: Upload package with all optimization details

### 4. Performance Tracker
**File**: `analytics/performance_tracker.py`

Analyzes channel performance and provides insights:
- Video performance metrics
- Content pattern analysis
- Trend identification
- Actionable recommendations

**Usage**:
```bash
python3 analytics/performance_tracker.py --channel-id YOUR_CHANNEL_ID --niche "AI"
```

**Output**: Comprehensive performance report

### 5. Master Workflow
**File**: `master_workflow.py`

Orchestrates the complete daily workflow:
- Runs all tools in sequence
- Manages file organization
- Creates daily summaries
- Handles error recovery

**Usage**:
```bash
python3 master_workflow.py --config config/channel_config.json
```

## ⚙️ Configuration

### Channel Configuration
Create `config/channel_config.json`:

```json
{
  "channel": {
    "niche": "AI",
    "channel_name": "Daily AI Insights",
    "channel_id": "YOUR_CHANNEL_ID",
    "keywords": ["artificial intelligence", "AI news", "machine learning"],
    "upload_schedule": "09:00",
    "timezone": "UTC"
  },
  "content": {
    "target_duration": "5-7 minutes",
    "style": "professional",
    "include_timestamps": true,
    "add_call_to_action": true
  },
  "automation": {
    "auto_research": true,
    "auto_script_generation": true,
    "auto_upload_preparation": true,
    "send_notifications": true
  },
  "analytics": {
    "track_performance": true,
    "generate_weekly_reports": true,
    "monitor_competitors": false
  }
}
```

## 🔄 Daily Workflow

The complete daily workflow follows these steps:

1. **Research Phase** (5-10 minutes)
   - Scrape trending content from multiple sources
   - Identify top stories and trending topics
   - Generate structured research report

2. **Content Generation** (5-10 minutes)
   - Convert research into engaging video script
   - Optimize for NotebookLM video generation
   - Create step-by-step instructions

3. **Video Production** (5-10 minutes)
   - Use NotebookLM to generate video from script
   - Download and review generated video
   - Add custom branding if needed

4. **Upload Preparation** (5-10 minutes)
   - Generate SEO-optimized metadata
   - Create thumbnail using specifications
   - Schedule upload for optimal time

5. **Performance Monitoring** (5 minutes)
   - Track video performance
   - Analyze audience engagement
   - Adjust strategy based on insights

**Total Time**: 25-45 minutes per day

## 🤖 Automation Setup

### Daily Automation with Cron

1. **Generate automation script**:
   ```bash
   python3 master_workflow.py --setup
   ```

2. **Add to crontab**:
   ```bash
   crontab -e
   ```
   
   Add line (for 9 AM daily):
   ```
   0 9 * * * /path/to/automation_tools/run_daily_workflow.sh
   ```

### Alternative: n8n Workflow

For users preferring n8n automation:

1. Create new workflow in n8n
2. Add schedule trigger (daily at desired time)
3. Add HTTP request node to call master workflow
4. Add notification nodes for success/failure

## 📊 Output Files

The automation system generates organized output:

```
daily_output/
├── reports/
│   └── daily_research_AI_20240829.md
├── scripts/
│   └── AI_20240829_142030/
│       ├── script.txt
│       ├── script_optimized.txt
│       ├── notebooklm_instructions.md
│       └── metadata.json
├── uploads/
│   └── upload_20240829_142045/
│       ├── upload_config.json
│       ├── upload_instructions.md
│       └── thumbnail_specs.json
└── analytics_data/
    ├── analytics_20240829_142100.json
    ├── video_metrics_20240829_142100.csv
    └── performance_report_20240829_142100.md
```

## 🔍 Troubleshooting

### Common Issues

1. **API Rate Limits**
   - Solution: Add delays between API calls
   - Check: Rate limiting in scraper scripts

2. **Missing Dependencies**
   - Solution: Install required packages
   - Check: `pip3 install requests beautifulsoup4`

3. **Configuration Errors**
   - Solution: Validate config with `--validate` flag
   - Check: All required fields are filled

4. **File Permissions**
   - Solution: Make scripts executable
   - Check: `chmod +x *.py`

### Validation

Run validation to check setup:
```bash
python3 master_workflow.py --validate
```

This checks:
- ✅ Configuration validity
- ✅ Directory structure
- ✅ Dependencies
- ✅ API access

## 📈 Performance Optimization

### Best Practices

1. **Research Quality**
   - Use diverse keyword sets
   - Monitor multiple sources
   - Focus on trending topics

2. **Content Optimization**
   - Maintain consistent style
   - Use engaging titles
   - Include clear call-to-actions

3. **Upload Timing**
   - Test different upload times
   - Consider audience timezone
   - Maintain daily consistency

4. **Analytics Review**
   - Check performance weekly
   - Implement recommendations
   - Track improvement trends

## 🆘 Support

For issues or questions:

1. Check the troubleshooting section
2. Review configuration files
3. Run validation checks
4. Check log files for errors

## 🔄 Updates

To update the automation tools:

1. Backup current configuration
2. Download latest version
3. Restore configuration
4. Run validation
5. Test with single workflow

---

*This automation system is designed to make running a daily insights YouTube channel as simple as possible while maintaining high quality and consistency.*

