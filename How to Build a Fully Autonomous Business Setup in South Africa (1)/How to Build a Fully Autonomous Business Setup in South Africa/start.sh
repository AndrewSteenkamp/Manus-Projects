#!/bin/bash

echo "========================================"
echo "  AUTONOMOUS AI BUSINESS - STARTING"
echo "========================================"
echo ""
echo "Starting your AI business system..."
echo ""
echo "The dashboard will open in your browser automatically."
echo ""
echo "To stop the system, press CTRL+C"
echo ""
echo "========================================"
echo ""

# Load environment variables from config.txt
if [ -f config.txt ]; then
    export $(cat config.txt | xargs)
fi

# Start the Flask application
python3 app.py
