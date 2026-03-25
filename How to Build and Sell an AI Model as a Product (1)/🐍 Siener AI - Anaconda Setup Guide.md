# 🐍 Siener AI - Anaconda Setup Guide

**Complete step-by-step guide for running Siener AI on your computer using Anaconda and Spyder**

## 📋 Prerequisites

Before starting, make sure you have:
- **Anaconda Distribution** installed on your computer
- **Internet connection** for downloading packages and market data
- **Yoco developer account** (free to create at https://developer.yoco.com/)

## 🚀 Phase 1: Environment Setup

### Step 1.1: Open Anaconda Navigator
1. **Windows:** Click Start Menu → Anaconda3 → Anaconda Navigator
2. **Mac:** Applications → Anaconda Navigator  
3. **Linux:** Open terminal and type `anaconda-navigator`

### Step 1.2: Create Siener AI Environment
1. In Anaconda Navigator, click **"Environments"** on the left sidebar
2. Click **"Create"** button at the bottom
3. **Name:** `siener-ai`
4. **Python version:** Select `3.11`
5. Click **"Create"** and wait for environment creation (2-3 minutes)

### Step 1.3: Activate Environment
1. In the Environments tab, click on **"siener-ai"** environment
2. Wait for it to load (green arrow will appear)
3. Click the **green play button** next to "siener-ai"
4. Select **"Open Terminal"**

## 📦 Phase 2: Install Dependencies

### Step 2.1: Navigate to Project Folder
In the terminal that opened:
```bash
# Change to your Downloads folder (or wherever you extracted the ZIP)
cd Downloads/siener-ai-complete-package

# Verify you're in the right folder
ls
```
You should see: `app.py`, `market_data.py`, `yoco_payments.py`, `requirements.txt`

### Step 2.2: Install Required Packages
```bash
# Install all dependencies
pip install -r requirements.txt
```
This will install:
- Flask (web framework)
- yfinance (market data)
- requests (API calls)
- python-dotenv (configuration)
- Flask-CORS (web security)

**Wait for installation to complete (2-3 minutes)**

## 🔧 Phase 3: Configuration

### Step 3.1: Create Environment File
```bash
# Copy the template
copy .env.template .env
```

### Step 3.2: Get Yoco API Keys
1. Go to https://developer.yoco.com/
2. **Sign up** for a free developer account
3. **Verify your email** address
4. **Login** to the developer dashboard
5. Navigate to **"API Keys"** section
6. Copy your **Test Secret Key** (starts with `sk_test_`)
7. Copy your **Test Public Key** (starts with `pk_test_`)

### Step 3.3: Configure API Keys
1. **Open Spyder:** In Anaconda Navigator, go to Home tab, select "siener-ai" environment, launch Spyder
2. **Open .env file:** File → Open → Navigate to your project folder → Select `.env`
3. **Edit the file:**
```
YOCO_SECRET_KEY=sk_test_your_actual_secret_key_here
YOCO_PUBLIC_KEY=pk_test_your_actual_public_key_here
FLASK_ENV=development
FLASK_DEBUG=True
APP_NAME=Siener AI
APP_VERSION=1.0.0
```
4. **Save the file:** Ctrl+S

## 🎯 Phase 4: Launch Siener AI

### Step 4.1: Run the Application
In your terminal (or Spyder console):
```bash
python app.py
```

You should see:
```
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://[your-ip]:5000
```

### Step 4.2: Access Your Platform
Open your web browser and go to:
- **Main Dashboard:** http://localhost:5000
- **Pricing Page:** http://localhost:5000/pricing
- **API Health:** http://localhost:5000/api/health

## 🎨 What You'll See

### Dashboard Features:
- **Market Overview:** ECM confidence, market direction, volatility
- **Support & Resistance:** Key price levels
- **Sector Performance:** Technology, Energy, Financials, Healthcare
- **AI Predictions:** Real-time market forecasts
- **Professional Design:** Blue gradient, glass-morphism cards

### Pricing Page:
- **Basic Plan:** R499/month
- **Professional Plan:** R999/month (Featured)
- **Enterprise Plan:** R2499/month

## 🔍 Testing Your System

### Test 1: Market Data
1. Go to http://localhost:5000/api/market-data
2. You should see real JSE stock prices for:
   - Anglo American (AGL.JO)
   - FirstRand (FSR.JO)  
   - Naspers (NPN.JO)
   - Standard Bank (SBK.JO)
   - Shoprite (SHP.JO)

### Test 2: Payment Plans
1. Go to http://localhost:5000/api/plans
2. You should see all 3 subscription plans with features

### Test 3: System Health
1. Go to http://localhost:5000/api/health
2. You should see: `"status": "healthy"`

## 🚨 Troubleshooting

### Problem: "Module not found" error
**Solution:** Make sure you activated the siener-ai environment
```bash
conda activate siener-ai
pip install -r requirements.txt
```

### Problem: "Port 5000 already in use"
**Solution:** Kill existing processes
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID [process_id] /F

# Mac/Linux  
lsof -ti:5000 | xargs kill -9
```

### Problem: No market data showing
**Solution:** Check internet connection and try again in a few minutes

### Problem: Yoco payments not working
**Solution:** Verify your API keys in the .env file are correct

## 💰 Revenue Generation

### Getting Your First Customer:
1. **Share your local URL** with friends/family for testing
2. **Deploy to a VPS** for public access (DigitalOcean, Linode)
3. **Market on social media** - LinkedIn, Twitter, Facebook groups
4. **Target JSE traders** - They need this exact data

### Expected Timeline:
- **Week 1:** System running locally, testing complete
- **Week 2:** Deploy to VPS, get domain name
- **Week 3:** First marketing campaigns, beta users
- **Week 4:** First paying customers

### Scaling Strategy:
- **Month 1:** 10 customers × R750 avg = R7,500/month
- **Month 3:** 30 customers × R750 avg = R22,500/month  
- **Month 6:** 100 customers × R750 avg = R75,000/month

## 🎯 Next Steps

1. **Test everything locally** using this guide
2. **Customize branding** and pricing if needed
3. **Deploy to production** hosting
4. **Start marketing** to JSE traders
5. **Scale and optimize** based on customer feedback

---

**🎉 You now have a complete, professional trading platform running on your own computer!**

**This system provides real value that South African traders will pay R499-R2499/month for.**
