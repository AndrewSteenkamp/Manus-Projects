# 📦 PricePulse System Files Package

## 🎯 Complete File Structure for Download

### **Backend Files (Flask API)**
**Location**: `C:\PricePulse\backend\`

```
backend/
├── src/
│   ├── main.py                           # Main Flask application
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── products.py                   # Product search endpoints
│   │   ├── enhanced_search.py            # Enhanced search with costs
│   │   ├── smart_search.py               # AI-powered smart search
│   │   ├── currency.py                   # Currency conversion
│   │   ├── affiliate.py                  # Affiliate link management
│   │   └── marketplace.py                # Platform integrations
│   ├── services/
│   │   ├── __init__.py
│   │   ├── enhanced_price_collector.py   # Real-time price collection
│   │   ├── smart_comparison_engine.py    # AI product matching
│   │   ├── currency_service.py           # Primary currency service
│   │   ├── fallback_currency_service.py  # Backup currency system
│   │   ├── cost_calculator.py            # Total cost calculations
│   │   ├── affiliate_manager.py          # Revenue management
│   │   ├── data_collector.py             # Basic data collection
│   │   ├── real_price_collector.py       # Real-time price scraping
│   │   └── marketplace_integrations.py   # Platform API integrations
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                       # User data models
│   │   └── product.py                    # Product data models
│   └── database/
│       └── app.db                        # SQLite database
├── requirements.txt                      # Python dependencies
├── .env                                  # Environment variables (create this)
├── Procfile                              # Heroku deployment config
├── runtime.txt                           # Python version for Heroku
└── README.md                             # Setup instructions
```

### **Frontend Files (React Application)**
**Location**: `C:\PricePulse\frontend\`

```
frontend/
├── public/
│   ├── index.html                        # Main HTML file
│   ├── favicon.ico                       # Website icon
│   └── manifest.json                     # PWA manifest
├── src/
│   ├── components/
│   │   └── ui/                           # UI components (shadcn/ui)
│   │       ├── button.jsx
│   │       ├── input.jsx
│   │       ├── card.jsx
│   │       ├── badge.jsx
│   │       ├── select.jsx
│   │       ├── tabs.jsx
│   │       ├── progress.jsx
│   │       └── separator.jsx
│   ├── App.jsx                           # Main React component
│   ├── App.css                           # Styling with Tailwind CSS
│   ├── index.css                         # Global styles
│   └── main.jsx                          # React entry point
├── package.json                          # Node.js dependencies
├── package-lock.json                     # Dependency lock file
├── vite.config.js                        # Vite build configuration
├── tailwind.config.js                    # Tailwind CSS config
├── components.json                       # shadcn/ui config
└── README.md                             # Frontend setup instructions
```

---

## 📋 File Contents for Manual Creation

### **1. requirements.txt** (Backend)
```txt
Flask==2.3.3
Flask-CORS==4.0.0
Flask-SQLAlchemy==3.0.5
requests==2.31.0
beautifulsoup4==4.12.2
pandas==2.0.3
numpy==1.24.3
python-dotenv==1.0.0
lxml==4.9.3
selenium==4.11.2
```

### **2. .env** (Backend - Create and customize)
```env
# Affiliate Configuration - REPLACE WITH YOUR IDs
AMAZON_AFFILIATE_ID=YOUR_AMAZON_ID-20
EBAY_AFFILIATE_ID=YOUR_EBAY_CAMPAIGN_ID
ALIEXPRESS_AFFILIATE_ID=YOUR_ALIEXPRESS_ID
WALMART_AFFILIATE_ID=YOUR_WALMART_ID
BESTBUY_AFFILIATE_ID=YOUR_BESTBUY_ID
TEMU_AFFILIATE_ID=YOUR_TEMU_ID

# Database Configuration
DATABASE_URL=sqlite:///database/app.db

# Flask Configuration
FLASK_ENV=production
SECRET_KEY=change-this-to-a-random-secret-key
FLASK_DEBUG=False

# API Keys (Optional - for enhanced features)
EXCHANGE_RATE_API_KEY=your_exchange_rate_api_key
GOOGLE_ANALYTICS_ID=your_google_analytics_id
```

### **3. Procfile** (Backend - for Heroku deployment)
```
web: python src/main.py
```

### **4. runtime.txt** (Backend - for Heroku)
```
python-3.11.0
```

### **5. package.json** (Frontend)
```json
{
  "name": "pricepulse-frontend",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "lucide-react": "^0.263.1",
    "@radix-ui/react-select": "^1.2.2",
    "@radix-ui/react-tabs": "^1.0.4",
    "@radix-ui/react-progress": "^1.0.3",
    "@radix-ui/react-separator": "^1.0.3",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.0.0",
    "tailwind-merge": "^1.14.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.15",
    "@types/react-dom": "^18.2.7",
    "@vitejs/plugin-react": "^4.0.3",
    "autoprefixer": "^10.4.14",
    "postcss": "^8.4.27",
    "tailwindcss": "^3.3.3",
    "vite": "^4.4.5"
  }
}
```

---

## 🔧 Configuration Files to Customize

### **Critical File: affiliate_manager.py**
**Location**: `backend/src/services/affiliate_manager.py`

**MUST UPDATE with your affiliate IDs**:

```python
# Line 15-50 approximately - UPDATE THESE VALUES
AFFILIATE_PROGRAMS = {
    'Amazon': {
        'affiliate_id': 'YOUR_AMAZON_ID-20',  # ← CHANGE THIS
        'commission_rate': 0.05,
        'base_url': 'https://amazon.com',
        'link_format': '{product_url}?tag={affiliate_id}&linkCode=as2'
    },
    'eBay': {
        'affiliate_id': 'YOUR_EBAY_CAMPAIGN_ID',  # ← CHANGE THIS
        'commission_rate': 0.03,
        'base_url': 'https://ebay.com',
        'link_format': '{product_url}&campid={affiliate_id}'
    },
    'AliExpress': {
        'affiliate_id': 'YOUR_ALIEXPRESS_ID',  # ← CHANGE THIS
        'commission_rate': 0.06,
        'base_url': 'https://aliexpress.com',
        'link_format': '{product_url}?aff_trace_key={affiliate_id}'
    },
    'Walmart': {
        'affiliate_id': 'YOUR_WALMART_ID',  # ← CHANGE THIS
        'commission_rate': 0.03,
        'base_url': 'https://walmart.com',
        'link_format': '{product_url}?u1={affiliate_id}'
    },
    'Best Buy': {
        'affiliate_id': 'YOUR_BESTBUY_ID',  # ← CHANGE THIS
        'commission_rate': 0.02,
        'base_url': 'https://bestbuy.com',
        'link_format': '{product_url}?ref={affiliate_id}'
    },
    'Temu': {
        'affiliate_id': 'YOUR_TEMU_ID',  # ← CHANGE THIS
        'commission_rate': 0.05,
        'base_url': 'https://temu.com',
        'link_format': '{product_url}?_bg_fs=1&sharechannel={affiliate_id}'
    }
}
```

### **Frontend API Configuration**
**Location**: `frontend/src/App.jsx`

**Line 13 - UPDATE after backend deployment**:
```javascript
// CHANGE THIS to your deployed backend URL
const API_BASE_URL = 'https://your-heroku-app.herokuapp.com/api'
```

---

## 🚀 Deployment Configuration Files

### **For Heroku Deployment**

**1. Create Heroku app.json** (Backend):
```json
{
  "name": "PricePulse API",
  "description": "Global price comparison platform API",
  "repository": "https://github.com/yourusername/pricepulse-backend",
  "keywords": ["python", "flask", "price-comparison", "affiliate"],
  "env": {
    "FLASK_ENV": {
      "description": "Flask environment",
      "value": "production"
    },
    "SECRET_KEY": {
      "description": "Secret key for Flask sessions",
      "generator": "secret"
    }
  },
  "buildpacks": [
    {
      "url": "heroku/python"
    }
  ]
}
```

### **For Netlify Deployment**

**1. Create _redirects file** (Frontend public folder):
```
/*    /index.html   200
```

**2. Create netlify.toml** (Frontend root):
```toml
[build]
  publish = "dist"
  command = "npm run build"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

---

## 📦 Download Instructions

### **Method 1: Manual File Creation**
1. Create the folder structure as shown above
2. Copy each file content from the deployed system
3. Customize affiliate IDs and configuration
4. Test locally before deployment

### **Method 2: Git Clone (If available)**
```bash
# Backend
git clone https://github.com/yourusername/pricepulse-backend.git
cd pricepulse-backend

# Frontend  
git clone https://github.com/yourusername/pricepulse-frontend.git
cd pricepulse-frontend
```

### **Method 3: ZIP Download**
- Download complete system as ZIP file
- Extract to `C:\PricePulse\`
- Follow configuration steps

---

## ✅ Post-Download Checklist

### **Backend Setup**
- [ ] All files in `C:\PricePulse\backend\`
- [ ] Created `.env` file with your affiliate IDs
- [ ] Updated `affiliate_manager.py` with your IDs
- [ ] Installed Python dependencies
- [ ] Tested locally in Spyder

### **Frontend Setup**
- [ ] All files in `C:\PricePulse\frontend\`
- [ ] Updated API URL in `App.jsx`
- [ ] Installed Node.js dependencies
- [ ] Built for production
- [ ] Ready for deployment

### **Configuration Verification**
- [ ] Affiliate accounts created and approved
- [ ] Affiliate IDs correctly formatted
- [ ] Environment variables set
- [ ] Database initialized
- [ ] All dependencies installed

**Once all items are checked, you're ready to deploy and start earning revenue!**

---

*This package contains everything needed to deploy PricePulse. Simply download, configure your affiliate IDs, and deploy to start generating income from day one!*
