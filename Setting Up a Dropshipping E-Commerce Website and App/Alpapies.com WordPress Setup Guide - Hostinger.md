# Alpapies.com WordPress Setup Guide - Hostinger

## Prerequisites
- ✅ Domain: alpapies.com (registered on Hostinger)
- ✅ Hosting: Hostinger account with hosting plan
- ✅ Brand Assets: Logo and brand guidelines ready
- ✅ Product Research: ZQ Dropshipping integration planned

## Phase 1: WordPress Installation on Hostinger

### Step 1: Access Hostinger Control Panel
1. Log into your Hostinger account
2. Navigate to the hosting control panel (hPanel)
3. Find your alpapies.com domain in the list

### Step 2: Install WordPress
1. In hPanel, click "Auto Installer" or "Website" section
2. Select "WordPress" from the CMS options
3. Choose your domain: alpapies.com
4. Set up admin credentials:
   - **Username**: Choose a secure admin username (not "admin")
   - **Password**: Use a strong password
   - **Email**: Your business email address
5. Click "Install" and wait for completion (usually 1-2 minutes)

### Step 3: Initial WordPress Setup
1. Access your WordPress admin: alpapies.com/wp-admin
2. Log in with your credentials
3. Complete the initial setup wizard
4. Set timezone to your business location
5. Configure basic settings

## Phase 2: Essential Plugin Installation

### Required Plugins (Install in this order):

#### 1. WooCommerce (E-commerce Foundation)
```
Plugin: WooCommerce
Purpose: E-commerce functionality
Installation: Plugins > Add New > Search "WooCommerce" > Install & Activate
```

#### 2. Security Plugin
```
Plugin: Wordfence Security
Purpose: Website security and firewall
Installation: Plugins > Add New > Search "Wordfence" > Install & Activate
```

#### 3. Performance Optimization
```
Plugin: WP Rocket (Premium) or W3 Total Cache (Free)
Purpose: Caching and speed optimization
Installation: Plugins > Add New > Search plugin name > Install & Activate
```

#### 4. SEO Plugin
```
Plugin: Yoast SEO
Purpose: Search engine optimization
Installation: Plugins > Add New > Search "Yoast SEO" > Install & Activate
```

#### 5. Backup Plugin
```
Plugin: UpdraftPlus
Purpose: Automated backups
Installation: Plugins > Add New > Search "UpdraftPlus" > Install & Activate
```

#### 6. Email Marketing
```
Plugin: Mailchimp for WooCommerce
Purpose: Email marketing integration
Installation: Plugins > Add New > Search "Mailchimp" > Install & Activate
```

## Phase 3: WooCommerce Configuration

### Step 1: WooCommerce Setup Wizard
1. Navigate to WooCommerce > Home
2. Run the setup wizard:
   - **Store Location**: Your business location
   - **Currency**: USD (or your preferred currency)
   - **Product Types**: Physical products
   - **Business Details**: Fill in your business information
   - **Theme**: Skip for now (we'll customize later)

### Step 2: Payment Gateway Setup
```
Recommended Payment Methods:
1. PayPal Standard (Easy setup, widely trusted)
2. Stripe (Credit card processing)
3. Square (Alternative payment processor)

Setup Process:
- Go to WooCommerce > Settings > Payments
- Enable PayPal and Stripe
- Configure API keys (get from PayPal/Stripe accounts)
- Test payment processing
```

### Step 3: Shipping Configuration
```
Shipping Setup for Dropshipping:
- Go to WooCommerce > Settings > Shipping
- Create shipping zones (US, International, etc.)
- Set up shipping methods:
  * Free shipping (for orders over $50)
  * Standard shipping ($5.99)
  * Express shipping ($12.99)
- Configure shipping classes for different product types
```

### Step 4: Tax Settings
```
Tax Configuration:
- Go to WooCommerce > Settings > Tax
- Enable tax calculation
- Set up tax rates for your business location
- Configure automated tax calculation
```

## Phase 4: Theme Selection and Customization

### Recommended E-commerce Themes:

#### Option 1: Astra (Free/Pro)
```
Features:
- Fast loading and SEO optimized
- WooCommerce integration
- Customizable with Elementor
- Mobile responsive
- Good for beginners

Installation:
- Appearance > Themes > Add New
- Search "Astra" > Install & Activate
```

#### Option 2: Storefront (Free - WooCommerce Official)
```
Features:
- Official WooCommerce theme
- Deep WooCommerce integration
- Customizable
- Regular updates
- Reliable and stable

Installation:
- Appearance > Themes > Add New
- Search "Storefront" > Install & Activate
```

#### Option 3: OceanWP (Free/Pro)
```
Features:
- Highly customizable
- Fast performance
- WooCommerce ready
- Multiple demos available
- Good support

Installation:
- Appearance > Themes > Add New
- Search "OceanWP" > Install & Activate
```

### Theme Customization Steps:
1. **Install chosen theme**
2. **Customize appearance**:
   - Go to Appearance > Customize
   - Upload Alpapies logo
   - Set brand colors (#1E3A8A, #3B82F6, #F59E0B)
   - Configure typography
   - Set up header and footer
3. **Create custom pages** (see Phase 5)

## Phase 5: Essential Page Creation

### Required Pages:

#### 1. Homepage
```
Content Structure:
- Hero section with value proposition
- Featured product categories
- New arrivals section
- Best sellers
- Customer testimonials
- Newsletter signup

Creation:
- Pages > Add New
- Title: "Home"
- Use page builder or blocks to create sections
- Set as homepage: Settings > Reading > Static Page
```

#### 2. Shop Page (Auto-created by WooCommerce)
```
Customization:
- WooCommerce > Settings > Products
- Configure shop page layout
- Set products per page
- Configure product sorting options
```

#### 3. About Us Page
```
Content:
- Company story and mission
- Why choose Alpapies
- Quality commitment
- Team information (optional)

Creation:
- Pages > Add New
- Title: "About Us"
- Write compelling brand story
```

#### 4. Contact Page
```
Content:
- Contact form
- Business address
- Email and phone
- Customer service hours
- FAQ section

Creation:
- Pages > Add New
- Title: "Contact"
- Install Contact Form 7 plugin for forms
```

#### 5. Legal Pages
```
Required Pages:
- Privacy Policy
- Terms of Service
- Return & Refund Policy
- Shipping Policy

Creation:
- Use WordPress privacy policy generator
- Customize for your business
- Link in footer
```

## Phase 6: Product Catalog Setup

### Product Categories Structure:
```
Main Categories:
├── iPhone Accessories
│   ├── iPhone 16 Series
│   ├── iPhone 15 Series
│   └── iPhone 14 Series
├── Samsung Accessories
│   ├── Galaxy S25 Series
│   ├── Galaxy S24 Series
│   └── Galaxy Foldables
├── Google Pixel Accessories
└── Universal Accessories
    ├── Wireless Chargers
    ├── Power Banks
    ├── Car Mounts
    └── Cables & Adapters
```

### Category Creation:
1. Go to Products > Categories
2. Create main categories first
3. Create subcategories with proper parent assignment
4. Add category descriptions for SEO
5. Upload category images

### Sample Product Creation:
```
Product Example: iPhone 16 Pro Case
- Product Name: "iPhone 16 Pro Premium Shield Case"
- SKU: ALP-IP16P-CASE-001
- Price: $24.99
- Categories: iPhone Accessories > iPhone 16 Series
- Tags: iPhone 16 Pro, case, protection, premium
- Description: Detailed product description
- Images: High-quality product photos
- Attributes: Color, Material, Compatibility
- Inventory: Manage stock (sync with ZQ Dropshipping)
```

## Phase 7: ZQ Dropshipping Integration

### Integration Options:

#### Option 1: Manual Integration
```
Process:
1. Create products manually in WooCommerce
2. Set up order notification system
3. Forward orders to ZQ Dropshipping
4. Update tracking information manually
```

#### Option 2: Plugin Integration
```
Recommended Plugin: WooCommerce Dropshipping
Installation:
- Search for dropshipping plugins
- Install compatible plugin
- Configure ZQ Dropshipping API (if available)
- Set up automated order forwarding
```

#### Option 3: Custom Integration
```
Development Required:
- Custom API integration with ZQ Dropshipping
- Automated product sync
- Real-time inventory updates
- Automated order processing
```

## Phase 8: SEO Optimization

### Yoast SEO Configuration:
1. **General Settings**:
   - Set up site title and tagline
   - Configure social media accounts
   - Set up Google Search Console

2. **Product SEO**:
   - Optimize product titles and descriptions
   - Add meta descriptions
   - Use proper heading structure
   - Optimize product images with alt text

3. **Category SEO**:
   - Write SEO-friendly category descriptions
   - Optimize category page titles
   - Create category-specific content

### Technical SEO:
```
Checklist:
□ Install SSL certificate (should be automatic on Hostinger)
□ Set up Google Analytics
□ Submit XML sitemap to Google
□ Optimize site speed
□ Configure breadcrumbs
□ Set up schema markup for products
```

## Phase 9: Performance Optimization

### Speed Optimization:
1. **Image Optimization**:
   - Install Smush or ShortPixel plugin
   - Compress all images
   - Use WebP format when possible

2. **Caching Setup**:
   - Configure WP Rocket or W3 Total Cache
   - Enable browser caching
   - Set up CDN (Cloudflare recommended)

3. **Database Optimization**:
   - Install WP-Optimize plugin
   - Clean up database regularly
   - Remove unused plugins and themes

### Performance Targets:
```
Goals:
- Page load time: < 3 seconds
- Mobile performance: > 90 (Google PageSpeed)
- Desktop performance: > 95 (Google PageSpeed)
- Uptime: > 99.9%
```

## Phase 10: Security Hardening

### Wordfence Configuration:
1. **Firewall Setup**:
   - Enable Web Application Firewall
   - Configure country blocking if needed
   - Set up rate limiting

2. **Scan Configuration**:
   - Schedule regular malware scans
   - Enable real-time file monitoring
   - Set up email alerts

3. **Login Security**:
   - Enable two-factor authentication
   - Limit login attempts
   - Hide wp-admin from unauthorized users

### Additional Security Measures:
```
Security Checklist:
□ Change default admin username
□ Use strong passwords
□ Keep WordPress and plugins updated
□ Regular backups with UpdraftPlus
□ Hide WordPress version
□ Disable file editing in admin
□ Secure wp-config.php file
```

## Phase 11: Testing and Launch Preparation

### Pre-Launch Testing:
1. **Functionality Testing**:
   - Test all forms and contact methods
   - Verify payment processing
   - Test order placement and confirmation
   - Check email notifications

2. **Cross-Browser Testing**:
   - Test on Chrome, Firefox, Safari, Edge
   - Verify mobile responsiveness
   - Check tablet compatibility

3. **Performance Testing**:
   - Run Google PageSpeed Insights
   - Test with GTmetrix
   - Check mobile performance

### Launch Checklist:
```
Pre-Launch Checklist:
□ All pages created and optimized
□ Products added with proper categories
□ Payment gateways tested
□ Shipping methods configured
□ Legal pages completed
□ Contact forms working
□ Analytics installed
□ SEO optimized
□ Security configured
□ Backups scheduled
□ SSL certificate active
□ 404 error page customized
□ Site search functionality working
```

## Phase 12: Post-Launch Optimization

### Week 1 Tasks:
- Monitor site performance
- Check for any errors or issues
- Test order processing
- Gather initial user feedback
- Monitor security alerts

### Month 1 Tasks:
- Analyze traffic and conversion data
- Optimize underperforming pages
- Add more products based on demand
- Implement customer feedback
- Start content marketing

### Ongoing Maintenance:
```
Regular Tasks:
- Weekly: Check for plugin updates
- Monthly: Review analytics and performance
- Quarterly: Security audit and backup verification
- As needed: Add new products and categories
```

## Support Resources

### Hostinger Support:
- Live chat support 24/7
- Knowledge base and tutorials
- WordPress-specific help guides

### WordPress Resources:
- WordPress.org documentation
- WooCommerce documentation
- Plugin-specific support forums

### Emergency Contacts:
- Hostinger support: Available in your account
- WordPress developer: Consider hiring for complex issues
- ZQ Dropshipping support: support@zqdropshipping.com

This comprehensive guide will help you set up a professional, secure, and optimized e-commerce website for Alpapies.com on your Hostinger hosting.

