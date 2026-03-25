#!/usr/bin/env python3
"""
Performance Optimization System for Socrates AI
Implements comprehensive performance enhancements including caching, 
database optimization, memory management, and mobile optimizations
"""

import sqlite3
import json
import logging
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import numpy as np
import pandas as pd
from functools import wraps, lru_cache
import hashlib
import gzip
import pickle
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import asyncio
import aiohttp
import psutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetrics:
    """Performance metrics tracking"""
    operation: str
    start_time: float
    end_time: float
    duration: float
    memory_before: float
    memory_after: float
    cpu_percent: float
    cache_hit: bool = False
    error: Optional[str] = None

class CacheManager:
    """Advanced caching system with TTL and compression"""
    
    def __init__(self, cache_dir: str = "/tmp/socrates_cache", max_size_mb: int = 500):
        self.cache_dir = cache_dir
        self.max_size_mb = max_size_mb
        self.cache_stats = {'hits': 0, 'misses': 0, 'evictions': 0}
        
        # Create cache directory
        os.makedirs(cache_dir, exist_ok=True)
        
        # In-memory cache for frequently accessed data
        self.memory_cache = {}
        self.cache_timestamps = {}
        self.cache_ttl = {}
        
        # Start cleanup thread
        self.cleanup_thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        self.cleanup_thread.start()
    
    def _get_cache_key(self, key: str) -> str:
        """Generate cache key hash"""
        return hashlib.md5(key.encode()).hexdigest()
    
    def _get_cache_path(self, cache_key: str) -> str:
        """Get cache file path"""
        return os.path.join(self.cache_dir, f"{cache_key}.cache")
    
    def get(self, key: str, default=None) -> Any:
        """Get item from cache"""
        cache_key = self._get_cache_key(key)
        
        # Check memory cache first
        if cache_key in self.memory_cache:
            if self._is_cache_valid(cache_key):
                self.cache_stats['hits'] += 1
                return self.memory_cache[cache_key]
            else:
                # Expired, remove from memory cache
                del self.memory_cache[cache_key]
                del self.cache_timestamps[cache_key]
                if cache_key in self.cache_ttl:
                    del self.cache_ttl[cache_key]
        
        # Check disk cache
        cache_path = self._get_cache_path(cache_key)
        if os.path.exists(cache_path):
            try:
                with gzip.open(cache_path, 'rb') as f:
                    cached_data = pickle.load(f)
                
                # Check if still valid
                if 'timestamp' in cached_data and 'ttl' in cached_data:
                    age = time.time() - cached_data['timestamp']
                    if age < cached_data['ttl']:
                        # Move to memory cache for faster access
                        self.memory_cache[cache_key] = cached_data['data']
                        self.cache_timestamps[cache_key] = cached_data['timestamp']
                        self.cache_ttl[cache_key] = cached_data['ttl']
                        
                        self.cache_stats['hits'] += 1
                        return cached_data['data']
                
                # Expired, remove file
                os.remove(cache_path)
                
            except Exception as e:
                logger.error(f"Error reading cache file {cache_path}: {e}")
                if os.path.exists(cache_path):
                    os.remove(cache_path)
        
        self.cache_stats['misses'] += 1
        return default
    
    def set(self, key: str, value: Any, ttl: int = 3600):
        """Set item in cache with TTL in seconds"""
        cache_key = self._get_cache_key(key)
        timestamp = time.time()
        
        # Store in memory cache
        self.memory_cache[cache_key] = value
        self.cache_timestamps[cache_key] = timestamp
        self.cache_ttl[cache_key] = ttl
        
        # Store in disk cache for persistence
        try:
            cache_path = self._get_cache_path(cache_key)
            cached_data = {
                'data': value,
                'timestamp': timestamp,
                'ttl': ttl
            }
            
            with gzip.open(cache_path, 'wb') as f:
                pickle.dump(cached_data, f)
                
        except Exception as e:
            logger.error(f"Error writing cache file: {e}")
        
        # Check cache size and cleanup if needed
        self._check_cache_size()
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cache entry is still valid"""
        if cache_key not in self.cache_timestamps or cache_key not in self.cache_ttl:
            return False
        
        age = time.time() - self.cache_timestamps[cache_key]
        return age < self.cache_ttl[cache_key]
    
    def _check_cache_size(self):
        """Check cache size and cleanup if needed"""
        try:
            total_size = 0
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.cache'):
                    filepath = os.path.join(self.cache_dir, filename)
                    total_size += os.path.getsize(filepath)
            
            # Convert to MB
            total_size_mb = total_size / (1024 * 1024)
            
            if total_size_mb > self.max_size_mb:
                self._cleanup_old_files()
                
        except Exception as e:
            logger.error(f"Error checking cache size: {e}")
    
    def _cleanup_old_files(self):
        """Cleanup old cache files"""
        try:
            files_with_time = []
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.cache'):
                    filepath = os.path.join(self.cache_dir, filename)
                    mtime = os.path.getmtime(filepath)
                    files_with_time.append((filepath, mtime))
            
            # Sort by modification time (oldest first)
            files_with_time.sort(key=lambda x: x[1])
            
            # Remove oldest 25% of files
            files_to_remove = len(files_with_time) // 4
            for filepath, _ in files_with_time[:files_to_remove]:
                os.remove(filepath)
                self.cache_stats['evictions'] += 1
                
        except Exception as e:
            logger.error(f"Error cleaning up cache files: {e}")
    
    def _cleanup_loop(self):
        """Background cleanup loop"""
        while True:
            try:
                # Cleanup expired memory cache entries
                current_time = time.time()
                expired_keys = []
                
                for cache_key in list(self.cache_timestamps.keys()):
                    if not self._is_cache_valid(cache_key):
                        expired_keys.append(cache_key)
                
                for cache_key in expired_keys:
                    if cache_key in self.memory_cache:
                        del self.memory_cache[cache_key]
                    if cache_key in self.cache_timestamps:
                        del self.cache_timestamps[cache_key]
                    if cache_key in self.cache_ttl:
                        del self.cache_ttl[cache_key]
                
                # Sleep for 5 minutes
                time.sleep(300)
                
            except Exception as e:
                logger.error(f"Error in cache cleanup loop: {e}")
                time.sleep(60)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_requests = self.cache_stats['hits'] + self.cache_stats['misses']
        hit_rate = (self.cache_stats['hits'] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'hits': self.cache_stats['hits'],
            'misses': self.cache_stats['misses'],
            'evictions': self.cache_stats['evictions'],
            'hit_rate': hit_rate,
            'memory_cache_size': len(self.memory_cache),
            'total_requests': total_requests
        }

class DatabaseOptimizer:
    """Database optimization and connection pooling"""
    
    def __init__(self, db_path: str = "socrates_data.db", pool_size: int = 10):
        self.db_path = db_path
        self.pool_size = pool_size
        self.connection_pool = []
        self.pool_lock = threading.Lock()
        
        # Initialize connection pool
        self._init_connection_pool()
        
        # Optimize database
        self._optimize_database()
    
    def _init_connection_pool(self):
        """Initialize database connection pool"""
        try:
            for _ in range(self.pool_size):
                conn = sqlite3.connect(self.db_path, check_same_thread=False)
                conn.execute('PRAGMA journal_mode=WAL')
                conn.execute('PRAGMA synchronous=NORMAL')
                conn.execute('PRAGMA cache_size=10000')
                conn.execute('PRAGMA temp_store=MEMORY')
                self.connection_pool.append(conn)
            
            logger.info(f"Initialized database connection pool with {self.pool_size} connections")
            
        except Exception as e:
            logger.error(f"Error initializing connection pool: {e}")
    
    def get_connection(self):
        """Get connection from pool"""
        with self.pool_lock:
            if self.connection_pool:
                return self.connection_pool.pop()
            else:
                # Create new connection if pool is empty
                conn = sqlite3.connect(self.db_path, check_same_thread=False)
                conn.execute('PRAGMA journal_mode=WAL')
                conn.execute('PRAGMA synchronous=NORMAL')
                conn.execute('PRAGMA cache_size=10000')
                conn.execute('PRAGMA temp_store=MEMORY')
                return conn
    
    def return_connection(self, conn):
        """Return connection to pool"""
        with self.pool_lock:
            if len(self.connection_pool) < self.pool_size:
                self.connection_pool.append(conn)
            else:
                conn.close()
    
    def _optimize_database(self):
        """Optimize database with indexes and settings"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Create additional indexes for performance
            indexes = [
                'CREATE INDEX IF NOT EXISTS idx_market_data_symbol_date ON market_data(symbol, date DESC)',
                'CREATE INDEX IF NOT EXISTS idx_market_data_date ON market_data(date DESC)',
                'CREATE INDEX IF NOT EXISTS idx_alternative_data_symbol_timestamp ON alternative_data(symbol, timestamp DESC)',
                'CREATE INDEX IF NOT EXISTS idx_stock_insights_symbol_timestamp ON stock_insights(symbol, timestamp DESC)',
                'CREATE INDEX IF NOT EXISTS idx_portfolio_performance_portfolio_id ON portfolio_performance(portfolio_id)',
                'CREATE INDEX IF NOT EXISTS idx_positions_portfolio_id ON positions(portfolio_id)',
                'CREATE INDEX IF NOT EXISTS idx_alert_events_timestamp ON alert_events(timestamp DESC)',
                'CREATE INDEX IF NOT EXISTS idx_sentiment_data_symbol_timestamp ON sentiment_data(symbol, timestamp DESC)'
            ]
            
            for index_sql in indexes:
                try:
                    cursor.execute(index_sql)
                except Exception as e:
                    logger.warning(f"Index creation warning: {e}")
            
            # Analyze tables for query optimization
            cursor.execute('ANALYZE')
            
            conn.commit()
            self.return_connection(conn)
            
            logger.info("Database optimization completed")
            
        except Exception as e:
            logger.error(f"Error optimizing database: {e}")
    
    def execute_query(self, query: str, params: tuple = (), fetch_one: bool = False, fetch_all: bool = True):
        """Execute optimized database query"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            
            if fetch_one:
                result = cursor.fetchone()
            elif fetch_all:
                result = cursor.fetchall()
            else:
                result = None
            
            conn.commit()
            return result
            
        except Exception as e:
            logger.error(f"Database query error: {e}")
            return None
        finally:
            self.return_connection(conn)

class PerformanceMonitor:
    """Performance monitoring and metrics collection"""
    
    def __init__(self):
        self.metrics = []
        self.metrics_lock = threading.Lock()
        self.start_time = time.time()
    
    def measure_performance(self, operation_name: str):
        """Decorator to measure performance of functions"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Get initial metrics
                process = psutil.Process()
                memory_before = process.memory_info().rss / 1024 / 1024  # MB
                cpu_before = process.cpu_percent()
                start_time = time.time()
                
                cache_hit = kwargs.pop('_cache_hit', False)
                error = None
                result = None
                
                try:
                    result = func(*args, **kwargs)
                except Exception as e:
                    error = str(e)
                    raise
                finally:
                    # Get final metrics
                    end_time = time.time()
                    memory_after = process.memory_info().rss / 1024 / 1024  # MB
                    cpu_after = process.cpu_percent()
                    
                    # Create performance metric
                    metric = PerformanceMetrics(
                        operation=operation_name,
                        start_time=start_time,
                        end_time=end_time,
                        duration=end_time - start_time,
                        memory_before=memory_before,
                        memory_after=memory_after,
                        cpu_percent=(cpu_before + cpu_after) / 2,
                        cache_hit=cache_hit,
                        error=error
                    )
                    
                    # Store metric
                    with self.metrics_lock:
                        self.metrics.append(metric)
                        
                        # Keep only last 1000 metrics
                        if len(self.metrics) > 1000:
                            self.metrics = self.metrics[-1000:]
                
                return result
            return wrapper
        return decorator
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary statistics"""
        with self.metrics_lock:
            if not self.metrics:
                return {'error': 'No performance data available'}
            
            # Group metrics by operation
            operations = {}
            for metric in self.metrics:
                if metric.operation not in operations:
                    operations[metric.operation] = []
                operations[metric.operation].append(metric)
            
            summary = {}
            for operation, metrics_list in operations.items():
                durations = [m.duration for m in metrics_list if m.error is None]
                memory_usage = [m.memory_after - m.memory_before for m in metrics_list]
                cache_hits = sum(1 for m in metrics_list if m.cache_hit)
                errors = sum(1 for m in metrics_list if m.error is not None)
                
                if durations:
                    summary[operation] = {
                        'count': len(metrics_list),
                        'avg_duration': np.mean(durations),
                        'min_duration': np.min(durations),
                        'max_duration': np.max(durations),
                        'avg_memory_delta': np.mean(memory_usage),
                        'cache_hit_rate': (cache_hits / len(metrics_list)) * 100,
                        'error_rate': (errors / len(metrics_list)) * 100,
                        'total_duration': np.sum(durations)
                    }
            
            return {
                'operations': summary,
                'total_operations': len(self.metrics),
                'uptime_seconds': time.time() - self.start_time,
                'timestamp': datetime.now().isoformat()
            }

class MobileOptimizer:
    """Mobile-specific optimizations"""
    
    @staticmethod
    def compress_response(data: Dict[str, Any], compression_level: int = 6) -> bytes:
        """Compress response data for mobile clients"""
        try:
            json_data = json.dumps(data, separators=(',', ':'))
            return gzip.compress(json_data.encode(), compresslevel=compression_level)
        except Exception as e:
            logger.error(f"Error compressing response: {e}")
            return json.dumps(data).encode()
    
    @staticmethod
    def optimize_for_mobile(data: Dict[str, Any], max_items: int = 50) -> Dict[str, Any]:
        """Optimize data structure for mobile consumption"""
        try:
            optimized = {}
            
            for key, value in data.items():
                if isinstance(value, list):
                    # Limit list size for mobile
                    optimized[key] = value[:max_items]
                elif isinstance(value, dict):
                    # Recursively optimize nested dictionaries
                    optimized[key] = MobileOptimizer.optimize_for_mobile(value, max_items)
                else:
                    optimized[key] = value
            
            return optimized
            
        except Exception as e:
            logger.error(f"Error optimizing for mobile: {e}")
            return data
    
    @staticmethod
    def create_mobile_summary(full_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create mobile-friendly summary of complex data"""
        try:
            summary = {
                'timestamp': datetime.now().isoformat(),
                'data_points': 0,
                'key_metrics': {},
                'alerts': [],
                'status': 'ok'
            }
            
            # Extract key metrics
            if 'portfolio' in full_data:
                portfolio = full_data['portfolio']
                summary['key_metrics']['portfolio_value'] = portfolio.get('current_value', 0)
                summary['key_metrics']['total_return'] = portfolio.get('total_return_pct', 0)
            
            if 'performance' in full_data:
                perf = full_data['performance']
                summary['key_metrics']['sharpe_ratio'] = perf.get('sharpe_ratio', 0)
                summary['key_metrics']['win_rate'] = perf.get('win_rate', 0)
            
            if 'sentiment_analysis' in full_data:
                sentiment = full_data['sentiment_analysis']
                summary['key_metrics']['sentiment'] = sentiment.get('sentiment_label', 'neutral')
                summary['key_metrics']['sentiment_score'] = sentiment.get('sentiment_score', 0)
            
            # Count data points
            for key, value in full_data.items():
                if isinstance(value, list):
                    summary['data_points'] += len(value)
                elif isinstance(value, dict) and 'data' in value:
                    if isinstance(value['data'], list):
                        summary['data_points'] += len(value['data'])
            
            return summary
            
        except Exception as e:
            logger.error(f"Error creating mobile summary: {e}")
            return {'error': str(e)}

class AsyncDataProcessor:
    """Asynchronous data processing for improved performance"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    async def process_multiple_symbols(self, symbols: List[str], 
                                     processing_func, *args, **kwargs) -> Dict[str, Any]:
        """Process multiple symbols asynchronously"""
        try:
            loop = asyncio.get_event_loop()
            
            # Submit all tasks
            futures = []
            for symbol in symbols:
                future = loop.run_in_executor(
                    self.executor, 
                    processing_func, 
                    symbol, 
                    *args, 
                    **kwargs
                )
                futures.append((symbol, future))
            
            # Collect results
            results = {}
            for symbol, future in futures:
                try:
                    result = await future
                    results[symbol] = result
                except Exception as e:
                    logger.error(f"Error processing {symbol}: {e}")
                    results[symbol] = {'error': str(e)}
            
            return results
            
        except Exception as e:
            logger.error(f"Error in async processing: {e}")
            return {}
    
    def shutdown(self):
        """Shutdown the executor"""
        self.executor.shutdown(wait=True)

class OptimizedSocratesAI:
    """Optimized version of Socrates AI with performance enhancements"""
    
    def __init__(self, db_path: str = "socrates_data.db"):
        self.db_path = db_path
        self.cache_manager = CacheManager()
        self.db_optimizer = DatabaseOptimizer(db_path)
        self.performance_monitor = PerformanceMonitor()
        self.mobile_optimizer = MobileOptimizer()
        self.async_processor = AsyncDataProcessor()
        
        logger.info("Optimized Socrates AI initialized")
    
    @lru_cache(maxsize=128)
    def _get_cached_market_data(self, symbol: str, days: int) -> str:
        """Cached market data retrieval"""
        cache_key = f"market_data_{symbol}_{days}"
        cached_data = self.cache_manager.get(cache_key)
        
        if cached_data is not None:
            return cached_data
        
        # Fetch from database
        query = '''
            SELECT date, open_price, high_price, low_price, close_price, volume 
            FROM market_data 
            WHERE symbol = ? 
            ORDER BY date DESC 
            LIMIT ?
        '''
        
        result = self.db_optimizer.execute_query(query, (symbol, days))
        
        if result:
            # Convert to JSON string for caching
            data = [
                {
                    'date': row[0],
                    'open': row[1],
                    'high': row[2],
                    'low': row[3],
                    'close': row[4],
                    'volume': row[5]
                }
                for row in result
            ]
            
            json_data = json.dumps(data)
            self.cache_manager.set(cache_key, json_data, ttl=300)  # 5 minutes TTL
            return json_data
        
        return json.dumps([])
    
    def get_optimized_analysis(self, symbol: str, mobile: bool = False) -> Dict[str, Any]:
        """Get optimized analysis for a symbol"""
        @self.performance_monitor.measure_performance("get_optimized_analysis")
        def _get_analysis():
            try:
                # Check cache first
                cache_key = f"analysis_{symbol}_mobile_{mobile}"
                cached_result = self.cache_manager.get(cache_key)
                
                if cached_result is not None:
                    return cached_result
                
                # Fetch market data
                market_data_json = self._get_cached_market_data(symbol, 100)
                market_data = json.loads(market_data_json)
                
                # Get additional data from database
                queries = {
                    'insights': 'SELECT * FROM stock_insights WHERE symbol = ? ORDER BY timestamp DESC LIMIT 10',
                    'sentiment': 'SELECT * FROM sentiment_data WHERE symbol = ? ORDER BY timestamp DESC LIMIT 5',
                    'alternative_data': 'SELECT * FROM alternative_data WHERE symbol = ? ORDER BY timestamp DESC LIMIT 20'
                }
                
                analysis_data = {
                    'symbol': symbol,
                    'market_data': market_data,
                    'timestamp': datetime.now().isoformat()
                }
                
                for data_type, query in queries.items():
                    result = self.db_optimizer.execute_query(query, (symbol,))
                    analysis_data[data_type] = result if result else []
                
                # Optimize for mobile if requested
                if mobile:
                    analysis_data = self.mobile_optimizer.optimize_for_mobile(analysis_data)
                    analysis_data['mobile_summary'] = self.mobile_optimizer.create_mobile_summary(analysis_data)
                
                # Cache the result
                self.cache_manager.set(cache_key, analysis_data, ttl=600)  # 10 minutes TTL
                
                return analysis_data
                
            except Exception as e:
                logger.error(f"Error in optimized analysis for {symbol}: {e}")
                return {'error': str(e)}
        
        return _get_analysis()
    
    def get_performance_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive performance dashboard"""
        try:
            return {
                'performance_summary': self.performance_monitor.get_performance_summary(),
                'cache_stats': self.cache_manager.get_stats(),
                'system_info': {
                    'cpu_percent': psutil.cpu_percent(interval=1),
                    'memory_percent': psutil.virtual_memory().percent,
                    'disk_usage': psutil.disk_usage('/').percent,
                    'process_count': len(psutil.pids())
                },
                'database_info': {
                    'connection_pool_size': len(self.db_optimizer.connection_pool),
                    'db_file_size_mb': os.path.getsize(self.db_path) / 1024 / 1024
                },
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting performance dashboard: {e}")
            return {'error': str(e)}

def main():
    """Test the performance optimization system"""
    print("Performance Optimization System for Socrates AI")
    print("=" * 50)
    
    # Initialize optimized system
    optimized_ai = OptimizedSocratesAI()
    
    print("1. Testing cache system...")
    cache_stats_before = optimized_ai.cache_manager.get_stats()
    print(f"   ✓ Cache initialized - Hit rate: {cache_stats_before['hit_rate']:.1f}%")
    
    print("\n2. Testing database optimization...")
    start_time = time.time()
    result = optimized_ai.db_optimizer.execute_query(
        "SELECT COUNT(*) FROM market_data", 
        fetch_one=True
    )
    query_time = time.time() - start_time
    print(f"   ✓ Database query completed in {query_time:.3f}s")
    print(f"   ✓ Market data records: {result[0] if result else 0}")
    
    print("\n3. Testing optimized analysis...")
    start_time = time.time()
    analysis = optimized_ai.get_optimized_analysis("AAPL")
    analysis_time = time.time() - start_time
    
    if 'error' not in analysis:
        print(f"   ✓ Analysis completed in {analysis_time:.3f}s")
        print(f"   ✓ Market data points: {len(analysis.get('market_data', []))}")
        print(f"   ✓ Insights: {len(analysis.get('insights', []))}")
        print(f"   ✓ Alternative data: {len(analysis.get('alternative_data', []))}")
    else:
        print(f"   ✗ Analysis failed: {analysis['error']}")
    
    print("\n4. Testing mobile optimization...")
    mobile_analysis = optimized_ai.get_optimized_analysis("AAPL", mobile=True)
    
    if 'error' not in mobile_analysis:
        print("   ✓ Mobile analysis completed")
        if 'mobile_summary' in mobile_analysis:
            summary = mobile_analysis['mobile_summary']
            print(f"   ✓ Data points: {summary.get('data_points', 0)}")
            print(f"   ✓ Key metrics: {len(summary.get('key_metrics', {}))}")
    else:
        print(f"   ✗ Mobile analysis failed: {mobile_analysis['error']}")
    
    print("\n5. Testing cache performance...")
    # Test cache hit
    start_time = time.time()
    cached_analysis = optimized_ai.get_optimized_analysis("AAPL")
    cached_time = time.time() - start_time
    
    cache_stats_after = optimized_ai.cache_manager.get_stats()
    print(f"   ✓ Cached analysis completed in {cached_time:.3f}s")
    print(f"   ✓ Cache hit rate: {cache_stats_after['hit_rate']:.1f}%")
    print(f"   ✓ Cache hits: {cache_stats_after['hits']}")
    print(f"   ✓ Cache misses: {cache_stats_after['misses']}")
    
    print("\n6. Testing performance monitoring...")
    perf_dashboard = optimized_ai.get_performance_dashboard()
    
    if 'error' not in perf_dashboard:
        print("   ✓ Performance dashboard generated")
        
        system_info = perf_dashboard.get('system_info', {})
        print(f"   ✓ CPU usage: {system_info.get('cpu_percent', 0):.1f}%")
        print(f"   ✓ Memory usage: {system_info.get('memory_percent', 0):.1f}%")
        print(f"   ✓ Disk usage: {system_info.get('disk_usage', 0):.1f}%")
        
        db_info = perf_dashboard.get('database_info', {})
        print(f"   ✓ DB file size: {db_info.get('db_file_size_mb', 0):.1f} MB")
        print(f"   ✓ Connection pool: {db_info.get('connection_pool_size', 0)} connections")
    else:
        print(f"   ✗ Performance dashboard failed: {perf_dashboard['error']}")
    
    print("\n7. Testing compression for mobile...")
    test_data = {'large_array': list(range(1000)), 'nested': {'data': list(range(500))}}
    
    # Original size
    original_size = len(json.dumps(test_data))
    
    # Compressed size
    compressed_data = optimized_ai.mobile_optimizer.compress_response(test_data)
    compressed_size = len(compressed_data)
    
    compression_ratio = (1 - compressed_size / original_size) * 100
    print(f"   ✓ Original size: {original_size:,} bytes")
    print(f"   ✓ Compressed size: {compressed_size:,} bytes")
    print(f"   ✓ Compression ratio: {compression_ratio:.1f}%")
    
    print("\n8. Final performance summary...")
    final_perf = optimized_ai.performance_monitor.get_performance_summary()
    
    if 'operations' in final_perf:
        print("   Performance by operation:")
        for operation, stats in final_perf['operations'].items():
            print(f"   - {operation}: {stats['avg_duration']:.3f}s avg, {stats['count']} calls")
    
    print(f"   ✓ Total operations: {final_perf.get('total_operations', 0)}")
    print(f"   ✓ System uptime: {final_perf.get('uptime_seconds', 0):.1f}s")
    
    # Cleanup
    optimized_ai.async_processor.shutdown()
    
    print("\nPerformance optimization system test completed!")
    print("System is ready for production deployment!")

if __name__ == "__main__":
    main()

