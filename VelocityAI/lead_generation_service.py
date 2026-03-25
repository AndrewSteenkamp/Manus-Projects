"""
Lead Generation Service for UGC Ads Agency
Integrates with BuiltWith, Apollo.io, and Million Verifier to find and validate leads
Supports ALL e-commerce platforms: Shopify, WooCommerce, Magento, BigCommerce, Squarespace, Wix, etc.
Targets multiple product categories across all online stores
"""

import requests
import json
import csv
import time
from typing import List, Dict, Any
import sqlite3
from datetime import datetime

class LeadGenerationService:
    def __init__(self):
        self.builtwith_api_key = "YOUR_BUILTWITH_API_KEY"
        self.apollo_api_key = "YOUR_APOLLO_API_KEY"
        self.million_verifier_api_key = "YOUR_MILLION_VERIFIER_API_KEY"
        
        # Initialize database for lead storage
        self.init_database()
        
        # E-commerce platform configurations
        self.ecommerce_platforms = {
            "shopify": {
                "name": "Shopify",
                "market_share": "10.3%",
                "typical_size": "SMB to Enterprise",
                "technologies": ["Shopify", "Shopify Plus"]
            },
            "woocommerce": {
                "name": "WooCommerce", 
                "market_share": "28.24%",
                "typical_size": "SMB to Mid-market",
                "technologies": ["WooCommerce", "WordPress"]
            },
            "magento": {
                "name": "Magento",
                "market_share": "7.18%", 
                "typical_size": "Mid-market to Enterprise",
                "technologies": ["Magento", "Adobe Commerce"]
            },
            "bigcommerce": {
                "name": "BigCommerce",
                "market_share": "3.15%",
                "typical_size": "SMB to Enterprise", 
                "technologies": ["BigCommerce"]
            },
            "squarespace": {
                "name": "Squarespace Commerce",
                "market_share": "3.79%",
                "typical_size": "SMB",
                "technologies": ["Squarespace Commerce"]
            },
            "wix": {
                "name": "Wix eCommerce",
                "market_share": "3.38%",
                "typical_size": "SMB",
                "technologies": ["Wix Stores"]
            },
            "prestashop": {
                "name": "PrestaShop",
                "market_share": "5.29%",
                "typical_size": "SMB",
                "technologies": ["PrestaShop"]
            },
            "opencart": {
                "name": "OpenCart", 
                "market_share": "4.81%",
                "typical_size": "SMB",
                "technologies": ["OpenCart"]
            },
            "custom": {
                "name": "Custom E-commerce",
                "market_share": "15%+",
                "typical_size": "All sizes",
                "technologies": ["Custom", "React", "Vue", "Angular", "Laravel", "Django"]
            }
        }
        
        # Category-specific search terms for better targeting
        self.category_keywords = {
            "supplements": ["vitamin", "protein", "supplement", "nutrition", "health", "wellness", "organic"],
            "electronics": ["phone", "laptop", "gadget", "tech", "electronic", "device", "computer"],
            "beauty": ["skincare", "makeup", "cosmetic", "beauty", "hair", "skin", "cosmetics"],
            "outdoor": ["outdoor", "camping", "hiking", "sports", "adventure", "gear", "equipment"],
            "fashion": ["clothing", "fashion", "apparel", "style", "wear", "accessories", "shoes"],
            "home": ["home", "furniture", "decor", "kitchen", "organization", "living", "house"],
            "fitness": ["fitness", "workout", "gym", "exercise", "training", "activewear", "sports"],
            "automotive": ["car", "auto", "vehicle", "motorcycle", "parts", "accessories", "tools"],
            "baby": ["baby", "kids", "children", "infant", "toddler", "maternity", "parenting"],
            "pet": ["pet", "dog", "cat", "animal", "veterinary", "pet supplies", "pet food"],
            "jewelry": ["jewelry", "watches", "rings", "necklace", "earrings", "luxury", "accessories"],
            "books": ["books", "education", "learning", "publishing", "ebooks", "courses"],
            "food": ["food", "gourmet", "organic", "snacks", "beverages", "specialty food"],
            "crafts": ["crafts", "DIY", "handmade", "art", "supplies", "creative", "hobby"]
        }
    
    def init_database(self):
        """Initialize SQLite database for lead storage"""
        conn = sqlite3.connect('leads.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                domain TEXT UNIQUE,
                company_name TEXT,
                email TEXT,
                category TEXT,
                ecommerce_platform TEXT,
                platform_version TEXT,
                contact_name TEXT,
                phone TEXT,
                country TEXT,
                employee_count TEXT,
                revenue TEXT,
                monthly_traffic TEXT,
                email_verified BOOLEAN DEFAULT FALSE,
                contacted BOOLEAN DEFAULT FALSE,
                response_status TEXT,
                technologies TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def fetch_builtwith_leads(self, category: str = "all", platform: str = "all", limit: int = 1000) -> List[Dict]:
        """
        Fetch e-commerce store leads from BuiltWith API across all platforms
        """
        try:
            leads = []
            
            # Simulate BuiltWith API response for all e-commerce platforms
            sample_leads = [
                # Shopify stores
                {
                    "domain": "vitaboost-supplements.myshopify.com",
                    "company_name": "VitaBoost Supplements",
                    "category": "supplements",
                    "ecommerce_platform": "shopify",
                    "platform_version": "Shopify Plus",
                    "country": "US",
                    "employee_count": "10-50",
                    "monthly_traffic": "50K-100K",
                    "technologies": ["Shopify", "Facebook Pixel", "Google Analytics", "Klaviyo"]
                },
                # WooCommerce stores
                {
                    "domain": "techgear-pro.com",
                    "company_name": "TechGear Pro",
                    "category": "electronics", 
                    "ecommerce_platform": "woocommerce",
                    "platform_version": "WooCommerce 8.0",
                    "country": "US",
                    "employee_count": "50-100",
                    "monthly_traffic": "100K-500K",
                    "technologies": ["WooCommerce", "WordPress", "Stripe", "PayPal"]
                },
                # Magento stores
                {
                    "domain": "luxe-beauty-store.com",
                    "company_name": "Luxe Beauty Store",
                    "category": "beauty",
                    "ecommerce_platform": "magento",
                    "platform_version": "Adobe Commerce 2.4",
                    "country": "US",
                    "employee_count": "100-250",
                    "monthly_traffic": "500K-1M",
                    "technologies": ["Magento", "Adobe Commerce", "Elasticsearch", "Redis"]
                },
                # BigCommerce stores
                {
                    "domain": "outdoor-adventures-gear.com",
                    "company_name": "Outdoor Adventures Gear",
                    "category": "outdoor",
                    "ecommerce_platform": "bigcommerce",
                    "platform_version": "BigCommerce Enterprise",
                    "country": "US",
                    "employee_count": "25-50",
                    "monthly_traffic": "25K-50K",
                    "technologies": ["BigCommerce", "Yotpo", "Mailchimp"]
                },
                # Squarespace stores
                {
                    "domain": "fashion-forward-boutique.com",
                    "company_name": "Fashion Forward Boutique",
                    "category": "fashion",
                    "ecommerce_platform": "squarespace",
                    "platform_version": "Squarespace Commerce",
                    "country": "US",
                    "employee_count": "5-10",
                    "monthly_traffic": "10K-25K",
                    "technologies": ["Squarespace Commerce", "Instagram Shopping"]
                },
                # Wix stores
                {
                    "domain": "home-decor-paradise.com",
                    "company_name": "Home Decor Paradise",
                    "category": "home",
                    "ecommerce_platform": "wix",
                    "platform_version": "Wix Stores",
                    "country": "US",
                    "employee_count": "5-10",
                    "monthly_traffic": "5K-10K",
                    "technologies": ["Wix Stores", "Facebook Pixel"]
                },
                # Custom e-commerce
                {
                    "domain": "premium-supplements-direct.com",
                    "company_name": "Premium Supplements Direct",
                    "category": "supplements",
                    "ecommerce_platform": "custom",
                    "platform_version": "React + Node.js",
                    "country": "US",
                    "employee_count": "50-100",
                    "monthly_traffic": "200K-500K",
                    "technologies": ["React", "Node.js", "Stripe", "MongoDB"]
                },
                # Additional categories
                {
                    "domain": "auto-parts-warehouse.com",
                    "company_name": "Auto Parts Warehouse",
                    "category": "automotive",
                    "ecommerce_platform": "woocommerce",
                    "platform_version": "WooCommerce",
                    "country": "US",
                    "employee_count": "25-50",
                    "monthly_traffic": "100K-200K",
                    "technologies": ["WooCommerce", "WordPress", "WooCommerce Subscriptions"]
                },
                {
                    "domain": "baby-essentials-store.com",
                    "company_name": "Baby Essentials Store",
                    "category": "baby",
                    "ecommerce_platform": "shopify",
                    "platform_version": "Shopify",
                    "country": "US",
                    "employee_count": "10-25",
                    "monthly_traffic": "50K-100K",
                    "technologies": ["Shopify", "Klaviyo", "Gorgias"]
                },
                {
                    "domain": "pet-paradise-supplies.com",
                    "company_name": "Pet Paradise Supplies",
                    "category": "pet",
                    "ecommerce_platform": "bigcommerce",
                    "platform_version": "BigCommerce",
                    "country": "US",
                    "employee_count": "15-30",
                    "monthly_traffic": "75K-150K",
                    "technologies": ["BigCommerce", "Yotpo", "Zendesk"]
                }
            ]
            
            # Filter by category if specified
            if category != "all":
                sample_leads = [lead for lead in sample_leads if lead["category"] == category]
            
            # Filter by platform if specified
            if platform != "all":
                sample_leads = [lead for lead in sample_leads if lead["ecommerce_platform"] == platform]
            
            return sample_leads[:limit]
            
        except Exception as e:
            print(f"Error fetching BuiltWith leads: {str(e)}")
            return []
    
    def fetch_apollo_leads(self, category: str = "all", limit: int = 1000) -> List[Dict]:
        """
        Fetch leads from Apollo.io filtered by Shopify technology
        """
        try:
            # Simulate Apollo.io API response
            # In production, this would call Apollo.io API with Shopify filter
            
            apollo_leads = [
                {
                    "domain": "premium-supplements.com",
                    "company_name": "Premium Supplements Co",
                    "email": "marketing@premium-supplements.com",
                    "contact_name": "Sarah Johnson",
                    "title": "Marketing Director",
                    "category": "supplements",
                    "phone": "+1-555-0123",
                    "employee_count": "50-100",
                    "revenue": "$5M-$10M"
                },
                {
                    "domain": "smart-electronics.com",
                    "company_name": "Smart Electronics",
                    "email": "ads@smart-electronics.com", 
                    "contact_name": "Mike Chen",
                    "title": "Digital Marketing Manager",
                    "category": "electronics",
                    "phone": "+1-555-0456",
                    "employee_count": "100-250",
                    "revenue": "$10M-$25M"
                },
                {
                    "domain": "luxe-beauty.com",
                    "company_name": "Luxe Beauty",
                    "email": "partnerships@luxe-beauty.com",
                    "contact_name": "Emma Rodriguez",
                    "title": "Brand Partnerships",
                    "category": "beauty",
                    "phone": "+1-555-0789",
                    "employee_count": "25-50", 
                    "revenue": "$2M-$5M"
                }
            ]
            
            # Filter by category if specified
            if category != "all":
                apollo_leads = [lead for lead in apollo_leads if lead["category"] == category]
            
            return apollo_leads[:limit]
            
        except Exception as e:
            print(f"Error fetching Apollo leads: {str(e)}")
            return []
    
    def verify_emails(self, emails: List[str]) -> Dict[str, bool]:
        """
        Verify email addresses using Million Verifier
        """
        try:
            verified_emails = {}
            
            # Simulate Million Verifier API response
            # In production, this would call Million Verifier API
            
            for email in emails:
                # Simulate verification (90% success rate)
                import random
                verified_emails[email] = random.random() > 0.1
                time.sleep(0.1)  # Rate limiting simulation
            
            return verified_emails
            
        except Exception as e:
            print(f"Error verifying emails: {str(e)}")
            return {email: False for email in emails}
    
    def save_leads_to_database(self, leads: List[Dict]):
        """
        Save leads to SQLite database
        """
        try:
            conn = sqlite3.connect('leads.db')
            cursor = conn.cursor()
            
            for lead in leads:
                cursor.execute('''
                    INSERT OR REPLACE INTO leads 
                    (domain, company_name, email, category, contact_name, phone, country, employee_count, revenue, email_verified)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    lead.get('domain', ''),
                    lead.get('company_name', ''),
                    lead.get('email', ''),
                    lead.get('category', ''),
                    lead.get('contact_name', ''),
                    lead.get('phone', ''),
                    lead.get('country', ''),
                    lead.get('employee_count', ''),
                    lead.get('revenue', ''),
                    lead.get('email_verified', False)
                ))
            
            conn.commit()
            conn.close()
            
            print(f"Saved {len(leads)} leads to database")
            
        except Exception as e:
            print(f"Error saving leads to database: {str(e)}")
    
    def export_leads_to_csv(self, category: str = "all", verified_only: bool = True) -> str:
        """
        Export leads to CSV file for cold email campaigns
        """
        try:
            conn = sqlite3.connect('leads.db')
            cursor = conn.cursor()
            
            query = "SELECT * FROM leads WHERE 1=1"
            params = []
            
            if category != "all":
                query += " AND category = ?"
                params.append(category)
            
            if verified_only:
                query += " AND email_verified = 1"
            
            query += " AND email IS NOT NULL AND email != ''"
            
            cursor.execute(query, params)
            leads = cursor.fetchall()
            
            # Get column names
            column_names = [description[0] for description in cursor.description]
            
            # Create CSV file
            filename = f"leads_{category}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(column_names)
                writer.writerows(leads)
            
            conn.close()
            
            print(f"Exported {len(leads)} leads to {filename}")
            return filename
            
        except Exception as e:
            print(f"Error exporting leads to CSV: {str(e)}")
            return ""
    
    def generate_leads_for_category(self, category: str, limit: int = 500) -> Dict[str, Any]:
        """
        Complete lead generation process for a specific category
        """
        try:
            print(f"Starting lead generation for {category} category...")
            
            # Step 1: Fetch leads from BuiltWith
            print("Fetching leads from BuiltWith...")
            builtwith_leads = self.fetch_builtwith_leads(category, limit//2)
            
            # Step 2: Fetch leads from Apollo.io
            print("Fetching leads from Apollo.io...")
            apollo_leads = self.fetch_apollo_leads(category, limit//2)
            
            # Step 3: Combine and deduplicate leads
            all_leads = builtwith_leads + apollo_leads
            unique_leads = {}
            
            for lead in all_leads:
                domain = lead.get('domain', '')
                if domain and domain not in unique_leads:
                    unique_leads[domain] = lead
            
            leads_list = list(unique_leads.values())
            
            # Step 4: Extract and verify emails
            emails_to_verify = [lead.get('email') for lead in leads_list if lead.get('email')]
            
            if emails_to_verify:
                print(f"Verifying {len(emails_to_verify)} email addresses...")
                verified_emails = self.verify_emails(emails_to_verify)
                
                # Update leads with verification status
                for lead in leads_list:
                    email = lead.get('email')
                    if email:
                        lead['email_verified'] = verified_emails.get(email, False)
            
            # Step 5: Save to database
            print("Saving leads to database...")
            self.save_leads_to_database(leads_list)
            
            # Step 6: Export verified leads to CSV
            csv_filename = self.export_leads_to_csv(category, verified_only=True)
            
            verified_count = sum(1 for lead in leads_list if lead.get('email_verified', False))
            
            return {
                "success": True,
                "category": category,
                "total_leads": len(leads_list),
                "verified_emails": verified_count,
                "csv_file": csv_filename,
                "leads_sample": leads_list[:5]  # Return first 5 for preview
            }
            
        except Exception as e:
            print(f"Error in lead generation: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "category": category
            }
    
    def generate_all_categories(self, limit_per_category: int = 200) -> Dict[str, Any]:
        """
        Generate leads for all supported categories
        """
        results = {}
        
        for category in self.category_keywords.keys():
            print(f"\n=== Processing {category.upper()} category ===")
            results[category] = self.generate_leads_for_category(category, limit_per_category)
            time.sleep(2)  # Rate limiting between categories
        
        # Generate summary
        total_leads = sum(result.get('total_leads', 0) for result in results.values())
        total_verified = sum(result.get('verified_emails', 0) for result in results.values())
        
        return {
            "success": True,
            "categories_processed": len(results),
            "total_leads_generated": total_leads,
            "total_verified_emails": total_verified,
            "category_results": results
        }

# Example usage and testing
if __name__ == "__main__":
    service = LeadGenerationService()
    
    # Test lead generation for supplements category
    result = service.generate_leads_for_category("supplements", 100)
    print(json.dumps(result, indent=2))
    
    # Uncomment to generate leads for all categories
    # all_results = service.generate_all_categories(50)
    # print(json.dumps(all_results, indent=2))

