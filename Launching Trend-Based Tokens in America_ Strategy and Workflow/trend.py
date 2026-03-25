from src.models.user import db
from datetime import datetime

class Trend(db.Model):
    __tablename__ = 'trends'
    
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(255), nullable=False)
    search_volume = db.Column(db.String(50), nullable=True)
    sentiment_score = db.Column(db.Float, nullable=True)
    virality_score = db.Column(db.Float, nullable=True)
    source = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_processed = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'keyword': self.keyword,
            'search_volume': self.search_volume,
            'sentiment_score': self.sentiment_score,
            'virality_score': self.virality_score,
            'source': self.source,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_processed': self.is_processed
        }

class Token(db.Model):
    __tablename__ = 'tokens'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    contract_address = db.Column(db.String(255), nullable=True)
    blockchain = db.Column(db.String(50), nullable=False)
    trend_id = db.Column(db.Integer, db.ForeignKey('trends.id'), nullable=False)
    initial_supply = db.Column(db.BigInteger, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='created')  # created, deployed, marketing, trading, sold
    
    trend = db.relationship('Trend', backref=db.backref('tokens', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'symbol': self.symbol,
            'contract_address': self.contract_address,
            'blockchain': self.blockchain,
            'trend_id': self.trend_id,
            'initial_supply': self.initial_supply,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'status': self.status
        }

class MarketingCampaign(db.Model):
    __tablename__ = 'marketing_campaigns'
    
    id = db.Column(db.Integer, primary_key=True)
    token_id = db.Column(db.Integer, db.ForeignKey('tokens.id'), nullable=False)
    platform = db.Column(db.String(100), nullable=False)
    campaign_type = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default='pending')  # pending, active, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    token = db.relationship('Token', backref=db.backref('marketing_campaigns', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'token_id': self.token_id,
            'platform': self.platform,
            'campaign_type': self.campaign_type,
            'content': self.content,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

