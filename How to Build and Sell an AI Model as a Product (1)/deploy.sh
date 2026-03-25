#!/bin/bash

# Siener AI - Automated Deployment Script
# Version: 2.1.0
# Date: August 21, 2025

set -e  # Exit on any error

echo "🔮 SIENER AI - Automated Deployment Script"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root"
   exit 1
fi

# Get domain name
read -p "Enter your domain name (e.g., sienerai.com): " DOMAIN_NAME
if [[ -z "$DOMAIN_NAME" ]]; then
    print_error "Domain name is required"
    exit 1
fi

# Get email for SSL certificate
read -p "Enter your email for SSL certificate: " SSL_EMAIL
if [[ -z "$SSL_EMAIL" ]]; then
    print_error "Email is required for SSL certificate"
    exit 1
fi

print_status "Starting Siener AI deployment for domain: $DOMAIN_NAME"
echo ""

# Update system
print_status "Updating system packages..."
sudo apt update && sudo apt upgrade -y
print_success "System updated successfully"

# Install dependencies
print_status "Installing system dependencies..."
sudo apt install -y python3.11 python3.11-venv python3-pip nodejs npm nginx certbot python3-certbot-nginx ufw git curl wget
print_success "System dependencies installed"

# Install pnpm
print_status "Installing pnpm..."
sudo npm install -g pnpm
print_success "pnpm installed"

# Setup firewall
print_status "Configuring firewall..."
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw --force enable
print_success "Firewall configured"

# Create application directory
APP_DIR="/var/www/siener-ai"
print_status "Creating application directory: $APP_DIR"
sudo mkdir -p $APP_DIR
sudo chown $USER:$USER $APP_DIR
print_success "Application directory created"

# Copy application files
print_status "Copying application files..."
cp -r backend $APP_DIR/
cp -r frontend $APP_DIR/
cp -r marketing-site $APP_DIR/
cp -r admin-dashboard $APP_DIR/
cp -r documentation $APP_DIR/
cp -r modules $APP_DIR/
print_success "Application files copied"

# Setup Python backend
print_status "Setting up Python backend..."
cd $APP_DIR/backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
print_success "Python backend setup complete"

# Build React frontend
print_status "Building React frontend..."
cd $APP_DIR/frontend
pnpm install
pnpm run build
cp -r dist/* $APP_DIR/backend/src/static/
print_success "React frontend built and deployed"

# Build marketing site
print_status "Building marketing site..."
cd $APP_DIR/marketing-site
pnpm install
pnpm run build
print_success "Marketing site built"

# Build admin dashboard
print_status "Building admin dashboard..."
cd $APP_DIR/admin-dashboard
pnpm install
pnpm run build
print_success "Admin dashboard built"

# Create environment file
print_status "Creating environment configuration..."
cd $APP_DIR/backend
cat > .env << EOF
# Flask Configuration
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
FLASK_ENV=production
FLASK_DEBUG=False

# Database Configuration
DATABASE_URL=sqlite:///siener_ai.db

# Stripe Configuration (UPDATE THESE WITH YOUR KEYS)
STRIPE_PUBLISHABLE_KEY=pk_test_your_key_here
STRIPE_SECRET_KEY=sk_test_your_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here

# Email Configuration (UPDATE THESE)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Security
CORS_ORIGINS=https://$DOMAIN_NAME,https://www.$DOMAIN_NAME
ALLOWED_HOSTS=$DOMAIN_NAME,www.$DOMAIN_NAME

# Application Settings
APP_NAME=Siener AI
APP_URL=https://$DOMAIN_NAME
SUPPORT_EMAIL=support@$DOMAIN_NAME
EOF
print_success "Environment configuration created"

# Create Nginx configuration
print_status "Creating Nginx configuration..."
sudo tee /etc/nginx/sites-available/siener-ai > /dev/null << EOF
server {
    listen 80;
    server_name $DOMAIN_NAME www.$DOMAIN_NAME;
    
    # Redirect HTTP to HTTPS
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name $DOMAIN_NAME www.$DOMAIN_NAME;
    
    # SSL configuration (will be added by certbot)
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied expired no-cache no-store private must-revalidate auth;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/javascript;
    
    # Main application
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Static files
    location /static/ {
        alias $APP_DIR/backend/src/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # API endpoints
    location /api/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable site
sudo ln -sf /etc/nginx/sites-available/siener-ai /etc/nginx/sites-enabled/
sudo nginx -t
print_success "Nginx configuration created"

# Install PM2 for process management
print_status "Installing PM2 for process management..."
sudo npm install -g pm2
print_success "PM2 installed"

# Create PM2 ecosystem file
print_status "Creating PM2 configuration..."
cd $APP_DIR
cat > ecosystem.config.js << EOF
module.exports = {
  apps: [{
    name: 'siener-ai',
    cwd: '$APP_DIR/backend',
    script: 'src/main.py',
    interpreter: '$APP_DIR/backend/venv/bin/python',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    env: {
      FLASK_ENV: 'production'
    },
    error_file: '$APP_DIR/logs/err.log',
    out_file: '$APP_DIR/logs/out.log',
    log_file: '$APP_DIR/logs/combined.log',
    time: true
  }]
};
EOF

# Create logs directory
mkdir -p $APP_DIR/logs
print_success "PM2 configuration created"

# Start application with PM2
print_status "Starting Siener AI application..."
cd $APP_DIR
pm2 start ecosystem.config.js
pm2 save
pm2 startup | tail -1 | sudo bash
print_success "Application started with PM2"

# Restart Nginx
print_status "Restarting Nginx..."
sudo systemctl restart nginx
print_success "Nginx restarted"

# Setup SSL certificate
print_status "Setting up SSL certificate with Let's Encrypt..."
sudo certbot --nginx -d $DOMAIN_NAME -d www.$DOMAIN_NAME --email $SSL_EMAIL --agree-tos --non-interactive
print_success "SSL certificate installed"

# Create backup script
print_status "Creating backup script..."
sudo tee /usr/local/bin/siener-ai-backup.sh > /dev/null << 'EOF'
#!/bin/bash
BACKUP_DIR="/var/backups/siener-ai"
APP_DIR="/var/www/siener-ai"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup database
cp $APP_DIR/backend/instance/siener_ai.db $BACKUP_DIR/siener_ai_$DATE.db

# Backup configuration
cp $APP_DIR/backend/.env $BACKUP_DIR/env_$DATE.backup

# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.db" -mtime +7 -delete
find $BACKUP_DIR -name "*.backup" -mtime +7 -delete

echo "Backup completed: $DATE"
EOF

sudo chmod +x /usr/local/bin/siener-ai-backup.sh

# Setup daily backup cron job
print_status "Setting up daily backups..."
(crontab -l 2>/dev/null; echo "0 2 * * * /usr/local/bin/siener-ai-backup.sh") | crontab -
print_success "Daily backups configured"

# Create update script
print_status "Creating update script..."
sudo tee /usr/local/bin/siener-ai-update.sh > /dev/null << EOF
#!/bin/bash
APP_DIR="/var/www/siener-ai"

echo "Updating Siener AI..."

# Backup before update
/usr/local/bin/siener-ai-backup.sh

# Stop application
pm2 stop siener-ai

# Update dependencies
cd \$APP_DIR/backend
source venv/bin/activate
pip install -r requirements.txt --upgrade

# Restart application
pm2 start siener-ai

echo "Update completed"
EOF

sudo chmod +x /usr/local/bin/siener-ai-update.sh
print_success "Update script created"

# Final status check
print_status "Performing final status check..."
sleep 5

# Check if application is running
if pm2 list | grep -q "siener-ai.*online"; then
    print_success "✅ Siener AI application is running"
else
    print_error "❌ Application failed to start"
fi

# Check if Nginx is running
if sudo systemctl is-active --quiet nginx; then
    print_success "✅ Nginx is running"
else
    print_error "❌ Nginx is not running"
fi

# Check if SSL is working
if curl -s -I https://$DOMAIN_NAME | grep -q "200 OK"; then
    print_success "✅ SSL certificate is working"
else
    print_warning "⚠️  SSL certificate may need time to propagate"
fi

echo ""
echo "🎉 DEPLOYMENT COMPLETED SUCCESSFULLY!"
echo "=========================================="
echo ""
echo "📊 Your Siener AI application is now live at:"
echo "   🌐 Main Site: https://$DOMAIN_NAME"
echo "   🔧 Admin: https://$DOMAIN_NAME/admin"
echo "   📈 API Health: https://$DOMAIN_NAME/api/siener/health"
echo ""
echo "📋 Next Steps:"
echo "   1. Update Stripe API keys in: $APP_DIR/backend/.env"
echo "   2. Configure email settings in: $APP_DIR/backend/.env"
echo "   3. Test payment processing"
echo "   4. Setup monitoring and analytics"
echo "   5. Begin marketing and customer acquisition"
echo ""
echo "🛠️  Management Commands:"
echo "   📊 Check status: pm2 status"
echo "   📝 View logs: pm2 logs siener-ai"
echo "   🔄 Restart app: pm2 restart siener-ai"
echo "   💾 Backup: sudo /usr/local/bin/siener-ai-backup.sh"
echo "   🔄 Update: sudo /usr/local/bin/siener-ai-update.sh"
echo ""
echo "📚 Documentation available in: $APP_DIR/documentation/"
echo ""
echo "🚀 Your SaaS business is ready to launch!"
echo "   Follow the Autonomous Assistant Guide to start acquiring customers."
echo ""
print_success "Deployment completed successfully! 🎉"

