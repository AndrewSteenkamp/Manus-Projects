#!/usr/bin/env python3
"""
Socrates AI API Routes
Flask blueprint for Socrates AI analysis endpoints
"""

import os
import sys
from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
import logging

# Add the src directory to the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.socrates_ai_architecture import SocratesAI
from src.data_collector import DataCollector
from src.analysis_pipeline import AdvancedAnalyzer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create blueprint
socrates_bp = Blueprint('socrates', __name__)

# Initialize Socrates AI components
db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'socrates_data.db')
socrates_ai = SocratesAI(db_path)
data_collector = DataCollector(db_path)
advanced_analyzer = AdvancedAnalyzer(db_path)

@socrates_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Socrates AI",
        "timestamp": datetime.now().isoformat()
    })

@socrates_bp.route('/analyze/market/<symbol>', methods=['GET'])
def analyze_market(symbol):
    """
    Analyze a specific market symbol
    
    Args:
        symbol: Market symbol (e.g., AAPL, GOOGL)
        
    Returns:
        Comprehensive market analysis
    """
    try:
        logger.info(f"Analyzing market: {symbol}")
        
        # Get analysis date from query params
        analysis_date_str = request.args.get('date')
        if analysis_date_str:
            analysis_date = datetime.fromisoformat(analysis_date_str)
        else:
            analysis_date = datetime.now()
        
        # Perform analysis
        analysis_results = socrates_ai.analyze_market(symbol, analysis_date)
        
        if "error" in analysis_results:
            return jsonify({
                "error": analysis_results["error"],
                "symbol": symbol
            }), 400
        
        return jsonify({
            "success": True,
            "data": analysis_results
        })
        
    except Exception as e:
        logger.error(f"Error analyzing market {symbol}: {str(e)}")
        return jsonify({
            "error": f"Analysis failed: {str(e)}",
            "symbol": symbol
        }), 500

@socrates_bp.route('/analyze/global', methods=['GET'])
def analyze_global_markets():
    """
    Analyze global markets
    
    Query params:
        symbols: Comma-separated list of symbols (default: major markets)
        
    Returns:
        Global market analysis
    """
    try:
        # Get symbols from query params
        symbols_param = request.args.get('symbols')
        if symbols_param:
            symbols = [s.strip() for s in symbols_param.split(',')]
        else:
            # Default major markets
            symbols = ["AAPL", "GOOGL", "MSFT", "SPY", "GLD", "EURUSD=X", "GC=F"]
        
        logger.info(f"Analyzing global markets: {symbols}")
        
        # Get analysis date
        analysis_date_str = request.args.get('date')
        if analysis_date_str:
            analysis_date = datetime.fromisoformat(analysis_date_str)
        else:
            analysis_date = datetime.now()
        
        # Perform global analysis
        global_results = socrates_ai.analyze_global_markets(symbols, analysis_date)
        
        return jsonify({
            "success": True,
            "data": global_results
        })
        
    except Exception as e:
        logger.error(f"Error in global analysis: {str(e)}")
        return jsonify({
            "error": f"Global analysis failed: {str(e)}"
        }), 500

@socrates_bp.route('/analyze/cycles/<symbol>', methods=['GET'])
def analyze_cycles(symbol):
    """
    Analyze market cycles for a specific symbol
    
    Args:
        symbol: Market symbol
        
    Returns:
        Cycle analysis results
    """
    try:
        logger.info(f"Analyzing cycles for: {symbol}")
        
        # Perform cycle analysis
        cycle_results = advanced_analyzer.analyze_market_cycles(symbol)
        
        if "error" in cycle_results:
            return jsonify({
                "error": cycle_results["error"],
                "symbol": symbol
            }), 400
        
        return jsonify({
            "success": True,
            "data": cycle_results
        })
        
    except Exception as e:
        logger.error(f"Error analyzing cycles for {symbol}: {str(e)}")
        return jsonify({
            "error": f"Cycle analysis failed: {str(e)}",
            "symbol": symbol
        }), 500

@socrates_bp.route('/analyze/correlations', methods=['GET'])
def analyze_correlations():
    """
    Analyze cross-market correlations
    
    Query params:
        symbols: Comma-separated list of symbols
        window: Rolling window for correlation (default: 252)
        
    Returns:
        Cross-market correlation analysis
    """
    try:
        # Get parameters
        symbols_param = request.args.get('symbols')
        if symbols_param:
            symbols = [s.strip() for s in symbols_param.split(',')]
        else:
            symbols = ["AAPL", "GOOGL", "MSFT", "SPY"]
        
        window = int(request.args.get('window', 252))
        
        logger.info(f"Analyzing correlations for: {symbols}")
        
        # Perform correlation analysis
        corr_results = advanced_analyzer.analyze_cross_market_correlations(symbols, window)
        
        if "error" in corr_results:
            return jsonify({
                "error": corr_results["error"],
                "symbols": symbols
            }), 400
        
        return jsonify({
            "success": True,
            "data": corr_results
        })
        
    except Exception as e:
        logger.error(f"Error analyzing correlations: {str(e)}")
        return jsonify({
            "error": f"Correlation analysis failed: {str(e)}"
        }), 500

@socrates_bp.route('/forecast/<symbol>', methods=['GET'])
def forecast_market(symbol):
    """
    Generate market forecast for a specific symbol
    
    Args:
        symbol: Market symbol
        
    Query params:
        horizon: Forecast horizon in days (default: 30)
        
    Returns:
        Market forecast
    """
    try:
        horizon = int(request.args.get('horizon', 30))
        
        logger.info(f"Generating {horizon}-day forecast for: {symbol}")
        
        # Generate forecast
        forecast_results = advanced_analyzer.generate_market_forecast(symbol, horizon)
        
        if "error" in forecast_results:
            return jsonify({
                "error": forecast_results["error"],
                "symbol": symbol
            }), 400
        
        return jsonify({
            "success": True,
            "data": forecast_results
        })
        
    except Exception as e:
        logger.error(f"Error forecasting {symbol}: {str(e)}")
        return jsonify({
            "error": f"Forecast failed: {str(e)}",
            "symbol": symbol
        }), 500

@socrates_bp.route('/data/collect', methods=['POST'])
def collect_data():
    """
    Trigger data collection
    
    JSON body:
        {
            "data_types": ["stocks", "forex", "commodities", "economic"],
            "symbols": ["AAPL", "GOOGL", ...] (optional)
        }
        
    Returns:
        Data collection results
    """
    try:
        data = request.get_json() or {}
        data_types = data.get('data_types', ['stocks'])
        symbols = data.get('symbols')
        
        logger.info(f"Collecting data types: {data_types}")
        
        results = {}
        
        if 'stocks' in data_types:
            stock_symbols = symbols or ["AAPL", "GOOGL", "MSFT", "SPY", "GLD"]
            results['stocks'] = data_collector.collect_stock_data(stock_symbols)
        
        if 'forex' in data_types:
            results['forex'] = data_collector.collect_forex_data()
        
        if 'commodities' in data_types:
            results['commodities'] = data_collector.collect_commodities_data()
        
        if 'economic' in data_types:
            results['economic'] = data_collector.collect_economic_indicators()
        
        return jsonify({
            "success": True,
            "data": results
        })
        
    except Exception as e:
        logger.error(f"Error collecting data: {str(e)}")
        return jsonify({
            "error": f"Data collection failed: {str(e)}"
        }), 500

@socrates_bp.route('/data/summary', methods=['GET'])
def data_summary():
    """
    Get data collection summary
    
    Returns:
        Summary of available data
    """
    try:
        summary = data_collector.get_collection_summary()
        
        return jsonify({
            "success": True,
            "data": summary
        })
        
    except Exception as e:
        logger.error(f"Error getting data summary: {str(e)}")
        return jsonify({
            "error": f"Failed to get data summary: {str(e)}"
        }), 500

@socrates_bp.route('/daily-report', methods=['GET'])
def daily_report():
    """
    Generate daily market report
    
    Query params:
        date: Analysis date (default: today)
        
    Returns:
        Comprehensive daily market report
    """
    try:
        # Get analysis date
        date_str = request.args.get('date')
        if date_str:
            analysis_date = datetime.fromisoformat(date_str)
        else:
            analysis_date = datetime.now()
        
        logger.info(f"Generating daily report for: {analysis_date.date()}")
        
        # Major markets to analyze
        major_markets = ["AAPL", "GOOGL", "MSFT", "SPY", "GLD", "EURUSD=X", "GC=F", "CL=F"]
        
        # Global analysis
        global_analysis = socrates_ai.analyze_global_markets(major_markets, analysis_date)
        
        # Individual market highlights
        market_highlights = {}
        for symbol in ["SPY", "GLD", "EURUSD=X"]:  # Key indicators
            try:
                analysis = socrates_ai.analyze_market(symbol, analysis_date)
                if "error" not in analysis:
                    market_highlights[symbol] = {
                        "confidence": analysis.get("overall_confidence", 0),
                        "momentum": analysis.get("momentum_analysis", {}),
                        "ecm_phase": analysis.get("ecm_analysis", {}).get("phase", "unknown")
                    }
            except Exception as e:
                logger.warning(f"Error analyzing {symbol} for daily report: {e}")
        
        # Economic Confidence Model summary
        ecm_summary = global_analysis.get("global_ecm", {})
        
        # Capital flow analysis
        capital_flows = global_analysis.get("capital_flow_analysis", {})
        
        # Generate summary insights
        insights = []
        
        # ECM insights
        if ecm_summary:
            phase = ecm_summary.get("phase", "unknown")
            days_into_cycle = ecm_summary.get("days_into_cycle", 0)
            insights.append(f"ECM Analysis: Currently in {phase} phase, {days_into_cycle} days into the 8.6-year cycle.")
        
        # Capital flow insights
        if capital_flows:
            concentration = capital_flows.get("concentration_level", "unknown")
            insights.append(f"Capital Flow: {concentration} concentration detected across global markets.")
        
        # Market momentum insights
        bullish_markets = []
        bearish_markets = []
        for symbol, data in market_highlights.items():
            momentum = data.get("momentum", {})
            direction = momentum.get("direction", "neutral")
            if direction == "bullish":
                bullish_markets.append(symbol)
            elif direction == "bearish":
                bearish_markets.append(symbol)
        
        if bullish_markets:
            insights.append(f"Bullish momentum detected in: {', '.join(bullish_markets)}")
        if bearish_markets:
            insights.append(f"Bearish momentum detected in: {', '.join(bearish_markets)}")
        
        # Compile daily report
        daily_report = {
            "date": analysis_date.date().isoformat(),
            "global_confidence": global_analysis.get("global_confidence", 0),
            "ecm_analysis": ecm_summary,
            "capital_flow_analysis": capital_flows,
            "market_highlights": market_highlights,
            "key_insights": insights,
            "markets_analyzed": len(major_markets),
            "report_generated": datetime.now().isoformat()
        }
        
        return jsonify({
            "success": True,
            "data": daily_report
        })
        
    except Exception as e:
        logger.error(f"Error generating daily report: {str(e)}")
        return jsonify({
            "error": f"Daily report generation failed: {str(e)}"
        }), 500

@socrates_bp.route('/markets/available', methods=['GET'])
def available_markets():
    """
    Get list of available markets in the database
    
    Returns:
        List of available market symbols
    """
    try:
        import sqlite3
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get unique symbols from market_data table
        cursor.execute('SELECT DISTINCT symbol FROM market_data ORDER BY symbol')
        symbols = [row[0] for row in cursor.fetchall()]
        
        # Get forex pairs
        cursor.execute('SELECT DISTINCT pair FROM forex_data ORDER BY pair')
        forex_pairs = [row[0] for row in cursor.fetchall()]
        
        # Get commodities
        cursor.execute('SELECT DISTINCT commodity FROM commodities_data ORDER BY commodity')
        commodities = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        
        return jsonify({
            "success": True,
            "data": {
                "stocks": symbols,
                "forex": forex_pairs,
                "commodities": commodities,
                "total_markets": len(symbols) + len(forex_pairs) + len(commodities)
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting available markets: {str(e)}")
        return jsonify({
            "error": f"Failed to get available markets: {str(e)}"
        }), 500

