#!/usr/bin/env python3
"""
Socrates AI Data Collector
Interfaces with various APIs to collect comprehensive market data

Data Sources:
- Yahoo Finance (via Manus API Hub)
- World Bank DataBank (via Manus API Hub)
- Alpha Vantage API
- FRED Economic Data

Author: AI Replication Project
"""

import sys
import os
import requests
import sqlite3
import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import pandas as pd

# Add Manus API client
sys.path.append('/opt/.manus/.sandbox-runtime')
from data_api import ApiClient

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class DataSource:
    """Configuration for data sources"""
    name: str
    api_type: str  # "manus", "external"
    base_url: Optional[str] = None
    api_key: Optional[str] = None
    rate_limit: int = 5  # requests per second
    
class DataCollector:
    """
    Main data collection system for Socrates AI
    
    Handles:
    - Market data collection from multiple sources
    - Economic indicators
    - Data validation and cleaning
    - Database storage
    """
    
    def __init__(self, db_path: str = "socrates_data.db"):
        self.db_path = db_path
        self.manus_client = ApiClient()
        
        # Configure data sources
        self.data_sources = {
            "yahoo_finance": DataSource("Yahoo Finance", "manus"),
            "world_bank": DataSource("World Bank", "manus"),
            "alpha_vantage": DataSource("Alpha Vantage", "external", 
                                      "https://www.alphavantage.co/query"),
            "fred": DataSource("FRED", "external", 
                             "https://api.stlouisfed.org/fred")
        }
        
        # Initialize database
        self._init_database()
        
        logger.info("Data Collector initialized")
    
    def _init_database(self):
        """Initialize database tables for data storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Market data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS market_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                date TEXT NOT NULL,
                open_price REAL,
                high_price REAL,
                low_price REAL,
                close_price REAL,
                volume INTEGER,
                adjusted_close REAL,
                currency TEXT DEFAULT 'USD',
                source TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(symbol, date, source)
            )
        ''')
        
        # Economic indicators table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS economic_indicators (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                indicator_id TEXT NOT NULL,
                name TEXT,
                value REAL,
                date TEXT,
                country TEXT,
                source TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(indicator_id, date, country, source)
            )
        ''')
        
        # Forex data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS forex_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pair TEXT NOT NULL,
                date TEXT NOT NULL,
                rate REAL,
                source TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(pair, date, source)
            )
        ''')
        
        # Commodities data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS commodities_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                commodity TEXT NOT NULL,
                date TEXT NOT NULL,
                price REAL,
                currency TEXT DEFAULT 'USD',
                source TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(commodity, date, source)
            )
        ''')
        
        # Data collection log
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS collection_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                collection_date TEXT NOT NULL,
                data_type TEXT,
                symbol TEXT,
                records_collected INTEGER,
                source TEXT,
                status TEXT,
                error_message TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
        logger.info("Database tables initialized")
    
    def collect_stock_data(self, symbols: List[str], range_period: str = "2y") -> Dict[str, Any]:
        """
        Collect stock data using Yahoo Finance API
        
        Args:
            symbols: List of stock symbols
            range_period: Time range (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            
        Returns:
            Collection results summary
        """
        logger.info(f"Collecting stock data for {len(symbols)} symbols")
        
        results = {
            "successful": 0,
            "failed": 0,
            "errors": [],
            "symbols_processed": []
        }
        
        for symbol in symbols:
            try:
                # Call Yahoo Finance API via Manus
                response = self.manus_client.call_api('YahooFinance/get_stock_chart', query={
                    'symbol': symbol,
                    'region': 'US',
                    'interval': '1d',
                    'range': range_period,
                    'includeAdjustedClose': True,
                    'events': 'div,split'
                })
                
                if response and 'chart' in response and 'result' in response['chart']:
                    result = response['chart']['result'][0]
                    
                    # Extract data
                    timestamps = result['timestamp']
                    quotes = result['indicators']['quote'][0]
                    meta = result['meta']
                    
                    # Store data
                    records_stored = self._store_stock_data(symbol, timestamps, quotes, meta)
                    
                    results["successful"] += 1
                    results["symbols_processed"].append(symbol)
                    
                    # Log collection
                    self._log_collection("stock_data", symbol, records_stored, "yahoo_finance", "success")
                    
                    logger.info(f"Collected {records_stored} records for {symbol}")
                    
                else:
                    error_msg = f"No data returned for {symbol}"
                    results["failed"] += 1
                    results["errors"].append(error_msg)
                    self._log_collection("stock_data", symbol, 0, "yahoo_finance", "failed", error_msg)
                    
                # Rate limiting
                time.sleep(0.2)  # 5 requests per second
                
            except Exception as e:
                error_msg = f"Error collecting data for {symbol}: {str(e)}"
                results["failed"] += 1
                results["errors"].append(error_msg)
                self._log_collection("stock_data", symbol, 0, "yahoo_finance", "error", error_msg)
                logger.error(error_msg)
        
        logger.info(f"Stock data collection completed: {results['successful']} successful, {results['failed']} failed")
        return results
    
    def collect_economic_indicators(self, indicators: List[str] = None) -> Dict[str, Any]:
        """
        Collect economic indicators from World Bank
        
        Args:
            indicators: List of indicator IDs (default: common economic indicators)
            
        Returns:
            Collection results summary
        """
        if indicators is None:
            # Common economic indicators
            indicators = [
                "NY.GDP.MKTP.CD",  # GDP (current US$)
                "SP.POP.TOTL",     # Population, total
                "NY.GDP.PCAP.CD",  # GDP per capita
                "SL.UEM.TOTL.ZS",  # Unemployment rate
                "FP.CPI.TOTL.ZG"   # Inflation rate
            ]
        
        logger.info(f"Collecting economic indicators: {len(indicators)} indicators")
        
        results = {
            "successful": 0,
            "failed": 0,
            "errors": [],
            "indicators_processed": []
        }
        
        for indicator_id in indicators:
            try:
                # Get indicator details
                detail_response = self.manus_client.call_api('DataBank/indicator_detail', 
                                                           path_params={'indicatorCode': indicator_id})
                
                if detail_response:
                    # Store indicator information
                    records_stored = self._store_economic_indicator(detail_response)
                    
                    results["successful"] += 1
                    results["indicators_processed"].append(indicator_id)
                    
                    self._log_collection("economic_indicator", indicator_id, records_stored, 
                                       "world_bank", "success")
                    
                    logger.info(f"Collected indicator: {indicator_id}")
                    
                else:
                    error_msg = f"No data returned for indicator {indicator_id}"
                    results["failed"] += 1
                    results["errors"].append(error_msg)
                    self._log_collection("economic_indicator", indicator_id, 0, 
                                       "world_bank", "failed", error_msg)
                
                # Rate limiting
                time.sleep(0.2)
                
            except Exception as e:
                error_msg = f"Error collecting indicator {indicator_id}: {str(e)}"
                results["failed"] += 1
                results["errors"].append(error_msg)
                self._log_collection("economic_indicator", indicator_id, 0, 
                                   "world_bank", "error", error_msg)
                logger.error(error_msg)
        
        logger.info(f"Economic indicators collection completed: {results['successful']} successful, {results['failed']} failed")
        return results
    
    def collect_forex_data(self, currency_pairs: List[str] = None) -> Dict[str, Any]:
        """
        Collect forex data for major currency pairs
        
        Args:
            currency_pairs: List of currency pairs (e.g., ['EURUSD', 'GBPUSD'])
            
        Returns:
            Collection results summary
        """
        if currency_pairs is None:
            # Major currency pairs
            currency_pairs = [
                "EURUSD=X", "GBPUSD=X", "USDJPY=X", "USDCHF=X",
                "AUDUSD=X", "USDCAD=X", "NZDUSD=X"
            ]
        
        logger.info(f"Collecting forex data for {len(currency_pairs)} pairs")
        
        results = {
            "successful": 0,
            "failed": 0,
            "errors": [],
            "pairs_processed": []
        }
        
        for pair in currency_pairs:
            try:
                # Use Yahoo Finance for forex data
                response = self.manus_client.call_api('YahooFinance/get_stock_chart', query={
                    'symbol': pair,
                    'region': 'US',
                    'interval': '1d',
                    'range': '1y',
                    'includeAdjustedClose': False
                })
                
                if response and 'chart' in response and 'result' in response['chart']:
                    result = response['chart']['result'][0]
                    
                    # Extract forex data
                    timestamps = result['timestamp']
                    quotes = result['indicators']['quote'][0]
                    
                    # Store forex data
                    records_stored = self._store_forex_data(pair, timestamps, quotes)
                    
                    results["successful"] += 1
                    results["pairs_processed"].append(pair)
                    
                    self._log_collection("forex_data", pair, records_stored, "yahoo_finance", "success")
                    
                    logger.info(f"Collected {records_stored} forex records for {pair}")
                    
                else:
                    error_msg = f"No forex data returned for {pair}"
                    results["failed"] += 1
                    results["errors"].append(error_msg)
                    self._log_collection("forex_data", pair, 0, "yahoo_finance", "failed", error_msg)
                
                # Rate limiting
                time.sleep(0.2)
                
            except Exception as e:
                error_msg = f"Error collecting forex data for {pair}: {str(e)}"
                results["failed"] += 1
                results["errors"].append(error_msg)
                self._log_collection("forex_data", pair, 0, "yahoo_finance", "error", error_msg)
                logger.error(error_msg)
        
        logger.info(f"Forex data collection completed: {results['successful']} successful, {results['failed']} failed")
        return results
    
    def collect_commodities_data(self, commodities: List[str] = None) -> Dict[str, Any]:
        """
        Collect commodities data
        
        Args:
            commodities: List of commodity symbols
            
        Returns:
            Collection results summary
        """
        if commodities is None:
            # Major commodities
            commodities = [
                "GC=F",   # Gold
                "SI=F",   # Silver
                "CL=F",   # Crude Oil
                "NG=F",   # Natural Gas
                "HG=F",   # Copper
                "ZW=F",   # Wheat
                "ZC=F",   # Corn
                "ZS=F"    # Soybeans
            ]
        
        logger.info(f"Collecting commodities data for {len(commodities)} commodities")
        
        results = {
            "successful": 0,
            "failed": 0,
            "errors": [],
            "commodities_processed": []
        }
        
        for commodity in commodities:
            try:
                # Use Yahoo Finance for commodities data
                response = self.manus_client.call_api('YahooFinance/get_stock_chart', query={
                    'symbol': commodity,
                    'region': 'US',
                    'interval': '1d',
                    'range': '2y',
                    'includeAdjustedClose': False
                })
                
                if response and 'chart' in response and 'result' in response['chart']:
                    result = response['chart']['result'][0]
                    
                    # Extract commodities data
                    timestamps = result['timestamp']
                    quotes = result['indicators']['quote'][0]
                    meta = result['meta']
                    
                    # Store commodities data
                    records_stored = self._store_commodities_data(commodity, timestamps, quotes, meta)
                    
                    results["successful"] += 1
                    results["commodities_processed"].append(commodity)
                    
                    self._log_collection("commodities_data", commodity, records_stored, 
                                       "yahoo_finance", "success")
                    
                    logger.info(f"Collected {records_stored} commodities records for {commodity}")
                    
                else:
                    error_msg = f"No commodities data returned for {commodity}"
                    results["failed"] += 1
                    results["errors"].append(error_msg)
                    self._log_collection("commodities_data", commodity, 0, 
                                       "yahoo_finance", "failed", error_msg)
                
                # Rate limiting
                time.sleep(0.2)
                
            except Exception as e:
                error_msg = f"Error collecting commodities data for {commodity}: {str(e)}"
                results["failed"] += 1
                results["errors"].append(error_msg)
                self._log_collection("commodities_data", commodity, 0, 
                                   "yahoo_finance", "error", error_msg)
                logger.error(error_msg)
        
        logger.info(f"Commodities data collection completed: {results['successful']} successful, {results['failed']} failed")
        return results
    
    def _store_stock_data(self, symbol: str, timestamps: List[int], quotes: Dict, meta: Dict) -> int:
        """Store stock data in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        records_stored = 0
        currency = meta.get('currency', 'USD')
        
        for i, timestamp in enumerate(timestamps):
            if i < len(quotes.get('open', [])):
                date = datetime.fromtimestamp(timestamp).date().isoformat()
                
                try:
                    cursor.execute('''
                        INSERT OR REPLACE INTO market_data 
                        (symbol, date, open_price, high_price, low_price, close_price, 
                         volume, adjusted_close, currency, source)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        symbol, date,
                        quotes['open'][i] if quotes['open'][i] is not None else 0,
                        quotes['high'][i] if quotes['high'][i] is not None else 0,
                        quotes['low'][i] if quotes['low'][i] is not None else 0,
                        quotes['close'][i] if quotes['close'][i] is not None else 0,
                        quotes['volume'][i] if quotes['volume'][i] is not None else 0,
                        quotes['close'][i] if quotes['close'][i] is not None else 0,  # Use close as adjusted for now
                        currency,
                        'yahoo_finance'
                    ))
                    records_stored += 1
                except Exception as e:
                    logger.warning(f"Error storing record for {symbol} on {date}: {e}")
        
        conn.commit()
        conn.close()
        
        return records_stored
    
    def _store_economic_indicator(self, indicator_data: Dict) -> int:
        """Store economic indicator data in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO economic_indicators 
                (indicator_id, name, value, date, country, source)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                indicator_data.get('indicatorCode', ''),
                indicator_data.get('indicatorName', ''),
                0,  # Placeholder value - would need actual time series data
                datetime.now().date().isoformat(),
                'Global',  # Placeholder
                'world_bank'
            ))
            
            conn.commit()
            conn.close()
            return 1
            
        except Exception as e:
            logger.error(f"Error storing economic indicator: {e}")
            conn.close()
            return 0
    
    def _store_forex_data(self, pair: str, timestamps: List[int], quotes: Dict) -> int:
        """Store forex data in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        records_stored = 0
        
        for i, timestamp in enumerate(timestamps):
            if i < len(quotes.get('close', [])) and quotes['close'][i] is not None:
                date = datetime.fromtimestamp(timestamp).date().isoformat()
                
                try:
                    cursor.execute('''
                        INSERT OR REPLACE INTO forex_data 
                        (pair, date, rate, source)
                        VALUES (?, ?, ?, ?)
                    ''', (
                        pair, date, quotes['close'][i], 'yahoo_finance'
                    ))
                    records_stored += 1
                except Exception as e:
                    logger.warning(f"Error storing forex record for {pair} on {date}: {e}")
        
        conn.commit()
        conn.close()
        
        return records_stored
    
    def _store_commodities_data(self, commodity: str, timestamps: List[int], quotes: Dict, meta: Dict) -> int:
        """Store commodities data in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        records_stored = 0
        currency = meta.get('currency', 'USD')
        
        for i, timestamp in enumerate(timestamps):
            if i < len(quotes.get('close', [])) and quotes['close'][i] is not None:
                date = datetime.fromtimestamp(timestamp).date().isoformat()
                
                try:
                    cursor.execute('''
                        INSERT OR REPLACE INTO commodities_data 
                        (commodity, date, price, currency, source)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (
                        commodity, date, quotes['close'][i], currency, 'yahoo_finance'
                    ))
                    records_stored += 1
                except Exception as e:
                    logger.warning(f"Error storing commodities record for {commodity} on {date}: {e}")
        
        conn.commit()
        conn.close()
        
        return records_stored
    
    def _log_collection(self, data_type: str, symbol: str, records: int, source: str, 
                       status: str, error_msg: str = None):
        """Log data collection activity"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO collection_log 
            (collection_date, data_type, symbol, records_collected, source, status, error_message)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            data_type,
            symbol,
            records,
            source,
            status,
            error_msg
        ))
        
        conn.commit()
        conn.close()
    
    def get_collection_summary(self) -> Dict[str, Any]:
        """Get summary of data collection activities"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get record counts by table
        tables = ['market_data', 'economic_indicators', 'forex_data', 'commodities_data']
        record_counts = {}
        
        for table in tables:
            cursor.execute(f'SELECT COUNT(*) FROM {table}')
            record_counts[table] = cursor.fetchone()[0]
        
        # Get recent collection activity
        cursor.execute('''
            SELECT data_type, COUNT(*) as collections, 
                   SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as successful,
                   SUM(records_collected) as total_records
            FROM collection_log 
            WHERE collection_date >= date('now', '-7 days')
            GROUP BY data_type
        ''')
        
        recent_activity = {}
        for row in cursor.fetchall():
            recent_activity[row[0]] = {
                'collections': row[1],
                'successful': row[2],
                'total_records': row[3]
            }
        
        conn.close()
        
        return {
            'record_counts': record_counts,
            'recent_activity': recent_activity,
            'last_updated': datetime.now().isoformat()
        }

def main():
    """Main function for testing data collection"""
    collector = DataCollector()
    
    print("Socrates AI Data Collector")
    print("=" * 40)
    
    # Test stock data collection
    test_symbols = ["AAPL", "GOOGL", "MSFT", "SPY", "GLD"]
    print(f"Collecting stock data for: {test_symbols}")
    stock_results = collector.collect_stock_data(test_symbols, "6mo")
    print(f"Stock data collection: {stock_results['successful']} successful, {stock_results['failed']} failed")
    
    # Test economic indicators
    print("\nCollecting economic indicators...")
    econ_results = collector.collect_economic_indicators()
    print(f"Economic indicators: {econ_results['successful']} successful, {econ_results['failed']} failed")
    
    # Test forex data
    print("\nCollecting forex data...")
    forex_results = collector.collect_forex_data()
    print(f"Forex data: {forex_results['successful']} successful, {forex_results['failed']} failed")
    
    # Test commodities data
    print("\nCollecting commodities data...")
    commodities_results = collector.collect_commodities_data()
    print(f"Commodities data: {commodities_results['successful']} successful, {commodities_results['failed']} failed")
    
    # Get collection summary
    print("\nCollection Summary:")
    summary = collector.get_collection_summary()
    for table, count in summary['record_counts'].items():
        print(f"{table}: {count} records")
    
    print("\nData collection test completed!")

if __name__ == "__main__":
    main()

