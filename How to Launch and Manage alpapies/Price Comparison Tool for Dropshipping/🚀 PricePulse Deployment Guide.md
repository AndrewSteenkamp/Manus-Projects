# 🚀 PricePulse Deployment Guide

## Quick Deploy (5 Minutes)

### **Step 1: Clone Repository**
```bash
git clone https://github.com/yourusername/PricePulse-Complete.git
cd PricePulse-Complete
```

### **Step 2: Set Up Affiliate IDs**
1. **Register for affiliate programs**:
   - Amazon Associates: https://affiliate-program.amazon.com/
   - eBay Partner Network: https://partnernetwork.ebay.com/
   - AliExpress: https://portals.aliexpress.com/

2. **Configure your IDs**:
```bash
cd backend
cp .env.example .env
# Edit .env with your affiliate IDs
```

### **Step 3: Deploy Backend**
```bash
# Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
heroku login
heroku create your-pricepulse-api

# Deploy
git subtree push --prefix backend heroku main

# Set environment variables
heroku config:set AMAZON_AFFILIATE_ID=your-amazon-id-20
heroku config:set EBAY_AFFILIATE_ID=your-ebay-id
# ... repeat for all affiliate IDs
```

### **Step 4: Deploy Frontend**
```bash
cd frontend

# Update API URL in src/App.jsx line 13
# Change to: const API_BASE_URL = 'https://your-pricepulse-api.herokuapp.com/api'

# Install dependencies and build
npm install
npm run build

# Deploy to Netlify
# 1. Go to https://netlify.com
# 2. Drag and drop the 'dist' folder
# 3. Your site is live!
```

### **Step 5: Test Everything**
```bash
# Test backend
curl https://your-pricepulse-api.herokuapp.com/api/health

# Test search
curl "https://your-pricepulse-api.herokuapp.com/api/smart-search?q=laptop&currency=USD&max_results=2"
```

## ✅ Success Checklist

- [ ] Backend deployed and responding
- [ ] Frontend deployed and accessible
- [ ] Search returns products from multiple platforms
- [ ] Affiliate links contain your IDs
- [ ] Currency conversion working
- [ ] Mobile responsive design

## 💰 Start Earning

Once deployed:
1. Share your site on social media
2. Submit to price comparison directories
3. Create product comparison blog posts
4. Set up Google Analytics
5. Monitor affiliate dashboards for earnings

**Expected Timeline**: Revenue within 30 days, $1000+/month within 3 months.

## 🆘 Need Help?

- Check the [troubleshooting guide](docs/TROUBLESHOOTING.md)
- Review [API documentation](docs/API.md)
- Open an issue on GitHub
