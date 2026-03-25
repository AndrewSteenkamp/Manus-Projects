#!/usr/bin/env python3
"""
Deployment Script for Siener AI Autonomous System
Automatically deploys and configures the entire autonomous business system
"""

import os
import sys
import subprocess
import json
import shutil
import time
from pathlib import Path
import argparse

class SienerAIDeployer:
    """Automated deployment system for Siener AI"""
    
    def __init__(self, deployment_path="/opt/siener-ai"):
        self.deployment_path = Path(deployment_path)
        self.current_path = Path(__file__).parent
        self.config = {}
        
    def deploy(self, environment="production"):
        """Deploy the complete Siener AI autonomous system"""
        print("🚀 Starting Siener AI Autonomous System Deployment...")
        
        try:
            # Step 1: System preparation
            self.prepare_system()
            
            # Step 2: Install dependencies
            self.install_dependencies()
            
            # Step 3: Setup directory structure
            self.setup_directories()
            
            # Step 4: Copy application files
            self.copy_application_files()
            
            # Step 5: Configure environment
            self.configure_environment(environment)
            
            # Step 6: Setup database
            self.setup_database()
            
            # Step 7: Configure services
            self.configure_services()
            
            # Step 8: Setup monitoring
            self.setup_monitoring()
            
            # Step 9: Start services
            self.start_services()
            
            # Step 10: Verify deployment
            self.verify_deployment()
            
            print("✅ Siener AI Autonomous System deployed successfully!")
            self.print_deployment_summary()
            
        except Exception as e:
            print(f"❌ Deployment failed: {str(e)}")
            self.cleanup_failed_deployment()
            sys.exit(1)
            
    def prepare_system(self):
        """Prepare the system for deployment"""
        print("📋 Preparing system...")
        
        # Update system packages
        subprocess.run(['sudo', 'apt', 'update'], check=True)
        subprocess.run(['sudo', 'apt', 'upgrade', '-y'], check=True)
        
        # Install system dependencies
        system_packages = [
            'python3', 'python3-pip', 'python3-venv',
            'nodejs', 'npm', 'nginx', 'sqlite3',
            'supervisor', 'htop', 'curl', 'wget',
            'git', 'unzip', 'certbot'
        ]
        
        subprocess.run(['sudo', 'apt', 'install', '-y'] + system_packages, check=True)
        
        # Install PM2 globally
        subprocess.run(['sudo', 'npm', 'install', '-g', 'pm2'], check=True)
        
        print("✅ System preparation completed")
        
    def install_dependencies(self):
        """Install Python dependencies"""
        print("📦 Installing Python dependencies...")
        
        # Create virtual environment
        venv_path = self.deployment_path / "venv"
        subprocess.run([
            'python3', '-m', 'venv', str(venv_path)
        ], check=True)
        
        # Install requirements
        pip_path = venv_path / "bin" / "pip"
        requirements = [
            'fastapi', 'uvicorn', 'flask', 'flask-cors',
            'requests', 'pandas', 'numpy', 'sqlite3',
            'openai', 'yfinance', 'psutil', 'schedule',
            'asyncio', 'aiohttp', 'python-multipart',
            'jinja2', 'python-dotenv', 'cryptography',
            'bcrypt', 'jwt', 'stripe', 'sendgrid',
            'celery', 'redis', 'docker', 'gitpython'
        ]
        
        for package in requirements:
            subprocess.run([str(pip_path), 'install', package], check=True)
            
        print("✅ Dependencies installed")
        
    def setup_directories(self):
        """Setup directory structure"""
        print("📁 Setting up directories...")
        
        directories = [
            self.deployment_path,
            self.deployment_path / "agents",
            self.deployment_path / "core",
            self.deployment_path / "config",
            self.deployment_path / "logs",
            self.deployment_path / "data",
            self.deployment_path / "backups",
            self.deployment_path / "static",
            self.deployment_path / "templates",
            "/var/log/siener-ai",
            "/var/lib/siener-ai",
            "/etc/siener-ai"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            
        # Set permissions
        subprocess.run(['sudo', 'chown', '-R', f'{os.getenv("USER")}:www-data', str(self.deployment_path)], check=True)
        subprocess.run(['sudo', 'chmod', '-R', '755', str(self.deployment_path)], check=True)
        
        print("✅ Directory structure created")
        
    def copy_application_files(self):
        """Copy application files to deployment directory"""
        print("📋 Copying application files...")
        
        # Copy core files
        source_files = [
            'main_orchestrator.py',
            'core/',
            'agents/',
        ]
        
        for file_path in source_files:
            source = self.current_path / file_path
            if source.is_file():
                shutil.copy2(source, self.deployment_path)
            elif source.is_dir():
                dest = self.deployment_path / file_path
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(source, dest)
                
        # Copy configuration templates
        self.create_configuration_files()
        
        print("✅ Application files copied")
        
    def create_configuration_files(self):
        """Create configuration files"""
        print("⚙️ Creating configuration files...")
        
        # Environment configuration
        env_config = """
# Siener AI Environment Configuration
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///var/lib/siener-ai/siener_ai.db

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key
OPENAI_API_BASE=https://api.openai.com/v1

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
DIRECTOR_EMAIL=director@siener-ai.com

# Stripe Configuration
STRIPE_PUBLISHABLE_KEY=pk_test_your-key
STRIPE_SECRET_KEY=sk_test_your-key
STRIPE_WEBHOOK_SECRET=whsec_your-webhook-secret

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Security Configuration
JWT_SECRET_KEY=your-jwt-secret-key
BCRYPT_LOG_ROUNDS=12

# Business Configuration
COMPANY_NAME=Siener AI
COMPANY_EMAIL=info@siener-ai.com
COMPANY_PHONE=+27-xxx-xxx-xxxx
COMPANY_ADDRESS=Your Address, South Africa
"""
        
        with open(self.deployment_path / "config" / ".env", "w") as f:
            f.write(env_config)
            
        # PM2 ecosystem configuration
        pm2_config = {
            "apps": [
                {
                    "name": "siener-ai-orchestrator",
                    "script": str(self.deployment_path / "main_orchestrator.py"),
                    "interpreter": str(self.deployment_path / "venv" / "bin" / "python"),
                    "cwd": str(self.deployment_path),
                    "instances": 1,
                    "exec_mode": "fork",
                    "watch": False,
                    "max_memory_restart": "1G",
                    "env": {
                        "NODE_ENV": "production",
                        "PYTHONPATH": str(self.deployment_path)
                    },
                    "log_file": "/var/log/siener-ai/orchestrator.log",
                    "out_file": "/var/log/siener-ai/orchestrator-out.log",
                    "error_file": "/var/log/siener-ai/orchestrator-error.log",
                    "log_date_format": "YYYY-MM-DD HH:mm:ss Z"
                }
            ]
        }
        
        with open(self.deployment_path / "config" / "ecosystem.config.json", "w") as f:
            json.dump(pm2_config, f, indent=2)
            
        # Nginx configuration
        nginx_config = f"""
server {{
    listen 80;
    server_name siener-ai.local localhost;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}}

server {{
    listen 443 ssl http2;
    server_name siener-ai.local localhost;
    
    # SSL Configuration (self-signed for local development)
    ssl_certificate /etc/ssl/certs/siener-ai.crt;
    ssl_certificate_key /etc/ssl/private/siener-ai.key;
    
    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Static files
    location /static/ {{
        alias {self.deployment_path}/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }}
    
    # API endpoints
    location /api/ {{
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
    
    # Main application
    location / {{
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }}
}}
"""
        
        with open("/tmp/siener-ai-nginx.conf", "w") as f:
            f.write(nginx_config)
            
        print("✅ Configuration files created")
        
    def configure_environment(self, environment):
        """Configure environment-specific settings"""
        print(f"🔧 Configuring {environment} environment...")
        
        if environment == "production":
            # Production-specific configurations
            self.configure_ssl_certificates()
            self.configure_firewall()
            self.configure_log_rotation()
            
        elif environment == "development":
            # Development-specific configurations
            self.create_self_signed_certificates()
            
        print(f"✅ {environment.title()} environment configured")
        
    def configure_ssl_certificates(self):
        """Configure SSL certificates for production"""
        print("🔒 Configuring SSL certificates...")
        
        # This would typically use Let's Encrypt
        # For now, create self-signed certificates
        self.create_self_signed_certificates()
        
    def create_self_signed_certificates(self):
        """Create self-signed SSL certificates"""
        subprocess.run([
            'sudo', 'openssl', 'req', '-x509', '-nodes', '-days', '365',
            '-newkey', 'rsa:2048',
            '-keyout', '/etc/ssl/private/siener-ai.key',
            '-out', '/etc/ssl/certs/siener-ai.crt',
            '-subj', '/C=ZA/ST=Gauteng/L=Johannesburg/O=Siener AI/CN=siener-ai.local'
        ], check=True)
        
    def configure_firewall(self):
        """Configure firewall rules"""
        print("🛡️ Configuring firewall...")
        
        # Enable UFW
        subprocess.run(['sudo', 'ufw', 'enable'], check=True)
        
        # Allow necessary ports
        ports = ['22', '80', '443', '3000', '5000']
        for port in ports:
            subprocess.run(['sudo', 'ufw', 'allow', port], check=True)
            
    def configure_log_rotation(self):
        """Configure log rotation"""
        logrotate_config = """
/var/log/siener-ai/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 ubuntu ubuntu
    postrotate
        pm2 reload siener-ai-orchestrator
    endscript
}
"""
        
        with open("/tmp/siener-ai-logrotate", "w") as f:
            f.write(logrotate_config)
            
        subprocess.run(['sudo', 'mv', '/tmp/siener-ai-logrotate', '/etc/logrotate.d/siener-ai'], check=True)
        
    def setup_database(self):
        """Setup database"""
        print("🗄️ Setting up database...")
        
        db_path = "/var/lib/siener-ai/siener_ai.db"
        
        # Create database schema
        schema_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            subscription_tier TEXT DEFAULT 'free',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        );
        
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER REFERENCES users(id),
            tier TEXT NOT NULL,
            status TEXT DEFAULT 'active',
            stripe_subscription_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER REFERENCES users(id),
            event_type TEXT NOT NULL,
            event_data TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS market_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            data TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        subprocess.run(['sqlite3', db_path, schema_sql], check=True)
        subprocess.run(['sudo', 'chown', 'ubuntu:www-data', db_path], check=True)
        subprocess.run(['sudo', 'chmod', '664', db_path], check=True)
        
        print("✅ Database setup completed")
        
    def configure_services(self):
        """Configure system services"""
        print("⚙️ Configuring services...")
        
        # Configure Nginx
        subprocess.run(['sudo', 'cp', '/tmp/siener-ai-nginx.conf', '/etc/nginx/sites-available/siener-ai'], check=True)
        subprocess.run(['sudo', 'ln', '-sf', '/etc/nginx/sites-available/siener-ai', '/etc/nginx/sites-enabled/'], check=True)
        subprocess.run(['sudo', 'nginx', '-t'], check=True)
        subprocess.run(['sudo', 'systemctl', 'reload', 'nginx'], check=True)
        
        # Configure PM2
        pm2_config_path = self.deployment_path / "config" / "ecosystem.config.json"
        subprocess.run(['pm2', 'delete', 'all'], check=False)  # Don't fail if no processes
        subprocess.run(['pm2', 'start', str(pm2_config_path)], check=True)
        subprocess.run(['pm2', 'save'], check=True)
        subprocess.run(['pm2', 'startup'], check=True)
        
        print("✅ Services configured")
        
    def setup_monitoring(self):
        """Setup monitoring and alerting"""
        print("📊 Setting up monitoring...")
        
        # Create monitoring script
        monitoring_script = f"""#!/bin/bash
# Siener AI Monitoring Script

LOG_FILE="/var/log/siener-ai/monitoring.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$DATE] Starting monitoring check..." >> $LOG_FILE

# Check if orchestrator is running
if pm2 list | grep -q "siener-ai-orchestrator.*online"; then
    echo "[$DATE] Orchestrator: RUNNING" >> $LOG_FILE
else
    echo "[$DATE] Orchestrator: STOPPED - Restarting..." >> $LOG_FILE
    pm2 restart siener-ai-orchestrator
fi

# Check disk space
DISK_USAGE=$(df / | awk 'NR==2 {{print $5}}' | sed 's/%//')
if [ $DISK_USAGE -gt 90 ]; then
    echo "[$DATE] WARNING: Disk usage is $DISK_USAGE%" >> $LOG_FILE
fi

# Check memory usage
MEMORY_USAGE=$(free | awk 'NR==2{{printf "%.0f", $3*100/$2}}')
if [ $MEMORY_USAGE -gt 90 ]; then
    echo "[$DATE] WARNING: Memory usage is $MEMORY_USAGE%" >> $LOG_FILE
fi

echo "[$DATE] Monitoring check completed" >> $LOG_FILE
"""
        
        with open(self.deployment_path / "monitoring.sh", "w") as f:
            f.write(monitoring_script)
            
        subprocess.run(['chmod', '+x', str(self.deployment_path / "monitoring.sh")], check=True)
        
        # Add to crontab
        cron_job = f"*/5 * * * * {self.deployment_path}/monitoring.sh\n"
        subprocess.run(['crontab', '-l'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        
        # Add monitoring cron job
        current_crontab = subprocess.run(['crontab', '-l'], capture_output=True, text=True, stderr=subprocess.DEVNULL)
        new_crontab = current_crontab.stdout + cron_job
        
        process = subprocess.Popen(['crontab', '-'], stdin=subprocess.PIPE, text=True)
        process.communicate(input=new_crontab)
        
        print("✅ Monitoring setup completed")
        
    def start_services(self):
        """Start all services"""
        print("🚀 Starting services...")
        
        # Start PM2 processes
        subprocess.run(['pm2', 'start', str(self.deployment_path / "config" / "ecosystem.config.json")], check=True)
        
        # Restart Nginx
        subprocess.run(['sudo', 'systemctl', 'restart', 'nginx'], check=True)
        
        # Wait for services to start
        time.sleep(10)
        
        print("✅ Services started")
        
    def verify_deployment(self):
        """Verify deployment is working"""
        print("🔍 Verifying deployment...")
        
        # Check PM2 status
        result = subprocess.run(['pm2', 'list'], capture_output=True, text=True)
        if 'siener-ai-orchestrator' not in result.stdout:
            raise Exception("Orchestrator not running in PM2")
            
        # Check if orchestrator is responding
        time.sleep(5)  # Give it time to start
        
        # Check log files
        log_files = [
            "/var/log/siener-ai/orchestrator.log",
            "/var/log/siener-ai/orchestrator-out.log"
        ]
        
        for log_file in log_files:
            if not os.path.exists(log_file):
                print(f"⚠️ Warning: Log file {log_file} not found")
                
        print("✅ Deployment verification completed")
        
    def print_deployment_summary(self):
        """Print deployment summary"""
        print("\n" + "="*60)
        print("🎉 SIENER AI AUTONOMOUS SYSTEM DEPLOYMENT COMPLETE!")
        print("="*60)
        print(f"📁 Installation Path: {self.deployment_path}")
        print(f"🌐 Web Interface: https://localhost")
        print(f"📊 Admin Dashboard: https://localhost/admin")
        print(f"🔧 Configuration: {self.deployment_path}/config/")
        print(f"📋 Logs: /var/log/siener-ai/")
        print(f"🗄️ Database: /var/lib/siener-ai/siener_ai.db")
        print("\n📋 NEXT STEPS:")
        print("1. Update configuration files with your API keys:")
        print(f"   - Edit {self.deployment_path}/config/.env")
        print("2. Configure your domain name in Nginx")
        print("3. Set up SSL certificates for production")
        print("4. Configure email settings for notifications")
        print("5. Set up Stripe for payment processing")
        print("\n🔧 MANAGEMENT COMMANDS:")
        print("- View status: pm2 status")
        print("- View logs: pm2 logs siener-ai-orchestrator")
        print("- Restart: pm2 restart siener-ai-orchestrator")
        print("- Stop: pm2 stop siener-ai-orchestrator")
        print("\n🎯 Your autonomous business system is now running!")
        print("="*60)
        
    def cleanup_failed_deployment(self):
        """Cleanup after failed deployment"""
        print("🧹 Cleaning up failed deployment...")
        
        try:
            # Stop PM2 processes
            subprocess.run(['pm2', 'delete', 'all'], check=False)
            
            # Remove deployment directory
            if self.deployment_path.exists():
                shutil.rmtree(self.deployment_path)
                
            # Remove Nginx configuration
            subprocess.run(['sudo', 'rm', '-f', '/etc/nginx/sites-enabled/siener-ai'], check=False)
            subprocess.run(['sudo', 'rm', '-f', '/etc/nginx/sites-available/siener-ai'], check=False)
            
        except Exception as e:
            print(f"Cleanup error: {str(e)}")

def main():
    """Main deployment function"""
    parser = argparse.ArgumentParser(description="Deploy Siener AI Autonomous System")
    parser.add_argument("--environment", choices=["development", "production"], 
                       default="development", help="Deployment environment")
    parser.add_argument("--path", default="/opt/siener-ai", 
                       help="Deployment path")
    
    args = parser.parse_args()
    
    deployer = SienerAIDeployer(args.path)
    deployer.deploy(args.environment)

if __name__ == "__main__":
    main()

