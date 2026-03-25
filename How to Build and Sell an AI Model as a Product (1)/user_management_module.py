"""
User Management and Analytics Module
Comprehensive user lifecycle management, analytics, and business intelligence system
"""

import json
import asyncio
import hashlib
import secrets
import jwt
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import sqlite3
import bcrypt
from collections import defaultdict
import statistics

class UserRole(Enum):
    FREE_TRIAL = "free_trial"
    BASIC = "basic"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"
    ADMIN = "admin"

class UserStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    CHURNED = "churned"
    TRIAL_EXPIRED = "trial_expired"

class SubscriptionStatus(Enum):
    TRIAL = "trial"
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELLED = "cancelled"
    EXPIRED = "expired"

class EventType(Enum):
    LOGIN = "login"
    LOGOUT = "logout"
    FEATURE_USAGE = "feature_usage"
    SUBSCRIPTION_CHANGE = "subscription_change"
    PAYMENT = "payment"
    SUPPORT_TICKET = "support_ticket"
    API_CALL = "api_call"
    DASHBOARD_VIEW = "dashboard_view"
    REPORT_GENERATED = "report_generated"

@dataclass
class User:
    id: str
    email: str
    password_hash: str
    first_name: str
    last_name: str
    role: UserRole
    status: UserStatus
    created_at: datetime
    last_login: Optional[datetime]
    trial_end_date: Optional[datetime]
    subscription_id: Optional[str]
    company: Optional[str]
    phone: Optional[str]
    country: str
    timezone: str
    preferences: Dict[str, Any]
    metadata: Dict[str, Any]

@dataclass
class Subscription:
    id: str
    user_id: str
    plan_name: str
    status: SubscriptionStatus
    current_period_start: datetime
    current_period_end: datetime
    trial_end: Optional[datetime]
    cancel_at_period_end: bool
    amount: float
    currency: str
    payment_method_id: Optional[str]
    created_at: datetime
    updated_at: datetime

@dataclass
class UserEvent:
    id: str
    user_id: str
    event_type: EventType
    event_data: Dict[str, Any]
    timestamp: datetime
    session_id: Optional[str]
    ip_address: Optional[str]
    user_agent: Optional[str]
    metadata: Dict[str, Any]

@dataclass
class UserAnalytics:
    user_id: str
    total_sessions: int
    total_session_duration: int  # in seconds
    avg_session_duration: float
    features_used: List[str]
    most_used_feature: str
    last_active: datetime
    engagement_score: float
    churn_risk_score: float
    lifetime_value: float
    conversion_probability: float

class UserManagementModule:
    """Comprehensive user management and analytics system"""
    
    def __init__(self, db_path: str = "socrates_ai_users.db"):
        self.db_path = db_path
        self.jwt_secret = secrets.token_urlsafe(32)
        self.analytics_engine = UserAnalyticsEngine()
        self.churn_predictor = ChurnPredictor()
        self.engagement_tracker = EngagementTracker()
        self.lifecycle_manager = UserLifecycleManager()
        self._initialize_database()
        
    def _initialize_database(self):
        """Initialize SQLite database with all required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                role TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL,
                last_login TIMESTAMP,
                trial_end_date TIMESTAMP,
                subscription_id TEXT,
                company TEXT,
                phone TEXT,
                country TEXT NOT NULL,
                timezone TEXT NOT NULL,
                preferences TEXT,
                metadata TEXT
            )
        ''')
        
        # Subscriptions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subscriptions (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                plan_name TEXT NOT NULL,
                status TEXT NOT NULL,
                current_period_start TIMESTAMP NOT NULL,
                current_period_end TIMESTAMP NOT NULL,
                trial_end TIMESTAMP,
                cancel_at_period_end BOOLEAN NOT NULL,
                amount REAL NOT NULL,
                currency TEXT NOT NULL,
                payment_method_id TEXT,
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # User events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_events (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                event_data TEXT NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                session_id TEXT,
                ip_address TEXT,
                user_agent TEXT,
                metadata TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # User sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                session_token TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                ip_address TEXT,
                user_agent TEXT,
                is_active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # User analytics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_analytics (
                user_id TEXT PRIMARY KEY,
                total_sessions INTEGER DEFAULT 0,
                total_session_duration INTEGER DEFAULT 0,
                avg_session_duration REAL DEFAULT 0,
                features_used TEXT,
                most_used_feature TEXT,
                last_active TIMESTAMP,
                engagement_score REAL DEFAULT 0,
                churn_risk_score REAL DEFAULT 0,
                lifetime_value REAL DEFAULT 0,
                conversion_probability REAL DEFAULT 0,
                updated_at TIMESTAMP NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    async def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user account"""
        
        # Validate email uniqueness
        if await self._email_exists(user_data['email']):
            return {"success": False, "error": "Email already exists"}
        
        # Generate user ID
        user_id = secrets.token_urlsafe(16)
        
        # Hash password
        password_hash = bcrypt.hashpw(
            user_data['password'].encode('utf-8'), 
            bcrypt.gensalt()
        ).decode('utf-8')
        
        # Determine trial end date
        trial_end_date = datetime.now() + timedelta(days=14)
        
        # Create user object
        user = User(
            id=user_id,
            email=user_data['email'],
            password_hash=password_hash,
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            role=UserRole.FREE_TRIAL,
            status=UserStatus.ACTIVE,
            created_at=datetime.now(),
            last_login=None,
            trial_end_date=trial_end_date,
            subscription_id=None,
            company=user_data.get('company'),
            phone=user_data.get('phone'),
            country=user_data.get('country', 'US'),
            timezone=user_data.get('timezone', 'UTC'),
            preferences=user_data.get('preferences', {}),
            metadata={}
        )
        
        # Save to database
        success = await self._save_user(user)
        
        if success:
            # Initialize user analytics
            await self.analytics_engine.initialize_user_analytics(user_id)
            
            # Track user creation event
            await self.track_event(user_id, EventType.FEATURE_USAGE, {
                "feature": "account_creation",
                "source": user_data.get('source', 'direct')
            })
            
            # Start user lifecycle management
            await self.lifecycle_manager.start_user_journey(user)
            
            return {
                "success": True,
                "user_id": user_id,
                "trial_end_date": trial_end_date.isoformat(),
                "message": "User created successfully"
            }
        else:
            return {"success": False, "error": "Failed to create user"}
    
    async def authenticate_user(self, email: str, password: str, ip_address: str = None, user_agent: str = None) -> Dict[str, Any]:
        """Authenticate user and create session"""
        
        user = await self._get_user_by_email(email)
        if not user:
            return {"success": False, "error": "Invalid credentials"}
        
        # Verify password
        if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            return {"success": False, "error": "Invalid credentials"}
        
        # Check user status
        if user.status != UserStatus.ACTIVE:
            return {"success": False, "error": f"Account is {user.status.value}"}
        
        # Create session
        session_token = await self._create_session(user.id, ip_address, user_agent)
        
        # Update last login
        await self._update_last_login(user.id)
        
        # Track login event
        await self.track_event(user.id, EventType.LOGIN, {
            "ip_address": ip_address,
            "user_agent": user_agent
        })
        
        # Generate JWT token
        jwt_token = self._generate_jwt_token(user)
        
        return {
            "success": True,
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role.value,
                "status": user.status.value,
                "trial_end_date": user.trial_end_date.isoformat() if user.trial_end_date else None
            },
            "session_token": session_token,
            "jwt_token": jwt_token,
            "expires_at": (datetime.now() + timedelta(hours=24)).isoformat()
        }
    
    async def track_event(self, user_id: str, event_type: EventType, event_data: Dict[str, Any], session_id: str = None, ip_address: str = None, user_agent: str = None):
        """Track user events for analytics"""
        
        event = UserEvent(
            id=secrets.token_urlsafe(16),
            user_id=user_id,
            event_type=event_type,
            event_data=event_data,
            timestamp=datetime.now(),
            session_id=session_id,
            ip_address=ip_address,
            user_agent=user_agent,
            metadata={}
        )
        
        # Save event to database
        await self._save_event(event)
        
        # Update real-time analytics
        await self.analytics_engine.process_event(event)
        
        # Update engagement tracking
        await self.engagement_tracker.update_engagement(user_id, event_type, event_data)
        
        # Check for lifecycle triggers
        await self.lifecycle_manager.process_event(user_id, event)
    
    async def get_user_analytics(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive user analytics"""
        
        # Get basic analytics
        analytics = await self.analytics_engine.get_user_analytics(user_id)
        
        # Get engagement metrics
        engagement = await self.engagement_tracker.get_engagement_metrics(user_id)
        
        # Get churn prediction
        churn_risk = await self.churn_predictor.predict_churn_risk(user_id)
        
        # Get usage patterns
        usage_patterns = await self._get_usage_patterns(user_id)
        
        # Get revenue metrics
        revenue_metrics = await self._get_revenue_metrics(user_id)
        
        return {
            "user_id": user_id,
            "analytics": analytics,
            "engagement": engagement,
            "churn_risk": churn_risk,
            "usage_patterns": usage_patterns,
            "revenue_metrics": revenue_metrics,
            "last_updated": datetime.now().isoformat()
        }
    
    async def get_business_analytics(self, date_range: Tuple[datetime, datetime] = None) -> Dict[str, Any]:
        """Get comprehensive business analytics"""
        
        if not date_range:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            date_range = (start_date, end_date)
        
        # User metrics
        user_metrics = await self._get_user_metrics(date_range)
        
        # Revenue metrics
        revenue_metrics = await self._get_business_revenue_metrics(date_range)
        
        # Engagement metrics
        engagement_metrics = await self._get_business_engagement_metrics(date_range)
        
        # Churn analysis
        churn_analysis = await self._get_churn_analysis(date_range)
        
        # Feature usage
        feature_usage = await self._get_feature_usage_analytics(date_range)
        
        # Cohort analysis
        cohort_analysis = await self._get_cohort_analysis(date_range)
        
        return {
            "date_range": {
                "start": date_range[0].isoformat(),
                "end": date_range[1].isoformat()
            },
            "user_metrics": user_metrics,
            "revenue_metrics": revenue_metrics,
            "engagement_metrics": engagement_metrics,
            "churn_analysis": churn_analysis,
            "feature_usage": feature_usage,
            "cohort_analysis": cohort_analysis,
            "generated_at": datetime.now().isoformat()
        }
    
    async def update_subscription(self, user_id: str, subscription_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update user subscription"""
        
        user = await self._get_user_by_id(user_id)
        if not user:
            return {"success": False, "error": "User not found"}
        
        # Create or update subscription
        subscription = Subscription(
            id=subscription_data.get('id', secrets.token_urlsafe(16)),
            user_id=user_id,
            plan_name=subscription_data['plan_name'],
            status=SubscriptionStatus(subscription_data['status']),
            current_period_start=datetime.fromisoformat(subscription_data['current_period_start']),
            current_period_end=datetime.fromisoformat(subscription_data['current_period_end']),
            trial_end=datetime.fromisoformat(subscription_data['trial_end']) if subscription_data.get('trial_end') else None,
            cancel_at_period_end=subscription_data.get('cancel_at_period_end', False),
            amount=subscription_data['amount'],
            currency=subscription_data.get('currency', 'USD'),
            payment_method_id=subscription_data.get('payment_method_id'),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Save subscription
        success = await self._save_subscription(subscription)
        
        if success:
            # Update user role based on plan
            new_role = self._get_role_from_plan(subscription.plan_name)
            await self._update_user_role(user_id, new_role)
            
            # Track subscription change
            await self.track_event(user_id, EventType.SUBSCRIPTION_CHANGE, {
                "old_plan": user.role.value,
                "new_plan": subscription.plan_name,
                "amount": subscription.amount,
                "currency": subscription.currency
            })
            
            return {"success": True, "subscription_id": subscription.id}
        else:
            return {"success": False, "error": "Failed to update subscription"}
    
    # Helper methods
    async def _email_exists(self, email: str) -> bool:
        """Check if email already exists"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    
    async def _save_user(self, user: User) -> bool:
        """Save user to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (
                    id, email, password_hash, first_name, last_name, role, status,
                    created_at, last_login, trial_end_date, subscription_id, company,
                    phone, country, timezone, preferences, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user.id, user.email, user.password_hash, user.first_name, user.last_name,
                user.role.value, user.status.value, user.created_at, user.last_login,
                user.trial_end_date, user.subscription_id, user.company, user.phone,
                user.country, user.timezone, json.dumps(user.preferences), json.dumps(user.metadata)
            ))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving user: {e}")
            return False
    
    async def _get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return User(
                id=row[0], email=row[1], password_hash=row[2], first_name=row[3],
                last_name=row[4], role=UserRole(row[5]), status=UserStatus(row[6]),
                created_at=datetime.fromisoformat(row[7]),
                last_login=datetime.fromisoformat(row[8]) if row[8] else None,
                trial_end_date=datetime.fromisoformat(row[9]) if row[9] else None,
                subscription_id=row[10], company=row[11], phone=row[12],
                country=row[13], timezone=row[14],
                preferences=json.loads(row[15]) if row[15] else {},
                metadata=json.loads(row[16]) if row[16] else {}
            )
        return None
    
    async def _get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return User(
                id=row[0], email=row[1], password_hash=row[2], first_name=row[3],
                last_name=row[4], role=UserRole(row[5]), status=UserStatus(row[6]),
                created_at=datetime.fromisoformat(row[7]),
                last_login=datetime.fromisoformat(row[8]) if row[8] else None,
                trial_end_date=datetime.fromisoformat(row[9]) if row[9] else None,
                subscription_id=row[10], company=row[11], phone=row[12],
                country=row[13], timezone=row[14],
                preferences=json.loads(row[15]) if row[15] else {},
                metadata=json.loads(row[16]) if row[16] else {}
            )
        return None
    
    def _generate_jwt_token(self, user: User) -> str:
        """Generate JWT token for user"""
        payload = {
            "user_id": user.id,
            "email": user.email,
            "role": user.role.value,
            "exp": datetime.utcnow() + timedelta(hours=24)
        }
        return jwt.encode(payload, self.jwt_secret, algorithm="HS256")
    
    # Additional helper methods would continue here...

class UserAnalyticsEngine:
    """Advanced analytics engine for user behavior analysis"""
    
    def __init__(self):
        self.metrics_cache = {}
        
    async def initialize_user_analytics(self, user_id: str):
        """Initialize analytics for a new user"""
        # Implementation for initializing user analytics
        pass
    
    async def process_event(self, event: UserEvent):
        """Process user event for real-time analytics"""
        # Implementation for processing events
        pass
    
    async def get_user_analytics(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive user analytics"""
        # Implementation for getting user analytics
        return {
            "total_sessions": 0,
            "avg_session_duration": 0,
            "features_used": [],
            "engagement_score": 0,
            "last_active": datetime.now().isoformat()
        }

class ChurnPredictor:
    """ML-based churn prediction system"""
    
    def __init__(self):
        self.model = None  # Would load ML model here
        
    async def predict_churn_risk(self, user_id: str) -> Dict[str, Any]:
        """Predict churn risk for user"""
        # Implementation for churn prediction
        return {
            "churn_probability": 0.15,
            "risk_level": "low",
            "key_factors": ["low_engagement", "trial_ending_soon"],
            "recommended_actions": ["send_engagement_email", "offer_discount"]
        }

class EngagementTracker:
    """Track and analyze user engagement patterns"""
    
    def __init__(self):
        self.engagement_data = defaultdict(dict)
        
    async def update_engagement(self, user_id: str, event_type: EventType, event_data: Dict[str, Any]):
        """Update engagement metrics for user"""
        # Implementation for updating engagement
        pass
    
    async def get_engagement_metrics(self, user_id: str) -> Dict[str, Any]:
        """Get engagement metrics for user"""
        return {
            "daily_active_days": 15,
            "weekly_active_weeks": 3,
            "monthly_active_months": 1,
            "engagement_score": 0.75,
            "engagement_trend": "increasing"
        }

class UserLifecycleManager:
    """Manage user lifecycle and automated workflows"""
    
    def __init__(self):
        self.lifecycle_rules = {}
        
    async def start_user_journey(self, user: User):
        """Start user onboarding journey"""
        # Implementation for starting user journey
        pass
    
    async def process_event(self, user_id: str, event: UserEvent):
        """Process event for lifecycle triggers"""
        # Implementation for processing lifecycle events
        pass

# Example usage
async def main():
    """Example usage of the User Management Module"""
    
    user_mgmt = UserManagementModule()
    
    # Create a test user
    user_data = {
        "email": "john.doe@example.com",
        "password": "secure_password_123",
        "first_name": "John",
        "last_name": "Doe",
        "company": "Trading Corp",
        "country": "US",
        "timezone": "America/New_York",
        "source": "marketing_campaign"
    }
    
    result = await user_mgmt.create_user(user_data)
    print(f"User creation result: {result}")
    
    if result["success"]:
        user_id = result["user_id"]
        
        # Authenticate user
        auth_result = await user_mgmt.authenticate_user(
            "john.doe@example.com", 
            "secure_password_123",
            "192.168.1.1",
            "Mozilla/5.0..."
        )
        print(f"Authentication result: {auth_result}")
        
        # Track some events
        await user_mgmt.track_event(user_id, EventType.DASHBOARD_VIEW, {
            "page": "main_dashboard",
            "duration": 120
        })
        
        await user_mgmt.track_event(user_id, EventType.FEATURE_USAGE, {
            "feature": "market_analysis",
            "analysis_type": "ECM",
            "duration": 300
        })
        
        # Get user analytics
        analytics = await user_mgmt.get_user_analytics(user_id)
        print(f"User analytics: {analytics}")
        
        # Get business analytics
        business_analytics = await user_mgmt.get_business_analytics()
        print(f"Business analytics: {business_analytics}")

if __name__ == "__main__":
    asyncio.run(main())

