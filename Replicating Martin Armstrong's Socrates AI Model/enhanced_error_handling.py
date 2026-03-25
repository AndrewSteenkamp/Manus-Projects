#!/usr/bin/env python3
"""
Enhanced Error Handling and Rate Limiting for Socrates AI
Addresses API rate limiting and improves system reliability
"""

import time
import random
import logging
import functools
from typing import Callable, Any, Dict, Optional
from datetime import datetime, timedelta
import threading
from collections import defaultdict, deque
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RateLimiter:
    """Advanced rate limiter with multiple strategies"""
    
    def __init__(self, calls_per_minute: int = 60, burst_limit: int = 10):
        self.calls_per_minute = calls_per_minute
        self.burst_limit = burst_limit
        self.calls = deque()
        self.lock = threading.Lock()
        
    def wait_if_needed(self):
        """Wait if rate limit would be exceeded"""
        with self.lock:
            now = time.time()
            
            # Remove calls older than 1 minute
            while self.calls and self.calls[0] < now - 60:
                self.calls.popleft()
            
            # Check if we're at the limit
            if len(self.calls) >= self.calls_per_minute:
                sleep_time = 60 - (now - self.calls[0])
                if sleep_time > 0:
                    logger.info(f"Rate limit reached, sleeping for {sleep_time:.2f} seconds")
                    time.sleep(sleep_time)
            
            # Check burst limit
            recent_calls = sum(1 for call_time in self.calls if call_time > now - 10)
            if recent_calls >= self.burst_limit:
                sleep_time = 10 - (now - max(call for call in self.calls if call > now - 10))
                if sleep_time > 0:
                    logger.info(f"Burst limit reached, sleeping for {sleep_time:.2f} seconds")
                    time.sleep(sleep_time)
            
            # Record this call
            self.calls.append(now)

class ExponentialBackoff:
    """Exponential backoff with jitter"""
    
    def __init__(self, base_delay: float = 1.0, max_delay: float = 60.0, max_retries: int = 5):
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.max_retries = max_retries
    
    def calculate_delay(self, attempt: int) -> float:
        """Calculate delay for given attempt"""
        if attempt <= 0:
            return 0
        
        # Exponential backoff with jitter
        delay = min(self.base_delay * (2 ** (attempt - 1)), self.max_delay)
        jitter = random.uniform(0, delay * 0.1)  # 10% jitter
        return delay + jitter

class EnhancedHTTPSession:
    """HTTP session with advanced retry and error handling"""
    
    def __init__(self, rate_limiter: Optional[RateLimiter] = None):
        self.session = requests.Session()
        self.rate_limiter = rate_limiter or RateLimiter()
        self.backoff = ExponentialBackoff()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"],
            backoff_factor=1
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Set reasonable timeouts
        self.session.timeout = (10, 30)  # (connect, read)
    
    def get(self, url: str, **kwargs) -> requests.Response:
        """GET request with rate limiting and error handling"""
        return self._request('GET', url, **kwargs)
    
    def post(self, url: str, **kwargs) -> requests.Response:
        """POST request with rate limiting and error handling"""
        return self._request('POST', url, **kwargs)
    
    def _request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Make HTTP request with comprehensive error handling"""
        for attempt in range(self.backoff.max_retries + 1):
            try:
                # Apply rate limiting
                self.rate_limiter.wait_if_needed()
                
                # Make the request
                response = self.session.request(method, url, **kwargs)
                
                # Handle specific status codes
                if response.status_code == 429:  # Too Many Requests
                    retry_after = response.headers.get('Retry-After')
                    if retry_after:
                        sleep_time = int(retry_after)
                        logger.warning(f"Rate limited, waiting {sleep_time} seconds")
                        time.sleep(sleep_time)
                        continue
                
                # Check if response is successful
                response.raise_for_status()
                return response
                
            except requests.exceptions.RequestException as e:
                if attempt == self.backoff.max_retries:
                    logger.error(f"Request failed after {attempt + 1} attempts: {e}")
                    raise
                
                delay = self.backoff.calculate_delay(attempt + 1)
                logger.warning(f"Request failed (attempt {attempt + 1}), retrying in {delay:.2f}s: {e}")
                time.sleep(delay)
        
        raise requests.exceptions.RequestException(f"Request failed after {self.backoff.max_retries + 1} attempts")

class CircuitBreaker:
    """Circuit breaker pattern for external service calls"""
    
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
        self.lock = threading.Lock()
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker protection"""
        with self.lock:
            if self.state == 'OPEN':
                if time.time() - self.last_failure_time > self.recovery_timeout:
                    self.state = 'HALF_OPEN'
                    logger.info("Circuit breaker transitioning to HALF_OPEN")
                else:
                    raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            
            with self.lock:
                if self.state == 'HALF_OPEN':
                    self.state = 'CLOSED'
                    self.failure_count = 0
                    logger.info("Circuit breaker reset to CLOSED")
            
            return result
            
        except Exception as e:
            with self.lock:
                self.failure_count += 1
                self.last_failure_time = time.time()
                
                if self.failure_count >= self.failure_threshold:
                    self.state = 'OPEN'
                    logger.warning(f"Circuit breaker opened after {self.failure_count} failures")
            
            raise

class ErrorHandler:
    """Centralized error handling with logging and recovery"""
    
    def __init__(self):
        self.error_counts = defaultdict(int)
        self.last_errors = {}
    
    def handle_error(self, error: Exception, context: str = "unknown", 
                    recoverable: bool = True) -> Dict[str, Any]:
        """Handle error with logging and return error info"""
        error_type = type(error).__name__
        error_message = str(error)
        
        # Update error statistics
        self.error_counts[error_type] += 1
        self.last_errors[context] = {
            'error_type': error_type,
            'message': error_message,
            'timestamp': datetime.now().isoformat(),
            'recoverable': recoverable
        }
        
        # Log error with appropriate level
        if recoverable:
            logger.warning(f"Recoverable error in {context}: {error_type} - {error_message}")
        else:
            logger.error(f"Critical error in {context}: {error_type} - {error_message}")
        
        return {
            'success': False,
            'error': error_type,
            'message': error_message,
            'context': context,
            'recoverable': recoverable,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_error_stats(self) -> Dict[str, Any]:
        """Get error statistics"""
        return {
            'error_counts': dict(self.error_counts),
            'last_errors': dict(self.last_errors),
            'total_errors': sum(self.error_counts.values())
        }

def retry_with_exponential_backoff(max_retries: int = 3, base_delay: float = 1.0, 
                                 max_delay: float = 60.0, exceptions: tuple = (Exception,)):
    """Decorator for exponential backoff retry"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            backoff = ExponentialBackoff(base_delay, max_delay, max_retries)
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_retries:
                        raise
                    
                    delay = backoff.calculate_delay(attempt + 1)
                    logger.warning(f"{func.__name__} failed (attempt {attempt + 1}), "
                                 f"retrying in {delay:.2f}s: {e}")
                    time.sleep(delay)
            
            return None
        return wrapper
    return decorator

def rate_limited(calls_per_minute: int = 60):
    """Decorator for rate limiting function calls"""
    rate_limiter = RateLimiter(calls_per_minute)
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            rate_limiter.wait_if_needed()
            return func(*args, **kwargs)
        return wrapper
    return decorator

def circuit_breaker(failure_threshold: int = 5, recovery_timeout: int = 60):
    """Decorator for circuit breaker pattern"""
    breaker = CircuitBreaker(failure_threshold, recovery_timeout)
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return breaker.call(func, *args, **kwargs)
        return wrapper
    return decorator

class MemoryManager:
    """Memory usage monitoring and optimization"""
    
    def __init__(self, max_memory_mb: int = 1024):
        self.max_memory_mb = max_memory_mb
        self.cache = {}
        self.cache_access_times = {}
    
    def get_memory_usage(self) -> float:
        """Get current memory usage in MB"""
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024
        except ImportError:
            # Fallback if psutil not available
            import sys
            return sys.getsizeof(self.cache) / 1024 / 1024
    
    def cleanup_if_needed(self):
        """Clean up memory if usage is too high"""
        current_usage = self.get_memory_usage()
        
        if current_usage > self.max_memory_mb:
            logger.warning(f"Memory usage ({current_usage:.1f} MB) exceeds limit ({self.max_memory_mb} MB)")
            
            # Clear old cache entries
            now = time.time()
            old_keys = [key for key, access_time in self.cache_access_times.items() 
                       if now - access_time > 3600]  # 1 hour
            
            for key in old_keys:
                self.cache.pop(key, None)
                self.cache_access_times.pop(key, None)
            
            logger.info(f"Cleared {len(old_keys)} old cache entries")
    
    def cache_result(self, key: str, value: Any, ttl: int = 3600):
        """Cache result with TTL"""
        self.cleanup_if_needed()
        self.cache[key] = value
        self.cache_access_times[key] = time.time()
    
    def get_cached_result(self, key: str) -> Optional[Any]:
        """Get cached result if available and not expired"""
        if key in self.cache:
            access_time = self.cache_access_times.get(key, 0)
            if time.time() - access_time < 3600:  # 1 hour TTL
                self.cache_access_times[key] = time.time()  # Update access time
                return self.cache[key]
            else:
                # Expired, remove from cache
                self.cache.pop(key, None)
                self.cache_access_times.pop(key, None)
        
        return None

# Global instances
global_rate_limiter = RateLimiter()
global_http_session = EnhancedHTTPSession(global_rate_limiter)
global_error_handler = ErrorHandler()
global_memory_manager = MemoryManager()

def create_robust_api_client(base_url: str, api_key: str = None) -> 'RobustAPIClient':
    """Create a robust API client with all error handling features"""
    return RobustAPIClient(base_url, api_key)

class RobustAPIClient:
    """Robust API client with comprehensive error handling"""
    
    def __init__(self, base_url: str, api_key: str = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = EnhancedHTTPSession()
        self.error_handler = ErrorHandler()
        self.memory_manager = MemoryManager()
        
        # Set default headers
        if api_key:
            self.session.session.headers.update({'Authorization': f'Bearer {api_key}'})
        
        self.session.session.headers.update({
            'User-Agent': 'Socrates-AI/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
    
    @retry_with_exponential_backoff(max_retries=3)
    @rate_limited(calls_per_minute=60)
    def get(self, endpoint: str, params: Dict = None) -> Dict[str, Any]:
        """GET request with comprehensive error handling"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            # Check cache first
            cache_key = f"GET:{url}:{str(params)}"
            cached_result = self.memory_manager.get_cached_result(cache_key)
            if cached_result:
                return cached_result
            
            response = self.session.get(url, params=params)
            result = response.json()
            
            # Cache successful results
            self.memory_manager.cache_result(cache_key, result)
            
            return result
            
        except Exception as e:
            return self.error_handler.handle_error(e, f"GET {endpoint}")
    
    @retry_with_exponential_backoff(max_retries=3)
    @rate_limited(calls_per_minute=30)  # Lower rate limit for POST
    def post(self, endpoint: str, data: Dict = None) -> Dict[str, Any]:
        """POST request with comprehensive error handling"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.post(url, json=data)
            return response.json()
            
        except Exception as e:
            return self.error_handler.handle_error(e, f"POST {endpoint}")
    
    def get_client_stats(self) -> Dict[str, Any]:
        """Get client statistics"""
        return {
            'error_stats': self.error_handler.get_error_stats(),
            'memory_usage_mb': self.memory_manager.get_memory_usage(),
            'cache_size': len(self.memory_manager.cache)
        }

def main():
    """Test the enhanced error handling system"""
    print("Enhanced Error Handling and Rate Limiting Test")
    print("=" * 50)
    
    # Test rate limiter
    print("Testing rate limiter...")
    rate_limiter = RateLimiter(calls_per_minute=5)  # Very low for testing
    
    start_time = time.time()
    for i in range(3):
        rate_limiter.wait_if_needed()
        print(f"Call {i + 1} at {time.time() - start_time:.2f}s")
    
    # Test exponential backoff
    print("\nTesting exponential backoff...")
    backoff = ExponentialBackoff()
    
    for attempt in range(5):
        delay = backoff.calculate_delay(attempt)
        print(f"Attempt {attempt}: delay = {delay:.2f}s")
    
    # Test circuit breaker
    print("\nTesting circuit breaker...")
    
    @circuit_breaker(failure_threshold=2, recovery_timeout=5)
    def failing_function():
        raise Exception("Simulated failure")
    
    for i in range(5):
        try:
            failing_function()
        except Exception as e:
            print(f"Call {i + 1}: {e}")
    
    print("\nEnhanced error handling system test completed!")

if __name__ == "__main__":
    main()

