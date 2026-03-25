#!/usr/bin/env python3
"""
Enhanced Flask Backend for Socrates AI with WebSocket Streaming
Integrates all components into a comprehensive API server
"""

import os
import sys
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import time

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

# Import our components
from socrates_ai_architecture import SocratesAI
from data_collector import DataCollector
from analysis_pipeline import AdvancedAnalyzer
from enhanced_error_handling import ErrorHandler, RobustAPIClient
from database_fixes import DatabaseManager
from websocket_streaming import WebSocketStreamer, StreamType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedSocratesAPI:
    """Enhanced Socrates AI API with WebSocket streaming"""
    
    def __init__(self, db_path: str = "socrates_data.db"):
        self.db_path = db_path
        
        # Initialize Flask app
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'socrates_ai_enhanced_secret_key'
        
        # Enable CORS for all routes
        CORS(self.app, origins="*", allow_headers="*", methods="*")
        
        # Initialize components
        self.db_manager = DatabaseManager(db_path)
        self.socrates_ai = SocratesAI(db_path)
        self.data_collector = DataCollector(db_path)
        self.analyzer = AdvancedAnalyzer(db_path)
        self.error_handler = ErrorHandler()
        
        # Initialize WebSocket streaming