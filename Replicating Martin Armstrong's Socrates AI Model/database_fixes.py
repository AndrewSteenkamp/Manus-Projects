#!/usr/bin/env python3
"""
Database Schema Fixes and Improvements for Socrates AI
Addresses common database issues and implements better schema management
"""

import sqlite3
import os
import logging
from datetime import datetime
from typing import Dict, Any, List
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Enhanced database manager with schema validation and migration support"""
    
    def __init__(self, db_path: str = "socrates_data.db"):
        self.db_path = db_path
        self.schema_version = "2.0"
        
    def get_connection(self):
        """Get database connection with proper configuration"""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        conn.execute("PRAGMA journal_mode=WAL")  # Better concurrency
        conn.execute("PRAGMA synchronous=NORMAL")  # Better performance
        conn.execute("PRAGMA cache_size=10000")  # Larger cache
        conn.execute("PRAGMA temp_store=MEMORY")  # Use memory for temp tables
        return conn
    
    def initialize_database(self):
        """Initialize database with improved schema"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Create schema version table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS schema_info (
                    version TEXT PRIMARY KEY,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    description TEXT
                )
            ''')
            
            # Market data table with improved schema
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
                    source TEXT DEFAULT 'unknown',
                    data_quality REAL DEFAULT 1.0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(symbol, date, source)
                )
            ''')
            
            # Create indexes for better performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_market_symbol_date ON market_data(symbol, date)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_market_date ON market_data(date)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_market_symbol ON market_data(symbol)')
            
            # Economic indicators table with improved schema
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS economic_indicators (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    indicator_id TEXT NOT NULL,
                    name TEXT,
                    value REAL,
                    date TEXT,
                    country TEXT,
                    source TEXT,
                    unit TEXT,
                    frequency TEXT,
                    data_quality REAL DEFAULT 1.0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(indicator_id, date, country, source)
                )
            ''')
            
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_econ_indicator_date ON economic_indicators(indicator_id, date)')
            
            # Forex data table with improved schema
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS forex_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pair TEXT NOT NULL,
                    date TEXT NOT NULL,
                    rate REAL,
                    bid REAL,
                    ask REAL,
                    spread REAL,
                    volume INTEGER,
                    source TEXT DEFAULT 'unknown',
                    data_quality REAL DEFAULT 1.0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(pair, date, source)
                )
            ''')
            
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_forex_pair_date ON forex_data(pair, date)')
            
            # Commodities data table with improved schema
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS commodities_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    commodity TEXT NOT NULL,
                    date TEXT NOT NULL,
                    price REAL,
                    volume INTEGER,
                    open_interest INTEGER,
                    currency TEXT DEFAULT 'USD',
                    exchange TEXT,
                    contract_month TEXT,
                    source TEXT DEFAULT 'unknown',
                    data_quality REAL DEFAULT 1.0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(commodity, date, source)
                )
            ''')
            
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_commodities_commodity_date ON commodities_data(commodity, date)')
            
            # Analysis results table with improved schema
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS analysis_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    analysis_id TEXT UNIQUE,
                    analysis_date TEXT NOT NULL,
                    symbol TEXT,
                    analysis_type TEXT,
                    results TEXT,
                    confidence_score REAL,
                    execution_time REAL,
                    model_version TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    expires_at TEXT
                )
            ''')
            
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_analysis_symbol_date ON analysis_results(symbol, analysis_date)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_analysis_type ON analysis_results(analysis_type)')
            
            # Data collection log with improved schema
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS collection_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    collection_id TEXT UNIQUE,
                    collection_date TEXT NOT NULL,
                    data_type TEXT,
                    symbol TEXT,
                    records_collected INTEGER DEFAULT 0,
                    records_failed INTEGER DEFAULT 0,
                    source TEXT,
                    status TEXT,
                    error_message TEXT,
                    execution_time REAL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_collection_date ON collection_log(collection_date)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_collection_status ON collection_log(status)')
            
            # System configuration table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_config (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    data_type TEXT DEFAULT 'string',
                    description TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Cache table for performance optimization
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cache (
                    cache_key TEXT PRIMARY KEY,
                    cache_value TEXT,
                    expires_at TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_cache_expires ON cache(expires_at)')
            
            # Insert schema version
            cursor.execute('''
                INSERT OR REPLACE INTO schema_info (version, description)
                VALUES (?, ?)
            ''', (self.schema_version, "Enhanced schema with performance optimizations"))
            
            # Insert default configuration
            default_configs = [
                ('api_rate_limit', '100', 'integer', 'API requests per minute'),
                ('max_analysis_age', '3600', 'integer', 'Max age of cached analysis in seconds'),
                ('data_retention_days', '365', 'integer', 'Days to retain historical data'),
                ('enable_caching', 'true', 'boolean', 'Enable result caching'),
                ('log_level', 'INFO', 'string', 'Logging level')
            ]
            
            for key, value, data_type, description in default_configs:
                cursor.execute('''
                    INSERT OR IGNORE INTO system_config (key, value, data_type, description)
                    VALUES (?, ?, ?, ?)
                ''', (key, value, data_type, description))
            
            conn.commit()
            logger.info(f"Database initialized successfully with schema version {self.schema_version}")
            
        except Exception as e:
            conn.rollback()
            logger.error(f"Error initializing database: {e}")
            raise
        finally:
            conn.close()
    
    def migrate_existing_data(self):
        """Migrate data from old schema to new schema"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Check if old tables exist and migrate data
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            existing_tables = [row[0] for row in cursor.fetchall()]
            
            # Add missing columns to existing tables
            if 'market_data' in existing_tables:
                self._add_column_if_not_exists(cursor, 'market_data', 'source', 'TEXT DEFAULT "unknown"')
                self._add_column_if_not_exists(cursor, 'market_data', 'data_quality', 'REAL DEFAULT 1.0')
                self._add_column_if_not_exists(cursor, 'market_data', 'created_at', 'TEXT')
                self._add_column_if_not_exists(cursor, 'market_data', 'updated_at', 'TEXT')
                
                # Update NULL values with current timestamp
                cursor.execute("UPDATE market_data SET created_at = datetime('now') WHERE created_at IS NULL")
                cursor.execute("UPDATE market_data SET updated_at = datetime('now') WHERE updated_at IS NULL")
            
            if 'economic_indicators' in existing_tables:
                self._add_column_if_not_exists(cursor, 'economic_indicators', 'unit', 'TEXT')
                self._add_column_if_not_exists(cursor, 'economic_indicators', 'frequency', 'TEXT')
                self._add_column_if_not_exists(cursor, 'economic_indicators', 'data_quality', 'REAL DEFAULT 1.0')
                self._add_column_if_not_exists(cursor, 'economic_indicators', 'created_at', 'TEXT')
                self._add_column_if_not_exists(cursor, 'economic_indicators', 'updated_at', 'TEXT')
                
                # Update NULL values with current timestamp
                cursor.execute("UPDATE economic_indicators SET created_at = datetime('now') WHERE created_at IS NULL")
                cursor.execute("UPDATE economic_indicators SET updated_at = datetime('now') WHERE updated_at IS NULL")
            
            if 'forex_data' in existing_tables:
                self._add_column_if_not_exists(cursor, 'forex_data', 'bid', 'REAL')
                self._add_column_if_not_exists(cursor, 'forex_data', 'ask', 'REAL')
                self._add_column_if_not_exists(cursor, 'forex_data', 'spread', 'REAL')
                self._add_column_if_not_exists(cursor, 'forex_data', 'volume', 'INTEGER')
                self._add_column_if_not_exists(cursor, 'forex_data', 'source', 'TEXT DEFAULT "unknown"')
                self._add_column_if_not_exists(cursor, 'forex_data', 'data_quality', 'REAL DEFAULT 1.0')
                self._add_column_if_not_exists(cursor, 'forex_data', 'created_at', 'TEXT')
                self._add_column_if_not_exists(cursor, 'forex_data', 'updated_at', 'TEXT')
                
                # Update NULL values with current timestamp
                cursor.execute("UPDATE forex_data SET created_at = datetime('now') WHERE created_at IS NULL")
                cursor.execute("UPDATE forex_data SET updated_at = datetime('now') WHERE updated_at IS NULL")
            
            if 'commodities_data' in existing_tables:
                self._add_column_if_not_exists(cursor, 'commodities_data', 'volume', 'INTEGER')
                self._add_column_if_not_exists(cursor, 'commodities_data', 'open_interest', 'INTEGER')
                self._add_column_if_not_exists(cursor, 'commodities_data', 'exchange', 'TEXT')
                self._add_column_if_not_exists(cursor, 'commodities_data', 'contract_month', 'TEXT')
                self._add_column_if_not_exists(cursor, 'commodities_data', 'source', 'TEXT DEFAULT "unknown"')
                self._add_column_if_not_exists(cursor, 'commodities_data', 'data_quality', 'REAL DEFAULT 1.0')
                self._add_column_if_not_exists(cursor, 'commodities_data', 'created_at', 'TEXT')
                self._add_column_if_not_exists(cursor, 'commodities_data', 'updated_at', 'TEXT')
                
                # Update NULL values with current timestamp
                cursor.execute("UPDATE commodities_data SET created_at = datetime('now') WHERE created_at IS NULL")
                cursor.execute("UPDATE commodities_data SET updated_at = datetime('now') WHERE updated_at IS NULL")
            
            conn.commit()
            logger.info("Database migration completed successfully")
            
        except Exception as e:
            conn.rollback()
            logger.error(f"Error during database migration: {e}")
            raise
        finally:
            conn.close()
    
    def _add_column_if_not_exists(self, cursor, table_name: str, column_name: str, column_definition: str):
        """Add column if it doesn't exist"""
        try:
            cursor.execute(f"SELECT {column_name} FROM {table_name} LIMIT 1")
        except sqlite3.OperationalError:
            # Column doesn't exist, add it
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_definition}")
            logger.info(f"Added column {column_name} to table {table_name}")
    
    def optimize_database(self):
        """Optimize database performance"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Analyze tables for query optimization
            cursor.execute("ANALYZE")
            
            # Vacuum database to reclaim space
            cursor.execute("VACUUM")
            
            # Update statistics
            cursor.execute("PRAGMA optimize")
            
            logger.info("Database optimization completed")
            
        except Exception as e:
            logger.error(f"Error optimizing database: {e}")
            raise
        finally:
            conn.close()
    
    def cleanup_old_data(self, retention_days: int = 365):
        """Clean up old data based on retention policy"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cutoff_date = datetime.now().strftime('%Y-%m-%d')
            
            # Clean up old analysis results (if table exists)
            try:
                cursor.execute('''
                    DELETE FROM analysis_results 
                    WHERE created_at < date(?, '-{} days')
                '''.format(retention_days), (cutoff_date,))
                logger.info(f"Cleaned up {cursor.rowcount} old analysis results")
            except sqlite3.OperationalError:
                logger.info("Analysis results table not found or no created_at column")
            
            # Clean up old collection logs (if table exists)
            try:
                cursor.execute('''
                    DELETE FROM collection_log 
                    WHERE created_at < date(?, '-{} days')
                '''.format(retention_days * 2), (cutoff_date,))  # Keep logs longer
                logger.info(f"Cleaned up {cursor.rowcount} old collection logs")
            except sqlite3.OperationalError:
                logger.info("Collection log table not found or no created_at column")
            
            # Clean up expired cache entries (if table exists)
            try:
                cursor.execute('''
                    DELETE FROM cache 
                    WHERE expires_at < datetime('now')
                ''')
                logger.info(f"Cleaned up {cursor.rowcount} expired cache entries")
            except sqlite3.OperationalError:
                logger.info("Cache table not found or no expires_at column")
            
            conn.commit()
            logger.info("Data cleanup completed successfully")
            
        except Exception as e:
            conn.rollback()
            logger.error(f"Error cleaning up old data: {e}")
            raise
        finally:
            conn.close()
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            stats = {}
            
            # Get table sizes
            tables = ['market_data', 'economic_indicators', 'forex_data', 'commodities_data', 
                     'analysis_results', 'collection_log']
            
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                stats[f"{table}_count"] = cursor.fetchone()[0]
            
            # Get database file size
            if os.path.exists(self.db_path):
                stats['database_size_mb'] = os.path.getsize(self.db_path) / (1024 * 1024)
            
            # Get schema version
            cursor.execute("SELECT version FROM schema_info ORDER BY created_at DESC LIMIT 1")
            result = cursor.fetchone()
            stats['schema_version'] = result[0] if result else 'unknown'
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            return {}
        finally:
            conn.close()
    
    def backup_database(self, backup_path: str = None):
        """Create database backup"""
        if backup_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = f"socrates_backup_{timestamp}.db"
        
        try:
            # Create backup using SQLite backup API
            source = self.get_connection()
            backup = sqlite3.connect(backup_path)
            
            source.backup(backup)
            
            backup.close()
            source.close()
            
            logger.info(f"Database backup created: {backup_path}")
            return backup_path
            
        except Exception as e:
            logger.error(f"Error creating database backup: {e}")
            raise

def main():
    """Main function to run database fixes"""
    print("Socrates AI Database Fixes and Improvements")
    print("=" * 50)
    
    db_manager = DatabaseManager()
    
    # Initialize improved database schema
    print("1. Initializing improved database schema...")
    db_manager.initialize_database()
    
    # Migrate existing data
    print("2. Migrating existing data...")
    db_manager.migrate_existing_data()
    
    # Optimize database
    print("3. Optimizing database performance...")
    db_manager.optimize_database()
    
    # Clean up old data
    print("4. Cleaning up old data...")
    db_manager.cleanup_old_data()
    
    # Create backup
    print("5. Creating database backup...")
    backup_path = db_manager.backup_database()
    
    # Get statistics
    print("6. Database statistics:")
    stats = db_manager.get_database_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("\nDatabase fixes and improvements completed successfully!")
    print(f"Backup created: {backup_path}")

if __name__ == "__main__":
    main()

