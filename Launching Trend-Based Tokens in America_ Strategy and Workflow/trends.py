from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.trend import Trend, Token, MarketingCampaign
import requests
import json
from datetime import datetime, timedelta
import time

trends_bp = Blueprint('trends', __name__)

@trends_bp.route('/trends', methods=['GET'])
def get_trends():
    """Get all trends from the database"""
    trends = Trend.query.order_by(Trend.created_at.desc()).all()
    return jsonify([trend.to_dict() for trend in trends])

@trends_bp.route('/trends/fetch', methods=['POST'])
def fetch_trends():
    """Fetch trending topics from Google Trends API (simulated)"""
    try:
        # Simulate fetching trends from Google Trends
        # In a real implementation, you would use the pytrends library or Google Trends API
        simulated_trends = [
            {"keyword": "charlie kirk", "search_volume": "10M+", "source": "google_trends"},
            {"keyword": "dna", "search_volume": "1M+", "source": "google_trends"},
            {"keyword": "colorado school shooting", "search_volume": "1M+", "source": "google_trends"},
            {"keyword": "nato article 4", "search_volume": "200K+", "source": "google_trends"},
            {"keyword": "spotify lossless music", "search_volume": "100K+", "source": "google_trends"},
            {"keyword": "life on mars", "search_volume": "20K+", "source": "google_trends"},
            {"keyword": "bachelorette 2025", "search_volume": "100K+", "source": "google_trends"},
            {"keyword": "klarna stock", "search_volume": "20K+", "source": "google_trends"}
        ]
        
        trends_added = 0
        for trend_data in simulated_trends:
            # Check if trend already exists
            existing_trend = Trend.query.filter_by(keyword=trend_data['keyword']).first()
            if not existing_trend:
                # Calculate sentiment and virality scores (simulated)
                sentiment_score = calculate_sentiment_score(trend_data['keyword'])
                virality_score = calculate_virality_score(trend_data['search_volume'])
                
                new_trend = Trend(
                    keyword=trend_data['keyword'],
                    search_volume=trend_data['search_volume'],
                    sentiment_score=sentiment_score,
                    virality_score=virality_score,
                    source=trend_data['source']
                )
                db.session.add(new_trend)
                trends_added += 1
        
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': f'Added {trends_added} new trends',
            'trends_added': trends_added
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@trends_bp.route('/trends/<int:trend_id>/analyze', methods=['POST'])
def analyze_trend(trend_id):
    """Analyze a specific trend for tokenization potential"""
    try:
        trend = Trend.query.get_or_404(trend_id)
        
        # Perform analysis (simulated)
        analysis_result = {
            'trend_id': trend_id,
            'keyword': trend.keyword,
            'tokenization_potential': 'high' if trend.virality_score > 0.7 else 'medium' if trend.virality_score > 0.4 else 'low',
            'recommended_action': 'create_token' if trend.virality_score > 0.6 and trend.sentiment_score > 0.5 else 'monitor',
            'risk_level': 'low' if trend.sentiment_score > 0.6 else 'medium' if trend.sentiment_score > 0.3 else 'high'
        }
        
        return jsonify(analysis_result)
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@trends_bp.route('/trends/monitor', methods=['POST'])
def start_monitoring():
    """Start continuous trend monitoring"""
    try:
        # This would typically start a background task
        # For now, we'll simulate by fetching trends immediately
        fetch_result = fetch_trends()
        
        return jsonify({
            'status': 'success',
            'message': 'Trend monitoring started',
            'fetch_result': fetch_result.get_json()
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

def calculate_sentiment_score(keyword):
    """Calculate sentiment score for a keyword (simulated)"""
    # In a real implementation, this would use sentiment analysis APIs
    # For now, we'll simulate based on keyword characteristics
    positive_keywords = ['music', 'mars', 'bachelorette', 'stock']
    negative_keywords = ['shooting', 'killed', 'attack']
    
    if any(neg in keyword.lower() for neg in negative_keywords):
        return 0.2 + (hash(keyword) % 30) / 100  # 0.2-0.5 range
    elif any(pos in keyword.lower() for pos in positive_keywords):
        return 0.6 + (hash(keyword) % 40) / 100  # 0.6-1.0 range
    else:
        return 0.3 + (hash(keyword) % 50) / 100  # 0.3-0.8 range

def calculate_virality_score(search_volume):
    """Calculate virality score based on search volume"""
    if '10M+' in search_volume:
        return 0.9
    elif '1M+' in search_volume:
        return 0.8
    elif '500K+' in search_volume:
        return 0.7
    elif '200K+' in search_volume:
        return 0.6
    elif '100K+' in search_volume:
        return 0.5
    elif '50K+' in search_volume:
        return 0.4
    elif '20K+' in search_volume:
        return 0.3
    elif '10K+' in search_volume:
        return 0.2
    else:
        return 0.1

