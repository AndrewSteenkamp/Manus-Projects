#!/bin/bash

# 🚀 Alpapies Quick Deployment Script
# Deploy your complete e-commerce empire in 5 minutes!

echo "🛡️ ALPAPIES QUICK DEPLOYMENT STARTING..."
echo "================================================"

# Check if we're in the right directory
if [ ! -f "README.md" ]; then
    echo "❌ Error: Please run this script from the alpapies-complete-project directory"
    exit 1
fi

echo "✅ Project directory confirmed"

# Check for required tools
echo "🔍 Checking requirements..."

# Check for Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js first:"
    echo "   https://nodejs.org/"
    exit 1
fi

echo "✅ Node.js found: $(node --version)"

# Check for npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm not found. Please install npm first"
    exit 1
fi

echo "✅ npm found: $(npm --version)"

# Navigate to frontend directory
cd frontend

echo "📦 Installing dependencies..."
npm install

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed successfully"

echo "🏗️ Building production version..."
npm run build

if [ $? -ne 0 ]; then
    echo "❌ Build failed"
    exit 1
fi

echo "✅ Build completed successfully"

# Check if Vercel CLI is available
if command -v vercel &> /dev/null; then
    echo "🚀 Deploying to Vercel..."
    vercel --prod --yes
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "🎉 DEPLOYMENT SUCCESSFUL!"
        echo "================================================"
        echo "✅ Your Alpapies website is now LIVE!"
        echo "✅ Check the URL provided by Vercel above"
        echo "✅ Your e-commerce empire is ready to start earning!"
        echo ""
        echo "📋 Next Steps:"
        echo "1. Add your products to the catalog"
        echo "2. Set up payment processing"
        echo "3. Connect with ZQ Dropshipping"
        echo "4. Start your AI agents"
        echo "5. Begin marketing campaigns"
        echo ""
        echo "💰 Ready to scale to $1M monthly revenue!"
        exit 0
    else
        echo "❌ Vercel deployment failed"
    fi
else
    echo "⚠️ Vercel CLI not found. Installing..."
    npm install -g vercel
    
    if [ $? -eq 0 ]; then
        echo "✅ Vercel CLI installed"
        echo "🚀 Deploying to Vercel..."
        vercel --prod --yes
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "🎉 DEPLOYMENT SUCCESSFUL!"
            echo "================================================"
            echo "✅ Your Alpapies website is now LIVE!"
            echo "✅ Check the URL provided by Vercel above"
            echo "✅ Your e-commerce empire is ready to start earning!"
            echo ""
            echo "📋 Next Steps:"
            echo "1. Add your products to the catalog"
            echo "2. Set up payment processing"
            echo "3. Connect with ZQ Dropshipping"
            echo "4. Start your AI agents"
            echo "5. Begin marketing campaigns"
            echo ""
            echo "💰 Ready to scale to $1M monthly revenue!"
            exit 0
        fi
    fi
fi

# Fallback: Local deployment
echo ""
echo "🏠 FALLBACK: Setting up local deployment..."
echo "================================================"

# Start local development server
echo "🚀 Starting local development server..."
echo "📱 Your website will be available at: http://localhost:3000"
echo ""
echo "🎯 To deploy to production later:"
echo "1. Install Vercel CLI: npm install -g vercel"
echo "2. Run: vercel --prod"
echo "3. Or upload the 'dist' folder to any web hosting service"
echo ""
echo "💡 Alternative deployment options:"
echo "- Netlify: Drag 'dist' folder to netlify.com"
echo "- GitHub Pages: Enable in repository settings"
echo "- Any web hosting: Upload 'dist' folder contents"
echo ""

npm run dev

echo ""
echo "🎊 ALPAPIES DEPLOYMENT COMPLETE!"
echo "Your e-commerce empire is ready to launch!"

