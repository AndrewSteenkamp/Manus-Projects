#!/usr/bin/env python3
"""
Socrates AI - Market Analysis System
Replication of Martin Armstrong's Socrates AI based on comprehensive research

This system implements:
1. Economic Confidence Model (ECM) - 8.6-year cycle analysis
2. Multi-market correlation analysis
3. Capital flow tracking
4. Pattern recognition across global markets
5. Cyclical analysis and timing arrays
6. Unbiased technical analysis

Author: AI Replication Project
Based on: Martin Armstrong's Socrates AI research
"""

import numpy as np
import pandas as pd
import sqlite3
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod
import math

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class MarketData:
    """Data structure for market information"""
    symbol: str
    date: datetime
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: int
    adjusted_close: float
    currency: str = "USD"

@dataclass
class EconomicIndicator:
    """Data structure for economic indicators"""
    indicator_id: str
    name: str
    value: float
    date: datetime
    country: str
    source: str

@dataclass
class CycleAnalysis:
    """Data structure for cycle analysis results"""
    cycle_length: float
    confidence: float
    next_turning_point: datetime
    cycle_position: str  # "peak", "trough", "rising", "declining"
    historical_accuracy: float

@dataclass
class CapitalFlow:
    """Data structure for capital flow analysis"""
    from_region: str
    to_region: str
    amount: float
    date: datetime
    asset_class: str
    flow_type: str  # "inflow", "outflow"

class DataProcessor(ABC):
    """Abstract base class for data processing components"""
    
    @abstractmethod
    def process(self, data: Any) -> Any:
        pass
    
    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

class EconomicConfidenceModel:
    """
    Implementation of Armstrong's Economic Confidence Model (ECM)
    
    Core principles:
    - 8.6-year cycle (π × 1,000 days = 3,141 days)
    - Global capital flow tracking
    - Public vs Private confidence waves
    - Fractal nature across time scales
    """
    
    def __init__(self):
        self.base_cycle_days = 3141  # π × 1,000 days
        self.base_cycle_years = 8.6
        self.long_wave_cycles = 6  # 6 cycles = 51.6 years
        self.historical_turning_points = {
            "1929": "private_peak",
            "1981": "public_to_private_transition", 
            "1989": "japan_bubble",
            "2007.15": "real_estate_peak"
        }
        
    def calculate_cycle_position(self, current_date: datetime, reference_date: datetime) -> Dict[str, Any]:
        """
        Calculate current position in the ECM cycle
        
        Args:
            current_date: Current date for analysis
            reference_date: Reference turning point date
            
        Returns:
            Dictionary with cycle analysis
        """
        days_diff = (current_date - reference_date).days
        cycle_position = (days_diff % self.base_cycle_days) / self.base_cycle_days
        
        # Determine cycle phase
        if 0 <= cycle_position < 0.25:
            phase = "early_expansion"
        elif 0.25 <= cycle_position < 0.5:
            phase = "late_expansion"
        elif 0.5 <= cycle_position < 0.75:
            phase = "early_contraction"
        else:
            phase = "late_contraction"
            
        # Calculate next turning point
        days_to_next_turn = self.base_cycle_days - (days_diff % self.base_cycle_days)
        next_turning_point = current_date + timedelta(days=days_to_next_turn)
        
        return {
            "cycle_position": cycle_position,
            "phase": phase,
            "days_into_cycle": days_diff % self.base_cycle_days,
            "days_to_next_turn": days_to_next_turn,
            "next_turning_point": next_turning_point,
            "confidence_level": self._calculate_confidence(cycle_position)
        }
    
    def _calculate_confidence(self, cycle_position: float) -> float:
        """Calculate confidence level based on cycle position"""
        # Higher confidence near turning points (0, 0.5, 1.0)
        distance_to_turn = min(
            abs(cycle_position),
            abs(cycle_position - 0.5),
            abs(cycle_position - 1.0)
        )
        return 1.0 - (distance_to_turn * 2)  # Normalize to 0-1 range

class PatternRecognition:
    """
    Pattern recognition system for market behavior analysis
    
    Implements:
    - Historical pattern matching
    - Momentum detection
    - Pressure point identification
    - Behavioral pattern recognition
    """
    
    def __init__(self):
        self.pattern_library = {}
        self.momentum_threshold = 0.02  # 2% threshold for momentum detection
        
    def detect_momentum(self, price_data: List[float], window: int = 20) -> Dict[str, Any]:
        """
        Detect market momentum using price data
        
        Args:
            price_data: List of price values
            window: Rolling window for momentum calculation
            
        Returns:
            Momentum analysis results
        """
        if len(price_data) < window:
            return {"momentum": 0, "direction": "neutral", "strength": 0}
            
        # Calculate momentum using rate of change
        recent_prices = price_data[-window:]
        momentum = (recent_prices[-1] - recent_prices[0]) / recent_prices[0]
        
        # Determine direction and strength
        if momentum > self.momentum_threshold:
            direction = "bullish"
            strength = min(abs(momentum) / self.momentum_threshold, 1.0)
        elif momentum < -self.momentum_threshold:
            direction = "bearish"
            strength = min(abs(momentum) / self.momentum_threshold, 1.0)
        else:
            direction = "neutral"
            strength = 0
            
        return {
            "momentum": momentum,
            "direction": direction,
            "strength": strength,
            "window": window
        }
    
    def identify_pressure_points(self, price_data: List[float], volume_data: List[int]) -> List[Dict[str, Any]]:
        """
        Identify price levels where pressure may exist
        
        Args:
            price_data: Historical price data
            volume_data: Historical volume data
            
        Returns:
            List of pressure points with levels and types
        """
        pressure_points = []
        
        # Find support and resistance levels
        for i in range(2, len(price_data) - 2):
            current_price = price_data[i]
            
            # Check for local maxima (resistance)
            if (price_data[i] > price_data[i-1] and price_data[i] > price_data[i+1] and
                price_data[i] > price_data[i-2] and price_data[i] > price_data[i+2]):
                
                pressure_points.append({
                    "level": current_price,
                    "type": "resistance",
                    "strength": volume_data[i] / max(volume_data),
                    "date_index": i
                })
                
            # Check for local minima (support)
            elif (price_data[i] < price_data[i-1] and price_data[i] < price_data[i+1] and
                  price_data[i] < price_data[i-2] and price_data[i] < price_data[i+2]):
                
                pressure_points.append({
                    "level": current_price,
                    "type": "support",
                    "strength": volume_data[i] / max(volume_data),
                    "date_index": i
                })
        
        return pressure_points

class CapitalFlowAnalyzer:
    """
    Capital flow analysis system
    
    Tracks:
    - International capital movements
    - Regional concentration patterns
    - Asset class rotation
    - Market correlation changes
    """
    
    def __init__(self):
        self.flow_data = []
        self.correlation_threshold = 0.7
        
    def analyze_capital_concentration(self, market_data: Dict[str, List[float]]) -> Dict[str, Any]:
        """
        Analyze capital concentration patterns across markets
        
        Args:
            market_data: Dictionary of market symbols to price data
            
        Returns:
            Capital concentration analysis
        """
        # Calculate correlations between markets
        correlations = {}
        market_symbols = list(market_data.keys())
        
        for i, symbol1 in enumerate(market_symbols):
            for j, symbol2 in enumerate(market_symbols[i+1:], i+1):
                if len(market_data[symbol1]) == len(market_data[symbol2]):
                    corr = np.corrcoef(market_data[symbol1], market_data[symbol2])[0, 1]
                    correlations[f"{symbol1}_{symbol2}"] = corr
        
        # Identify high correlation clusters (capital concentration)
        high_corr_pairs = {k: v for k, v in correlations.items() if abs(v) > self.correlation_threshold}
        
        # Calculate concentration score
        concentration_score = len(high_corr_pairs) / len(correlations) if correlations else 0
        
        return {
            "concentration_score": concentration_score,
            "high_correlation_pairs": high_corr_pairs,
            "total_correlations": len(correlations),
            "concentration_level": self._classify_concentration(concentration_score)
        }
    
    def _classify_concentration(self, score: float) -> str:
        """Classify concentration level"""
        if score > 0.7:
            return "high_concentration"
        elif score > 0.4:
            return "moderate_concentration"
        else:
            return "low_concentration"

class TechnicalAnalyzer:
    """
    Technical analysis system implementing Armstrong's unbiased approach
    
    Features:
    - No fundamental analysis bias
    - Pure mathematical analysis
    - Historical pattern correlation
    - Multi-timeframe analysis
    """
    
    def __init__(self):
        self.indicators = {}
        
    def calculate_cyclical_indicators(self, price_data: List[float], periods: List[int] = None) -> Dict[str, Any]:
        """
        Calculate cyclical indicators for different time periods
        
        Args:
            price_data: Historical price data
            periods: List of periods to analyze
            
        Returns:
            Cyclical analysis results
        """
        if periods is None:
            periods = [8, 21, 55, 144]  # Fibonacci-based periods
            
        indicators = {}
        
        for period in periods:
            if len(price_data) >= period:
                # Simple moving average
                sma = np.mean(price_data[-period:])
                
                # Rate of change
                roc = (price_data[-1] - price_data[-period]) / price_data[-period] if price_data[-period] != 0 else 0
                
                # Volatility (standard deviation)
                volatility = np.std(price_data[-period:])
                
                indicators[f"period_{period}"] = {
                    "sma": sma,
                    "roc": roc,
                    "volatility": volatility,
                    "current_vs_sma": (price_data[-1] - sma) / sma if sma != 0 else 0
                }
        
        return indicators

class SocratesAI:
    """
    Main Socrates AI system integrating all components
    
    This is the central orchestrator that combines:
    - Economic Confidence Model
    - Pattern Recognition
    - Capital Flow Analysis
    - Technical Analysis
    - Multi-market correlation
    """
    
    def __init__(self, db_path: str = "socrates_data.db"):
        self.db_path = db_path
        self.ecm = EconomicConfidenceModel()
        self.pattern_recognizer = PatternRecognition()
        self.capital_flow_analyzer = CapitalFlowAnalyzer()
        self.technical_analyzer = TechnicalAnalyzer()
        
        # Initialize database
        self._init_database()
        
        logger.info("Socrates AI system initialized")
    
    def _init_database(self):
        """Initialize SQLite database for data storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
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
                UNIQUE(symbol, date)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS economic_indicators (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                indicator_id TEXT NOT NULL,
                name TEXT,
                value REAL,
                date TEXT,
                country TEXT,
                source TEXT,
                UNIQUE(indicator_id, date, country)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analysis_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                analysis_date TEXT NOT NULL,
                symbol TEXT,
                analysis_type TEXT,
                results TEXT,
                confidence_score REAL
            )
        ''')
        
        conn.commit()
        conn.close()
        
        logger.info("Database initialized successfully")
    
    def analyze_market(self, symbol: str, analysis_date: datetime = None) -> Dict[str, Any]:
        """
        Perform comprehensive market analysis for a given symbol
        
        Args:
            symbol: Market symbol to analyze
            analysis_date: Date for analysis (default: current date)
            
        Returns:
            Comprehensive analysis results
        """
        if analysis_date is None:
            analysis_date = datetime.now()
            
        logger.info(f"Starting analysis for {symbol} on {analysis_date}")
        
        # Get market data
        market_data = self._get_market_data(symbol)
        if not market_data:
            logger.warning(f"No market data found for {symbol}")
            return {"error": "No market data available"}
        
        # Extract price and volume data
        prices = [data.close_price for data in market_data]
        volumes = [data.volume for data in market_data]
        
        # Perform ECM analysis
        ecm_reference = datetime(2007, 2, 27)  # 2007.15 reference point
        ecm_analysis = self.ecm.calculate_cycle_position(analysis_date, ecm_reference)
        
        # Pattern recognition
        momentum_analysis = self.pattern_recognizer.detect_momentum(prices)
        pressure_points = self.pattern_recognizer.identify_pressure_points(prices, volumes)
        
        # Technical analysis
        technical_indicators = self.technical_analyzer.calculate_cyclical_indicators(prices)
        
        # Compile results
        analysis_results = {
            "symbol": symbol,
            "analysis_date": analysis_date.isoformat(),
            "ecm_analysis": ecm_analysis,
            "momentum_analysis": momentum_analysis,
            "pressure_points": pressure_points[-5:],  # Last 5 pressure points
            "technical_indicators": technical_indicators,
            "overall_confidence": self._calculate_overall_confidence(
                ecm_analysis, momentum_analysis, technical_indicators
            )
        }
        
        # Store results
        self._store_analysis_results(analysis_results)
        
        logger.info(f"Analysis completed for {symbol}")
        return analysis_results
    
    def analyze_global_markets(self, symbols: List[str], analysis_date: datetime = None) -> Dict[str, Any]:
        """
        Perform global market analysis across multiple symbols
        
        Args:
            symbols: List of market symbols to analyze
            analysis_date: Date for analysis
            
        Returns:
            Global market analysis results
        """
        if analysis_date is None:
            analysis_date = datetime.now()
            
        logger.info(f"Starting global analysis for {len(symbols)} markets")
        
        # Analyze individual markets
        individual_analyses = {}
        market_data_dict = {}
        
        for symbol in symbols:
            analysis = self.analyze_market(symbol, analysis_date)
            if "error" not in analysis:
                individual_analyses[symbol] = analysis
                
                # Collect price data for correlation analysis
                market_data = self._get_market_data(symbol)
                if market_data:
                    market_data_dict[symbol] = [data.close_price for data in market_data]
        
        # Capital flow analysis
        capital_flow_analysis = self.capital_flow_analyzer.analyze_capital_concentration(market_data_dict)
        
        # Global ECM analysis
        ecm_reference = datetime(2007, 2, 27)
        global_ecm = self.ecm.calculate_cycle_position(analysis_date, ecm_reference)
        
        # Compile global results
        global_analysis = {
            "analysis_date": analysis_date.isoformat(),
            "markets_analyzed": len(individual_analyses),
            "global_ecm": global_ecm,
            "capital_flow_analysis": capital_flow_analysis,
            "individual_markets": individual_analyses,
            "market_correlations": capital_flow_analysis.get("high_correlation_pairs", {}),
            "global_confidence": self._calculate_global_confidence(
                global_ecm, capital_flow_analysis, individual_analyses
            )
        }
        
        logger.info("Global analysis completed")
        return global_analysis
    
    def _get_market_data(self, symbol: str, days: int = 252) -> List[MarketData]:
        """Retrieve market data from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT symbol, date, open_price, high_price, low_price, close_price, volume, adjusted_close, currency
            FROM market_data 
            WHERE symbol = ? 
            ORDER BY date DESC 
            LIMIT ?
        ''', (symbol, days))
        
        rows = cursor.fetchall()
        conn.close()
        
        market_data = []
        for row in rows:
            market_data.append(MarketData(
                symbol=row[0],
                date=datetime.fromisoformat(row[1]),
                open_price=row[2],
                high_price=row[3],
                low_price=row[4],
                close_price=row[5],
                volume=row[6],
                adjusted_close=row[7],
                currency=row[8]
            ))
        
        return list(reversed(market_data))  # Return in chronological order
    
    def _store_analysis_results(self, results: Dict[str, Any]):
        """Store analysis results in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Convert datetime objects to strings for JSON serialization
        def convert_datetime(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            elif isinstance(obj, dict):
                return {k: convert_datetime(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_datetime(item) for item in obj]
            return obj
        
        serializable_results = convert_datetime(results)
        
        cursor.execute('''
            INSERT OR REPLACE INTO analysis_results 
            (analysis_date, symbol, analysis_type, results, confidence_score)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            results["analysis_date"],
            results["symbol"],
            "comprehensive",
            json.dumps(serializable_results),
            results["overall_confidence"]
        ))
        
        conn.commit()
        conn.close()
    
    def _calculate_overall_confidence(self, ecm_analysis: Dict, momentum_analysis: Dict, 
                                    technical_indicators: Dict) -> float:
        """Calculate overall confidence score for analysis"""
        # Weight different components
        ecm_weight = 0.4
        momentum_weight = 0.3
        technical_weight = 0.3
        
        ecm_confidence = ecm_analysis.get("confidence_level", 0)
        momentum_confidence = momentum_analysis.get("strength", 0)
        
        # Average technical indicator confidence
        tech_confidence = 0
        if technical_indicators:
            tech_values = []
            for period_data in technical_indicators.values():
                # Use absolute ROC as confidence indicator
                tech_values.append(min(abs(period_data.get("roc", 0)) * 10, 1.0))
            tech_confidence = np.mean(tech_values) if tech_values else 0
        
        overall_confidence = (
            ecm_confidence * ecm_weight +
            momentum_confidence * momentum_weight +
            tech_confidence * technical_weight
        )
        
        return min(overall_confidence, 1.0)
    
    def _calculate_global_confidence(self, global_ecm: Dict, capital_flow: Dict, 
                                   individual_analyses: Dict) -> float:
        """Calculate global confidence score"""
        # Global ECM confidence
        ecm_confidence = global_ecm.get("confidence_level", 0)
        
        # Capital flow concentration confidence
        concentration_score = capital_flow.get("concentration_score", 0)
        
        # Average individual market confidence
        individual_confidences = [
            analysis.get("overall_confidence", 0) 
            for analysis in individual_analyses.values()
        ]
        avg_individual_confidence = np.mean(individual_confidences) if individual_confidences else 0
        
        # Weighted global confidence
        global_confidence = (
            ecm_confidence * 0.4 +
            concentration_score * 0.3 +
            avg_individual_confidence * 0.3
        )
        
        return min(global_confidence, 1.0)

def main():
    """Main function for testing the Socrates AI system"""
    # Initialize Socrates AI
    socrates = SocratesAI()
    
    # Test symbols
    test_symbols = ["AAPL", "GOOGL", "MSFT", "SPY", "GLD"]
    
    print("Socrates AI - Market Analysis System")
    print("=" * 50)
    
    # Perform global analysis
    global_results = socrates.analyze_global_markets(test_symbols)
    
    print(f"Global Analysis Results:")
    print(f"Markets Analyzed: {global_results['markets_analyzed']}")
    print(f"Global Confidence: {global_results['global_confidence']:.2f}")
    print(f"Capital Concentration: {global_results['capital_flow_analysis']['concentration_level']}")
    
    # Display ECM analysis
    ecm = global_results['global_ecm']
    print(f"\nECM Analysis:")
    print(f"Cycle Phase: {ecm['phase']}")
    print(f"Days into Cycle: {ecm['days_into_cycle']}")
    print(f"Next Turning Point: {ecm['next_turning_point']}")
    
    print("\nSocrates AI analysis completed successfully!")

if __name__ == "__main__":
    main()

