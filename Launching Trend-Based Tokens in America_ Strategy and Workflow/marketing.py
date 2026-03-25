from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.trend import Trend, Token, MarketingCampaign
import requests
import json
from datetime import datetime
import secrets
import random

marketing_bp = Blueprint('marketing', __name__)

@marketing_bp.route('/marketing/campaigns', methods=['GET'])
def get_campaigns():
    """Get all marketing campaigns"""
    campaigns = MarketingCampaign.query.order_by(MarketingCampaign.created_at.desc()).all()
    return jsonify([campaign.to_dict() for campaign in campaigns])

@marketing_bp.route('/marketing/campaigns/create', methods=['POST'])
def create_campaign():
    """Create a new marketing campaign for a token"""
    try:
        data = request.get_json()
        token_id = data.get('token_id')
        platform = data.get('platform', 'twitter')
        campaign_type = data.get('campaign_type', 'viral_post')
        
        if not token_id:
            return jsonify({'status': 'error', 'message': 'token_id is required'}), 400
        
        token = Token.query.get_or_404(token_id)
        trend = token.trend
        
        # Generate marketing content based on token and trend
        content = generate_marketing_content(token, trend, platform, campaign_type)
        
        # Create campaign record
        new_campaign = MarketingCampaign(
            token_id=token_id,
            platform=platform,
            campaign_type=campaign_type,
            content=content,
            status='pending'
        )
        
        db.session.add(new_campaign)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Marketing campaign created successfully',
            'campaign': new_campaign.to_dict()
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@marketing_bp.route('/marketing/campaigns/<int:campaign_id>/launch', methods=['POST'])
def launch_campaign(campaign_id):
    """Launch a marketing campaign"""
    try:
        campaign = MarketingCampaign.query.get_or_404(campaign_id)
        
        if campaign.status != 'pending':
            return jsonify({'status': 'error', 'message': 'Campaign is not in pending status'}), 400
        
        # Simulate campaign launch
        launch_result = simulate_campaign_launch(campaign)
        
        if launch_result['success']:
            campaign.status = 'active'
            db.session.commit()
            
            return jsonify({
                'status': 'success',
                'message': 'Campaign launched successfully',
                'metrics': launch_result['metrics']
            })
        else:
            campaign.status = 'failed'
            db.session.commit()
            
            return jsonify({
                'status': 'error',
                'message': 'Campaign launch failed',
                'error': launch_result['error']
            }), 500
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@marketing_bp.route('/marketing/campaigns/<int:campaign_id>/metrics', methods=['GET'])
def get_campaign_metrics(campaign_id):
    """Get metrics for a marketing campaign"""
    try:
        campaign = MarketingCampaign.query.get_or_404(campaign_id)
        
        # Simulate campaign metrics
        metrics = simulate_campaign_metrics(campaign)
        
        return jsonify({
            'campaign': campaign.to_dict(),
            'metrics': metrics
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@marketing_bp.route('/marketing/auto-launch', methods=['POST'])
def auto_launch_campaigns():
    """Automatically launch marketing campaigns for deployed tokens"""
    try:
        # Find deployed tokens without active marketing campaigns
        tokens_needing_marketing = Token.query.filter(
            Token.status == 'deployed'
        ).all()
        
        campaigns_created = 0
        created_campaigns = []
        
        for token in tokens_needing_marketing:
            # Check if token already has active campaigns
            existing_campaigns = MarketingCampaign.query.filter(
                MarketingCampaign.token_id == token.id,
                MarketingCampaign.status.in_(['pending', 'active'])
            ).count()
            
            if existing_campaigns == 0:
                # Create multiple campaigns for different platforms
                platforms = ['twitter', 'telegram', 'reddit', 'discord']
                campaign_types = ['viral_post', 'meme_campaign', 'community_engagement']
                
                for platform in platforms[:2]:  # Limit to 2 platforms per token
                    for campaign_type in campaign_types[:1]:  # 1 campaign type per platform
                        content = generate_marketing_content(token, token.trend, platform, campaign_type)
                        
                        new_campaign = MarketingCampaign(
                            token_id=token.id,
                            platform=platform,
                            campaign_type=campaign_type,
                            content=content,
                            status='pending'
                        )
                        
                        db.session.add(new_campaign)
                        campaigns_created += 1
                        created_campaigns.append(new_campaign.to_dict())
                
                # Update token status to marketing
                token.status = 'marketing'
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': f'Created {campaigns_created} marketing campaigns automatically',
            'campaigns_created': campaigns_created,
            'campaigns': created_campaigns
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@marketing_bp.route('/marketing/content/generate', methods=['POST'])
def generate_content():
    """Generate marketing content for a specific token and platform"""
    try:
        data = request.get_json()
        token_id = data.get('token_id')
        platform = data.get('platform', 'twitter')
        campaign_type = data.get('campaign_type', 'viral_post')
        
        if not token_id:
            return jsonify({'status': 'error', 'message': 'token_id is required'}), 400
        
        token = Token.query.get_or_404(token_id)
        trend = token.trend
        
        content = generate_marketing_content(token, trend, platform, campaign_type)
        
        return jsonify({
            'status': 'success',
            'content': content,
            'platform': platform,
            'campaign_type': campaign_type
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

def generate_marketing_content(token, trend, platform, campaign_type):
    """Generate marketing content based on token, trend, platform, and campaign type"""
    
    # Content templates based on platform and campaign type
    templates = {
        'twitter': {
            'viral_post': [
                f"🚀 {token.symbol} is here! Riding the {trend.keyword} wave! 📈 #crypto #trending #{token.symbol}",
                f"💎 New gem alert! {token.name} ({token.symbol}) is trending harder than {trend.keyword}! 🔥",
                f"🌟 {trend.keyword} is everywhere and so is {token.symbol}! Don't miss out! 🚀 #DeFi #crypto",
                f"🔥 {token.symbol} token just launched! Capitalizing on the {trend.keyword} trend! 💰"
            ],
            'meme_campaign': [
                f"When {trend.keyword} is trending but you're holding {token.symbol} 😎💎🙌",
                f"Me: Sees {trend.keyword} trending\nAlso me: Buys {token.symbol} 🚀",
                f"{trend.keyword} + {token.symbol} = 🚀🌙 (not financial advice but... 👀)"
            ],
            'community_engagement': [
                f"Who else is excited about {token.symbol}? The {trend.keyword} community is growing! 🌱",
                f"Drop a 🚀 if you're bullish on {token.symbol}! #{trend.keyword} #{token.symbol}",
                f"Building the future with {token.symbol}! Join our {trend.keyword} community! 🏗️"
            ]
        },
        'telegram': {
            'viral_post': [
                f"🎯 {token.name} ({token.symbol}) is LIVE!\n\n🔥 Trending topic: {trend.keyword}\n💎 Contract: {token.contract_address}\n🚀 Join the movement!",
                f"📢 BREAKING: {token.symbol} token launched!\n\n✨ Based on trending: {trend.keyword}\n💰 Early bird gets the worm!\n🌐 Contract: {token.contract_address}"
            ],
            'community_engagement': [
                f"Welcome to {token.name} community! 🎉\n\nWe're riding the {trend.keyword} wave together!\n\n💎 HODL strong\n🚀 To the moon\n🤝 Community first"
            ]
        },
        'reddit': {
            'viral_post': [
                f"🚀 New token alert: {token.name} ({token.symbol})\n\nCapitalizing on the {trend.keyword} trend that's taking over!\n\nContract: {token.contract_address}\n\nDYOR but this looks promising! 💎",
                f"Anyone else seeing the {trend.keyword} trend? Just found {token.symbol} token that's built around it. Early days but could be huge! 🌙"
            ]
        },
        'discord': {
            'community_engagement': [
                f"🎮 Welcome to {token.name} Discord!\n\n🔥 We're all about the {trend.keyword} movement\n💎 {token.symbol} holders unite!\n🚀 Let's build something amazing together!"
            ]
        }
    }
    
    # Get appropriate template
    platform_templates = templates.get(platform, templates['twitter'])
    campaign_templates = platform_templates.get(campaign_type, platform_templates['viral_post'])
    
    # Select random template
    selected_template = random.choice(campaign_templates)
    
    return selected_template

def simulate_campaign_launch(campaign):
    """Simulate launching a marketing campaign"""
    # Simulate success/failure
    if random.random() > 0.05:  # 95% success rate
        return {
            'success': True,
            'metrics': {
                'reach': random.randint(1000, 50000),
                'engagement': random.randint(100, 5000),
                'clicks': random.randint(50, 1000),
                'shares': random.randint(10, 500)
            }
        }
    else:
        return {
            'success': False,
            'error': 'Platform API rate limit exceeded'
        }

def simulate_campaign_metrics(campaign):
    """Simulate campaign performance metrics"""
    # Base metrics on campaign age and platform
    age_hours = (datetime.utcnow() - campaign.created_at).total_seconds() / 3600
    
    # Platform multipliers
    platform_multipliers = {
        'twitter': 1.5,
        'telegram': 1.2,
        'reddit': 1.0,
        'discord': 0.8
    }
    
    multiplier = platform_multipliers.get(campaign.platform, 1.0)
    
    base_reach = 1000 * multiplier
    reach_growth = age_hours * 100 * multiplier
    
    return {
        'reach': int(base_reach + reach_growth + random.randint(-500, 1000)),
        'engagement': int((base_reach + reach_growth) * 0.1 + random.randint(-50, 200)),
        'clicks': int((base_reach + reach_growth) * 0.05 + random.randint(-20, 100)),
        'shares': int((base_reach + reach_growth) * 0.02 + random.randint(-10, 50)),
        'conversion_rate': round(random.uniform(0.5, 5.0), 2),
        'cost_per_engagement': round(random.uniform(0.01, 0.50), 3),
        'viral_score': round(random.uniform(0.1, 1.0), 2)
    }

