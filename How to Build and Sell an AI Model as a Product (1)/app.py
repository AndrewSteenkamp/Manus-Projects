"""
Siener AI - Main Flask Application
Complete autonomous business system with 4 world-class agents
"""

import os
import asyncio
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
import logging
import json

# Import core components
from core.agent_orchestrator import orchestrator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'siener-ai-secret-key')
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'

# Global variables
orchestrator_started = False

@app.before_first_request
async def initialize_system():
    """Initialize the Siener AI system"""
    global orchestrator_started
    
    if not orchestrator_started:
        try:
            logger.info("Initializing Siener AI system...")
            await orchestrator.start()
            orchestrator_started = True
            logger.info("Siener AI system initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize system: {str(e)}")

# Health check endpoints
@app.route('/health')
def health_check():
    """Basic health check"""
    return jsonify({
