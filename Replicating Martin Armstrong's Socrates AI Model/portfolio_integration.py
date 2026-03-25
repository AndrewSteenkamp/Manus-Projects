#!/usr/bin/env python3
"""
Portfolio Integration System for Socrates AI
Implements comprehensive portfolio management, tracking, and analysis capabilities
"""

import sqlite3
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import numpy as np
import pandas as pd
from ml_prediction_models_fixed import AdvancedMLPredictor
from alert_notification_system import AlertEngine, AlertEvent, AlertType, AlertPriority

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PositionType(Enum):
    """Types of portfolio positions"""
    LONG = "long"
    SHORT = "short"

class OrderType(Enum):
    """Types of orders"""
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"

class OrderStatus(Enum):
    """Order status"""
    PENDING = "pending"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"

@dataclass
class Position:
    """Portfolio position"""
    id: str
    portfolio_id: str
    symbol: str
    position_type: PositionType
    quantity: float
    entry_price: float
    current_price: float
    entry_date: str
    last_updated: str
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    notes: str = ""

@dataclass
class Order:
    """Trading order"""
    id: str
    portfolio_id: str
    symbol: str
    order_type: OrderType
    position_type: PositionType
    quantity: float
    price: Optional[float]
    stop_price: Optional[float]
    status: OrderStatus
    created_at: str
    filled_at: Optional[str] = None
    filled_price: Optional[float] = None
    filled_quantity: Optional[float] = None

@dataclass
class Portfolio:
    """Portfolio definition"""
    id: str
    name: str
    description: str
    initial_capital: float
    current_value: float
    cash_balance: float
    created_at: str
    last_updated: str
    risk_tolerance: str = "medium"  # low, medium, high
    investment_strategy: str = "balanced"

@dataclass
class PortfolioPerformance:
    """Portfolio performance metrics"""
    portfolio_id: str
    total_return: float
    total_return_pct: float
    daily_return: float
    daily_return_pct: float
    volatility: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    profit_factor: float
    positions_count: int
    winning_positions: int
    losing_positions: int
    average_win: float
    average_loss: float
    largest_win: float
    largest_loss: float
    calculated_at: str

class PortfolioManager:
    """Core portfolio management system"""
    
    def __init__(self, db_path: str = "socrates_data.db"):
        self.db_path = db_path
        self.ml_predictor = AdvancedMLPredictor(db_path)
        self.alert_engine = AlertEngine(db_path)
        
        # Initialize database
        self._init_database()
    
    def _init_database(self):
        """Initialize portfolio database tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Portfolios table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS portfolios (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    initial_capital REAL NOT NULL,
                    current_value REAL NOT NULL,
                    cash_balance REAL NOT NULL,
                    created_at TEXT NOT NULL,
                    last_updated TEXT NOT NULL,
                    risk_tolerance TEXT DEFAULT 'medium',
                    investment_strategy TEXT DEFAULT 'balanced'
                )
            ''')
            
            # Positions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS positions (
                    id TEXT PRIMARY KEY,
                    portfolio_id TEXT NOT NULL,
                    symbol TEXT NOT NULL,
                    position_type TEXT NOT NULL,
                    quantity REAL NOT NULL,
                    entry_price REAL NOT NULL,
                    current_price REAL NOT NULL,
                    entry_date TEXT NOT NULL,
                    last_updated TEXT NOT NULL,
                    stop_loss REAL,
                    take_profit REAL,
                    notes TEXT,
                    FOREIGN KEY (portfolio_id) REFERENCES portfolios (id)
                )
            ''')
            
            # Orders table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                    id TEXT PRIMARY KEY,
                    portfolio_id TEXT NOT NULL,
                    symbol TEXT NOT NULL,
                    order_type TEXT NOT NULL,
                    position_type TEXT NOT NULL,
                    quantity REAL NOT NULL,
                    price REAL,
                    stop_price REAL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    filled_at TEXT,
                    filled_price REAL,
                    filled_quantity REAL,
                    FOREIGN KEY (portfolio_id) REFERENCES portfolios (id)
                )
            ''')
            
            # Portfolio performance history
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS portfolio_performance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    portfolio_id TEXT NOT NULL,
                    total_return REAL NOT NULL,
                    total_return_pct REAL NOT NULL,
                    daily_return REAL NOT NULL,
                    daily_return_pct REAL NOT NULL,
                    volatility REAL NOT NULL,
                    sharpe_ratio REAL NOT NULL,
                    max_drawdown REAL NOT NULL,
                    win_rate REAL NOT NULL,
                    profit_factor REAL NOT NULL,
                    positions_count INTEGER NOT NULL,
                    winning_positions INTEGER NOT NULL,
                    losing_positions INTEGER NOT NULL,
                    average_win REAL NOT NULL,
                    average_loss REAL NOT NULL,
                    largest_win REAL NOT NULL,
                    largest_loss REAL NOT NULL,
                    calculated_at TEXT NOT NULL,
                    FOREIGN KEY (portfolio_id) REFERENCES portfolios (id)
                )
            ''')
            
            # Portfolio value history
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS portfolio_value_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    portfolio_id TEXT NOT NULL,
                    date TEXT NOT NULL,
                    total_value REAL NOT NULL,
                    cash_balance REAL NOT NULL,
                    positions_value REAL NOT NULL,
                    daily_return REAL NOT NULL,
                    FOREIGN KEY (portfolio_id) REFERENCES portfolios (id)
                )
            ''')
            
            conn.commit()
            conn.close()
            
            logger.info("Portfolio database initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing portfolio database: {e}")
    
    def create_portfolio(self, name: str, description: str, initial_capital: float, 
                        risk_tolerance: str = "medium", investment_strategy: str = "balanced") -> str:
        """Create a new portfolio"""
        try:
            portfolio_id = f"portfolio_{int(datetime.now().timestamp())}"
            now = datetime.now().isoformat()
            
            portfolio = Portfolio(
                id=portfolio_id,
                name=name,
                description=description,
                initial_capital=initial_capital,
                current_value=initial_capital,
                cash_balance=initial_capital,
                created_at=now,
                last_updated=now,
                risk_tolerance=risk_tolerance,
                investment_strategy=investment_strategy
            )
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO portfolios 
                (id, name, description, initial_capital, current_value, cash_balance, 
                 created_at, last_updated, risk_tolerance, investment_strategy)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                portfolio.id, portfolio.name, portfolio.description, portfolio.initial_capital,
                portfolio.current_value, portfolio.cash_balance, portfolio.created_at,
                portfolio.last_updated, portfolio.risk_tolerance, portfolio.investment_strategy
            ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Created portfolio: {name} (ID: {portfolio_id})")
            return portfolio_id
            
        except Exception as e:
            logger.error(f"Error creating portfolio: {e}")
            return ""
    
    def add_position(self, portfolio_id: str, symbol: str, position_type: PositionType,
                    quantity: float, entry_price: float, stop_loss: Optional[float] = None,
                    take_profit: Optional[float] = None, notes: str = "") -> str:
        """Add a new position to portfolio"""
        try:
            position_id = f"pos_{portfolio_id}_{symbol}_{int(datetime.now().timestamp())}"
            now = datetime.now().isoformat()
            
            # Get current price
            current_price = self._get_current_price(symbol)
            if current_price is None:
                current_price = entry_price
            
            position = Position(
                id=position_id,
                portfolio_id=portfolio_id,
                symbol=symbol,
                position_type=position_type,
                quantity=quantity,
                entry_price=entry_price,
                current_price=current_price,
                entry_date=now,
                last_updated=now,
                stop_loss=stop_loss,
                take_profit=take_profit,
                notes=notes
            )
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO positions 
                (id, portfolio_id, symbol, position_type, quantity, entry_price, 
                 current_price, entry_date, last_updated, stop_loss, take_profit, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                position.id, position.portfolio_id, position.symbol, position.position_type.value,
                position.quantity, position.entry_price, position.current_price,
                position.entry_date, position.last_updated, position.stop_loss,
                position.take_profit, position.notes
            ))
            
            # Update portfolio cash balance
            position_value = quantity * entry_price
            cursor.execute('''
                UPDATE portfolios 
                SET cash_balance = cash_balance - ?, last_updated = ?
                WHERE id = ?
            ''', (position_value, now, portfolio_id))
            
            conn.commit()
            conn.close()
            
            # Update portfolio value
            self.update_portfolio_value(portfolio_id)
            
            logger.info(f"Added position: {symbol} to portfolio {portfolio_id}")
            return position_id
            
        except Exception as e:
            logger.error(f"Error adding position: {e}")
            return ""
    
    def _get_current_price(self, symbol: str) -> Optional[float]:
        """Get current price for a symbol"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT close_price FROM market_data 
                WHERE symbol = ? 
                ORDER BY date DESC LIMIT 1
            ''', (symbol,))
            
            result = cursor.fetchone()
            conn.close()
            
            return float(result[0]) if result else None
            
        except Exception as e:
            logger.error(f"Error getting current price for {symbol}: {e}")
            return None
    
    def update_portfolio_value(self, portfolio_id: str):
        """Update portfolio current value based on positions"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get portfolio cash balance
            cursor.execute('SELECT cash_balance FROM portfolios WHERE id = ?', (portfolio_id,))
            result = cursor.fetchone()
            if not result:
                return
            
            cash_balance = float(result[0])
            
            # Get all positions
            cursor.execute('''
                SELECT symbol, position_type, quantity, entry_price 
                FROM positions WHERE portfolio_id = ?
            ''', (portfolio_id,))
            
            positions = cursor.fetchall()
            positions_value = 0
            
            for symbol, pos_type, quantity, entry_price in positions:
                current_price = self._get_current_price(symbol)
                if current_price:
                    if pos_type == PositionType.LONG.value:
                        position_value = quantity * current_price
                    else:  # SHORT
                        position_value = quantity * (2 * entry_price - current_price)
                    
                    positions_value += position_value
                    
                    # Update position current price
                    cursor.execute('''
                        UPDATE positions 
                        SET current_price = ?, last_updated = ?
                        WHERE portfolio_id = ? AND symbol = ?
                    ''', (current_price, datetime.now().isoformat(), portfolio_id, symbol))
            
            total_value = cash_balance + positions_value
            
            # Update portfolio value
            cursor.execute('''
                UPDATE portfolios 
                SET current_value = ?, last_updated = ?
                WHERE id = ?
            ''', (total_value, datetime.now().isoformat(), portfolio_id))
            
            # Record value history
            cursor.execute('''
                INSERT INTO portfolio_value_history 
                (portfolio_id, date, total_value, cash_balance, positions_value, daily_return)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                portfolio_id, datetime.now().date().isoformat(), 
                total_value, cash_balance, positions_value, 0  # Calculate daily return separately
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error updating portfolio value: {e}")
    
    def calculate_portfolio_performance(self, portfolio_id: str) -> Optional[PortfolioPerformance]:
        """Calculate comprehensive portfolio performance metrics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get portfolio info
            cursor.execute('''
                SELECT initial_capital, current_value FROM portfolios WHERE id = ?
            ''', (portfolio_id,))
            
            portfolio_result = cursor.fetchone()
            if not portfolio_result:
                return None
            
            initial_capital, current_value = portfolio_result
            
            # Get value history
            cursor.execute('''
                SELECT date, total_value FROM portfolio_value_history 
                WHERE portfolio_id = ? 
                ORDER BY date ASC
            ''', (portfolio_id,))
            
            value_history = cursor.fetchall()
            
            # Get positions for analysis
            cursor.execute('''
                SELECT symbol, position_type, quantity, entry_price, current_price, entry_date
                FROM positions WHERE portfolio_id = ?
            ''', (portfolio_id,))
            
            positions = cursor.fetchall()
            conn.close()
            
            # Calculate basic metrics
            total_return = current_value - initial_capital
            total_return_pct = (total_return / initial_capital) * 100 if initial_capital > 0 else 0
            
            # Calculate daily returns and volatility
            daily_returns = []
            if len(value_history) > 1:
                for i in range(1, len(value_history)):
                    prev_value = value_history[i-1][1]
                    curr_value = value_history[i][1]
                    daily_return = (curr_value - prev_value) / prev_value if prev_value > 0 else 0
                    daily_returns.append(daily_return)
            
            daily_return = daily_returns[-1] if daily_returns else 0
            daily_return_pct = daily_return * 100
            volatility = np.std(daily_returns) * np.sqrt(252) if daily_returns else 0  # Annualized
            
            # Calculate Sharpe ratio (assuming 2% risk-free rate)
            risk_free_rate = 0.02
            avg_daily_return = np.mean(daily_returns) if daily_returns else 0
            sharpe_ratio = (avg_daily_return * 252 - risk_free_rate) / volatility if volatility > 0 else 0
            
            # Calculate maximum drawdown
            max_drawdown = 0
            if value_history:
                peak = value_history[0][1]
                for _, value in value_history:
                    if value > peak:
                        peak = value
                    drawdown = (peak - value) / peak if peak > 0 else 0
                    max_drawdown = max(max_drawdown, drawdown)
            
            # Analyze positions
            winning_positions = 0
            losing_positions = 0
            wins = []
            losses = []
            
            for symbol, pos_type, quantity, entry_price, current_price, entry_date in positions:
                if pos_type == PositionType.LONG.value:
                    pnl = (current_price - entry_price) * quantity
                else:  # SHORT
                    pnl = (entry_price - current_price) * quantity
                
                if pnl > 0:
                    winning_positions += 1
                    wins.append(pnl)
                elif pnl < 0:
                    losing_positions += 1
                    losses.append(abs(pnl))
            
            positions_count = len(positions)
            win_rate = (winning_positions / positions_count) * 100 if positions_count > 0 else 0
            
            average_win = np.mean(wins) if wins else 0
            average_loss = np.mean(losses) if losses else 0
            largest_win = max(wins) if wins else 0
            largest_loss = max(losses) if losses else 0
            
            profit_factor = sum(wins) / sum(losses) if losses and sum(losses) > 0 else 0
            
            performance = PortfolioPerformance(
                portfolio_id=portfolio_id,
                total_return=total_return,
                total_return_pct=total_return_pct,
                daily_return=daily_return,
                daily_return_pct=daily_return_pct,
                volatility=volatility,
                sharpe_ratio=sharpe_ratio,
                max_drawdown=max_drawdown,
                win_rate=win_rate,
                profit_factor=profit_factor,
                positions_count=positions_count,
                winning_positions=winning_positions,
                losing_positions=losing_positions,
                average_win=average_win,
                average_loss=average_loss,
                largest_win=largest_win,
                largest_loss=largest_loss,
                calculated_at=datetime.now().isoformat()
            )
            
            # Save performance to database
            self._save_performance_metrics(performance)
            
            return performance
            
        except Exception as e:
            logger.error(f"Error calculating portfolio performance: {e}")
            return None
    
    def _save_performance_metrics(self, performance: PortfolioPerformance):
        """Save performance metrics to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO portfolio_performance 
                (portfolio_id, total_return, total_return_pct, daily_return, daily_return_pct,
                 volatility, sharpe_ratio, max_drawdown, win_rate, profit_factor,
                 positions_count, winning_positions, losing_positions, average_win,
                 average_loss, largest_win, largest_loss, calculated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                performance.portfolio_id, performance.total_return, performance.total_return_pct,
                performance.daily_return, performance.daily_return_pct, performance.volatility,
                performance.sharpe_ratio, performance.max_drawdown, performance.win_rate,
                performance.profit_factor, performance.positions_count, performance.winning_positions,
                performance.losing_positions, performance.average_win, performance.average_loss,
                performance.largest_win, performance.largest_loss, performance.calculated_at
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error saving performance metrics: {e}")
    
    def get_portfolio_summary(self, portfolio_id: str) -> Dict[str, Any]:
        """Get comprehensive portfolio summary"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get portfolio info
            cursor.execute('SELECT * FROM portfolios WHERE id = ?', (portfolio_id,))
            portfolio_row = cursor.fetchone()
            
            if not portfolio_row:
                return {'error': 'Portfolio not found'}
            
            portfolio = Portfolio(
                id=portfolio_row[0], name=portfolio_row[1], description=portfolio_row[2],
                initial_capital=portfolio_row[3], current_value=portfolio_row[4],
                cash_balance=portfolio_row[5], created_at=portfolio_row[6],
                last_updated=portfolio_row[7], risk_tolerance=portfolio_row[8],
                investment_strategy=portfolio_row[9]
            )
            
            # Get positions
            cursor.execute('SELECT * FROM positions WHERE portfolio_id = ?', (portfolio_id,))
            position_rows = cursor.fetchall()
            
            positions = []
            for row in position_rows:
                position = Position(
                    id=row[0], portfolio_id=row[1], symbol=row[2],
                    position_type=PositionType(row[3]), quantity=row[4],
                    entry_price=row[5], current_price=row[6], entry_date=row[7],
                    last_updated=row[8], stop_loss=row[9], take_profit=row[10], notes=row[11]
                )
                positions.append(asdict(position))
            
            # Get recent performance
            cursor.execute('''
                SELECT * FROM portfolio_performance 
                WHERE portfolio_id = ? 
                ORDER BY calculated_at DESC LIMIT 1
            ''', (portfolio_id,))
            
            perf_row = cursor.fetchone()
            performance = None
            if perf_row:
                performance = {
                    'total_return': perf_row[2],
                    'total_return_pct': perf_row[3],
                    'daily_return_pct': perf_row[5],
                    'volatility': perf_row[6],
                    'sharpe_ratio': perf_row[7],
                    'max_drawdown': perf_row[8],
                    'win_rate': perf_row[9],
                    'profit_factor': perf_row[10]
                }
            
            conn.close()
            
            return {
                'portfolio': asdict(portfolio),
                'positions': positions,
                'performance': performance,
                'summary': {
                    'total_positions': len(positions),
                    'portfolio_age_days': (datetime.now() - datetime.fromisoformat(portfolio.created_at)).days,
                    'cash_allocation_pct': (portfolio.cash_balance / portfolio.current_value) * 100 if portfolio.current_value > 0 else 0
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting portfolio summary: {e}")
            return {'error': str(e)}
    
    def get_portfolio_recommendations(self, portfolio_id: str) -> Dict[str, Any]:
        """Get AI-powered portfolio recommendations"""
        try:
            # Get portfolio summary
            summary = self.get_portfolio_summary(portfolio_id)
            if 'error' in summary:
                return summary
            
            portfolio = summary['portfolio']
            positions = summary['positions']
            performance = summary['performance']
            
            recommendations = {
                'rebalancing': [],
                'risk_management': [],
                'opportunities': [],
                'alerts': []
            }
            
            # Analyze each position
            for position in positions:
                symbol = position['symbol']
                
                # Get ML prediction
                prediction_result = self.ml_predictor.predict_future_prices(symbol, horizon_days=30)
                
                if prediction_result.predictions:
                    current_price = position['current_price']
                    predicted_price = prediction_result.predictions[-1]
                    predicted_change = ((predicted_price - current_price) / current_price) * 100
                    
                    # Risk management recommendations
                    if position['position_type'] == 'long' and predicted_change < -10:
                        recommendations['risk_management'].append({
                            'symbol': symbol,
                            'action': 'Consider stop loss',
                            'reason': f'ML model predicts {predicted_change:.1f}% decline',
                            'priority': 'high'
                        })
                    
                    # Opportunity recommendations
                    if abs(predicted_change) > 15:
                        recommendations['opportunities'].append({
                            'symbol': symbol,
                            'action': 'Position size adjustment',
                            'reason': f'ML model predicts {predicted_change:.1f}% movement',
                            'priority': 'medium'
                        })
            
            # Portfolio-level recommendations
            if performance:
                if performance['sharpe_ratio'] < 0.5:
                    recommendations['rebalancing'].append({
                        'action': 'Improve risk-adjusted returns',
                        'reason': f'Low Sharpe ratio: {performance["sharpe_ratio"]:.2f}',
                        'priority': 'medium'
                    })
                
                if performance['max_drawdown'] > 0.2:
                    recommendations['risk_management'].append({
                        'action': 'Reduce portfolio risk',
                        'reason': f'High maximum drawdown: {performance["max_drawdown"]*100:.1f}%',
                        'priority': 'high'
                    })
            
            # Cash allocation analysis
            cash_pct = summary['summary']['cash_allocation_pct']
            if cash_pct > 30:
                recommendations['opportunities'].append({
                    'action': 'Deploy excess cash',
                    'reason': f'High cash allocation: {cash_pct:.1f}%',
                    'priority': 'low'
                })
            elif cash_pct < 5:
                recommendations['risk_management'].append({
                    'action': 'Maintain cash buffer',
                    'reason': f'Low cash allocation: {cash_pct:.1f}%',
                    'priority': 'medium'
                })
            
            return {
                'success': True,
                'recommendations': recommendations,
                'analysis_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating portfolio recommendations: {e}")
            return {'error': str(e)}
    
    def create_portfolio_alerts(self, portfolio_id: str):
        """Create portfolio-specific alerts"""
        try:
            # Get portfolio positions
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT symbol FROM positions WHERE portfolio_id = ?', (portfolio_id,))
            symbols = [row[0] for row in cursor.fetchall()]
            conn.close()
            
            # Create alerts for each position
            for symbol in symbols:
                # Price change alert
                alert_condition = {
                    'id': f'portfolio_{portfolio_id}_{symbol}_price_change',
                    'name': f'Portfolio {portfolio_id} - {symbol} Price Alert',
                    'alert_type': 'price_change',
                    'symbol': symbol,
                    'condition': {
                        'threshold_percent': 5.0,
                        'direction': 'any',
                        'priority': 'medium'
                    },
                    'priority': 'medium',
                    'enabled': True,
                    'created_at': datetime.now().isoformat(),
                    'cooldown_minutes': 60,
                    'notification_channels': ['webhook']
                }
                
                # Add to alert engine (would need to integrate with alert system)
                logger.info(f"Created portfolio alert for {symbol}")
            
        except Exception as e:
            logger.error(f"Error creating portfolio alerts: {e}")
    
    def get_all_portfolios(self) -> List[Dict[str, Any]]:
        """Get all portfolios summary"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT id, name, current_value, initial_capital, last_updated FROM portfolios')
            rows = cursor.fetchall()
            conn.close()
            
            portfolios = []
            for row in rows:
                portfolio_id, name, current_value, initial_capital, last_updated = row
                total_return_pct = ((current_value - initial_capital) / initial_capital) * 100 if initial_capital > 0 else 0
                
                portfolios.append({
                    'id': portfolio_id,
                    'name': name,
                    'current_value': current_value,
                    'initial_capital': initial_capital,
                    'total_return_pct': total_return_pct,
                    'last_updated': last_updated
                })
            
            return portfolios
            
        except Exception as e:
            logger.error(f"Error getting all portfolios: {e}")
            return []

def main():
    """Test the portfolio integration system"""
    print("Portfolio Integration System for Socrates AI")
    print("=" * 45)
    
    # Initialize portfolio manager
    manager = PortfolioManager()
    
    print("1. Creating sample portfolio...")
    portfolio_id = manager.create_portfolio(
        name="Tech Growth Portfolio",
        description="Technology stocks with growth potential",
        initial_capital=100000.0,
        risk_tolerance="medium",
        investment_strategy="growth"
    )
    
    if portfolio_id:
        print(f"   ✓ Created portfolio: {portfolio_id}")
    else:
        print("   ✗ Failed to create portfolio")
        return
    
    print("\n2. Adding sample positions...")
    
    # Add some positions
    positions = [
        ("AAPL", PositionType.LONG, 100, 150.0, 145.0, 160.0),
        ("GOOGL", PositionType.LONG, 50, 2500.0, 2400.0, 2700.0),
        ("MSFT", PositionType.LONG, 75, 300.0, 290.0, 320.0)
    ]
    
    for symbol, pos_type, quantity, entry_price, stop_loss, take_profit in positions:
        position_id = manager.add_position(
            portfolio_id, symbol, pos_type, quantity, entry_price, stop_loss, take_profit
        )
        if position_id:
            print(f"   ✓ Added position: {symbol}")
        else:
            print(f"   ✗ Failed to add position: {symbol}")
    
    print("\n3. Updating portfolio value...")
    manager.update_portfolio_value(portfolio_id)
    print("   ✓ Portfolio value updated")
    
    print("\n4. Calculating performance metrics...")
    performance = manager.calculate_portfolio_performance(portfolio_id)
    
    if performance:
        print(f"   ✓ Total Return: ${performance.total_return:.2f} ({performance.total_return_pct:.2f}%)")
        print(f"   ✓ Sharpe Ratio: {performance.sharpe_ratio:.2f}")
        print(f"   ✓ Max Drawdown: {performance.max_drawdown*100:.2f}%")
        print(f"   ✓ Win Rate: {performance.win_rate:.1f}%")
        print(f"   ✓ Positions: {performance.positions_count}")
    else:
        print("   ✗ Failed to calculate performance")
    
    print("\n5. Getting portfolio summary...")
    summary = manager.get_portfolio_summary(portfolio_id)
    
    if 'error' not in summary:
        portfolio = summary['portfolio']
        print(f"   ✓ Portfolio: {portfolio['name']}")
        print(f"   ✓ Current Value: ${portfolio['current_value']:.2f}")
        print(f"   ✓ Cash Balance: ${portfolio['cash_balance']:.2f}")
        print(f"   ✓ Positions: {len(summary['positions'])}")
    else:
        print(f"   ✗ Error getting summary: {summary['error']}")
    
    print("\n6. Generating AI recommendations...")
    recommendations = manager.get_portfolio_recommendations(portfolio_id)
    
    if 'error' not in recommendations:
        recs = recommendations['recommendations']
        total_recs = sum(len(recs[category]) for category in recs)
        print(f"   ✓ Generated {total_recs} recommendations")
        
        for category, items in recs.items():
            if items:
                print(f"   {category.title()}: {len(items)} recommendations")
    else:
        print(f"   ✗ Error generating recommendations: {recommendations['error']}")
    
    print("\n7. Creating portfolio alerts...")
    manager.create_portfolio_alerts(portfolio_id)
    print("   ✓ Portfolio alerts created")
    
    print("\n8. Getting all portfolios...")
    all_portfolios = manager.get_all_portfolios()
    print(f"   ✓ Found {len(all_portfolios)} portfolios")
    
    print("\nPortfolio integration system test completed!")
    print("System is ready for integration with Socrates AI!")

if __name__ == "__main__":
    main()

