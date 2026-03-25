#!/usr/bin/env python3
"""
Advanced Alert and Notification System for Socrates AI
Implements intelligent alerts, notifications, and automated monitoring
"""

import sqlite3
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import threading
import time
import schedule
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import numpy as np
import pandas as pd
from ml_prediction_models_fixed import AdvancedMLPredictor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AlertType(Enum):
    """Types of alerts"""
    PRICE_THRESHOLD = "price_threshold"
    PRICE_CHANGE = "price_change"
    VOLUME_SPIKE = "volume_spike"
    TECHNICAL_SIGNAL = "technical_signal"
    ECM_TURNING_POINT = "ecm_turning_point"
    MARKET_REGIME_CHANGE = "market_regime_change"
    VOLATILITY_SPIKE = "volatility_spike"
    CORRELATION_BREAK = "correlation_break"
    ML_PREDICTION = "ml_prediction"
    SYSTEM_STATUS = "system_status"

class AlertPriority(Enum):
    """Alert priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class NotificationChannel(Enum):
    """Notification delivery channels"""
    EMAIL = "email"
    WEBHOOK = "webhook"
    WEBSOCKET = "websocket"
    SMS = "sms"
    SLACK = "slack"
    DISCORD = "discord"
    TELEGRAM = "telegram"

@dataclass
class AlertCondition:
    """Alert condition definition"""
    id: str
    name: str
    alert_type: AlertType
    symbol: str
    condition: Dict[str, Any]
    priority: AlertPriority
    enabled: bool
    created_at: str
    last_triggered: Optional[str] = None
    trigger_count: int = 0
    cooldown_minutes: int = 60
    notification_channels: List[NotificationChannel] = None

@dataclass
class AlertEvent:
    """Alert event when condition is triggered"""
    id: str
    condition_id: str
    symbol: str
    alert_type: AlertType
    priority: AlertPriority
    message: str
    data: Dict[str, Any]
    timestamp: str
    acknowledged: bool = False
    resolved: bool = False

@dataclass
class NotificationConfig:
    """Notification channel configuration"""
    channel: NotificationChannel
    config: Dict[str, Any]
    enabled: bool = True

class AlertEngine:
    """Core alert engine for condition evaluation"""
    
    def __init__(self, db_path: str = "socrates_data.db"):
        self.db_path = db_path
        self.ml_predictor = AdvancedMLPredictor(db_path)
        self.alert_conditions = {}
        self.notification_configs = {}
        self.active_alerts = {}
        self.alert_history = []
        
        # Initialize database
        self._init_database()
        
        # Load existing conditions
        self._load_alert_conditions()
    
    def _init_database(self):
        """Initialize alert database tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Alert conditions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS alert_conditions (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    alert_type TEXT NOT NULL,
                    symbol TEXT NOT NULL,
                    condition_json TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    enabled BOOLEAN DEFAULT 1,
                    created_at TEXT NOT NULL,
                    last_triggered TEXT,
                    trigger_count INTEGER DEFAULT 0,
                    cooldown_minutes INTEGER DEFAULT 60,
                    notification_channels TEXT
                )
            ''')
            
            # Alert events table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS alert_events (
                    id TEXT PRIMARY KEY,
                    condition_id TEXT NOT NULL,
                    symbol TEXT NOT NULL,
                    alert_type TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    message TEXT NOT NULL,
                    data_json TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    acknowledged BOOLEAN DEFAULT 0,
                    resolved BOOLEAN DEFAULT 0,
                    FOREIGN KEY (condition_id) REFERENCES alert_conditions (id)
                )
            ''')
            
            # Notification configs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS notification_configs (
                    channel TEXT PRIMARY KEY,
                    config_json TEXT NOT NULL,
                    enabled BOOLEAN DEFAULT 1
                )
            ''')
            
            conn.commit()
            conn.close()
            
            logger.info("Alert database initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing alert database: {e}")
    
    def _load_alert_conditions(self):
        """Load alert conditions from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM alert_conditions WHERE enabled = 1')
            rows = cursor.fetchall()
            
            for row in rows:
                condition = AlertCondition(
                    id=row[0],
                    name=row[1],
                    alert_type=AlertType(row[2]),
                    symbol=row[3],
                    condition=json.loads(row[4]),
                    priority=AlertPriority(row[5]),
                    enabled=bool(row[6]),
                    created_at=row[7],
                    last_triggered=row[8],
                    trigger_count=row[9],
                    cooldown_minutes=row[10],
                    notification_channels=[NotificationChannel(ch) for ch in json.loads(row[11] or '[]')]
                )
                
                self.alert_conditions[condition.id] = condition
            
            conn.close()
            logger.info(f"Loaded {len(self.alert_conditions)} alert conditions")
            
        except Exception as e:
            logger.error(f"Error loading alert conditions: {e}")
    
    def add_alert_condition(self, condition: AlertCondition) -> bool:
        """Add new alert condition"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO alert_conditions 
                (id, name, alert_type, symbol, condition_json, priority, enabled, 
                 created_at, cooldown_minutes, notification_channels)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                condition.id,
                condition.name,
                condition.alert_type.value,
                condition.symbol,
                json.dumps(condition.condition),
                condition.priority.value,
                condition.enabled,
                condition.created_at,
                condition.cooldown_minutes,
                json.dumps([ch.value for ch in (condition.notification_channels or [])])
            ))
            
            conn.commit()
            conn.close()
            
            self.alert_conditions[condition.id] = condition
            logger.info(f"Added alert condition: {condition.name}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding alert condition: {e}")
            return False
    
    def evaluate_price_threshold(self, symbol: str, condition: Dict[str, Any]) -> Optional[AlertEvent]:
        """Evaluate price threshold conditions"""
        try:
            # Get current price
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT close_price FROM market_data 
                WHERE symbol = ? 
                ORDER BY date DESC LIMIT 1
            ''', (symbol,))
            
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                return None
            
            current_price = float(result[0])
            threshold_price = float(condition['threshold_price'])
            direction = condition['direction']  # 'above' or 'below'
            
            triggered = False
            if direction == 'above' and current_price > threshold_price:
                triggered = True
            elif direction == 'below' and current_price < threshold_price:
                triggered = True
            
            if triggered:
                return AlertEvent(
                    id=f"price_threshold_{symbol}_{int(time.time())}",
                    condition_id=condition.get('condition_id', ''),
                    symbol=symbol,
                    alert_type=AlertType.PRICE_THRESHOLD,
                    priority=AlertPriority(condition.get('priority', 'medium')),
                    message=f"{symbol} price ${current_price:.2f} is {direction} threshold ${threshold_price:.2f}",
                    data={
                        'current_price': current_price,
                        'threshold_price': threshold_price,
                        'direction': direction
                    },
                    timestamp=datetime.now().isoformat()
                )
            
            return None
            
        except Exception as e:
            logger.error(f"Error evaluating price threshold for {symbol}: {e}")
            return None
    
    def evaluate_price_change(self, symbol: str, condition: Dict[str, Any]) -> Optional[AlertEvent]:
        """Evaluate price change conditions"""
        try:
            # Get recent prices
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT close_price FROM market_data 
                WHERE symbol = ? 
                ORDER BY date DESC LIMIT 2
            ''', (symbol,))
            
            results = cursor.fetchall()
            conn.close()
            
            if len(results) < 2:
                return None
            
            current_price = float(results[0][0])
            previous_price = float(results[1][0])
            
            price_change_pct = ((current_price - previous_price) / previous_price) * 100
            threshold_pct = float(condition['threshold_percent'])
            direction = condition.get('direction', 'any')  # 'up', 'down', 'any'
            
            triggered = False
            if direction == 'up' and price_change_pct > threshold_pct:
                triggered = True
            elif direction == 'down' and price_change_pct < -threshold_pct:
                triggered = True
            elif direction == 'any' and abs(price_change_pct) > threshold_pct:
                triggered = True
            
            if triggered:
                return AlertEvent(
                    id=f"price_change_{symbol}_{int(time.time())}",
                    condition_id=condition.get('condition_id', ''),
                    symbol=symbol,
                    alert_type=AlertType.PRICE_CHANGE,
                    priority=AlertPriority(condition.get('priority', 'medium')),
                    message=f"{symbol} price changed {price_change_pct:.2f}% (${previous_price:.2f} → ${current_price:.2f})",
                    data={
                        'current_price': current_price,
                        'previous_price': previous_price,
                        'price_change_pct': price_change_pct,
                        'threshold_pct': threshold_pct
                    },
                    timestamp=datetime.now().isoformat()
                )
            
            return None
            
        except Exception as e:
            logger.error(f"Error evaluating price change for {symbol}: {e}")
            return None
    
    def evaluate_volume_spike(self, symbol: str, condition: Dict[str, Any]) -> Optional[AlertEvent]:
        """Evaluate volume spike conditions"""
        try:
            # Get recent volume data
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT volume FROM market_data 
                WHERE symbol = ? 
                ORDER BY date DESC LIMIT 21
            ''', (symbol,))
            
            results = cursor.fetchall()
            conn.close()
            
            if len(results) < 21:
                return None
            
            volumes = [float(r[0]) for r in results]
            current_volume = volumes[0]
            avg_volume = np.mean(volumes[1:21])  # 20-day average
            
            volume_ratio = current_volume / avg_volume if avg_volume > 0 else 0
            threshold_ratio = float(condition.get('threshold_ratio', 2.0))
            
            if volume_ratio > threshold_ratio:
                return AlertEvent(
                    id=f"volume_spike_{symbol}_{int(time.time())}",
                    condition_id=condition.get('condition_id', ''),
                    symbol=symbol,
                    alert_type=AlertType.VOLUME_SPIKE,
                    priority=AlertPriority(condition.get('priority', 'medium')),
                    message=f"{symbol} volume spike: {volume_ratio:.1f}x average ({current_volume:,.0f} vs {avg_volume:,.0f})",
                    data={
                        'current_volume': current_volume,
                        'average_volume': avg_volume,
                        'volume_ratio': volume_ratio,
                        'threshold_ratio': threshold_ratio
                    },
                    timestamp=datetime.now().isoformat()
                )
            
            return None
            
        except Exception as e:
            logger.error(f"Error evaluating volume spike for {symbol}: {e}")
            return None
    
    def evaluate_technical_signal(self, symbol: str, condition: Dict[str, Any]) -> Optional[AlertEvent]:
        """Evaluate technical analysis signals"""
        try:
            # Get recent market data
            df = self.ml_predictor.get_market_data(symbol, days=100)
            if df.empty:
                return None
            
            # Create technical features
            df = self.ml_predictor.feature_engineer.create_technical_features(df)
            
            signal_type = condition.get('signal_type', 'rsi_oversold')
            
            if signal_type == 'rsi_oversold':
                rsi = df['rsi_14'].iloc[-1]
                threshold = condition.get('threshold', 30)
                if rsi < threshold:
                    return AlertEvent(
                        id=f"rsi_oversold_{symbol}_{int(time.time())}",
                        condition_id=condition.get('condition_id', ''),
                        symbol=symbol,
                        alert_type=AlertType.TECHNICAL_SIGNAL,
                        priority=AlertPriority(condition.get('priority', 'medium')),
                        message=f"{symbol} RSI oversold: {rsi:.1f} < {threshold}",
                        data={'rsi': rsi, 'threshold': threshold, 'signal_type': signal_type},
                        timestamp=datetime.now().isoformat()
                    )
            
            elif signal_type == 'rsi_overbought':
                rsi = df['rsi_14'].iloc[-1]
                threshold = condition.get('threshold', 70)
                if rsi > threshold:
                    return AlertEvent(
                        id=f"rsi_overbought_{symbol}_{int(time.time())}",
                        condition_id=condition.get('condition_id', ''),
                        symbol=symbol,
                        alert_type=AlertType.TECHNICAL_SIGNAL,
                        priority=AlertPriority(condition.get('priority', 'medium')),
                        message=f"{symbol} RSI overbought: {rsi:.1f} > {threshold}",
                        data={'rsi': rsi, 'threshold': threshold, 'signal_type': signal_type},
                        timestamp=datetime.now().isoformat()
                    )
            
            elif signal_type == 'macd_crossover':
                macd = df['macd'].iloc[-1]
                macd_signal = df['macd_signal'].iloc[-1]
                prev_macd = df['macd'].iloc[-2]
                prev_signal = df['macd_signal'].iloc[-2]
                
                # Bullish crossover
                if macd > macd_signal and prev_macd <= prev_signal:
                    return AlertEvent(
                        id=f"macd_bullish_{symbol}_{int(time.time())}",
                        condition_id=condition.get('condition_id', ''),
                        symbol=symbol,
                        alert_type=AlertType.TECHNICAL_SIGNAL,
                        priority=AlertPriority(condition.get('priority', 'medium')),
                        message=f"{symbol} MACD bullish crossover",
                        data={'macd': macd, 'signal': macd_signal, 'signal_type': 'macd_bullish'},
                        timestamp=datetime.now().isoformat()
                    )
                
                # Bearish crossover
                elif macd < macd_signal and prev_macd >= prev_signal:
                    return AlertEvent(
                        id=f"macd_bearish_{symbol}_{int(time.time())}",
                        condition_id=condition.get('condition_id', ''),
                        symbol=symbol,
                        alert_type=AlertType.TECHNICAL_SIGNAL,
                        priority=AlertPriority(condition.get('priority', 'medium')),
                        message=f"{symbol} MACD bearish crossover",
                        data={'macd': macd, 'signal': macd_signal, 'signal_type': 'macd_bearish'},
                        timestamp=datetime.now().isoformat()
                    )
            
            return None
            
        except Exception as e:
            logger.error(f"Error evaluating technical signal for {symbol}: {e}")
            return None
    
    def evaluate_ml_prediction(self, symbol: str, condition: Dict[str, Any]) -> Optional[AlertEvent]:
        """Evaluate ML prediction alerts"""
        try:
            # Get ML prediction
            prediction_result = self.ml_predictor.predict_future_prices(symbol, horizon_days=5)
            
            if not prediction_result.predictions:
                return None
            
            current_price = prediction_result.metadata.get('base_price', 0)
            predicted_price = prediction_result.predictions[4]  # 5-day prediction
            
            if current_price > 0:
                predicted_change_pct = ((predicted_price - current_price) / current_price) * 100
                threshold_pct = float(condition.get('threshold_percent', 5.0))
                direction = condition.get('direction', 'any')
                
                triggered = False
                if direction == 'up' and predicted_change_pct > threshold_pct:
                    triggered = True
                elif direction == 'down' and predicted_change_pct < -threshold_pct:
                    triggered = True
                elif direction == 'any' and abs(predicted_change_pct) > threshold_pct:
                    triggered = True
                
                if triggered:
                    return AlertEvent(
                        id=f"ml_prediction_{symbol}_{int(time.time())}",
                        condition_id=condition.get('condition_id', ''),
                        symbol=symbol,
                        alert_type=AlertType.ML_PREDICTION,
                        priority=AlertPriority(condition.get('priority', 'medium')),
                        message=f"{symbol} ML prediction: {predicted_change_pct:.1f}% change in 5 days (${current_price:.2f} → ${predicted_price:.2f})",
                        data={
                            'current_price': current_price,
                            'predicted_price': predicted_price,
                            'predicted_change_pct': predicted_change_pct,
                            'model_performance': prediction_result.model_performance
                        },
                        timestamp=datetime.now().isoformat()
                    )
            
            return None
            
        except Exception as e:
            logger.error(f"Error evaluating ML prediction for {symbol}: {e}")
            return None
    
    def evaluate_all_conditions(self) -> List[AlertEvent]:
        """Evaluate all active alert conditions"""
        triggered_alerts = []
        
        for condition_id, condition in self.alert_conditions.items():
            if not condition.enabled:
                continue
            
            # Check cooldown
            if condition.last_triggered:
                last_trigger = datetime.fromisoformat(condition.last_triggered)
                cooldown_end = last_trigger + timedelta(minutes=condition.cooldown_minutes)
                if datetime.now() < cooldown_end:
                    continue
            
            try:
                alert_event = None
                
                if condition.alert_type == AlertType.PRICE_THRESHOLD:
                    alert_event = self.evaluate_price_threshold(condition.symbol, condition.condition)
                elif condition.alert_type == AlertType.PRICE_CHANGE:
                    alert_event = self.evaluate_price_change(condition.symbol, condition.condition)
                elif condition.alert_type == AlertType.VOLUME_SPIKE:
                    alert_event = self.evaluate_volume_spike(condition.symbol, condition.condition)
                elif condition.alert_type == AlertType.TECHNICAL_SIGNAL:
                    alert_event = self.evaluate_technical_signal(condition.symbol, condition.condition)
                elif condition.alert_type == AlertType.ML_PREDICTION:
                    alert_event = self.evaluate_ml_prediction(condition.symbol, condition.condition)
                
                if alert_event:
                    alert_event.condition_id = condition_id
                    triggered_alerts.append(alert_event)
                    
                    # Update condition
                    self._update_condition_trigger(condition_id)
                    
            except Exception as e:
                logger.error(f"Error evaluating condition {condition_id}: {e}")
        
        return triggered_alerts
    
    def _update_condition_trigger(self, condition_id: str):
        """Update condition trigger timestamp and count"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE alert_conditions 
                SET last_triggered = ?, trigger_count = trigger_count + 1
                WHERE id = ?
            ''', (datetime.now().isoformat(), condition_id))
            
            conn.commit()
            conn.close()
            
            # Update in memory
            if condition_id in self.alert_conditions:
                self.alert_conditions[condition_id].last_triggered = datetime.now().isoformat()
                self.alert_conditions[condition_id].trigger_count += 1
                
        except Exception as e:
            logger.error(f"Error updating condition trigger: {e}")
    
    def save_alert_event(self, alert_event: AlertEvent):
        """Save alert event to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO alert_events 
                (id, condition_id, symbol, alert_type, priority, message, data_json, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                alert_event.id,
                alert_event.condition_id,
                alert_event.symbol,
                alert_event.alert_type.value,
                alert_event.priority.value,
                alert_event.message,
                json.dumps(alert_event.data),
                alert_event.timestamp
            ))
            
            conn.commit()
            conn.close()
            
            self.alert_history.append(alert_event)
            logger.info(f"Saved alert event: {alert_event.message}")
            
        except Exception as e:
            logger.error(f"Error saving alert event: {e}")

class NotificationManager:
    """Manages notification delivery across multiple channels"""
    
    def __init__(self):
        self.notification_configs = {}
        self.delivery_stats = {}
    
    def add_notification_config(self, config: NotificationConfig):
        """Add notification channel configuration"""
        self.notification_configs[config.channel] = config
        logger.info(f"Added notification config for {config.channel.value}")
    
    def send_email_notification(self, alert_event: AlertEvent, config: Dict[str, Any]) -> bool:
        """Send email notification"""
        try:
            smtp_server = config.get('smtp_server', 'smtp.gmail.com')
            smtp_port = config.get('smtp_port', 587)
            username = config.get('username')
            password = config.get('password')
            to_emails = config.get('to_emails', [])
            
            if not username or not password or not to_emails:
                logger.error("Email configuration incomplete")
                return False
            
            msg = MIMEMultipart()
            msg['From'] = username
            msg['To'] = ', '.join(to_emails)
            msg['Subject'] = f"Socrates AI Alert: {alert_event.symbol} - {alert_event.alert_type.value}"
            
            body = f"""
            Alert: {alert_event.message}
            
            Symbol: {alert_event.symbol}
            Type: {alert_event.alert_type.value}
            Priority: {alert_event.priority.value}
            Time: {alert_event.timestamp}
            
            Data: {json.dumps(alert_event.data, indent=2)}
            
            ---
            Socrates AI Alert System
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(username, password)
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Email notification sent for alert: {alert_event.id}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email notification: {e}")
            return False
    
    def send_webhook_notification(self, alert_event: AlertEvent, config: Dict[str, Any]) -> bool:
        """Send webhook notification"""
        try:
            webhook_url = config.get('webhook_url')
            headers = config.get('headers', {'Content-Type': 'application/json'})
            
            if not webhook_url:
                logger.error("Webhook URL not configured")
                return False
            
            payload = {
                'alert_id': alert_event.id,
                'symbol': alert_event.symbol,
                'alert_type': alert_event.alert_type.value,
                'priority': alert_event.priority.value,
                'message': alert_event.message,
                'data': alert_event.data,
                'timestamp': alert_event.timestamp
            }
            
            response = requests.post(webhook_url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            
            logger.info(f"Webhook notification sent for alert: {alert_event.id}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending webhook notification: {e}")
            return False
    
    def send_slack_notification(self, alert_event: AlertEvent, config: Dict[str, Any]) -> bool:
        """Send Slack notification"""
        try:
            webhook_url = config.get('webhook_url')
            
            if not webhook_url:
                logger.error("Slack webhook URL not configured")
                return False
            
            color = {
                AlertPriority.LOW: "good",
                AlertPriority.MEDIUM: "warning", 
                AlertPriority.HIGH: "danger",
                AlertPriority.CRITICAL: "danger"
            }.get(alert_event.priority, "warning")
            
            payload = {
                "attachments": [{
                    "color": color,
                    "title": f"Socrates AI Alert: {alert_event.symbol}",
                    "text": alert_event.message,
                    "fields": [
                        {"title": "Type", "value": alert_event.alert_type.value, "short": True},
                        {"title": "Priority", "value": alert_event.priority.value, "short": True},
                        {"title": "Time", "value": alert_event.timestamp, "short": False}
                    ]
                }]
            }
            
            response = requests.post(webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            
            logger.info(f"Slack notification sent for alert: {alert_event.id}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending Slack notification: {e}")
            return False
    
    def send_notification(self, alert_event: AlertEvent, channels: List[NotificationChannel]):
        """Send notification to specified channels"""
        for channel in channels:
            if channel not in self.notification_configs:
                logger.warning(f"No configuration for notification channel: {channel.value}")
                continue
            
            config = self.notification_configs[channel]
            if not config.enabled:
                continue
            
            success = False
            try:
                if channel == NotificationChannel.EMAIL:
                    success = self.send_email_notification(alert_event, config.config)
                elif channel == NotificationChannel.WEBHOOK:
                    success = self.send_webhook_notification(alert_event, config.config)
                elif channel == NotificationChannel.SLACK:
                    success = self.send_slack_notification(alert_event, config.config)
                
                # Update delivery stats
                if channel.value not in self.delivery_stats:
                    self.delivery_stats[channel.value] = {'sent': 0, 'failed': 0}
                
                if success:
                    self.delivery_stats[channel.value]['sent'] += 1
                else:
                    self.delivery_stats[channel.value]['failed'] += 1
                    
            except Exception as e:
                logger.error(f"Error sending notification via {channel.value}: {e}")
                if channel.value not in self.delivery_stats:
                    self.delivery_stats[channel.value] = {'sent': 0, 'failed': 0}
                self.delivery_stats[channel.value]['failed'] += 1

class AlertMonitor:
    """Main alert monitoring service"""
    
    def __init__(self, db_path: str = "socrates_data.db"):
        self.db_path = db_path
        self.alert_engine = AlertEngine(db_path)
        self.notification_manager = NotificationManager()
        self.running = False
        self.monitor_thread = None
        
        # Setup default notification configs
        self._setup_default_configs()
    
    def _setup_default_configs(self):
        """Setup default notification configurations"""
        # Webhook config (for testing)
        webhook_config = NotificationConfig(
            channel=NotificationChannel.WEBHOOK,
            config={
                'webhook_url': 'http://localhost:5000/api/alerts/webhook',
                'headers': {'Content-Type': 'application/json'}
            }
        )
        self.notification_manager.add_notification_config(webhook_config)
    
    def add_sample_alerts(self):
        """Add sample alert conditions for testing"""
        sample_conditions = [
            AlertCondition(
                id="price_threshold_aapl_200",
                name="AAPL Price Above $200",
                alert_type=AlertType.PRICE_THRESHOLD,
                symbol="AAPL",
                condition={
                    'threshold_price': 200.0,
                    'direction': 'above',
                    'priority': 'medium'
                },
                priority=AlertPriority.MEDIUM,
                enabled=True,
                created_at=datetime.now().isoformat(),
                cooldown_minutes=60,
                notification_channels=[NotificationChannel.WEBHOOK]
            ),
            AlertCondition(
                id="price_change_aapl_5pct",
                name="AAPL Price Change >5%",
                alert_type=AlertType.PRICE_CHANGE,
                symbol="AAPL",
                condition={
                    'threshold_percent': 5.0,
                    'direction': 'any',
                    'priority': 'high'
                },
                priority=AlertPriority.HIGH,
                enabled=True,
                created_at=datetime.now().isoformat(),
                cooldown_minutes=30,
                notification_channels=[NotificationChannel.WEBHOOK]
            ),
            AlertCondition(
                id="volume_spike_aapl",
                name="AAPL Volume Spike",
                alert_type=AlertType.VOLUME_SPIKE,
                symbol="AAPL",
                condition={
                    'threshold_ratio': 2.0,
                    'priority': 'medium'
                },
                priority=AlertPriority.MEDIUM,
                enabled=True,
                created_at=datetime.now().isoformat(),
                cooldown_minutes=120,
                notification_channels=[NotificationChannel.WEBHOOK]
            ),
            AlertCondition(
                id="rsi_oversold_aapl",
                name="AAPL RSI Oversold",
                alert_type=AlertType.TECHNICAL_SIGNAL,
                symbol="AAPL",
                condition={
                    'signal_type': 'rsi_oversold',
                    'threshold': 30,
                    'priority': 'medium'
                },
                priority=AlertPriority.MEDIUM,
                enabled=True,
                created_at=datetime.now().isoformat(),
                cooldown_minutes=240,
                notification_channels=[NotificationChannel.WEBHOOK]
            ),
            AlertCondition(
                id="ml_prediction_aapl",
                name="AAPL ML Prediction Alert",
                alert_type=AlertType.ML_PREDICTION,
                symbol="AAPL",
                condition={
                    'threshold_percent': 3.0,
                    'direction': 'any',
                    'priority': 'high'
                },
                priority=AlertPriority.HIGH,
                enabled=True,
                created_at=datetime.now().isoformat(),
                cooldown_minutes=480,
                notification_channels=[NotificationChannel.WEBHOOK]
            )
        ]
        
        for condition in sample_conditions:
            self.alert_engine.add_alert_condition(condition)
        
        logger.info(f"Added {len(sample_conditions)} sample alert conditions")
    
    def start_monitoring(self, interval_seconds: int = 60):
        """Start the alert monitoring service"""
        if self.running:
            logger.warning("Alert monitoring is already running")
            return
        
        self.running = True
        
        def monitor_loop():
            while self.running:
                try:
                    # Evaluate all conditions
                    triggered_alerts = self.alert_engine.evaluate_all_conditions()
                    
                    # Process triggered alerts
                    for alert_event in triggered_alerts:
                        # Save to database
                        self.alert_engine.save_alert_event(alert_event)
                        
                        # Get notification channels for this condition
                        condition = self.alert_engine.alert_conditions.get(alert_event.condition_id)
                        if condition and condition.notification_channels:
                            self.notification_manager.send_notification(
                                alert_event, 
                                condition.notification_channels
                            )
                        
                        logger.info(f"Processed alert: {alert_event.message}")
                    
                    if triggered_alerts:
                        logger.info(f"Processed {len(triggered_alerts)} alerts")
                    
                except Exception as e:
                    logger.error(f"Error in monitoring loop: {e}")
                
                # Wait for next iteration
                time.sleep(interval_seconds)
        
        self.monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        logger.info(f"Alert monitoring started with {interval_seconds}s interval")
    
    def stop_monitoring(self):
        """Stop the alert monitoring service"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.info("Alert monitoring stopped")
    
    def get_alert_status(self) -> Dict[str, Any]:
        """Get current alert system status"""
        return {
            'running': self.running,
            'active_conditions': len(self.alert_engine.alert_conditions),
            'recent_alerts': len([a for a in self.alert_engine.alert_history if 
                                datetime.fromisoformat(a.timestamp) > datetime.now() - timedelta(hours=24)]),
            'notification_stats': self.notification_manager.delivery_stats,
            'conditions': [asdict(condition) for condition in self.alert_engine.alert_conditions.values()]
        }

def main():
    """Test the alert and notification system"""
    print("Advanced Alert and Notification System for Socrates AI")
    print("=" * 55)
    
    # Initialize alert monitor
    monitor = AlertMonitor()
    
    print("1. Adding sample alert conditions...")
    monitor.add_sample_alerts()
    print("   ✓ Sample conditions added")
    
    print("\n2. Testing alert evaluation...")
    triggered_alerts = monitor.alert_engine.evaluate_all_conditions()
    print(f"   ✓ Evaluated conditions, found {len(triggered_alerts)} triggered alerts")
    
    for alert in triggered_alerts:
        print(f"   Alert: {alert.message}")
    
    print("\n3. Getting alert system status...")
    status = monitor.get_alert_status()
    print(f"   ✓ Active conditions: {status['active_conditions']}")
    print(f"   ✓ Recent alerts: {status['recent_alerts']}")
    print(f"   ✓ Notification stats: {status['notification_stats']}")
    
    print("\n4. Starting monitoring service...")
    monitor.start_monitoring(interval_seconds=30)
    print("   ✓ Monitoring started (30s interval)")
    
    # Run for a short time to test
    print("\n5. Running monitoring for 60 seconds...")
    time.sleep(60)
    
    print("\n6. Stopping monitoring service...")
    monitor.stop_monitoring()
    print("   ✓ Monitoring stopped")
    
    print("\nAlert and notification system test completed!")
    print("System is ready for integration with Socrates AI!")

if __name__ == "__main__":
    main()

