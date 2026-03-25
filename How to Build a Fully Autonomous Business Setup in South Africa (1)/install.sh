#!/bin/bash

echo "========================================"
echo "  AUTONOMOUS AI BUSINESS - INSTALLER"
echo "========================================"
echo ""
echo "This will install everything you need."
echo "Please wait 2-3 minutes..."
echo ""

echo "[1/4] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed!"
    echo "Please install Python 3 from: https://www.python.org/downloads/"
    exit 1
fi
echo "Python found!"
echo ""

echo "[2/4] Upgrading pip..."
python3 -m pip install --upgrade pip --quiet
echo "Done!"
echo ""

echo "[3/4] Installing required packages..."
echo "This may take a minute..."
pip3 install Flask openai requests python-dotenv --quiet
echo "Done!"
echo ""

echo "[4/4] Creating configuration file..."
if [ ! -f config.txt ]; then
    cat > config.txt << EOF
OPENAI_API_KEY=YOUR_API_KEY_HERE
PAYFAST_MERCHANT_ID=10000100
PAYFAST_MERCHANT_KEY=46f0cd694581a
PAYFAST_PASSPHRASE=jt7NOE43FZPn
SANDBOX_MODE=true
EOF
    echo "Configuration file created!"
else
    echo "Configuration file already exists."
fi
echo ""

echo "========================================"
echo "  INSTALLATION COMPLETE!"
echo "========================================"
echo ""
echo "NEXT STEPS:"
echo "1. Edit config.txt and add your OpenAI API key"
echo "2. Run ./start.sh to start the system"
echo ""
echo "Press Enter to close..."
read
