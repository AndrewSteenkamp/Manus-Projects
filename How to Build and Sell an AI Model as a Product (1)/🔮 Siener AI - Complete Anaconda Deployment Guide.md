# 🔮 Siener AI - Complete Anaconda Deployment Guide

**Deploy your autonomous AI business system using Anaconda and Spyder**

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start (5 Minutes)](#quick-start)
3. [Detailed Setup Instructions](#detailed-setup)
4. [Spyder Configuration](#spyder-configuration)
5. [Running the System](#running-the-system)
6. [Testing and Verification](#testing-verification)
7. [Production Deployment](#production-deployment)
8. [Troubleshooting](#troubleshooting)
9. [Maintenance and Updates](#maintenance)

---

## 🎯 Prerequisites

### Required Software
- **Anaconda** or **Miniconda** (latest version)
- **Python 3.11+** (included with Anaconda)
- **Git** (for cloning repository)
- **Web browser** (Chrome, Firefox, Safari, Edge)

### Required API Keys
- **OpenAI API Key** - Get from https://platform.openai.com/api-keys
- **Email Account** - Gmail with app password (for notifications)
- **Stripe Account** - For payment processing (optional for testing)

### System Requirements
- **RAM:** 4GB minimum, 8GB recommended
- **Storage:** 2GB free space
- **OS:** Windows 10+, macOS 10.14+, or Linux
- **Internet:** Stable connection required

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Download and Extract
```bash
# Download the Siener AI package (provided separately)
# Extract to your desired location, e.g., C:\SienerAI or ~/SienerAI
```

### Step 2: Open Anaconda Navigator
1. **Launch Anaconda Navigator**
2. **Click "Environments"** in the left sidebar
3. **Click "Create"** to create new environment

### Step 3: Create Environment
1. **Name:** `siener-ai`
2. **Python Version:** 3.11
3. **Click "Create"**

### Step 4: Install Dependencies
1. **Select** the `siener-ai` environment
2. **Click "Open Terminal"**
3. **Run:**
```bash
cd /path/to/siener-ai-complete
pip install -r requirements.txt
```

### Step 5: Configure Environment
1. **Copy** `config/.env.template` to `config/.env`
2. **Edit** `config/.env` with your API keys:
```bash
OPENAI_API_KEY=sk-your-openai-key-here
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-16-character-app-password
DIRECTOR_EMAIL=your-director-email@gmail.com
```

### Step 6: Launch System
```bash
python app.py
```

**🎉 Your Siener AI system is now running!**
- **Dashboard:** http://localhost:5000/dashboard
- **API:** http://localhost:5000/api/siener/health

---

## 📖 Detailed Setup Instructions

### Phase 1: Environment Preparation (10 minutes)

#### 1.1 Install Anaconda
If you don't have Anaconda installed:

**Windows:**
1. Download from https://www.anaconda.com/products/distribution
2. Run the installer as Administrator
3. Choose "Add Anaconda to PATH" during installation
4. Restart your computer

**macOS:**
1. Download from https://www.anaconda.com/products/distribution
2. Run the .pkg installer
3. Follow the installation wizard
4. Open Terminal and verify: `conda --version`

**Linux:**
```bash
wget https://repo.anaconda.com/archive/Anaconda3-2023.09-Linux-x86_64.sh
bash Anaconda3-2023.09-Linux-x86_64.sh
source ~/.bashrc
```

#### 1.2 Verify Installation
Open **Anaconda Prompt** (Windows) or **Terminal** (macOS/Linux):
```bash
conda --version
python --version
```
You should see conda 23.x+ and Python 3.11+

#### 1.3 Update Anaconda
```bash
conda update conda
conda update anaconda
```

### Phase 2: Project Setup (15 minutes)

#### 2.1 Create Project Directory
Choose your project location:
- **Windows:** `C:\SienerAI`
- **macOS:** `~/SienerAI`
- **Linux:** `~/SienerAI`

```bash
# Create directory
mkdir SienerAI
cd SienerAI

# Extract the Siener AI package here
# You should have: siener-ai-complete/ folder
```

#### 2.2 Create Conda Environment
```bash
# Create environment with Python 3.11
conda create -n siener-ai python=3.11 -y

# Activate environment
conda activate siener-ai

# Verify activation (you should see (siener-ai) in prompt)
which python  # Should show path with siener-ai
```

#### 2.3 Install Dependencies
```bash
# Navigate to project directory
cd siener-ai-complete

# Install Python packages
pip install -r requirements.txt

# Verify installation
pip list | grep flask
pip list | grep openai
```

### Phase 3: Configuration (10 minutes)

#### 3.1 Environment Variables
```bash
# Copy template
cp config/.env.template config/.env

# Edit the file (use your preferred editor)
nano config/.env  # Linux/macOS
notepad config/.env  # Windows
```

#### 3.2 Required Configuration
Edit `config/.env` with these values:

```bash
# OpenAI Configuration (REQUIRED)
OPENAI_API_KEY=sk-your-actual-openai-api-key-here

# Email Configuration (REQUIRED for reports)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-16-character-app-password
DIRECTOR_EMAIL=your-director-email@gmail.com

# Business Configuration
COMPANY_NAME=Your Company Name
COMPANY_EMAIL=info@yourcompany.com

# Development Settings
FLASK_ENV=development
FLASK_DEBUG=True
API_HOST=0.0.0.0
API_PORT=5000
```

#### 3.3 Get OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Sign in or create account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. Paste into `config/.env`

#### 3.4 Setup Gmail App Password
1. Enable 2-Factor Authentication on Gmail
2. Go to https://myaccount.google.com/apppasswords
3. Generate app password for "Mail"
4. Use this 16-character password in `config/.env`

### Phase 4: Database Initialization (5 minutes)

#### 4.1 Create Database
```bash
# Create data directory
mkdir -p data

# Initialize database
python scripts/setup_database.py
```

#### 4.2 Verify Database
```bash
# Check if database was created
ls -la data/
# You should see: siener_ai.db
```

---

## 🔧 Spyder Configuration

### Setting up Spyder for Development

#### 1. Launch Spyder
1. **Open Anaconda Navigator**
2. **Select** `siener-ai` environment
3. **Click "Install"** on Spyder if not installed
4. **Click "Launch"** Spyder

#### 2. Configure Working Directory
1. **In Spyder:** Go to **Tools → Preferences**
2. **Select "Working Directory"**
3. **Set to:** `/path/to/siener-ai-complete`
4. **Click "Apply"** and **"OK"**

#### 3. Set Python Interpreter
1. **Tools → Preferences → Python Interpreter**
2. **Select "Use the following Python interpreter"**
3. **Browse to:** `/path/to/anaconda3/envs/siener-ai/bin/python`
4. **Click "Apply"** and restart Spyder

#### 4. Configure Console
1. **Tools → Preferences → IPython Console**
2. **Graphics → Backend:** Qt5
3. **Startup → Run file:** Browse to `app.py`
4. **Click "Apply"**

#### 5. Project Setup in Spyder
1. **Projects → New Project**
2. **Name:** Siener AI
3. **Location:** Your project directory
4. **Create**

---

## 🏃‍♂️ Running the System

### Method 1: Using Spyder (Recommended for Development)

#### 1. Open Files in Spyder
1. **File → Open:** `app.py`
2. **File → Open:** `core/agent_orchestrator.py`
3. **File → Open:** `agents/marketing_agent.py`

#### 2. Run the System
1. **Click "Run"** button or press **F5**
2. **Select "Run in console"**
3. **Watch the console output**

You should see:
```
🔮 Starting Siener AI - Complete Autonomous Business System
====================================================
🤖 4 World-Class Agents:
   • Marketing Agent - Content creation & campaign management
   • Engineering Agent - System monitoring & optimization
   • Product Agent - Market analysis & predictions
   • Operations Agent - Business reporting & analytics
====================================================
🚀 Siener AI running on http://0.0.0.0:5000
```

#### 3. Access the System
- **Dashboard:** http://localhost:5000/dashboard
- **Admin Panel:** http://localhost:5000/admin
- **API Health:** http://localhost:5000/api/siener/health

### Method 2: Using Terminal/Command Prompt

#### 1. Activate Environment
```bash
conda activate siener-ai
cd /path/to/siener-ai-complete
```

#### 2. Run Application
```bash
python app.py
```

#### 3. Keep Running
The system will run continuously. Press **Ctrl+C** to stop.

### Method 3: Background Service (Production)

#### 1. Install Process Manager
```bash
pip install supervisor  # Linux/macOS
# or use Windows Service for Windows
```

#### 2. Create Service Configuration
Create `siener-ai.conf`:
```ini
[program:siener-ai]
command=/path/to/anaconda3/envs/siener-ai/bin/python app.py
directory=/path/to/siener-ai-complete
autostart=true
autorestart=true
user=your-username
```

#### 3. Start Service
```bash
supervisorctl start siener-ai
```

---

## ✅ Testing and Verification

### System Health Check

#### 1. Basic Health Check
Open browser and visit:
- http://localhost:5000/health
- Should return: `{"service": "Siener AI", "status": "healthy"}`

#### 2. API Health Check
- http://localhost:5000/api/siener/health
- Should show all available endpoints

#### 3. System Status
- http://localhost:5000/api/siener/system/status
- Should show all 4 agents as "active"

### Agent Testing

#### 1. Test Marketing Agent
```bash
curl -X POST http://localhost:5000/api/siener/marketing/content \
  -H "Content-Type: application/json" \
  -d '{"type": "social_media", "topic": "AI predictions"}'
```

#### 2. Test Product Agent
```bash
curl http://localhost:5000/api/siener/market/analysis?symbols=AAPL,MSFT
```

#### 3. Test Engineering Agent
```bash
curl http://localhost:5000/api/siener/system/monitor
```

#### 4. Test Operations Agent
```bash
curl http://localhost:5000/api/siener/reports/daily
```

### Performance Verification

#### 1. Check System Metrics
Visit: http://localhost:5000/api/siener/system/status

Look for:
- `"overall_health": "excellent"`
- All agents showing `"status": "active"`
- Task success rate > 90%

#### 2. Monitor Logs
In Spyder console or terminal, you should see:
```
INFO:marketing:Marketing Agent 2.1.0 initialized
INFO:engineering:Engineering Agent 2.1.0 initialized
INFO:product:Product Agent 2.1.0 initialized
INFO:operations:Operations Agent 2.1.0 initialized
INFO:orchestrator:Agent Orchestrator started successfully
```

#### 3. Test Business Functions
1. **Market Analysis:** Should return real market data
2. **Predictions:** Should generate AI-powered forecasts
3. **Reports:** Should create business intelligence reports
4. **Content:** Should generate marketing content

---

## 🌐 Production Deployment

### Option 1: Local Server Deployment

#### 1. Configure for Production
Edit `config/.env`:
```bash
FLASK_ENV=production
FLASK_DEBUG=False
API_HOST=0.0.0.0
API_PORT=80
```

#### 2. Install Production Server
```bash
pip install gunicorn  # Linux/macOS
pip install waitress  # Windows
```

#### 3. Run Production Server
```bash
# Linux/macOS
gunicorn -w 4 -b 0.0.0.0:80 app:app

# Windows
waitress-serve --host=0.0.0.0 --port=80 app:app
```

### Option 2: Cloud Deployment (DigitalOcean)

#### 1. Create Droplet
1. **Sign up** at DigitalOcean
2. **Create Droplet:** Ubuntu 22.04, 2GB RAM
3. **SSH** into server

#### 2. Setup Server
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Anaconda
wget https://repo.anaconda.com/archive/Anaconda3-2023.09-Linux-x86_64.sh
bash Anaconda3-2023.09-Linux-x86_64.sh
source ~/.bashrc

# Clone your project
git clone your-repository-url
cd siener-ai-complete
```

#### 3. Deploy Application
```bash
# Create environment
conda create -n siener-ai python=3.11 -y
conda activate siener-ai

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp config/.env.template config/.env
nano config/.env  # Add your API keys

# Setup database
python scripts/setup_database.py

# Install and configure Nginx
sudo apt install nginx -y
sudo nano /etc/nginx/sites-available/siener-ai
```

#### 4. Nginx Configuration
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### 5. Start Services
```bash
# Enable Nginx site
sudo ln -s /etc/nginx/sites-available/siener-ai /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Start Siener AI
nohup python app.py &
```

### Option 3: Heroku Deployment

#### 1. Prepare for Heroku
Create `Procfile`:
```
web: python app.py
```

Create `runtime.txt`:
```
python-3.11.6
```

#### 2. Deploy to Heroku
```bash
# Install Heroku CLI
# Create Heroku app
heroku create siener-ai-your-name

# Set environment variables
heroku config:set OPENAI_API_KEY=your-key
heroku config:set EMAIL_USERNAME=your-email
heroku config:set EMAIL_PASSWORD=your-password

# Deploy
git push heroku main
```

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Issue 1: "Module not found" errors
**Solution:**
```bash
# Ensure environment is activated
conda activate siener-ai

# Reinstall requirements
pip install -r requirements.txt --force-reinstall

# Check Python path in Spyder
import sys
print(sys.path)
```

#### Issue 2: OpenAI API errors
**Solution:**
```bash
# Verify API key
echo $OPENAI_API_KEY

# Test API key
python -c "import openai; openai.api_key='your-key'; print(openai.Model.list())"

# Check billing at https://platform.openai.com/account/billing
```

#### Issue 3: Port already in use
**Solution:**
```bash
# Find process using port 5000
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill process
kill -9 PID  # Replace PID with actual process ID

# Or use different port
export API_PORT=5001
```

#### Issue 4: Database errors
**Solution:**
```bash
# Remove and recreate database
rm data/siener_ai.db
python scripts/setup_database.py

# Check permissions
chmod 755 data/
chmod 644 data/siener_ai.db
```

#### Issue 5: Email sending fails
**Solution:**
```bash
# Verify Gmail settings
# 1. Enable 2FA on Gmail
# 2. Generate app password
# 3. Use app password, not regular password
# 4. Check SMTP settings in config/.env
```

#### Issue 6: Spyder won't start
**Solution:**
```bash
# Reset Spyder configuration
spyder --reset

# Reinstall Spyder
conda remove spyder
conda install spyder

# Check environment
conda info --envs
```

### Performance Issues

#### Issue: Slow response times
**Solutions:**
1. **Increase system resources**
2. **Optimize database queries**
3. **Enable caching**
4. **Use production WSGI server**

#### Issue: High memory usage
**Solutions:**
1. **Monitor agent performance**
2. **Implement memory limits**
3. **Regular garbage collection**
4. **Optimize data structures**

### Debugging Tips

#### 1. Enable Debug Mode
```bash
export FLASK_DEBUG=True
export LOG_LEVEL=DEBUG
```

#### 2. Check Logs
```bash
# View application logs
tail -f logs/siener_ai.log

# View system logs
journalctl -u siener-ai -f
```

#### 3. Test Individual Components
```python
# In Spyder console
from agents.marketing_agent import MarketingAgent
agent = MarketingAgent()
result = agent.create_social_media_content("test topic")
print(result)
```

---

## 🔄 Maintenance and Updates

### Daily Maintenance

#### 1. Check System Health
```bash
curl http://localhost:5000/api/siener/system/status
```

#### 2. Monitor Logs
```bash
tail -f logs/siener_ai.log
```

#### 3. Backup Database
```bash
cp data/siener_ai.db backups/siener_ai_$(date +%Y%m%d).db
```

### Weekly Maintenance

#### 1. Update Dependencies
```bash
conda activate siener-ai
pip list --outdated
pip install --upgrade package-name
```

#### 2. Clean Logs
```bash
find logs/ -name "*.log" -mtime +7 -delete
```

#### 3. Performance Review
1. Check system metrics
2. Review agent performance
3. Optimize slow queries
4. Update configurations

### Monthly Maintenance

#### 1. Full System Backup
```bash
tar -czf siener_ai_backup_$(date +%Y%m%d).tar.gz siener-ai-complete/
```

#### 2. Security Updates
```bash
conda update --all
pip install --upgrade pip
```

#### 3. Performance Optimization
1. Database optimization
2. Code profiling
3. Resource usage analysis
4. Capacity planning

### Updating Siener AI

#### 1. Backup Current System
```bash
cp -r siener-ai-complete siener-ai-complete-backup
```

#### 2. Download Updates
```bash
# Download new version
# Extract to temporary directory
# Compare configurations
```

#### 3. Apply Updates
```bash
# Stop current system
# Replace code files
# Update dependencies
# Migrate database if needed
# Restart system
```

---

## 📞 Support and Resources

### Getting Help

#### 1. Documentation
- **README.md** - Project overview
- **API Documentation** - Available at `/api/docs`
- **Agent Documentation** - In `agents/` directory

#### 2. Logs and Debugging
- **Application Logs:** `logs/siener_ai.log`
- **Error Logs:** `logs/error.log`
- **Debug Mode:** Set `FLASK_DEBUG=True`

#### 3. Community Support
- **GitHub Issues** - Report bugs and feature requests
- **Discord Community** - Real-time help and discussion
- **Email Support** - support@siener-ai.com

### Performance Monitoring

#### 1. Built-in Monitoring
- **System Status:** http://localhost:5000/api/siener/system/status
- **Agent Status:** http://localhost:5000/api/siener/agents/status
- **Health Check:** http://localhost:5000/health

#### 2. External Monitoring
- **Uptime monitoring** with Pingdom or UptimeRobot
- **Performance monitoring** with New Relic or DataDog
- **Log aggregation** with ELK stack or Splunk

### Scaling Your Business

#### 1. Growth Milestones
- **100 users:** Optimize for performance
- **500 users:** Implement caching and CDN
- **2000 users:** Scale to multiple servers
- **10000 users:** Implement microservices architecture

#### 2. Revenue Optimization
- **A/B test pricing** strategies
- **Implement upselling** features
- **Add enterprise** features
- **Expand to new** markets

---

## 🎉 Success Checklist

### ✅ Deployment Complete When:

- [ ] All 4 agents are running and active
- [ ] System health check returns "excellent"
- [ ] Market analysis returns real data
- [ ] Predictions are being generated
- [ ] Business reports are created
- [ ] Marketing content is generated
- [ ] Email notifications are working
- [ ] Dashboard is accessible
- [ ] API endpoints respond correctly
- [ ] Database is properly initialized
- [ ] Logs are being written
- [ ] Backups are configured
- [ ] Monitoring is active

### 🚀 Ready for Business When:

- [ ] Production environment configured
- [ ] SSL certificates installed
- [ ] Domain name configured
- [ ] Payment processing setup
- [ ] Customer onboarding flow tested
- [ ] Marketing campaigns launched
- [ ] Support system ready
- [ ] Analytics tracking active
- [ ] Legal compliance verified
- [ ] Team training completed

---

**🔮 Congratulations! Your Siener AI autonomous business system is now ready to generate revenue 24/7!**

*For additional support, visit our documentation or contact our support team.*

