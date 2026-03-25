#!/usr/bin/env python3
"""
Daily Research Scraper for YouTube Insights Channel
This script automates the daily research process by gathering news and insights
from multiple sources and compiling them into a structured report.
"""

import sys
import os
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any
import time

# Add the Manus API client path
sys.path.append('/opt/.manus/.sandbox-runtime')
from data_api import ApiClient

class DailyResearchScraper:
    def __init__(self, niche: str, keywords: List[str]):
        """
        Initialize the research scraper
        
        Args:
            niche (str): The niche/topic for research (e.g., "AI", "crypto", "business")
            keywords (List[str]): List of keywords to search for
        """
        self.niche = niche
        self.keywords = keywords
        self.api_client = ApiClient()
        self.research_data = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "niche": niche,
            "sources": {
                "youtube": [],
                "reddit": [],
                "twitter": [],
                "news": []
            },
            "top_stories": [],
            "trending_topics": []
        }
    
    def search_youtube_content(self) -> List[Dict]:
        """Search for trending YouTube videos in the niche"""
        print(f"🔍 Searching YouTube for {self.niche} content...")
        
        all_videos = []
        for keyword in self.keywords:
            try:
                query = f"{keyword} {self.niche} news today"
                result = self.api_client.call_api('Youtube/search', query={
                    'q': query,
                    'hl': 'en',
                    'gl': 'US'
                })
                
                if result and 'contents' in result:
                    videos = []
                    for content in result['contents'][:5]:  # Top 5 results per keyword
                        if content.get('type') == 'video':
                            video = content.get('video', {})
                            videos.append({
                                'title': video.get('title', ''),
                                'channel': video.get('channelTitle', ''),
                                'published': video.get('publishedTimeText', ''),
                                'views': video.get('viewCountText', ''),
                                'duration': video.get('lengthText', ''),
                                'url': f"https://youtube.com/watch?v={video.get('videoId', '')}",
                                'keyword': keyword
                            })
                    all_videos.extend(videos)
                    time.sleep(1)  # Rate limiting
                    
            except Exception as e:
                print(f"Error searching YouTube for {keyword}: {e}")
        
        self.research_data['sources']['youtube'] = all_videos
        return all_videos
    
    def search_reddit_content(self) -> List[Dict]:
        """Search for trending Reddit posts in relevant subreddits"""
        print(f"🔍 Searching Reddit for {self.niche} content...")
        
        # Common subreddits for different niches
        subreddit_map = {
            "AI": ["artificial", "MachineLearning", "singularity", "OpenAI"],
            "crypto": ["cryptocurrency", "Bitcoin", "ethereum", "CryptoMarkets"],
            "business": ["business", "entrepreneur", "startups", "investing"],
            "tech": ["technology", "programming", "gadgets", "futurology"]
        }
        
        subreddits = subreddit_map.get(self.niche, [self.niche.lower()])
        all_posts = []
        
        for subreddit in subreddits:
            try:
                result = self.api_client.call_api('Reddit/AccessAPI', query={
                    'subreddit': subreddit,
                    'limit': '10'
                })
                
                if result and result.get('success') and 'posts' in result:
                    posts = []
                    for post_wrapper in result['posts'][:5]:  # Top 5 posts per subreddit
                        post = post_wrapper.get('data', {})
                        posts.append({
                            'title': post.get('title', ''),
                            'author': post.get('author', ''),
                            'score': post.get('score', 0),
                            'comments': post.get('num_comments', 0),
                            'url': f"https://reddit.com{post.get('permalink', '')}",
                            'subreddit': subreddit,
                            'created': post.get('created_utc', 0)
                        })
                    all_posts.extend(posts)
                    time.sleep(1)  # Rate limiting
                    
            except Exception as e:
                print(f"Error searching Reddit r/{subreddit}: {e}")
        
        self.research_data['sources']['reddit'] = all_posts
        return all_posts
    
    def search_twitter_content(self) -> List[Dict]:
        """Search for trending Twitter content"""
        print(f"🔍 Searching Twitter for {self.niche} content...")
        
        all_tweets = []
        for keyword in self.keywords:
            try:
                query = f"{keyword} {self.niche}"
                result = self.api_client.call_api('Twitter/search_twitter', query={
                    'query': query
                })
                
                if result and 'timeline' in result:
                    tweets = []
                    entries = result['timeline'].get('instructions', [{}])[0].get('entries', [])
                    
                    for entry in entries[:5]:  # Top 5 tweets per keyword
                        if 'content' in entry and 'itemContent' in entry['content']:
                            tweet_data = entry['content']['itemContent']
                            if 'tweet_results' in tweet_data:
                                tweet = tweet_data['tweet_results'].get('result', {})
                                legacy = tweet.get('legacy', {})
                                user = tweet.get('core', {}).get('user_results', {}).get('result', {}).get('legacy', {})
                                
                                tweets.append({
                                    'text': legacy.get('full_text', ''),
                                    'user': user.get('screen_name', ''),
                                    'likes': legacy.get('favorite_count', 0),
                                    'retweets': legacy.get('retweet_count', 0),
                                    'created': legacy.get('created_at', ''),
                                    'keyword': keyword
                                })
                    
                    all_tweets.extend(tweets)
                    time.sleep(1)  # Rate limiting
                    
            except Exception as e:
                print(f"Error searching Twitter for {keyword}: {e}")
        
        self.research_data['sources']['twitter'] = all_tweets
        return all_tweets
    
    def analyze_trending_topics(self) -> List[str]:
        """Analyze all collected data to identify trending topics"""
        print("📊 Analyzing trending topics...")
        
        # Count keyword frequency across all sources
        topic_counts = {}
        
        # Analyze YouTube titles
        for video in self.research_data['sources']['youtube']:
            title = video.get('title', '').lower()
            for keyword in self.keywords:
                if keyword.lower() in title:
                    topic_counts[keyword] = topic_counts.get(keyword, 0) + 1
        
        # Analyze Reddit titles
        for post in self.research_data['sources']['reddit']:
            title = post.get('title', '').lower()
            for keyword in self.keywords:
                if keyword.lower() in title:
                    topic_counts[keyword] = topic_counts.get(keyword, 0) + 1
        
        # Analyze Twitter content
        for tweet in self.research_data['sources']['twitter']:
            text = tweet.get('text', '').lower()
            for keyword in self.keywords:
                if keyword.lower() in text:
                    topic_counts[keyword] = topic_counts.get(keyword, 0) + 1
        
        # Sort by frequency
        trending = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)
        trending_topics = [topic for topic, count in trending[:5]]
        
        self.research_data['trending_topics'] = trending_topics
        return trending_topics
    
    def identify_top_stories(self) -> List[Dict]:
        """Identify the top stories based on engagement metrics"""
        print("📈 Identifying top stories...")
        
        all_stories = []
        
        # Add YouTube videos with high view counts
        for video in self.research_data['sources']['youtube']:
            views_text = video.get('views', '0')
            # Simple view count extraction (this could be improved)
            try:
                if 'K' in views_text:
                    views = float(views_text.replace('K', '').replace(' views', '')) * 1000
                elif 'M' in views_text:
                    views = float(views_text.replace('M', '').replace(' views', '')) * 1000000
                else:
                    views = float(views_text.replace(' views', '').replace(',', ''))
            except:
                views = 0
            
            all_stories.append({
                'title': video.get('title', ''),
                'source': 'YouTube',
                'engagement': views,
                'url': video.get('url', ''),
                'type': 'video'
            })
        
        # Add Reddit posts with high scores
        for post in self.research_data['sources']['reddit']:
            all_stories.append({
                'title': post.get('title', ''),
                'source': f"Reddit r/{post.get('subreddit', '')}",
                'engagement': post.get('score', 0),
                'url': post.get('url', ''),
                'type': 'discussion'
            })
        
        # Add Twitter posts with high engagement
        for tweet in self.research_data['sources']['twitter']:
            engagement = tweet.get('likes', 0) + tweet.get('retweets', 0)
            all_stories.append({
                'title': tweet.get('text', '')[:100] + '...',
                'source': f"Twitter @{tweet.get('user', '')}",
                'engagement': engagement,
                'url': f"https://twitter.com/{tweet.get('user', '')}/status/...",
                'type': 'tweet'
            })
        
        # Sort by engagement and take top 10
        top_stories = sorted(all_stories, key=lambda x: x['engagement'], reverse=True)[:10]
        self.research_data['top_stories'] = top_stories
        
        return top_stories
    
    def generate_report(self) -> str:
        """Generate a formatted research report"""
        print("📝 Generating research report...")
        
        report = f"""# Daily Research Report - {self.research_data['date']}
## Niche: {self.niche}

### 🔥 Trending Topics
{chr(10).join([f"- {topic}" for topic in self.research_data['trending_topics']])}

### 📈 Top Stories

"""
        
        for i, story in enumerate(self.research_data['top_stories'], 1):
            report += f"""#### {i}. {story['title']}
- **Source**: {story['source']}
- **Engagement**: {story['engagement']:,}
- **Type**: {story['type']}
- **URL**: {story['url']}

"""
        
        report += f"""### 📊 Source Summary
- **YouTube Videos**: {len(self.research_data['sources']['youtube'])} videos found
- **Reddit Posts**: {len(self.research_data['sources']['reddit'])} posts found
- **Twitter Posts**: {len(self.research_data['sources']['twitter'])} tweets found

### 🎯 Content Opportunities
Based on today's research, consider creating content about:
{chr(10).join([f"- {topic}" for topic in self.research_data['trending_topics'][:3]])}

---
*Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        return report
    
    def save_report(self, report: str, filename: str = None) -> str:
        """Save the research report to a file"""
        if not filename:
            filename = f"daily_research_{self.niche}_{datetime.now().strftime('%Y%m%d')}.md"
        
        filepath = os.path.join(os.path.dirname(__file__), '..', '..', 'reports', filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ Report saved to: {filepath}")
        return filepath
    
    def run_daily_research(self) -> str:
        """Run the complete daily research process"""
        print(f"🚀 Starting daily research for {self.niche}...")
        
        # Gather data from all sources
        self.search_youtube_content()
        self.search_reddit_content()
        self.search_twitter_content()
        
        # Analyze the data
        self.analyze_trending_topics()
        self.identify_top_stories()
        
        # Generate and save report
        report = self.generate_report()
        filepath = self.save_report(report)
        
        print("✅ Daily research complete!")
        return filepath

def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Daily Research Scraper for YouTube Channel')
    parser.add_argument('--niche', required=True, help='The niche/topic for research')
    parser.add_argument('--keywords', required=True, nargs='+', help='Keywords to search for')
    
    args = parser.parse_args()
    
    scraper = DailyResearchScraper(args.niche, args.keywords)
    report_path = scraper.run_daily_research()
    
    print(f"Research report saved to: {report_path}")

if __name__ == "__main__":
    main()

