#!/usr/bin/env python3
"""
Alternative Data Sources Integration for Socrates AI
Implements comprehensive integration with multiple data sources including
Yahoo Finance APIs, World Bank indicators, sentiment analysis, and more
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
import requests
import time

# Add the Manus API client path
sys.path.append('/opt/.manus/.sandbox-runtime')
from data_api import ApiClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class DataSource:
    """Data source configuration"""
    name: str
    api_endpoint: str
    description: str
    update_frequency: str  # daily, hourly, weekly
    data_type: str  # market, economic, sentiment, fundamental
    enabled: bool = True

@dataclass
class AlternativeDataPoint:
    """Alternative data point"""
    source: str
    symbol: str
    data_type: str
    timestamp: str
    value: float
    metadata: Dict[str, Any]

class AlternativeDataManager:
    """Manages alternative data sources and integration"""
    
    def __init__(self, db_path: str = "socrates_data.db"):
        self.db_path = db_path
        self.api_client = ApiClient()
        self.data_sources = {}
        
        # Initialize database
        self._init_database()
        
        # Setup data sources
        self._setup_data_sources()
    
    def _init_database(self):
        """Initialize alternative data database tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Alternative data table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS alternative_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT NOT NULL,
                    symbol TEXT NOT NULL,
                    data_type TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    value REAL NOT NULL,
                    metadata_json TEXT,
                    created_at TEXT NOT NULL
                )
            ''')
            
            # Stock insights table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS stock_insights (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    insight_type TEXT NOT NULL,
                    content TEXT NOT NULL,
                    score REAL,
                    timestamp TEXT NOT NULL,
                    source TEXT NOT NULL
                )
            ''')
            
            # Analyst reports table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS analyst_reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    title TEXT NOT NULL,
                    author TEXT,
                    provider TEXT,
                    report_type TEXT,
                    abstract TEXT,
                    url TEXT,
                    publication_date TEXT,
                    timestamp TEXT NOT NULL
                )
            ''')
            
            # Economic indicators table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS economic_indicators (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    indicator_code TEXT NOT NULL,
                    indicator_name TEXT NOT NULL,
                    country_code TEXT,
                    value REAL NOT NULL,
                    date TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
            ''')
            
            # Check if columns exist and add them if missing
            cursor.execute("PRAGMA table_info(economic_indicators)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'indicator_code' not in columns:
                cursor.execute('ALTER TABLE economic_indicators ADD COLUMN indicator_code TEXT')
            if 'indicator_name' not in columns:
                cursor.execute('ALTER TABLE economic_indicators ADD COLUMN indicator_name TEXT')
            if 'country_code' not in columns:
                cursor.execute('ALTER TABLE economic_indicators ADD COLUMN country_code TEXT')
            if 'date' not in columns:
                cursor.execute('ALTER TABLE economic_indicators ADD COLUMN date TEXT')
            if 'timestamp' not in columns:
                cursor.execute('ALTER TABLE economic_indicators ADD COLUMN timestamp TEXT')
            
            # Sentiment data table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sentiment_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    sentiment_score REAL NOT NULL,
                    sentiment_label TEXT NOT NULL,
                    source TEXT NOT NULL,
                    content TEXT,
                    timestamp TEXT NOT NULL
                )
            ''')
            
            # Create indexes for better performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_alt_data_symbol_timestamp ON alternative_data(symbol, timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_insights_symbol ON stock_insights(symbol)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_reports_symbol ON analyst_reports(symbol)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_indicators_code ON economic_indicators(indicator_code)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_sentiment_symbol ON sentiment_data(symbol)')
            
            conn.commit()
            conn.close()
            
            logger.info("Alternative data database initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing alternative data database: {e}")
    
    def _setup_data_sources(self):
        """Setup available data sources"""
        self.data_sources = {
            'yahoo_finance_insights': DataSource(
                name="Yahoo Finance Insights",
                api_endpoint="YahooFinance/get_stock_insights",
                description="Comprehensive financial analysis and insights",
                update_frequency="daily",
                data_type="fundamental"
            ),
            'yahoo_finance_analysts': DataSource(
                name="Yahoo Finance Analyst Reports",
                api_endpoint="YahooFinance/get_stock_what_analyst_are_saying",
                description="Analyst reports and recommendations",
                update_frequency="daily",
                data_type="sentiment"
            ),
            'yahoo_finance_profile': DataSource(
                name="Yahoo Finance Company Profile",
                api_endpoint="YahooFinance/get_stock_profile",
                description="Company profile and fundamental data",
                update_frequency="weekly",
                data_type="fundamental"
            ),
            'yahoo_finance_holders': DataSource(
                name="Yahoo Finance Stock Holders",
                api_endpoint="YahooFinance/get_stock_holders",
                description="Institutional and insider holdings",
                update_frequency="weekly",
                data_type="fundamental"
            ),
            'world_bank_indicators': DataSource(
                name="World Bank Economic Indicators",
                api_endpoint="DataBank/indicator_list",
                description="Global economic development indicators",
                update_frequency="monthly",
                data_type="economic"
            )
        }
        
        logger.info(f"Setup {len(self.data_sources)} alternative data sources")
    
    def fetch_stock_insights(self, symbol: str) -> Dict[str, Any]:
        """Fetch comprehensive stock insights from Yahoo Finance"""
        try:
            logger.info(f"Fetching stock insights for {symbol}")
            
            response = self.api_client.call_api(
                'YahooFinance/get_stock_insights',
                query={'symbol': symbol}
            )
            
            if response:
                # Save insights to database
                self._save_stock_insights(symbol, response)
                return response
            
            return {}
            
        except Exception as e:
            logger.error(f"Error fetching stock insights for {symbol}: {e}")
            return {}
    
    def _save_stock_insights(self, symbol: str, insights_data: Dict[str, Any]):
        """Save stock insights to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            timestamp = datetime.now().isoformat()
            
            # Extract and save different types of insights
            if 'insights' in insights_data:
                insights = insights_data['insights']
                
                for insight_type, content in insights.items():
                    # Calculate a simple score based on content
                    score = self._calculate_insight_score(content)
                    
                    cursor.execute('''
                        INSERT INTO stock_insights 
                        (symbol, insight_type, content, score, timestamp, source)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        symbol, insight_type, json.dumps(content), 
                        score, timestamp, 'yahoo_finance'
                    ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error saving stock insights: {e}")
    
    def _calculate_insight_score(self, content: Any) -> float:
        """Calculate a simple insight score"""
        try:
            if isinstance(content, dict):
                # Count positive vs negative indicators
                positive_keywords = ['strong', 'growth', 'positive', 'buy', 'outperform']
                negative_keywords = ['weak', 'decline', 'negative', 'sell', 'underperform']
                
                content_str = json.dumps(content).lower()
                positive_count = sum(1 for word in positive_keywords if word in content_str)
                negative_count = sum(1 for word in negative_keywords if word in content_str)
                
                if positive_count + negative_count > 0:
                    return (positive_count - negative_count) / (positive_count + negative_count)
                
            return 0.0
            
        except:
            return 0.0
    
    def fetch_analyst_reports(self, symbol: str) -> Dict[str, Any]:
        """Fetch analyst reports and recommendations"""
        try:
            logger.info(f"Fetching analyst reports for {symbol}")
            
            response = self.api_client.call_api(
                'YahooFinance/get_stock_what_analyst_are_saying',
                query={'symbol': symbol}
            )
            
            if response:
                # Save reports to database
                self._save_analyst_reports(symbol, response)
                return response
            
            return {}
            
        except Exception as e:
            logger.error(f"Error fetching analyst reports for {symbol}: {e}")
            return {}
    
    def _save_analyst_reports(self, symbol: str, reports_data: Dict[str, Any]):
        """Save analyst reports to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            timestamp = datetime.now().isoformat()
            
            # Extract reports from response
            if 'reports' in reports_data:
                reports = reports_data['reports']
                
                for report in reports:
                    cursor.execute('''
                        INSERT INTO analyst_reports 
                        (symbol, title, author, provider, report_type, abstract, url, 
                         publication_date, timestamp)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        symbol,
                        report.get('title', ''),
                        report.get('author', ''),
                        report.get('provider', ''),
                        report.get('reportType', ''),
                        report.get('abstract', ''),
                        report.get('url', ''),
                        report.get('publicationDate', ''),
                        timestamp
                    ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error saving analyst reports: {e}")
    
    def fetch_company_profile(self, symbol: str) -> Dict[str, Any]:
        """Fetch comprehensive company profile"""
        try:
            logger.info(f"Fetching company profile for {symbol}")
            
            response = self.api_client.call_api(
                'YahooFinance/get_stock_profile',
                query={'symbol': symbol}
            )
            
            if response:
                # Save profile data as alternative data points
                self._save_company_profile(symbol, response)
                return response
            
            return {}
            
        except Exception as e:
            logger.error(f"Error fetching company profile for {symbol}: {e}")
            return {}
    
    def _save_company_profile(self, symbol: str, profile_data: Dict[str, Any]):
        """Save company profile as alternative data points"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            timestamp = datetime.now().isoformat()
            
            # Extract key metrics from profile
            asset_profile = profile_data.get('assetProfile', {})
            summary_detail = profile_data.get('summaryDetail', {})
            
            # Save employee count
            if 'fullTimeEmployees' in asset_profile:
                self._save_alternative_data_point(
                    cursor, 'yahoo_finance', symbol, 'employee_count',
                    timestamp, float(asset_profile['fullTimeEmployees']),
                    {'sector': asset_profile.get('sector', ''), 'industry': asset_profile.get('industry', '')}
                )
            
            # Save market cap
            if 'marketCap' in summary_detail:
                market_cap = summary_detail['marketCap']
                if isinstance(market_cap, dict) and 'raw' in market_cap:
                    self._save_alternative_data_point(
                        cursor, 'yahoo_finance', symbol, 'market_cap',
                        timestamp, float(market_cap['raw']),
                        {'currency': profile_data.get('price', {}).get('currency', 'USD')}
                    )
            
            # Save P/E ratio
            if 'trailingPE' in summary_detail:
                pe_ratio = summary_detail['trailingPE']
                if isinstance(pe_ratio, dict) and 'raw' in pe_ratio:
                    self._save_alternative_data_point(
                        cursor, 'yahoo_finance', symbol, 'pe_ratio',
                        timestamp, float(pe_ratio['raw']),
                        {}
                    )
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error saving company profile: {e}")
    
    def _save_alternative_data_point(self, cursor, source: str, symbol: str, 
                                   data_type: str, timestamp: str, value: float, 
                                   metadata: Dict[str, Any]):
        """Save alternative data point to database"""
        cursor.execute('''
            INSERT INTO alternative_data 
            (source, symbol, data_type, timestamp, value, metadata_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            source, symbol, data_type, timestamp, value,
            json.dumps(metadata), datetime.now().isoformat()
        ))
    
    def fetch_stock_holders(self, symbol: str) -> Dict[str, Any]:
        """Fetch institutional and insider holdings"""
        try:
            logger.info(f"Fetching stock holders for {symbol}")
            
            response = self.api_client.call_api(
                'YahooFinance/get_stock_holders',
                query={'symbol': symbol}
            )
            
            if response:
                # Save holdings data
                self._save_stock_holders(symbol, response)
                return response
            
            return {}
            
        except Exception as e:
            logger.error(f"Error fetching stock holders for {symbol}: {e}")
            return {}
    
    def _save_stock_holders(self, symbol: str, holders_data: Dict[str, Any]):
        """Save stock holders data as alternative data points"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            timestamp = datetime.now().isoformat()
            
            # Process institutional holders
            institutional_holders = holders_data.get('institutionalHolders', {})
            if 'holders' in institutional_holders:
                total_institutional_shares = 0
                for holder in institutional_holders['holders']:
                    shares = holder.get('shares', {})
                    if isinstance(shares, dict) and 'raw' in shares:
                        total_institutional_shares += shares['raw']
                
                if total_institutional_shares > 0:
                    self._save_alternative_data_point(
                        cursor, 'yahoo_finance', symbol, 'institutional_ownership',
                        timestamp, float(total_institutional_shares),
                        {'holder_count': len(institutional_holders['holders'])}
                    )
            
            # Process insider holders
            insider_holders = holders_data.get('insiderHolders', {})
            if 'holders' in insider_holders:
                total_insider_shares = 0
                for holder in insider_holders['holders']:
                    position = holder.get('positionDirect', {})
                    if isinstance(position, dict) and 'raw' in position:
                        total_insider_shares += position['raw']
                
                if total_insider_shares > 0:
                    self._save_alternative_data_point(
                        cursor, 'yahoo_finance', symbol, 'insider_ownership',
                        timestamp, float(total_insider_shares),
                        {'holder_count': len(insider_holders['holders'])}
                    )
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error saving stock holders: {e}")
    
    def fetch_economic_indicators(self, indicator_codes: List[str] = None) -> Dict[str, Any]:
        """Fetch World Bank economic indicators"""
        try:
            if indicator_codes is None:
                # Default important economic indicators
                indicator_codes = [
                    'NY.GDP.MKTP.CD',  # GDP
                    'FP.CPI.TOTL.ZG',  # Inflation
                    'SL.UEM.TOTL.ZS',  # Unemployment
                    'SP.POP.TOTL'      # Population
                ]
            
            results = {}
            
            for indicator_code in indicator_codes:
                logger.info(f"Fetching economic indicator: {indicator_code}")
                
                try:
                    # Get indicator details
                    response = self.api_client.call_api(
                        'DataBank/indicator_detail',
                        path_params={'indicatorCode': indicator_code}
                    )
                    
                    if response:
                        results[indicator_code] = response
                        self._save_economic_indicator(indicator_code, response)
                    
                except Exception as e:
                    logger.error(f"Error fetching indicator {indicator_code}: {e}")
                
                # Rate limiting
                time.sleep(0.5)
            
            return results
            
        except Exception as e:
            logger.error(f"Error fetching economic indicators: {e}")
            return {}
    
    def _save_economic_indicator(self, indicator_code: str, indicator_data: Dict[str, Any]):
        """Save economic indicator to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            timestamp = datetime.now().isoformat()
            
            cursor.execute('''
                INSERT INTO economic_indicators 
                (indicator_code, indicator_name, country_code, value, date, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                indicator_code,
                indicator_data.get('indicatorName', ''),
                'WLD',  # World
                0.0,    # Placeholder value - would need actual data API
                datetime.now().date().isoformat(),
                timestamp
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error saving economic indicator: {e}")
    
    def analyze_sentiment_from_insights(self, symbol: str) -> Dict[str, Any]:
        """Analyze sentiment from various data sources"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get recent insights
            cursor.execute('''
                SELECT insight_type, content, score, timestamp 
                FROM stock_insights 
                WHERE symbol = ? 
                ORDER BY timestamp DESC 
                LIMIT 10
            ''', (symbol,))
            
            insights = cursor.fetchall()
            
            # Get recent analyst reports
            cursor.execute('''
                SELECT title, abstract, timestamp 
                FROM analyst_reports 
                WHERE symbol = ? 
                ORDER BY timestamp DESC 
                LIMIT 5
            ''', (symbol,))
            
            reports = cursor.fetchall()
            conn.close()
            
            # Calculate overall sentiment
            sentiment_scores = []
            
            # Process insights
            for insight_type, content, score, timestamp in insights:
                if score is not None:
                    sentiment_scores.append(score)
            
            # Process reports (simple keyword analysis)
            positive_keywords = ['buy', 'strong', 'outperform', 'positive', 'growth', 'bullish']
            negative_keywords = ['sell', 'weak', 'underperform', 'negative', 'decline', 'bearish']
            
            for title, abstract, timestamp in reports:
                text = f"{title} {abstract}".lower()
                positive_count = sum(1 for word in positive_keywords if word in text)
                negative_count = sum(1 for word in negative_keywords if word in text)
                
                if positive_count + negative_count > 0:
                    score = (positive_count - negative_count) / (positive_count + negative_count)
                    sentiment_scores.append(score)
            
            # Calculate overall sentiment
            if sentiment_scores:
                overall_sentiment = np.mean(sentiment_scores)
                sentiment_label = 'positive' if overall_sentiment > 0.1 else 'negative' if overall_sentiment < -0.1 else 'neutral'
                
                # Save sentiment to database
                self._save_sentiment_data(symbol, overall_sentiment, sentiment_label, 'aggregated')
                
                return {
                    'symbol': symbol,
                    'sentiment_score': overall_sentiment,
                    'sentiment_label': sentiment_label,
                    'data_points': len(sentiment_scores),
                    'timestamp': datetime.now().isoformat()
                }
            
            return {'symbol': symbol, 'sentiment_score': 0.0, 'sentiment_label': 'neutral'}
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment for {symbol}: {e}")
            return {}
    
    def _save_sentiment_data(self, symbol: str, sentiment_score: float, 
                           sentiment_label: str, source: str, content: str = ""):
        """Save sentiment data to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO sentiment_data 
                (symbol, sentiment_score, sentiment_label, source, content, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                symbol, sentiment_score, sentiment_label, source, content,
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error saving sentiment data: {e}")
    
    def get_comprehensive_analysis(self, symbol: str) -> Dict[str, Any]:
        """Get comprehensive analysis combining all alternative data sources"""
        try:
            logger.info(f"Generating comprehensive analysis for {symbol}")
            
            # Fetch all data sources
            insights = self.fetch_stock_insights(symbol)
            reports = self.fetch_analyst_reports(symbol)
            profile = self.fetch_company_profile(symbol)
            holders = self.fetch_stock_holders(symbol)
            sentiment = self.analyze_sentiment_from_insights(symbol)
            
            # Get historical alternative data
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT data_type, value, timestamp, metadata_json 
                FROM alternative_data 
                WHERE symbol = ? 
                ORDER BY timestamp DESC 
                LIMIT 50
            ''', (symbol,))
            
            alt_data = cursor.fetchall()
            conn.close()
            
            # Organize alternative data by type
            alt_data_by_type = {}
            for data_type, value, timestamp, metadata_json in alt_data:
                if data_type not in alt_data_by_type:
                    alt_data_by_type[data_type] = []
                
                metadata = json.loads(metadata_json) if metadata_json else {}
                alt_data_by_type[data_type].append({
                    'value': value,
                    'timestamp': timestamp,
                    'metadata': metadata
                })
            
            # Calculate data quality score
            data_quality_score = self._calculate_data_quality_score(
                insights, reports, profile, holders, alt_data
            )
            
            return {
                'symbol': symbol,
                'analysis_timestamp': datetime.now().isoformat(),
                'data_quality_score': data_quality_score,
                'insights': insights,
                'analyst_reports': reports,
                'company_profile': profile,
                'stock_holders': holders,
                'sentiment_analysis': sentiment,
                'alternative_data': alt_data_by_type,
                'summary': {
                    'total_data_points': len(alt_data),
                    'data_sources_available': len([x for x in [insights, reports, profile, holders] if x]),
                    'sentiment_score': sentiment.get('sentiment_score', 0.0),
                    'sentiment_label': sentiment.get('sentiment_label', 'neutral')
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating comprehensive analysis for {symbol}: {e}")
            return {'error': str(e)}
    
    def _calculate_data_quality_score(self, insights: Dict, reports: Dict, 
                                    profile: Dict, holders: Dict, alt_data: List) -> float:
        """Calculate data quality score based on available data"""
        try:
            score = 0.0
            max_score = 5.0
            
            # Score based on data availability
            if insights:
                score += 1.0
            if reports:
                score += 1.0
            if profile:
                score += 1.0
            if holders:
                score += 1.0
            if alt_data:
                score += 1.0
            
            return score / max_score
            
        except:
            return 0.0
    
    def get_data_source_status(self) -> Dict[str, Any]:
        """Get status of all data sources"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            status = {}
            
            # Check each data source
            for source_name, source_config in self.data_sources.items():
                # Count recent data points
                cursor.execute('''
                    SELECT COUNT(*) FROM alternative_data 
                    WHERE source = ? AND timestamp > ?
                ''', (source_name, (datetime.now() - timedelta(days=1)).isoformat()))
                
                recent_count = cursor.fetchone()[0]
                
                status[source_name] = {
                    'name': source_config.name,
                    'description': source_config.description,
                    'enabled': source_config.enabled,
                    'update_frequency': source_config.update_frequency,
                    'data_type': source_config.data_type,
                    'recent_data_points': recent_count,
                    'last_update': self._get_last_update(cursor, source_name)
                }
            
            conn.close()
            
            return {
                'status': status,
                'total_sources': len(self.data_sources),
                'active_sources': len([s for s in self.data_sources.values() if s.enabled]),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting data source status: {e}")
            return {'error': str(e)}
    
    def _get_last_update(self, cursor, source_name: str) -> str:
        """Get last update timestamp for a data source"""
        try:
            cursor.execute('''
                SELECT MAX(timestamp) FROM alternative_data WHERE source = ?
            ''', (source_name,))
            
            result = cursor.fetchone()
            return result[0] if result and result[0] else 'Never'
            
        except:
            return 'Unknown'

def main():
    """Test the alternative data sources integration"""
    print("Alternative Data Sources Integration for Socrates AI")
    print("=" * 55)
    
    # Initialize data manager
    manager = AlternativeDataManager()
    
    print("1. Testing data source status...")
    status = manager.get_data_source_status()
    print(f"   ✓ Total data sources: {status['total_sources']}")
    print(f"   ✓ Active data sources: {status['active_sources']}")
    
    print("\n2. Testing stock insights...")
    insights = manager.fetch_stock_insights("AAPL")
    if insights:
        print("   ✓ Stock insights fetched successfully")
        print(f"   ✓ Insights categories: {len(insights.get('insights', {}))}")
    else:
        print("   ✗ Failed to fetch stock insights")
    
    print("\n3. Testing analyst reports...")
    reports = manager.fetch_analyst_reports("AAPL")
    if reports:
        print("   ✓ Analyst reports fetched successfully")
    else:
        print("   ✗ Failed to fetch analyst reports")
    
    print("\n4. Testing company profile...")
    profile = manager.fetch_company_profile("AAPL")
    if profile:
        print("   ✓ Company profile fetched successfully")
        asset_profile = profile.get('assetProfile', {})
        if asset_profile:
            print(f"   ✓ Company: {asset_profile.get('longBusinessSummary', '')[:50]}...")
            print(f"   ✓ Sector: {asset_profile.get('sector', 'N/A')}")
            print(f"   ✓ Employees: {asset_profile.get('fullTimeEmployees', 'N/A'):,}" if asset_profile.get('fullTimeEmployees') else "   ✓ Employees: N/A")
    else:
        print("   ✗ Failed to fetch company profile")
    
    print("\n5. Testing stock holders...")
    holders = manager.fetch_stock_holders("AAPL")
    if holders:
        print("   ✓ Stock holders fetched successfully")
        institutional = holders.get('institutionalHolders', {})
        if institutional and 'holders' in institutional:
            print(f"   ✓ Institutional holders: {len(institutional['holders'])}")
    else:
        print("   ✗ Failed to fetch stock holders")
    
    print("\n6. Testing economic indicators...")
    indicators = manager.fetch_economic_indicators(['NY.GDP.MKTP.CD'])
    if indicators:
        print(f"   ✓ Economic indicators fetched: {len(indicators)}")
        for code, data in indicators.items():
            print(f"   ✓ {code}: {data.get('indicatorName', 'N/A')}")
    else:
        print("   ✗ Failed to fetch economic indicators")
    
    print("\n7. Testing sentiment analysis...")
    sentiment = manager.analyze_sentiment_from_insights("AAPL")
    if sentiment:
        print(f"   ✓ Sentiment analysis completed")
        print(f"   ✓ Sentiment: {sentiment.get('sentiment_label', 'N/A')} ({sentiment.get('sentiment_score', 0.0):.2f})")
        print(f"   ✓ Data points: {sentiment.get('data_points', 0)}")
    else:
        print("   ✗ Failed to analyze sentiment")
    
    print("\n8. Testing comprehensive analysis...")
    analysis = manager.get_comprehensive_analysis("AAPL")
    if 'error' not in analysis:
        print("   ✓ Comprehensive analysis completed")
        print(f"   ✓ Data quality score: {analysis.get('data_quality_score', 0.0):.2f}")
        print(f"   ✓ Total data points: {analysis.get('summary', {}).get('total_data_points', 0)}")
        print(f"   ✓ Data sources available: {analysis.get('summary', {}).get('data_sources_available', 0)}")
    else:
        print(f"   ✗ Failed comprehensive analysis: {analysis['error']}")
    
    print("\n9. Final data source status...")
    final_status = manager.get_data_source_status()
    print("   Data Source Summary:")
    for source_name, source_info in final_status['status'].items():
        print(f"   - {source_info['name']}: {source_info['recent_data_points']} recent data points")
    
    print("\nAlternative data sources integration test completed!")
    print("System is ready for integration with Socrates AI!")

if __name__ == "__main__":
    main()

