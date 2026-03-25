# Alpapies E-Commerce Website TODO

## Database Schema & Backend
- [x] Design database schema for products (categories, variants, pricing)
- [x] Design database schema for shopping cart
- [x] Design database schema for orders and order items
- [x] Design database schema for suppliers and supplier products
- [x] Implement tRPC procedures for product listing and filtering
- [x] Implement tRPC procedures for cart management (add, update, remove)
- [x] Implement tRPC procedures for checkout and order creation
- [x] Implement tRPC procedures for product comparison
- [x] Implement admin procedures for product management
- [x] Implement admin procedures for order management
- [x] Implement admin procedures for supplier integration

## Frontend - Public Pages
- [x] Design homepage with hero section and featured products
- [x] Build product catalog page with filtering and search
- [x] Build individual product detail page
- [x] Build shopping cart page
- [x] Build checkout flow (shipping, payment info)
- [ ] Build order confirmation page
- [x] Build product comparison tool interface
- [ ] Build user account page (order history)

## Frontend - Admin Dashboard
- [x] Build admin dashboard layout with navigation- [x] Build product management interface (CRUD) edit, delete)
- [x] Build order management interface (view, update status)
- [x] Build supplier integration interface
- [ ] Build analytics dashboard (sales, orders, products)

## Payment Integration
- [x] Build flexible payment system supporting multiple processors
- [x] Add payments database table and schema
- [x] Create payment database helpers
- [x] Add tRPC payment procedures
- [ ] Implement Stripe payment processor
- [ ] Implement PayFast payment processor (South Africa)
- [ ] Implement Paystack payment processor
- [ ] Implement PayPal payment processor
- [ ] Add payment method selection in checkout
- [ ] Create payment webhook handlers for all processors
- [ ] Add payment confirmation and receipt generation
- [x] Write unit tests for payment procedures
- [ ] Test payment flow for each processor

## AI Agents & Automation
- [ ] Build AI Product Research Agent (1688.com integration)
- [ ] Build AI Viral Marketing Agent (content generation)
- [ ] Build AI Inventory Optimization Agent
- [ ] Create agent dashboard for monitoring
- [ ] Implement autonomous product sourcing from 1688.com
- [ ] Add automated marketing content generation
- [ ] Implement intelligent inventory management

## Enhanced Price Comparison
- [ ] Integrate real competitor price scraping (Amazon, eBay, AliExpress)
- [ ] Add exchange rate conversion for international pricing
- [ ] Calculate total landed cost (shipping, VAT, taxes)
- [ ] Display price comparison on product pages
- [ ] Add "Best Deal" badges based on comparison

## Customer Features
- [ ] Build order confirmation page with tracking
- [ ] Build user account page (order history, profile)
- [ ] Implement order tracking system
- [ ] Add email notifications for order status
- [ ] Implement abandoned cart recovery emails
- [ ] Add product reviews and ratings system
- [ ] Build wishlist functionality

## Product & Search
- [ ] Implement advanced product search functionality
- [ ] Add real-time product filtering (category, price, rating)
- [ ] Add product image gallery with zoom
- [ ] Implement related products suggestions
- [ ] Add stock availability indicators

## Marketing & SEO
- [ ] Add SEO meta tags and structured data
- [ ] Implement social media sharing buttons
- [ ] Add newsletter signup form
- [ ] Create promotional banner system
- [ ] Add discount code functionality

## Testing & Deployment
- [x] Write vitest tests for tRPC procedures
- [x] Test all user flows (browse, cart, checkout)
- [x] Test admin dashboard functionality
- [x] Create deployment checkpoint
- [ ] Test Stripe payment integration
- [ ] Test AI agents functionality
- [ ] Test price comparison accuracy
- [ ] Test email notifications
- [ ] Write comprehensive deployment documentation
- [ ] Create Black Friday launch checklist

## Bug Fixes
- [x] Fix nested anchor tag error on homepage
- [x] Fix nested anchor tag error on product detail page
- [x] Fix nested anchor tag error on products page
- [x] Fix remaining nested anchor tag error on homepage (removed Button from inside Link-wrapped Cards)

## Current Sprint: Testing & Documentation (Beginner-Friendly MVP)

### Phase 1: Complete Testing (Before Any Payments)
- [x] Test homepage - verify all links work
- [x] Test product catalog - verify filtering and search
- [x] Test product detail pages - verify all information displays
- [x] Test shopping cart - add/remove/update items
- [x] Test checkout form - verify all fields work
- [x] Test admin dashboard - verify product management
- [x] Test user authentication - login/logout
- [x] Document all testing results in TESTING_LOG.md

### Phase 2: Create Beginner-Friendly Documentation
- [x] Write "Getting Started" guide for complete beginners
- [x] Create "How to Add Products" tutorial
- [x] Create "How to Manage Orders" tutorial
- [x] Create "Payment Setup Guide" for PayFast
- [x] Create "Launch Checklist" for going live
- [x] Document all testing results in TESTING_LOG.md

### Phase 3: Payment Integration (After Testing Complete)
- [x] Implement PayFast payment processor class
- [x] Add PayFast webhook route
- [ ] Create simple payment setup guide for beginners
- [ ] Test with PayFast sandbox (with user)
- [ ] Create payment troubleshooting guide

### Phase 2: Enhanced Price Comparison (Increases Conversions)
- [ ] Implement competitor price scraping (Amazon, eBay, AliExpress)
- [ ] Add real-time exchange rate conversion API
- [ ] Calculate total landed cost (product + shipping + VAT + taxes)
- [ ] Display price comparison on product detail pages
- [ ] Add "Best Deal" badges based on comparison
- [ ] Test price comparison accuracy

### Phase 3: Post-Launch (Can be added after revenue starts)
- [ ] Build AI Product Research Agent using LLM integration
- [ ] Integrate 1688.com product scraping via ZQ Dropshipping
- [ ] Add automated product import from AI agent recommendations

## Current Task: Add First 10 Real Products
- [x] Research top 5 best-selling phones worldwide (2026) - iPhone 16, iPhone 17, Galaxy S25 Ultra, Galaxy A16 5G, iPhone 16e
- [x] Research popular accessories for each phone - Cases, screen protectors, chargers
- [x] Research competitor pricing (Amazon, eBay, AliExpress)
- [x] Calculate profitable pricing for each product - Average 68% margin
- [x] Add 10 products to database (2 accessories per phone) - All products added successfully!
- [x] Test product display on website - Homepage displaying correctly
- [x] Create checkpoint with real products - Version 3c746a3b
