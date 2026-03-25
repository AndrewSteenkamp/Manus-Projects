#!/usr/bin/env python3
"""
Performance Tracker for YouTube Channel
This script tracks channel performance, analyzes trends, and provides
actionable insights for content optimization.
"""

import sys
import os
import json
import csv
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import statistics

# Add the Manus API client path
sys.path.append('/opt/.manus/.sandbox-runtime')
from data_api import ApiClient

class PerformanceTracker:
    def __init__(self, channel_id: str, niche: str):
        """
        Initialize the performance tracker
        
        Args:
            channel_id (str): YouTube channel ID
            niche (str): Channel niche for context
        """
        self.channel_id = channel_id
        self.niche = niche
        self.api_client = ApiClient()
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'analytics_data')
        os.makedirs(self.data_dir, exist_ok=True)
        
    def fetch_channel_analytics(self) -> Dict[str, Any]:
        """
        Fetch current channel analytics data
        
        Returns:
            Dict containing channel analytics
        """
        print(f"📊 Fetching analytics for channel: {self.channel_id}")
        
        try:
            # Get channel details
            channel_result = self.api_client.call_api('Youtube/get_channel_details', query={
                'id': self.channel_id,
                'hl': 'en'
            })
            
            # Get recent videos
            videos_result = self.api_client.call_api('Youtube/get_channel_videos', query={
                'id': self.channel_id,
                'filter': 'videos_latest',
                'hl': 'en'
            })
            
            analytics_data = {
                'timestamp': datetime.now().isoformat(),
                'channel_info': self._extract_channel_info(channel_result),
                'recent_videos': self._extract_video_metrics(videos_result),
                'performance_summary': {}
            }
            
            # Calculate performance summary
            analytics_data['performance_summary'] = self._calculate_performance_summary(
                analytics_data['recent_videos']
            )
            
            return analytics_data
            
        except Exception as e:
            print(f"Error fetching analytics: {e}")
            return {}
    
    def _extract_channel_info(self, channel_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract relevant channel information"""
        if not channel_data:
            return {}
        
        stats = channel_data.get('stats', {})
        
        return {
            'channel_id': channel_data.get('channelId', ''),
            'title': channel_data.get('title', ''),
            'subscriber_count': stats.get('subscribers', 0),
            'total_videos': stats.get('videos', 0),
            'total_views': stats.get('views', 0),
            'joined_date': channel_data.get('joinedDate', ''),
            'description': channel_data.get('description', '')[:200] + '...'
        }
    
    def _extract_video_metrics(self, videos_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract metrics from recent videos"""
        if not videos_data or 'contents' not in videos_data:
            return []
        
        video_metrics = []
        
        for content in videos_data['contents'][:20]:  # Last 20 videos
            if content.get('type') == 'video':
                video = content.get('video', {})
                stats = video.get('stats', {})
                
                # Parse view count
                views = 0
                view_text = stats.get('views', '0')
                if isinstance(view_text, str):
                    try:
                        # Remove commas and convert to int
                        views = int(view_text.replace(',', '').replace(' views', ''))
                    except:
                        views = 0
                elif isinstance(view_text, int):
                    views = view_text
                
                video_metrics.append({
                    'video_id': video.get('videoId', ''),
                    'title': video.get('title', ''),
                    'published': video.get('publishedTimeText', ''),
                    'duration': video.get('lengthSeconds', 0),
                    'views': views,
                    'thumbnail': video.get('thumbnails', [{}])[0].get('url', '') if video.get('thumbnails') else ''
                })
        
        return video_metrics
    
    def _calculate_performance_summary(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate performance summary statistics"""
        if not videos:
            return {}
        
        view_counts = [video['views'] for video in videos if video['views'] > 0]
        
        if not view_counts:
            return {}
        
        return {
            'total_videos_analyzed': len(videos),
            'average_views': statistics.mean(view_counts),
            'median_views': statistics.median(view_counts),
            'max_views': max(view_counts),
            'min_views': min(view_counts),
            'total_views': sum(view_counts),
            'view_consistency': self._calculate_consistency(view_counts),
            'top_performing_video': max(videos, key=lambda x: x['views']),
            'recent_trend': self._calculate_trend(videos[-10:])  # Last 10 videos
        }
    
    def _calculate_consistency(self, view_counts: List[int]) -> float:
        """Calculate view count consistency (lower is more consistent)"""
        if len(view_counts) < 2:
            return 0.0
        
        mean_views = statistics.mean(view_counts)
        if mean_views == 0:
            return 0.0
        
        std_dev = statistics.stdev(view_counts)
        coefficient_of_variation = std_dev / mean_views
        
        # Convert to consistency score (0-100, higher is more consistent)
        consistency = max(0, 100 - (coefficient_of_variation * 100))
        return round(consistency, 2)
    
    def _calculate_trend(self, recent_videos: List[Dict[str, Any]]) -> str:
        """Calculate recent performance trend"""
        if len(recent_videos) < 5:
            return "insufficient_data"
        
        views = [video['views'] for video in recent_videos if video['views'] > 0]
        if len(views) < 5:
            return "insufficient_data"
        
        # Compare first half vs second half
        mid_point = len(views) // 2
        first_half_avg = statistics.mean(views[:mid_point])
        second_half_avg = statistics.mean(views[mid_point:])
        
        if second_half_avg > first_half_avg * 1.1:
            return "improving"
        elif second_half_avg < first_half_avg * 0.9:
            return "declining"
        else:
            return "stable"
    
    def analyze_content_performance(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze which types of content perform best"""
        print("🔍 Analyzing content performance patterns...")
        
        # Analyze title patterns
        title_analysis = self._analyze_title_patterns(videos)
        
        # Analyze duration impact
        duration_analysis = self._analyze_duration_impact(videos)
        
        # Analyze publishing patterns
        publishing_analysis = self._analyze_publishing_patterns(videos)
        
        return {
            'title_patterns': title_analysis,
            'duration_impact': duration_analysis,
            'publishing_patterns': publishing_analysis,
            'recommendations': self._generate_content_recommendations(
                title_analysis, duration_analysis, publishing_analysis
            )
        }
    
    def _analyze_title_patterns(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze which title patterns perform best"""
        patterns = {
            'numbers': [],
            'questions': [],
            'urgent_words': [],
            'length_short': [],  # < 50 chars
            'length_medium': [],  # 50-70 chars
            'length_long': []  # > 70 chars
        }
        
        urgent_keywords = ['breaking', 'urgent', 'alert', 'now', 'today', 'latest', 'just', 'new']
        
        for video in videos:
            title = video.get('title', '').lower()
            views = video.get('views', 0)
            
            # Check for numbers
            if any(char.isdigit() for char in title):
                patterns['numbers'].append(views)
            
            # Check for questions
            if '?' in title:
                patterns['questions'].append(views)
            
            # Check for urgent words
            if any(word in title for word in urgent_keywords):
                patterns['urgent_words'].append(views)
            
            # Check title length
            title_length = len(video.get('title', ''))
            if title_length < 50:
                patterns['length_short'].append(views)
            elif title_length <= 70:
                patterns['length_medium'].append(views)
            else:
                patterns['length_long'].append(views)
        
        # Calculate averages
        analysis = {}
        for pattern, view_list in patterns.items():
            if view_list:
                analysis[pattern] = {
                    'average_views': statistics.mean(view_list),
                    'video_count': len(view_list),
                    'performance_score': statistics.mean(view_list) / max(1, statistics.mean([v['views'] for v in videos]))
                }
            else:
                analysis[pattern] = {
                    'average_views': 0,
                    'video_count': 0,
                    'performance_score': 0
                }
        
        return analysis
    
    def _analyze_duration_impact(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze how video duration affects performance"""
        duration_buckets = {
            'short': [],  # < 3 minutes
            'medium': [],  # 3-8 minutes
            'long': []  # > 8 minutes
        }
        
        for video in videos:
            duration = video.get('duration', 0)
            views = video.get('views', 0)
            
            if duration < 180:  # 3 minutes
                duration_buckets['short'].append(views)
            elif duration <= 480:  # 8 minutes
                duration_buckets['medium'].append(views)
            else:
                duration_buckets['long'].append(views)
        
        analysis = {}
        for bucket, view_list in duration_buckets.items():
            if view_list:
                analysis[bucket] = {
                    'average_views': statistics.mean(view_list),
                    'video_count': len(view_list),
                    'performance_score': statistics.mean(view_list) / max(1, statistics.mean([v['views'] for v in videos]))
                }
            else:
                analysis[bucket] = {
                    'average_views': 0,
                    'video_count': 0,
                    'performance_score': 0
                }
        
        return analysis
    
    def _analyze_publishing_patterns(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze publishing time patterns (limited by available data)"""
        # Note: This is simplified since we don't have exact timestamps
        # In a real implementation, you'd analyze day of week and time of day
        
        return {
            'note': 'Publishing pattern analysis requires more detailed timestamp data',
            'recommendation': 'Track upload times manually and correlate with performance',
            'best_practices': [
                'Upload consistently at the same time daily',
                'Consider your audience timezone',
                'Test different times and measure results'
            ]
        }
    
    def _generate_content_recommendations(self, title_analysis: Dict, duration_analysis: Dict, publishing_analysis: Dict) -> List[str]:
        """Generate actionable content recommendations"""
        recommendations = []
        
        # Title recommendations
        best_title_pattern = max(title_analysis.items(), key=lambda x: x[1]['performance_score'])
        recommendations.append(f"Use {best_title_pattern[0]} in titles - shows {best_title_pattern[1]['performance_score']:.1f}x better performance")
        
        # Duration recommendations
        best_duration = max(duration_analysis.items(), key=lambda x: x[1]['performance_score'])
        duration_map = {'short': 'under 3 minutes', 'medium': '3-8 minutes', 'long': 'over 8 minutes'}
        recommendations.append(f"Optimal video length: {duration_map[best_duration[0]]} - {best_duration[1]['performance_score']:.1f}x better performance")
        
        # General recommendations
        recommendations.extend([
            f"Focus on {self.niche} content with trending keywords",
            "Maintain consistent daily publishing schedule",
            "Use eye-catching thumbnails with clear text",
            "Engage with comments within first hour of publishing",
            "Cross-promote on social media platforms"
        ])
        
        return recommendations
    
    def generate_performance_report(self, analytics_data: Dict[str, Any]) -> str:
        """Generate a comprehensive performance report"""
        print("📋 Generating performance report...")
        
        if not analytics_data:
            return "No analytics data available"
        
        channel_info = analytics_data.get('channel_info', {})
        performance = analytics_data.get('performance_summary', {})
        videos = analytics_data.get('recent_videos', [])
        
        # Analyze content performance
        content_analysis = self.analyze_content_performance(videos)
        
        report = f"""# YouTube Channel Performance Report
## Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

### Channel Overview
- **Channel**: {channel_info.get('title', 'Unknown')}
- **Niche**: {self.niche}
- **Subscribers**: {channel_info.get('subscriber_count', 0):,}
- **Total Videos**: {channel_info.get('total_videos', 0):,}
- **Total Views**: {channel_info.get('total_views', 0):,}

### Recent Performance (Last {performance.get('total_videos_analyzed', 0)} Videos)
- **Average Views**: {performance.get('average_views', 0):,.0f}
- **Median Views**: {performance.get('median_views', 0):,.0f}
- **Best Performing Video**: {performance.get('max_views', 0):,} views
- **View Consistency Score**: {performance.get('view_consistency', 0):.1f}/100
- **Recent Trend**: {performance.get('recent_trend', 'unknown').title()}

### Top Performing Video
**Title**: {performance.get('top_performing_video', {}).get('title', 'N/A')}
**Views**: {performance.get('top_performing_video', {}).get('views', 0):,}

### Content Analysis

#### Title Patterns Performance
"""
        
        # Add title analysis
        title_patterns = content_analysis.get('title_patterns', {})
        for pattern, data in title_patterns.items():
            if data['video_count'] > 0:
                report += f"- **{pattern.replace('_', ' ').title()}**: {data['average_views']:,.0f} avg views ({data['video_count']} videos)\n"
        
        report += f"""
#### Duration Analysis
"""
        
        # Add duration analysis
        duration_analysis = content_analysis.get('duration_impact', {})
        for duration, data in duration_analysis.items():
            if data['video_count'] > 0:
                report += f"- **{duration.title()} Videos**: {data['average_views']:,.0f} avg views ({data['video_count']} videos)\n"
        
        report += f"""
### 🎯 Actionable Recommendations

"""
        
        # Add recommendations
        recommendations = content_analysis.get('recommendations', [])
        for i, rec in enumerate(recommendations, 1):
            report += f"{i}. {rec}\n"
        
        report += f"""
### 📊 Performance Metrics Tracking

#### Key Metrics to Monitor:
- **Click-through Rate (CTR)**: Aim for >10%
- **Average View Duration**: Aim for >50% of video length
- **Subscriber Growth Rate**: Track daily/weekly changes
- **Engagement Rate**: (Likes + Comments + Shares) / Views
- **Revenue per 1000 Views (RPM)**: Track monetization efficiency

#### Weekly Goals:
- Maintain {performance.get('average_views', 0):,.0f}+ views per video
- Improve consistency score to 80+
- Increase subscriber growth rate by 5%
- Achieve 15%+ engagement rate

### 📈 Growth Strategy

#### Short-term (Next 30 Days):
1. Implement top-performing title patterns
2. Optimize video duration based on analysis
3. Create content around trending {self.niche} topics
4. Improve thumbnail design and testing
5. Engage more actively with audience

#### Long-term (Next 90 Days):
1. Develop signature content series
2. Collaborate with other {self.niche} creators
3. Expand to additional content formats
4. Build email list for direct audience connection
5. Explore additional revenue streams

---
*Report generated by AI Performance Tracker*
"""
        
        return report
    
    def save_analytics_data(self, analytics_data: Dict[str, Any]) -> str:
        """Save analytics data to files"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save JSON data
        json_file = os.path.join(self.data_dir, f"analytics_{timestamp}.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(analytics_data, f, indent=2, default=str)
        
        # Save CSV for easy analysis
        csv_file = os.path.join(self.data_dir, f"video_metrics_{timestamp}.csv")
        videos = analytics_data.get('recent_videos', [])
        
        if videos:
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=videos[0].keys())
                writer.writeheader()
                writer.writerows(videos)
        
        # Generate and save report
        report = self.generate_performance_report(analytics_data)
        report_file = os.path.join(self.data_dir, f"performance_report_{timestamp}.md")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ Analytics data saved:")
        print(f"  - JSON: {json_file}")
        print(f"  - CSV: {csv_file}")
        print(f"  - Report: {report_file}")
        
        return report_file
    
    def run_analytics(self) -> str:
        """Run complete analytics workflow"""
        print(f"🚀 Running analytics for {self.niche} channel...")
        
        # Fetch analytics data
        analytics_data = self.fetch_channel_analytics()
        
        if not analytics_data:
            print("❌ Failed to fetch analytics data")
            return ""
        
        # Save data and generate report
        report_file = self.save_analytics_data(analytics_data)
        
        print("✅ Analytics complete!")
        return report_file

def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='YouTube Channel Performance Tracker')
    parser.add_argument('--channel-id', required=True, help='YouTube channel ID')
    parser.add_argument('--niche', required=True, help='Channel niche')
    
    args = parser.parse_args()
    
    tracker = PerformanceTracker(args.channel_id, args.niche)
    report_file = tracker.run_analytics()
    
    if report_file:
        print(f"Performance report generated: {report_file}")
    else:
        print("Failed to generate performance report")

if __name__ == "__main__":
    main()

