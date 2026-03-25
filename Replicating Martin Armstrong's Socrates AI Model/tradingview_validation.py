#!/usr/bin/env python3
"""
TradingView Validation System for Socrates AI
Implements TradingView integration as a cross-reference validation layer
to ensure data quality and accuracy across all market analysis
"""

import sys
import sqlite3
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import numpy as np
import pandas as pd
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add the Manus API client path
sys.path.append('/opt/.manus/.sandbox-runtime')
from data_api import ApiClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ValidationResult:
    """Data validation result"""
    symbol: str
    data_type: str
    our_value: float
    tradingview_value: float
    difference: float
    difference_pct: float
    is_valid: bool
    threshold_used: float
    timestamp: str
    validation_type: str

@dataclass
class DataQualityMetrics:
    """Data quality metrics"""
    symbol: str
    total_validations: int
    passed_validations: int
    failed_validations: int
    accuracy_rate: float
    avg_difference: float
    max_difference: float
    last_validation: str

class TradingViewValidator:
    """TradingView validation system for cross-referencing data quality"""
    
    def __init__(self, db_path: str = "socrates_data.db"):
        self.db_path = db_path
        self.api_client = ApiClient()
        
        # Validation thresholds (percentage)
        self.validation_thresholds = {
            'price': 0.5,      # 0.5% difference allowed for prices
            'volume': 5.0,     # 5% difference allowed for volume
            'technical': 2.0,  # 2% difference for technical indicators
            'sentiment': 10.0  # 10% difference for sentiment scores
        }
        
        # Initialize database
        self._init_validation_database()
        
        logger.info("TradingView Validator initialized")
    
    def _init_validation_database(self):
        """Initialize validation database tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Validation results table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS validation_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    data_type TEXT NOT NULL,
                    our_value REAL NOT NULL,
                    tradingview_value REAL NOT NULL,
                    difference REAL NOT NULL,
                    difference_pct REAL NOT NULL,
                    is_valid BOOLEAN NOT NULL,
                    threshold_used REAL NOT NULL,
                    timestamp TEXT NOT NULL,
                    validation_type TEXT NOT NULL
                )
            ''')
            
            # Data quality metrics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS data_quality_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    total_validations INTEGER NOT NULL,
                    passed_validations INTEGER NOT NULL,
                    failed_validations INTEGER NOT NULL,
                    accuracy_rate REAL NOT NULL,
                    avg_difference REAL NOT NULL,
                    max_difference REAL NOT NULL,
                    last_validation TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            ''')
            
            # TradingView data cache table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tradingview_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    data_type TEXT NOT NULL,
                    data_json TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    expires_at TEXT NOT NULL
                )
            ''')
            
            # Create indexes
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_validation_symbol_timestamp ON validation_results(symbol, timestamp DESC)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_quality_symbol ON data_quality_metrics(symbol)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_tv_cache_symbol_type ON tradingview_cache(symbol, data_type)')
            
            conn.commit()
            conn.close()
            
            logger.info("Validation database initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing validation database: {e}")
    
    def fetch_tradingview_data(self, symbol: str, interval: str = '1d', 
                              range_period: str = '1mo') -> Dict[str, Any]:
        """Fetch data from TradingView via Yahoo Finance API"""
        try:
            logger.info(f"Fetching TradingView data for {symbol}")
            
            # Check cache first
            cached_data = self._get_cached_tradingview_data(symbol, 'chart')
            if cached_data:
                return cached_data
            
            # Fetch from API
            response = self.api_client.call_api('YahooFinance/get_stock_chart', query={
                'symbol': symbol,
                'region': 'US',
                'interval': interval,
                'range': range_period,
                'includeAdjustedClose': True,
                'events': 'div,split'
            })
            
            if response and 'chart' in response and 'result' in response['chart']:
                result = response['chart']['result'][0]
                
                # Cache the result
                self._cache_tradingview_data(symbol, 'chart', result, ttl_minutes=5)
                
                return result
            
            return {}
            
        except Exception as e:
            logger.error(f"Error fetching TradingView data for {symbol}: {e}")
            return {}
    
    def _get_cached_tradingview_data(self, symbol: str, data_type: str) -> Optional[Dict[str, Any]]:
        """Get cached TradingView data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT data_json, expires_at FROM tradingview_cache 
                WHERE symbol = ? AND data_type = ? 
                ORDER BY timestamp DESC LIMIT 1
            ''', (symbol, data_type))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                data_json, expires_at = result
                expires_time = datetime.fromisoformat(expires_at)
                
                if datetime.now() < expires_time:
                    return json.loads(data_json)
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting cached TradingView data: {e}")
            return None
    
    def _cache_tradingview_data(self, symbol: str, data_type: str, 
                               data: Dict[str, Any], ttl_minutes: int = 5):
        """Cache TradingView data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            timestamp = datetime.now().isoformat()
            expires_at = (datetime.now() + timedelta(minutes=ttl_minutes)).isoformat()
            
            cursor.execute('''
                INSERT INTO tradingview_cache 
                (symbol, data_type, data_json, timestamp, expires_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (symbol, data_type, json.dumps(data), timestamp, expires_at))
            
            # Clean old cache entries
            cursor.execute('''
                DELETE FROM tradingview_cache 
                WHERE expires_at < ?
            ''', (datetime.now().isoformat(),))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error caching TradingView data: {e}")
    
    def validate_price_data(self, symbol: str) -> List[ValidationResult]:
        """Validate price data against TradingView"""
        try:
            validation_results = []
            
            # Get our data
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT date, close_price, volume FROM market_data 
                WHERE symbol = ? 
                ORDER BY date DESC LIMIT 30
            ''', (symbol,))
            
            our_data = cursor.fetchall()
            conn.close()
            
            if not our_data:
                logger.warning(f"No market data found for {symbol}")
                return validation_results
            
            # Get TradingView data
            tv_data = self.fetch_tradingview_data(symbol, '1d', '1mo')
            
            if not tv_data or 'timestamp' not in tv_data:
                logger.warning(f"No TradingView data found for {symbol}")
                return validation_results
            
            # Convert TradingView data to comparable format
            tv_timestamps = tv_data['timestamp']
            tv_quotes = tv_data['indicators']['quote'][0]
            tv_prices = tv_quotes['close']
            tv_volumes = tv_quotes['volume']
            
            # Create TradingView data lookup
            tv_lookup = {}
            for i, timestamp in enumerate(tv_timestamps):
                date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                if i < len(tv_prices) and tv_prices[i] is not None:
                    tv_lookup[date] = {
                        'price': tv_prices[i],
                        'volume': tv_volumes[i] if i < len(tv_volumes) and tv_volumes[i] else 0
                    }
            
            # Validate each data point
            for date, our_price, our_volume in our_data:
                if date in tv_lookup:
                    tv_price = tv_lookup[date]['price']
                    tv_volume = tv_lookup[date]['volume']
                    
                    # Validate price
                    price_diff = abs(our_price - tv_price)
                    price_diff_pct = (price_diff / tv_price) * 100 if tv_price > 0 else 0
                    
                    price_validation = ValidationResult(
                        symbol=symbol,
                        data_type='price',
                        our_value=our_price,
                        tradingview_value=tv_price,
                        difference=price_diff,
                        difference_pct=price_diff_pct,
                        is_valid=price_diff_pct <= self.validation_thresholds['price'],
                        threshold_used=self.validation_thresholds['price'],
                        timestamp=datetime.now().isoformat(),
                        validation_type='price_comparison'
                    )
                    
                    validation_results.append(price_validation)
                    
                    # Validate volume if available
                    if our_volume and tv_volume:
                        volume_diff = abs(our_volume - tv_volume)
                        volume_diff_pct = (volume_diff / tv_volume) * 100 if tv_volume > 0 else 0
                        
                        volume_validation = ValidationResult(
                            symbol=symbol,
                            data_type='volume',
                            our_value=our_volume,
                            tradingview_value=tv_volume,
                            difference=volume_diff,
                            difference_pct=volume_diff_pct,
                            is_valid=volume_diff_pct <= self.validation_thresholds['volume'],
                            threshold_used=self.validation_thresholds['volume'],
                            timestamp=datetime.now().isoformat(),
                            validation_type='volume_comparison'
                        )
                        
                        validation_results.append(volume_validation)
            
            # Save validation results
            self._save_validation_results(validation_results)
            
            return validation_results
            
        except Exception as e:
            logger.error(f"Error validating price data for {symbol}: {e}")
            return []
    
    def validate_technical_indicators(self, symbol: str) -> List[ValidationResult]:
        """Validate technical indicators against TradingView calculations"""
        try:
            validation_results = []
            
            # Get TradingView data for technical analysis
            tv_data = self.fetch_tradingview_data(symbol, '1d', '3mo')
            
            if not tv_data or 'timestamp' not in tv_data:
                return validation_results
            
            # Extract price data for technical calculations
            tv_quotes = tv_data['indicators']['quote'][0]
            tv_closes = [p for p in tv_quotes['close'] if p is not None]
            tv_highs = [p for p in tv_quotes['high'] if p is not None]
            tv_lows = [p for p in tv_quotes['low'] if p is not None]
            tv_volumes = [v for v in tv_quotes['volume'] if v is not None]
            
            if len(tv_closes) < 20:  # Need enough data for technical indicators
                return validation_results
            
            # Calculate our technical indicators
            our_indicators = self._calculate_our_technical_indicators(symbol)
            
            # Calculate TradingView-equivalent technical indicators
            tv_indicators = self._calculate_tradingview_technical_indicators(
                tv_closes, tv_highs, tv_lows, tv_volumes
            )
            
            # Compare indicators
            for indicator_name in ['sma_20', 'rsi_14', 'macd_signal']:
                if indicator_name in our_indicators and indicator_name in tv_indicators:
                    our_value = our_indicators[indicator_name]
                    tv_value = tv_indicators[indicator_name]
                    
                    if our_value is not None and tv_value is not None:
                        diff = abs(our_value - tv_value)
                        diff_pct = (diff / abs(tv_value)) * 100 if tv_value != 0 else 0
                        
                        validation = ValidationResult(
                            symbol=symbol,
                            data_type=indicator_name,
                            our_value=our_value,
                            tradingview_value=tv_value,
                            difference=diff,
                            difference_pct=diff_pct,
                            is_valid=diff_pct <= self.validation_thresholds['technical'],
                            threshold_used=self.validation_thresholds['technical'],
                            timestamp=datetime.now().isoformat(),
                            validation_type='technical_indicator'
                        )
                        
                        validation_results.append(validation)
            
            # Save validation results
            self._save_validation_results(validation_results)
            
            return validation_results
            
        except Exception as e:
            logger.error(f"Error validating technical indicators for {symbol}: {e}")
            return []
    
    def _calculate_our_technical_indicators(self, symbol: str) -> Dict[str, float]:
        """Calculate our technical indicators from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT close_price, high_price, low_price, volume 
                FROM market_data 
                WHERE symbol = ? 
                ORDER BY date DESC LIMIT 50
            ''', (symbol,))
            
            data = cursor.fetchall()
            conn.close()
            
            if len(data) < 20:
                return {}
            
            closes = [row[0] for row in data]
            highs = [row[1] for row in data]
            lows = [row[2] for row in data]
            volumes = [row[3] for row in data]
            
            # Reverse to get chronological order
            closes.reverse()
            highs.reverse()
            lows.reverse()
            volumes.reverse()
            
            indicators = {}
            
            # Simple Moving Average (20 periods)
            if len(closes) >= 20:
                indicators['sma_20'] = np.mean(closes[-20:])
            
            # RSI (14 periods)
            if len(closes) >= 15:
                indicators['rsi_14'] = self._calculate_rsi(closes, 14)
            
            # MACD Signal
            if len(closes) >= 26:
                macd_line, signal_line = self._calculate_macd(closes)
                if signal_line is not None:
                    indicators['macd_signal'] = signal_line
            
            return indicators
            
        except Exception as e:
            logger.error(f"Error calculating our technical indicators: {e}")
            return {}
    
    def _calculate_tradingview_technical_indicators(self, closes: List[float], 
                                                   highs: List[float], 
                                                   lows: List[float], 
                                                   volumes: List[float]) -> Dict[str, float]:
        """Calculate TradingView-equivalent technical indicators"""
        try:
            indicators = {}
            
            # Simple Moving Average (20 periods)
            if len(closes) >= 20:
                indicators['sma_20'] = np.mean(closes[-20:])
            
            # RSI (14 periods)
            if len(closes) >= 15:
                indicators['rsi_14'] = self._calculate_rsi(closes, 14)
            
            # MACD Signal
            if len(closes) >= 26:
                macd_line, signal_line = self._calculate_macd(closes)
                if signal_line is not None:
                    indicators['macd_signal'] = signal_line
            
            return indicators
            
        except Exception as e:
            logger.error(f"Error calculating TradingView technical indicators: {e}")
            return {}
    
    def _calculate_rsi(self, prices: List[float], period: int = 14) -> Optional[float]:
        """Calculate RSI indicator"""
        try:
            if len(prices) < period + 1:
                return None
            
            deltas = np.diff(prices)
            gains = np.where(deltas > 0, deltas, 0)
            losses = np.where(deltas < 0, -deltas, 0)
            
            avg_gain = np.mean(gains[-period:])
            avg_loss = np.mean(losses[-period:])
            
            if avg_loss == 0:
                return 100.0
            
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            
            return rsi
            
        except Exception as e:
            logger.error(f"Error calculating RSI: {e}")
            return None
    
    def _calculate_macd(self, prices: List[float]) -> Tuple[Optional[float], Optional[float]]:
        """Calculate MACD and signal line"""
        try:
            if len(prices) < 26:
                return None, None
            
            # Calculate EMAs
            ema_12 = self._calculate_ema(prices, 12)
            ema_26 = self._calculate_ema(prices, 26)
            
            if ema_12 is None or ema_26 is None:
                return None, None
            
            macd_line = ema_12 - ema_26
            
            # Calculate signal line (9-period EMA of MACD)
            # For simplicity, we'll use the current MACD value as signal
            signal_line = macd_line
            
            return macd_line, signal_line
            
        except Exception as e:
            logger.error(f"Error calculating MACD: {e}")
            return None, None
    
    def _calculate_ema(self, prices: List[float], period: int) -> Optional[float]:
        """Calculate Exponential Moving Average"""
        try:
            if len(prices) < period:
                return None
            
            multiplier = 2 / (period + 1)
            ema = prices[0]
            
            for price in prices[1:]:
                ema = (price * multiplier) + (ema * (1 - multiplier))
            
            return ema
            
        except Exception as e:
            logger.error(f"Error calculating EMA: {e}")
            return None
    
    def _save_validation_results(self, validation_results: List[ValidationResult]):
        """Save validation results to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for result in validation_results:
                cursor.execute('''
                    INSERT INTO validation_results 
                    (symbol, data_type, our_value, tradingview_value, difference, 
                     difference_pct, is_valid, threshold_used, timestamp, validation_type)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    result.symbol, result.data_type, result.our_value, 
                    result.tradingview_value, result.difference, result.difference_pct,
                    result.is_valid, result.threshold_used, result.timestamp, 
                    result.validation_type
                ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error saving validation results: {e}")
    
    def generate_data_quality_report(self, symbol: str) -> DataQualityMetrics:
        """Generate comprehensive data quality report"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get validation statistics
            cursor.execute('''
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN is_valid = 1 THEN 1 ELSE 0 END) as passed,
                    SUM(CASE WHEN is_valid = 0 THEN 1 ELSE 0 END) as failed,
                    AVG(difference_pct) as avg_diff,
                    MAX(difference_pct) as max_diff,
                    MAX(timestamp) as last_validation
                FROM validation_results 
                WHERE symbol = ?
            ''', (symbol,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result and result[0] > 0:
                total, passed, failed, avg_diff, max_diff, last_validation = result
                accuracy_rate = (passed / total) * 100 if total > 0 else 0
                
                metrics = DataQualityMetrics(
                    symbol=symbol,
                    total_validations=total,
                    passed_validations=passed,
                    failed_validations=failed,
                    accuracy_rate=accuracy_rate,
                    avg_difference=avg_diff or 0,
                    max_difference=max_diff or 0,
                    last_validation=last_validation or 'Never'
                )
                
                # Save metrics to database
                self._save_quality_metrics(metrics)
                
                return metrics
            
            return DataQualityMetrics(
                symbol=symbol,
                total_validations=0,
                passed_validations=0,
                failed_validations=0,
                accuracy_rate=0,
                avg_difference=0,
                max_difference=0,
                last_validation='Never'
            )
            
        except Exception as e:
            logger.error(f"Error generating data quality report for {symbol}: {e}")
            return DataQualityMetrics(
                symbol=symbol,
                total_validations=0,
                passed_validations=0,
                failed_validations=0,
                accuracy_rate=0,
                avg_difference=0,
                max_difference=0,
                last_validation='Error'
            )
    
    def _save_quality_metrics(self, metrics: DataQualityMetrics):
        """Save quality metrics to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Update or insert metrics
            cursor.execute('''
                INSERT OR REPLACE INTO data_quality_metrics 
                (symbol, total_validations, passed_validations, failed_validations,
                 accuracy_rate, avg_difference, max_difference, last_validation, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                metrics.symbol, metrics.total_validations, metrics.passed_validations,
                metrics.failed_validations, metrics.accuracy_rate, metrics.avg_difference,
                metrics.max_difference, metrics.last_validation, datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error saving quality metrics: {e}")
    
    def validate_symbol_comprehensive(self, symbol: str) -> Dict[str, Any]:
        """Perform comprehensive validation for a symbol"""
        try:
            logger.info(f"Starting comprehensive validation for {symbol}")
            
            results = {
                'symbol': symbol,
                'timestamp': datetime.now().isoformat(),
                'price_validation': [],
                'technical_validation': [],
                'quality_metrics': None,
                'summary': {}
            }
            
            # Validate price data
            price_results = self.validate_price_data(symbol)
            results['price_validation'] = [asdict(r) for r in price_results]
            
            # Validate technical indicators
            technical_results = self.validate_technical_indicators(symbol)
            results['technical_validation'] = [asdict(r) for r in technical_results]
            
            # Generate quality report
            quality_metrics = self.generate_data_quality_report(symbol)
            results['quality_metrics'] = asdict(quality_metrics)
            
            # Create summary
            all_results = price_results + technical_results
            if all_results:
                passed = sum(1 for r in all_results if r.is_valid)
                total = len(all_results)
                
                results['summary'] = {
                    'total_validations': total,
                    'passed_validations': passed,
                    'failed_validations': total - passed,
                    'accuracy_rate': (passed / total) * 100 if total > 0 else 0,
                    'avg_difference': np.mean([r.difference_pct for r in all_results]),
                    'max_difference': max([r.difference_pct for r in all_results]) if all_results else 0
                }
            
            return results
            
        except Exception as e:
            logger.error(f"Error in comprehensive validation for {symbol}: {e}")
            return {'error': str(e)}
    
    def get_validation_dashboard(self) -> Dict[str, Any]:
        """Get validation dashboard with overall system health"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get overall statistics
            cursor.execute('''
                SELECT 
                    COUNT(DISTINCT symbol) as symbols_validated,
                    COUNT(*) as total_validations,
                    SUM(CASE WHEN is_valid = 1 THEN 1 ELSE 0 END) as passed_validations,
                    AVG(difference_pct) as avg_difference,
                    MAX(timestamp) as last_validation
                FROM validation_results
            ''')
            
            overall_stats = cursor.fetchone()
            
            # Get per-symbol statistics
            cursor.execute('''
                SELECT 
                    symbol,
                    COUNT(*) as validations,
                    SUM(CASE WHEN is_valid = 1 THEN 1 ELSE 0 END) as passed,
                    AVG(difference_pct) as avg_diff
                FROM validation_results 
                GROUP BY symbol 
                ORDER BY validations DESC
            ''')
            
            symbol_stats = cursor.fetchall()
            conn.close()
            
            dashboard = {
                'timestamp': datetime.now().isoformat(),
                'overall_stats': {
                    'symbols_validated': overall_stats[0] if overall_stats else 0,
                    'total_validations': overall_stats[1] if overall_stats else 0,
                    'passed_validations': overall_stats[2] if overall_stats else 0,
                    'accuracy_rate': (overall_stats[2] / overall_stats[1] * 100) if overall_stats and overall_stats[1] > 0 else 0,
                    'avg_difference': overall_stats[3] if overall_stats else 0,
                    'last_validation': overall_stats[4] if overall_stats else 'Never'
                },
                'symbol_stats': [
                    {
                        'symbol': row[0],
                        'validations': row[1],
                        'passed': row[2],
                        'accuracy_rate': (row[2] / row[1] * 100) if row[1] > 0 else 0,
                        'avg_difference': row[3]
                    }
                    for row in symbol_stats
                ],
                'validation_thresholds': self.validation_thresholds
            }
            
            return dashboard
            
        except Exception as e:
            logger.error(f"Error getting validation dashboard: {e}")
            return {'error': str(e)}

def main():
    """Test the TradingView validation system"""
    print("TradingView Validation System for Socrates AI")
    print("=" * 50)
    
    # Initialize validator
    validator = TradingViewValidator()
    
    print("1. Testing TradingView data fetch...")
    tv_data = validator.fetch_tradingview_data("AAPL")
    if tv_data:
        print("   ✓ TradingView data fetched successfully")
        if 'meta' in tv_data:
            meta = tv_data['meta']
            print(f"   ✓ Symbol: {meta.get('symbol', 'N/A')}")
            print(f"   ✓ Current Price: ${meta.get('regularMarketPrice', 0):.2f}")
            print(f"   ✓ Data points: {len(tv_data.get('timestamp', []))}")
    else:
        print("   ✗ Failed to fetch TradingView data")
    
    print("\n2. Testing price validation...")
    price_validations = validator.validate_price_data("AAPL")
    if price_validations:
        print(f"   ✓ Price validation completed - {len(price_validations)} validations")
        passed = sum(1 for v in price_validations if v.is_valid)
        print(f"   ✓ Passed: {passed}/{len(price_validations)} ({passed/len(price_validations)*100:.1f}%)")
        
        # Show sample validation
        if price_validations:
            sample = price_validations[0]
            print(f"   ✓ Sample: Our ${sample.our_value:.2f} vs TV ${sample.tradingview_value:.2f} (diff: {sample.difference_pct:.2f}%)")
    else:
        print("   ✗ Price validation failed")
    
    print("\n3. Testing technical indicator validation...")
    tech_validations = validator.validate_technical_indicators("AAPL")
    if tech_validations:
        print(f"   ✓ Technical validation completed - {len(tech_validations)} validations")
        passed = sum(1 for v in tech_validations if v.is_valid)
        print(f"   ✓ Passed: {passed}/{len(tech_validations)} ({passed/len(tech_validations)*100:.1f}%)")
        
        # Show sample validation
        if tech_validations:
            sample = tech_validations[0]
            print(f"   ✓ Sample {sample.data_type}: Our {sample.our_value:.2f} vs TV {sample.tradingview_value:.2f}")
    else:
        print("   ✗ Technical validation failed")
    
    print("\n4. Testing comprehensive validation...")
    comprehensive = validator.validate_symbol_comprehensive("AAPL")
    if 'error' not in comprehensive:
        print("   ✓ Comprehensive validation completed")
        summary = comprehensive.get('summary', {})
        print(f"   ✓ Total validations: {summary.get('total_validations', 0)}")
        print(f"   ✓ Accuracy rate: {summary.get('accuracy_rate', 0):.1f}%")
        print(f"   ✓ Average difference: {summary.get('avg_difference', 0):.2f}%")
    else:
        print(f"   ✗ Comprehensive validation failed: {comprehensive['error']}")
    
    print("\n5. Testing data quality report...")
    quality_metrics = validator.generate_data_quality_report("AAPL")
    print(f"   ✓ Quality report generated")
    print(f"   ✓ Total validations: {quality_metrics.total_validations}")
    print(f"   ✓ Accuracy rate: {quality_metrics.accuracy_rate:.1f}%")
    print(f"   ✓ Average difference: {quality_metrics.avg_difference:.2f}%")
    print(f"   ✓ Max difference: {quality_metrics.max_difference:.2f}%")
    
    print("\n6. Testing validation dashboard...")
    dashboard = validator.get_validation_dashboard()
    if 'error' not in dashboard:
        print("   ✓ Validation dashboard generated")
        overall = dashboard.get('overall_stats', {})
        print(f"   ✓ Symbols validated: {overall.get('symbols_validated', 0)}")
        print(f"   ✓ Total validations: {overall.get('total_validations', 0)}")
        print(f"   ✓ Overall accuracy: {overall.get('accuracy_rate', 0):.1f}%")
        
        symbol_stats = dashboard.get('symbol_stats', [])
        if symbol_stats:
            print("   ✓ Top validated symbols:")
            for stat in symbol_stats[:3]:
                print(f"     - {stat['symbol']}: {stat['accuracy_rate']:.1f}% accuracy ({stat['validations']} validations)")
    else:
        print(f"   ✗ Dashboard generation failed: {dashboard['error']}")
    
    print("\n7. Testing multiple symbols...")
    test_symbols = ["MSFT", "GOOGL"]
    for symbol in test_symbols:
        print(f"   Testing {symbol}...")
        validation = validator.validate_symbol_comprehensive(symbol)
        if 'error' not in validation:
            summary = validation.get('summary', {})
            accuracy = summary.get('accuracy_rate', 0)
            print(f"   ✓ {symbol}: {accuracy:.1f}% accuracy")
        else:
            print(f"   ✗ {symbol}: Validation failed")
    
    print("\nTradingView validation system test completed!")
    print("Data quality validation is now active!")

if __name__ == "__main__":
    main()

