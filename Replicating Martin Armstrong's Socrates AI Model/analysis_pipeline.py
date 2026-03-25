#!/usr/bin/env python3
"""
Socrates AI Analysis Pipeline
Advanced data processing and analysis system

This pipeline implements:
1. Multi-timeframe analysis
2. Cross-market correlation analysis
3. Economic cycle detection
4. Pattern recognition and forecasting
5. Capital flow analysis
6. Risk assessment

Author: AI Replication Project
Based on: Martin Armstrong's Socrates AI methodology
"""

import numpy as np
import pandas as pd
import sqlite3
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.signal import find_peaks
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class AnalysisResult:
    """Data structure for analysis results"""
    symbol: str
    analysis_type: str
    timestamp: datetime
    confidence: float
    signals: Dict[str, Any]
    forecast: Dict[str, Any]
    risk_assessment: Dict[str, Any]

@dataclass
class MarketCycle:
    """Data structure for market cycle information"""
    cycle_length: int
    amplitude: float
    phase: float
    next_peak: datetime
    next_trough: datetime
    confidence: float

class AdvancedAnalyzer:
    """
    Advanced analysis system implementing sophisticated market analysis
    
    Features:
    - Multi-dimensional analysis
    - Machine learning pattern recognition
    - Statistical significance testing
    - Cross-market correlation analysis
    - Economic cycle detection
    """
    
    def __init__(self, db_path: str = "socrates_data.db"):
        self.db_path = db_path
        self.scaler = StandardScaler()
        
        # Analysis parameters
        self.short_window = 20
        self.medium_window = 50
        self.long_window = 200
        self.correlation_threshold = 0.7
        self.significance_level = 0.05
        
        logger.info("Advanced Analyzer initialized")
    
    def analyze_market_cycles(self, symbol: str) -> Dict[str, Any]:
        """
        Analyze market cycles using spectral analysis and peak detection
        
        Args:
            symbol: Market symbol to analyze
            
        Returns:
            Comprehensive cycle analysis
        """
        logger.info(f"Analyzing market cycles for {symbol}")
        
        # Get price data
        price_data = self._get_price_data(symbol)
        if len(price_data) < 100:
            return {"error": "Insufficient data for cycle analysis"}
        
        prices = np.array([p['close_price'] for p in price_data])
        dates = [datetime.fromisoformat(p['date']) for p in price_data]
        
        # Detrend the data
        detrended = self._detrend_data(prices)
        
        # Find cycles using FFT
        cycles = self._detect_cycles_fft(detrended)
        
        # Find peaks and troughs
        peaks, peak_properties = find_peaks(detrended, height=np.std(detrended) * 0.5)
        troughs, trough_properties = find_peaks(-detrended, height=np.std(detrended) * 0.5)
        
        # Calculate cycle statistics
        cycle_stats = self._calculate_cycle_statistics(peaks, troughs, len(prices))
        
        # Forecast next turning points
        forecast = self._forecast_turning_points(prices, dates, cycles)
        
        return {
            "symbol": symbol,
            "dominant_cycles": cycles[:5],  # Top 5 cycles
            "cycle_statistics": cycle_stats,
            "current_phase": self._determine_cycle_phase(prices, peaks, troughs),
            "forecast": forecast,
            "confidence": self._calculate_cycle_confidence(cycles, cycle_stats)
        }
    
    def analyze_cross_market_correlations(self, symbols: List[str], window: int = 252) -> Dict[str, Any]:
        """
        Analyze correlations between multiple markets
        
        Args:
            symbols: List of market symbols
            window: Rolling window for correlation calculation
            
        Returns:
            Cross-market correlation analysis
        """
        logger.info(f"Analyzing cross-market correlations for {len(symbols)} markets")
        
        # Get price data for all symbols
        market_data = {}
        for symbol in symbols:
            price_data = self._get_price_data(symbol)
            if price_data:
                market_data[symbol] = pd.DataFrame(price_data)
        
        if len(market_data) < 2:
            return {"error": "Insufficient market data for correlation analysis"}
        
        # Align data by date
        aligned_data = self._align_market_data(market_data)
        
        # Calculate correlations
        correlations = self._calculate_rolling_correlations(aligned_data, window)
        
        # Identify correlation clusters
        clusters = self._identify_correlation_clusters(correlations)
        
        # Analyze correlation stability
        stability = self._analyze_correlation_stability(correlations)
        
        # Capital flow analysis
        capital_flows = self._analyze_capital_flows(aligned_data, correlations)
        
        return {
            "correlation_matrix": correlations.iloc[-1].to_dict(),  # Latest correlations
            "correlation_clusters": clusters,
            "stability_analysis": stability,
            "capital_flow_analysis": capital_flows,
            "market_concentration": self._calculate_market_concentration(correlations.iloc[-1])
        }
    
    def analyze_economic_indicators(self) -> Dict[str, Any]:
        """
        Analyze economic indicators and their market impact
        
        Returns:
            Economic indicator analysis
        """
        logger.info("Analyzing economic indicators")
        
        # Get economic indicator data
        indicators = self._get_economic_indicators()
        if not indicators:
            return {"error": "No economic indicator data available"}
        
        # Analyze indicator trends
        trends = self._analyze_indicator_trends(indicators)
        
        # Calculate composite economic score
        composite_score = self._calculate_composite_economic_score(indicators)
        
        # Assess economic cycle position
        cycle_position = self._assess_economic_cycle_position(indicators, trends)
        
        return {
            "indicator_trends": trends,
            "composite_economic_score": composite_score,
            "economic_cycle_position": cycle_position,
            "leading_indicators": self._identify_leading_indicators(indicators),
            "economic_confidence": self._calculate_economic_confidence(composite_score, cycle_position)
        }
    
    def generate_market_forecast(self, symbol: str, horizon_days: int = 30) -> Dict[str, Any]:
        """
        Generate market forecast using multiple analysis techniques
        
        Args:
            symbol: Market symbol to forecast
            horizon_days: Forecast horizon in days
            
        Returns:
            Comprehensive market forecast
        """
        logger.info(f"Generating {horizon_days}-day forecast for {symbol}")
        
        # Get historical data
        price_data = self._get_price_data(symbol, days=500)  # More data for better forecasting
        if len(price_data) < 100:
            return {"error": "Insufficient data for forecasting"}
        
        prices = np.array([p['close_price'] for p in price_data])
        dates = [datetime.fromisoformat(p['date']) for p in price_data]
        
        # Multiple forecasting approaches
        forecasts = {}
        
        # 1. Trend-based forecast
        forecasts['trend'] = self._forecast_trend(prices, horizon_days)
        
        # 2. Cycle-based forecast
        forecasts['cycle'] = self._forecast_cycles(prices, dates, horizon_days)
        
        # 3. Mean reversion forecast
        forecasts['mean_reversion'] = self._forecast_mean_reversion(prices, horizon_days)
        
        # 4. Momentum-based forecast
        forecasts['momentum'] = self._forecast_momentum(prices, horizon_days)
        
        # Combine forecasts with weights
        combined_forecast = self._combine_forecasts(forecasts)
        
        # Calculate confidence intervals
        confidence_intervals = self._calculate_forecast_confidence(prices, combined_forecast)
        
        # Risk assessment
        risk_assessment = self._assess_forecast_risk(prices, combined_forecast)
        
        return {
            "symbol": symbol,
            "forecast_horizon": horizon_days,
            "individual_forecasts": forecasts,
            "combined_forecast": combined_forecast,
            "confidence_intervals": confidence_intervals,
            "risk_assessment": risk_assessment,
            "forecast_confidence": self._calculate_overall_forecast_confidence(forecasts, risk_assessment)
        }
    
    def _get_price_data(self, symbol: str, days: int = 252) -> List[Dict]:
        """Get price data from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT date, open_price, high_price, low_price, close_price, volume
            FROM market_data 
            WHERE symbol = ? 
            ORDER BY date DESC 
            LIMIT ?
        ''', (symbol, days))
        
        rows = cursor.fetchall()
        conn.close()
        
        data = []
        for row in rows:
            data.append({
                'date': row[0],
                'open_price': row[1],
                'high_price': row[2],
                'low_price': row[3],
                'close_price': row[4],
                'volume': row[5]
            })
        
        return list(reversed(data))  # Return in chronological order
    
    def _get_economic_indicators(self) -> List[Dict]:
        """Get economic indicators from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT indicator_id, name, value, date, country, source
            FROM economic_indicators 
            ORDER BY date DESC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        indicators = []
        for row in rows:
            indicators.append({
                'indicator_id': row[0],
                'name': row[1],
                'value': row[2],
                'date': row[3],
                'country': row[4],
                'source': row[5]
            })
        
        return indicators
    
    def _detrend_data(self, data: np.ndarray) -> np.ndarray:
        """Remove trend from data using linear detrending"""
        x = np.arange(len(data))
        slope, intercept, _, _, _ = stats.linregress(x, data)
        trend = slope * x + intercept
        return data - trend
    
    def _detect_cycles_fft(self, data: np.ndarray) -> List[Dict]:
        """Detect cycles using Fast Fourier Transform"""
        # Apply FFT
        fft = np.fft.fft(data)
        frequencies = np.fft.fftfreq(len(data))
        
        # Get power spectrum
        power = np.abs(fft) ** 2
        
        # Find dominant frequencies
        # Exclude DC component and negative frequencies
        valid_indices = np.where((frequencies > 0) & (frequencies < 0.5))[0]
        valid_frequencies = frequencies[valid_indices]
        valid_power = power[valid_indices]
        
        # Sort by power
        sorted_indices = np.argsort(valid_power)[::-1]
        
        cycles = []
        for i in range(min(10, len(sorted_indices))):  # Top 10 cycles
            idx = valid_indices[sorted_indices[i]]
            frequency = valid_frequencies[sorted_indices[i]]
            period = 1 / frequency if frequency > 0 else float('inf')
            power_val = valid_power[sorted_indices[i]]
            
            cycles.append({
                'period_days': int(period),
                'frequency': frequency,
                'power': power_val,
                'relative_strength': power_val / np.max(valid_power)
            })
        
        return cycles
    
    def _calculate_cycle_statistics(self, peaks: np.ndarray, troughs: np.ndarray, data_length: int) -> Dict:
        """Calculate cycle statistics from peaks and troughs"""
        if len(peaks) < 2 or len(troughs) < 2:
            return {"error": "Insufficient peaks/troughs for cycle analysis"}
        
        # Calculate peak-to-peak distances
        peak_distances = np.diff(peaks)
        trough_distances = np.diff(troughs)
        
        # Calculate average cycle length
        avg_peak_cycle = np.mean(peak_distances) if len(peak_distances) > 0 else 0
        avg_trough_cycle = np.mean(trough_distances) if len(trough_distances) > 0 else 0
        
        return {
            "average_peak_cycle": avg_peak_cycle,
            "average_trough_cycle": avg_trough_cycle,
            "peak_cycle_std": np.std(peak_distances) if len(peak_distances) > 0 else 0,
            "trough_cycle_std": np.std(trough_distances) if len(trough_distances) > 0 else 0,
            "total_peaks": len(peaks),
            "total_troughs": len(troughs),
            "cycle_regularity": self._calculate_cycle_regularity(peak_distances, trough_distances)
        }
    
    def _calculate_cycle_regularity(self, peak_distances: np.ndarray, trough_distances: np.ndarray) -> float:
        """Calculate how regular the cycles are (0 = irregular, 1 = perfectly regular)"""
        if len(peak_distances) == 0 and len(trough_distances) == 0:
            return 0
        
        all_distances = np.concatenate([peak_distances, trough_distances])
        if len(all_distances) < 2:
            return 0
        
        # Coefficient of variation (lower = more regular)
        cv = np.std(all_distances) / np.mean(all_distances) if np.mean(all_distances) > 0 else float('inf')
        
        # Convert to regularity score (0-1)
        regularity = max(0, 1 - cv)
        return min(1, regularity)
    
    def _determine_cycle_phase(self, prices: np.ndarray, peaks: np.ndarray, troughs: np.ndarray) -> Dict:
        """Determine current position in market cycle"""
        current_position = len(prices) - 1
        
        # Find nearest peak and trough
        nearest_peak = peaks[peaks <= current_position][-1] if len(peaks[peaks <= current_position]) > 0 else None
        nearest_trough = troughs[troughs <= current_position][-1] if len(troughs[troughs <= current_position]) > 0 else None
        
        # Determine phase
        if nearest_peak is None and nearest_trough is None:
            phase = "undefined"
            phase_progress = 0
        elif nearest_peak is None:
            phase = "early_uptrend"
            phase_progress = (current_position - nearest_trough) / 50  # Normalize
        elif nearest_trough is None:
            phase = "early_downtrend"
            phase_progress = (current_position - nearest_peak) / 50
        elif nearest_peak > nearest_trough:
            phase = "downtrend"
            phase_progress = (current_position - nearest_peak) / 50
        else:
            phase = "uptrend"
            phase_progress = (current_position - nearest_trough) / 50
        
        return {
            "phase": phase,
            "phase_progress": min(1.0, max(0.0, phase_progress)),
            "nearest_peak_distance": current_position - nearest_peak if nearest_peak is not None else None,
            "nearest_trough_distance": current_position - nearest_trough if nearest_trough is not None else None
        }
    
    def _forecast_turning_points(self, prices: np.ndarray, dates: List[datetime], cycles: List[Dict]) -> Dict:
        """Forecast next turning points based on cycle analysis"""
        if not cycles:
            return {"error": "No cycles detected for forecasting"}
        
        # Use dominant cycle for forecasting
        dominant_cycle = cycles[0]
        cycle_period = dominant_cycle['period_days']
        
        # Estimate next turning points
        last_date = dates[-1]
        
        # Simple estimation based on cycle period
        next_peak_date = last_date + timedelta(days=cycle_period // 2)
        next_trough_date = last_date + timedelta(days=cycle_period)
        
        # Estimate price levels (very simplified)
        current_price = prices[-1]
        price_volatility = np.std(prices[-50:])  # Last 50 days volatility
        
        return {
            "next_peak": {
                "date": next_peak_date.isoformat(),
                "estimated_price": current_price + price_volatility,
                "confidence": dominant_cycle['relative_strength']
            },
            "next_trough": {
                "date": next_trough_date.isoformat(),
                "estimated_price": current_price - price_volatility,
                "confidence": dominant_cycle['relative_strength']
            }
        }
    
    def _calculate_cycle_confidence(self, cycles: List[Dict], cycle_stats: Dict) -> float:
        """Calculate overall confidence in cycle analysis"""
        if not cycles or "error" in cycle_stats:
            return 0.0
        
        # Factors affecting confidence
        dominant_cycle_strength = cycles[0]['relative_strength'] if cycles else 0
        cycle_regularity = cycle_stats.get('cycle_regularity', 0)
        num_cycles_detected = len(cycles)
        
        # Weighted confidence score
        confidence = (
            dominant_cycle_strength * 0.4 +
            cycle_regularity * 0.4 +
            min(num_cycles_detected / 5, 1.0) * 0.2
        )
        
        return min(1.0, confidence)
    
    def _align_market_data(self, market_data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """Align market data by date"""
        aligned = pd.DataFrame()
        
        for symbol, data in market_data.items():
            data['date'] = pd.to_datetime(data['date'])
            data = data.set_index('date')
            aligned[symbol] = data['close_price']
        
        # Forward fill missing values
        aligned = aligned.fillna(method='ffill').dropna()
        
        return aligned
    
    def _calculate_rolling_correlations(self, data: pd.DataFrame, window: int) -> pd.DataFrame:
        """Calculate rolling correlations between markets"""
        correlations = pd.DataFrame(index=data.index)
        
        symbols = data.columns.tolist()
        for i, symbol1 in enumerate(symbols):
            for j, symbol2 in enumerate(symbols[i+1:], i+1):
                corr_name = f"{symbol1}_{symbol2}"
                correlations[corr_name] = data[symbol1].rolling(window).corr(data[symbol2])
        
        return correlations.dropna()
    
    def _identify_correlation_clusters(self, correlations: pd.DataFrame) -> Dict[str, List[str]]:
        """Identify correlation clusters using K-means"""
        if correlations.empty:
            return {}
        
        # Get latest correlation values
        latest_corr = correlations.iloc[-1].values.reshape(-1, 1)
        
        # Determine optimal number of clusters (2-4)
        n_clusters = min(4, max(2, len(correlations.columns) // 3))
        
        try:
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            cluster_labels = kmeans.fit_predict(latest_corr)
            
            clusters = {}
            for i, label in enumerate(cluster_labels):
                cluster_name = f"cluster_{label}"
                if cluster_name not in clusters:
                    clusters[cluster_name] = []
                clusters[cluster_name].append(correlations.columns[i])
            
            return clusters
        except Exception as e:
            logger.warning(f"Error in clustering: {e}")
            return {}
    
    def _analyze_correlation_stability(self, correlations: pd.DataFrame) -> Dict[str, float]:
        """Analyze stability of correlations over time"""
        if correlations.empty:
            return {}
        
        stability = {}
        for column in correlations.columns:
            corr_series = correlations[column].dropna()
            if len(corr_series) > 1:
                # Calculate coefficient of variation
                stability[column] = 1 - (corr_series.std() / abs(corr_series.mean())) if corr_series.mean() != 0 else 0
            else:
                stability[column] = 0
        
        return stability
    
    def _analyze_capital_flows(self, data: pd.DataFrame, correlations: pd.DataFrame) -> Dict[str, Any]:
        """Analyze capital flows between markets"""
        if data.empty or correlations.empty:
            return {}
        
        # Calculate momentum for each market
        momentum = {}
        for symbol in data.columns:
            returns = data[symbol].pct_change().dropna()
            momentum[symbol] = returns.rolling(20).mean().iloc[-1] if len(returns) > 20 else 0
        
        # Identify flow patterns
        high_momentum = {k: v for k, v in momentum.items() if v > 0.01}  # > 1% momentum
        low_momentum = {k: v for k, v in momentum.items() if v < -0.01}  # < -1% momentum
        
        return {
            "high_momentum_markets": high_momentum,
            "low_momentum_markets": low_momentum,
            "capital_flow_direction": "risk_on" if len(high_momentum) > len(low_momentum) else "risk_off",
            "flow_intensity": abs(sum(momentum.values())) / len(momentum)
        }
    
    def _calculate_market_concentration(self, latest_correlations: pd.Series) -> Dict[str, Any]:
        """Calculate market concentration metrics"""
        if latest_correlations.empty:
            return {}
        
        high_corr_count = len(latest_correlations[abs(latest_correlations) > self.correlation_threshold])
        total_pairs = len(latest_correlations)
        
        concentration_ratio = high_corr_count / total_pairs if total_pairs > 0 else 0
        
        return {
            "concentration_ratio": concentration_ratio,
            "high_correlation_pairs": high_corr_count,
            "total_pairs": total_pairs,
            "concentration_level": "high" if concentration_ratio > 0.6 else "medium" if concentration_ratio > 0.3 else "low"
        }
    
    def _forecast_trend(self, prices: np.ndarray, horizon: int) -> Dict[str, Any]:
        """Simple trend-based forecast"""
        # Linear regression on recent data
        recent_data = prices[-50:]  # Last 50 days
        x = np.arange(len(recent_data))
        slope, intercept, r_value, _, _ = stats.linregress(x, recent_data)
        
        # Forecast
        future_x = np.arange(len(recent_data), len(recent_data) + horizon)
        forecast = slope * future_x + intercept
        
        return {
            "forecast_values": forecast.tolist(),
            "trend_slope": slope,
            "r_squared": r_value ** 2,
            "confidence": abs(r_value)
        }
    
    def _forecast_cycles(self, prices: np.ndarray, dates: List[datetime], horizon: int) -> Dict[str, Any]:
        """Cycle-based forecast"""
        # Simplified cycle forecast
        detrended = self._detrend_data(prices)
        cycles = self._detect_cycles_fft(detrended)
        
        if not cycles:
            return {"error": "No cycles detected"}
        
        # Use dominant cycle
        dominant_cycle = cycles[0]
        period = dominant_cycle['period_days']
        
        # Simple sinusoidal projection
        current_phase = len(prices) % period
        amplitude = np.std(detrended)
        
        forecast = []
        for i in range(horizon):
            phase = (current_phase + i) * 2 * np.pi / period
            cycle_value = amplitude * np.sin(phase)
            forecast.append(prices[-1] + cycle_value)
        
        return {
            "forecast_values": forecast,
            "cycle_period": period,
            "confidence": dominant_cycle['relative_strength']
        }
    
    def _forecast_mean_reversion(self, prices: np.ndarray, horizon: int) -> Dict[str, Any]:
        """Mean reversion forecast"""
        # Calculate long-term mean
        long_term_mean = np.mean(prices[-200:]) if len(prices) >= 200 else np.mean(prices)
        current_price = prices[-1]
        
        # Mean reversion speed (simplified)
        reversion_speed = 0.05  # 5% per day
        
        forecast = []
        price = current_price
        for i in range(horizon):
            price = price + (long_term_mean - price) * reversion_speed
            forecast.append(price)
        
        return {
            "forecast_values": forecast,
            "long_term_mean": long_term_mean,
            "reversion_speed": reversion_speed,
            "confidence": 0.6  # Moderate confidence
        }
    
    def _forecast_momentum(self, prices: np.ndarray, horizon: int) -> Dict[str, Any]:
        """Momentum-based forecast"""
        # Calculate momentum
        returns = np.diff(prices) / prices[:-1]
        momentum = np.mean(returns[-20:])  # 20-day momentum
        
        # Project momentum with decay
        decay_factor = 0.95
        forecast = []
        current_price = prices[-1]
        
        for i in range(horizon):
            momentum *= decay_factor
            current_price *= (1 + momentum)
            forecast.append(current_price)
        
        return {
            "forecast_values": forecast,
            "initial_momentum": np.mean(returns[-20:]),
            "decay_factor": decay_factor,
            "confidence": 0.5  # Moderate confidence
        }
    
    def _combine_forecasts(self, forecasts: Dict[str, Dict]) -> Dict[str, Any]:
        """Combine multiple forecasts with weights"""
        weights = {
            'trend': 0.3,
            'cycle': 0.3,
            'mean_reversion': 0.2,
            'momentum': 0.2
        }
        
        # Get forecast values
        all_forecasts = []
        valid_forecasts = []
        
        for method, forecast in forecasts.items():
            if 'forecast_values' in forecast and method in weights:
                all_forecasts.append(np.array(forecast['forecast_values']))
                valid_forecasts.append(method)
        
        if not all_forecasts:
            return {"error": "No valid forecasts to combine"}
        
        # Combine with weights
        combined = np.zeros_like(all_forecasts[0])
        total_weight = 0
        
        for i, method in enumerate(valid_forecasts):
            weight = weights[method]
            combined += weight * all_forecasts[i]
            total_weight += weight
        
        if total_weight > 0:
            combined /= total_weight
        
        return {
            "forecast_values": combined.tolist(),
            "methods_used": valid_forecasts,
            "weights_applied": {method: weights[method] for method in valid_forecasts}
        }
    
    def _calculate_forecast_confidence(self, prices: np.ndarray, forecast: Dict) -> Dict[str, Any]:
        """Calculate confidence intervals for forecast"""
        if 'forecast_values' in forecast:
            # Use historical volatility for confidence intervals
            returns = np.diff(prices) / prices[:-1]
            volatility = np.std(returns)
            
            forecast_values = np.array(forecast['forecast_values'])
            
            # 95% confidence intervals
            upper_bound = forecast_values * (1 + 1.96 * volatility)
            lower_bound = forecast_values * (1 - 1.96 * volatility)
            
            return {
                "upper_95": upper_bound.tolist(),
                "lower_95": lower_bound.tolist(),
                "volatility_used": volatility
            }
        
        return {}
    
    def _assess_forecast_risk(self, prices: np.ndarray, forecast: Dict) -> Dict[str, Any]:
        """Assess risk associated with forecast"""
        if 'forecast_values' not in forecast:
            return {}
        
        current_price = prices[-1]
        forecast_values = np.array(forecast['forecast_values'])
        
        # Calculate potential returns
        potential_returns = (forecast_values - current_price) / current_price
        
        # Risk metrics
        max_gain = np.max(potential_returns)
        max_loss = np.min(potential_returns)
        volatility = np.std(potential_returns)
        
        return {
            "max_potential_gain": max_gain,
            "max_potential_loss": max_loss,
            "forecast_volatility": volatility,
            "risk_level": "high" if volatility > 0.1 else "medium" if volatility > 0.05 else "low"
        }
    
    def _calculate_overall_forecast_confidence(self, forecasts: Dict, risk_assessment: Dict) -> float:
        """Calculate overall confidence in forecast"""
        # Average individual forecast confidences
        confidences = []
        for forecast in forecasts.values():
            if 'confidence' in forecast:
                confidences.append(forecast['confidence'])
        
        avg_confidence = np.mean(confidences) if confidences else 0.5
        
        # Adjust for risk
        risk_penalty = 0
        if 'risk_level' in risk_assessment:
            risk_level = risk_assessment['risk_level']
            if risk_level == 'high':
                risk_penalty = 0.2
            elif risk_level == 'medium':
                risk_penalty = 0.1
        
        return max(0, min(1, avg_confidence - risk_penalty))

def main():
    """Main function for testing the analysis pipeline"""
    analyzer = AdvancedAnalyzer()
    
    print("Socrates AI - Advanced Analysis Pipeline")
    print("=" * 50)
    
    # Test cycle analysis
    print("Testing cycle analysis for AAPL...")
    cycle_results = analyzer.analyze_market_cycles("AAPL")
    if "error" not in cycle_results:
        print(f"Dominant cycles detected: {len(cycle_results['dominant_cycles'])}")
        print(f"Current phase: {cycle_results['current_phase']['phase']}")
        print(f"Cycle confidence: {cycle_results['confidence']:.2f}")
    
    # Test cross-market correlation
    print("\nTesting cross-market correlation analysis...")
    symbols = ["AAPL", "GOOGL", "MSFT", "SPY"]
    corr_results = analyzer.analyze_cross_market_correlations(symbols)
    if "error" not in corr_results:
        print(f"Market concentration: {corr_results['market_concentration']['concentration_level']}")
        print(f"Capital flow direction: {corr_results['capital_flow_analysis'].get('capital_flow_direction', 'N/A')}")
    
    # Test forecasting
    print("\nTesting market forecasting for AAPL...")
    forecast_results = analyzer.generate_market_forecast("AAPL", 30)
    if "error" not in forecast_results:
        print(f"Forecast confidence: {forecast_results['forecast_confidence']:.2f}")
        print(f"Risk level: {forecast_results['risk_assessment'].get('risk_level', 'N/A')}")
    
    print("\nAdvanced analysis pipeline test completed!")

if __name__ == "__main__":
    main()

