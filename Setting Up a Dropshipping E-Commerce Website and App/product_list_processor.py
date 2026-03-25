#!/usr/bin/env python3
"""
Product List Processor for 1688.com Search
Processes your 100 product list and returns real supplier recommendations
"""

import json
import time
from typing import List, Dict
from enhanced_1688_search import Enhanced1688SearchAgent
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProductListProcessor:
    """Process large product lists for 1688.com supplier search"""
    
    def __init__(self):
        self.agent = Enhanced1688SearchAgent(use_selenium=True)
        self.results = {}
        self.processed_count = 0
        
    def process_product_list(self, products: List[str], batch_size: int = 10) -> Dict:
        """Process a list of products in batches"""
        total_products = len(products)
        logger.info(f"Processing {total_products} products in batches of {batch_size}")
        
        all_results = {}
        
        # Process in batches to avoid overwhelming the system
        for i in range(0, total_products, batch_size):
            batch = products[i:i + batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = (total_products + batch_size - 1) // batch_size
            
            logger.info(f"Processing batch {batch_num}/{total_batches} ({len(batch)} products)")
            
            try:
                batch_results = self.agent.search_products(batch)
                all_results.update(batch_results)
                
                self.processed_count += len(batch)
                logger.info(f"Completed {self.processed_count}/{total_products} products")
                
                # Save intermediate results
                self.save_intermediate_results(all_results, batch_num)
                
                # Longer delay between batches
                if i + batch_size < total_products:
                    delay = 30  # 30 seconds between batches
                    logger.info(f"Waiting {delay} seconds before next batch...")
                    time.sleep(delay)
                    
            except Exception as e:
                logger.error(f"Error processing batch {batch_num}: {e}")
                continue
        
        return all_results
    
    def save_intermediate_results(self, results: Dict, batch_num: int):
        """Save intermediate results to prevent data loss"""
        filename = f'/home/ubuntu/alpapies-complete-project/1688_results_batch_{batch_num}.json'
        try:
            json_data = {}
            for product, suppliers in results.items():
                json_data[product] = [supplier.to_dict() for supplier in suppliers]
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Intermediate results saved to: {filename}")
        except Exception as e:
            logger.error(f"Error saving intermediate results: {e}")
    
    def generate_comprehensive_report(self, results: Dict) -> str:
        """Generate a comprehensive report for all products"""
        report = []
        report.append("🛡️ ALPAPIES COMPREHENSIVE 1688.COM SUPPLIER ANALYSIS")
        report.append("=" * 80)
        report.append(f"Analysis Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total Products Analyzed: {len(results)}")
        
        # Calculate overall statistics
        all_suppliers = []
        products_with_suppliers = 0
        products_without_suppliers = 0
        
        for product, suppliers in results.items():
            if suppliers:
                products_with_suppliers += 1
                all_suppliers.extend(suppliers)
            else:
                products_without_suppliers += 1
        
        report.append(f"Products with Suppliers Found: {products_with_suppliers}")
        report.append(f"Products without Suppliers: {products_without_suppliers}")
        report.append(f"Total Suppliers Found: {len(all_suppliers)}")
        
        if all_suppliers:
            avg_confidence = sum(s.confidence_score for s in all_suppliers) / len(all_suppliers)
            report.append(f"Average Confidence Score: {avg_confidence:.1f}/100")
        
        report.append("")
        
        # Categorize suppliers by confidence
        if all_suppliers:
            high_confidence = [s for s in all_suppliers if s.confidence_score >= 80]
            medium_confidence = [s for s in all_suppliers if 60 <= s.confidence_score < 80]
            low_confidence = [s for s in all_suppliers if s.confidence_score < 60]
            
            report.append("📊 SUPPLIER CONFIDENCE DISTRIBUTION")
            report.append("-" * 40)
            report.append(f"High Confidence (80-100): {len(high_confidence)} suppliers")
            report.append(f"Medium Confidence (60-79): {len(medium_confidence)} suppliers")
            report.append(f"Low Confidence (0-59): {len(low_confidence)} suppliers")
            report.append("")
        
        # Top recommendations
        if all_suppliers:
            top_suppliers = sorted(all_suppliers, key=lambda x: x.confidence_score, reverse=True)[:10]
            report.append("🏆 TOP 10 SUPPLIER RECOMMENDATIONS")
            report.append("-" * 50)
            
            for i, supplier in enumerate(top_suppliers, 1):
                report.append(f"{i:2d}. {supplier.name}")
                report.append(f"    Confidence: {supplier.confidence_score:.1f}/100")
                report.append(f"    Product: {supplier.product_title}")
                report.append(f"    Price: {supplier.price_range}")
                report.append(f"    Years: {supplier.years_in_business}, Response: {supplier.response_rate:.1f}%")
                report.append("")
        
        # Detailed product analysis
        report.append("📱 DETAILED PRODUCT ANALYSIS")
        report.append("=" * 50)
        
        for product, suppliers in results.items():
            report.append(f"\nProduct: {product}")
            report.append("-" * len(product))
            
            if not suppliers:
                report.append("❌ No suppliers found")
                report.append("💡 Recommendations:")
                report.append("   - Try alternative search terms")
                report.append("   - Check if product exists on 1688.com")
                report.append("   - Consider similar products")
                continue
            
            # Best supplier for this product
            best_supplier = suppliers[0]
            report.append(f"✅ {len(suppliers)} suppliers found")
            report.append(f"🏆 Best Supplier: {best_supplier.name}")
            report.append(f"   Confidence Score: {best_supplier.confidence_score:.1f}/100")
            report.append(f"   Price Range: {best_supplier.price_range}")
            report.append(f"   Min Order: {best_supplier.min_order_quantity}")
            report.append(f"   Years in Business: {best_supplier.years_in_business}")
            report.append(f"   Response Rate: {best_supplier.response_rate:.1f}%")
            
            if best_supplier.product_url:
                report.append(f"   🔗 Product URL: {best_supplier.product_url}")
            
            # Recommendation
            if best_supplier.confidence_score >= 80:
                report.append("   ✅ HIGHLY RECOMMENDED - Proceed with confidence")
            elif best_supplier.confidence_score >= 60:
                report.append("   ⚠️ RECOMMENDED - Verify details before ordering")
            else:
                report.append("   ❓ INVESTIGATE FURTHER - Limited information available")
        
        # Final recommendations
        report.append("\n" + "=" * 80)
        report.append("💡 FINAL RECOMMENDATIONS")
        report.append("=" * 80)
        
        if products_with_suppliers > 0:
            success_rate = (products_with_suppliers / len(results)) * 100
            report.append(f"✅ Success Rate: {success_rate:.1f}% of products have suppliers")
            
            if len(high_confidence) > 0:
                report.append(f"🎯 {len(high_confidence)} high-confidence suppliers ready for immediate sourcing")
            
            if len(medium_confidence) > 0:
                report.append(f"⚠️ {len(medium_confidence)} medium-confidence suppliers require verification")
            
            report.append("\n📋 NEXT STEPS:")
            report.append("1. Contact high-confidence suppliers for quotes")
            report.append("2. Verify medium-confidence suppliers")
            report.append("3. Request samples from top 3-5 suppliers")
            report.append("4. Negotiate pricing and terms")
            report.append("5. Set up ZQ Dropshipping integration")
        else:
            report.append("❌ No suppliers found for any products")
            report.append("💡 Consider:")
            report.append("   - Revising product list with more common items")
            report.append("   - Using alternative search terms")
            report.append("   - Checking 1688.com directly for availability")
        
        return "\n".join(report)
    
    def cleanup(self):
        """Cleanup resources"""
        if self.agent:
            self.agent.cleanup()

def load_product_list_from_file(filename: str) -> List[str]:
    """Load product list from a text file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            products = [line.strip() for line in f if line.strip()]
        return products
    except FileNotFoundError:
        logger.error(f"Product list file not found: {filename}")
        return []
    except Exception as e:
        logger.error(f"Error loading product list: {e}")
        return []

def create_sample_product_list() -> List[str]:
    """Create a sample 100-product list for testing"""
    products = [
        # iPhone Cases
        "iPhone 16 Pro Max case clear",
        "iPhone 16 Pro case leather",
        "iPhone 16 case silicone",
        "iPhone 15 Pro Max case",
        "iPhone 15 case with ring",
        "iPhone 14 Pro case magsafe",
        "iPhone 13 case transparent",
        "iPhone 12 case wallet",
        "iPhone SE case rugged",
        "iPhone 11 case waterproof",
        
        # Samsung Cases
        "Samsung Galaxy S25 Ultra case",
        "Samsung Galaxy S24 case",
        "Samsung Galaxy S23 case clear",
        "Samsung Galaxy A54 case",
        "Samsung Galaxy Note case",
        "Samsung Galaxy Z Fold case",
        "Samsung Galaxy Z Flip case",
        "Samsung Galaxy A34 case",
        "Samsung Galaxy S22 case",
        "Samsung Galaxy A14 case",
        
        # Screen Protectors
        "iPhone 16 Pro Max screen protector",
        "iPhone 16 tempered glass",
        "Samsung Galaxy S25 screen protector",
        "iPhone 15 Pro screen protector",
        "Samsung Galaxy S24 tempered glass",
        "iPhone 14 screen protector privacy",
        "Samsung Galaxy A54 screen protector",
        "iPhone 13 tempered glass",
        "Samsung Galaxy S23 screen protector",
        "iPhone 12 screen protector",
        
        # Wireless Chargers
        "MagSafe wireless charger",
        "15W wireless charging pad",
        "Samsung wireless charger",
        "iPhone wireless charger stand",
        "3-in-1 wireless charger",
        "Car wireless charger",
        "Fast wireless charger",
        "Qi wireless charging pad",
        "Wireless charger with cooling fan",
        "Portable wireless charger",
        
        # Cables and Adapters
        "USB-C to Lightning cable",
        "USB-C to USB-C cable",
        "Lightning to USB cable",
        "USB-C cable 6ft",
        "Lightning cable 10ft",
        "USB-C to HDMI adapter",
        "Lightning to 3.5mm adapter",
        "USB-C hub multiport",
        "Lightning to USB-C adapter",
        "Magnetic charging cable",
        
        # Power Banks
        "10000mAh power bank",
        "20000mAh power bank",
        "MagSafe power bank",
        "Wireless power bank",
        "Solar power bank",
        "Fast charging power bank",
        "Compact power bank",
        "Power bank with cable",
        "High capacity power bank",
        "Portable charger 5000mAh",
        
        # Car Accessories
        "Car phone mount",
        "Magnetic car mount",
        "Dashboard phone holder",
        "Air vent phone mount",
        "Car charger USB-C",
        "Car charger dual port",
        "Wireless car charger",
        "Car phone holder cup",
        "Windshield phone mount",
        "Car charger fast charging",
        
        # Audio Accessories
        "Bluetooth wireless earbuds",
        "AirPods case cover",
        "Wireless headphones",
        "USB-C earphones",
        "Lightning earphones",
        "Bluetooth speaker portable",
        "Phone microphone",
        "Audio splitter",
        "Bluetooth adapter",
        "Noise cancelling earbuds",
        
        # Phone Accessories
        "Phone ring holder",
        "Pop socket grip",
        "Phone lanyard strap",
        "Phone cleaning kit",
        "Phone camera lens protector",
        "Phone privacy screen",
        "Phone wallet case",
        "Phone armband",
        "Phone waterproof case",
        "Phone cooling fan",
        
        # Charging Accessories
        "Wall charger USB-C",
        "Fast charger 65W",
        "GaN charger compact",
        "Multi-port charger",
        "Charging station",
        "Wireless charging dock",
        "Car charger fast",
        "Travel charger adapter",
        "USB charger hub",
        "Charging cable organizer",
        
        # Gaming Accessories
        "Phone gaming controller",
        "Mobile game trigger",
        "Phone cooling pad",
        "Gaming phone case",
        "Phone joystick",
        "Mobile gaming grip",
        "Phone trigger buttons",
        "Gaming phone holder",
        "Phone game pad",
        "Mobile controller clip"
    ]
    
    return products

def main():
    """Main function to process product list"""
    print("🛡️ ALPAPIES 1688.COM PRODUCT LIST PROCESSOR")
    print("=" * 60)
    
    # Option 1: Load from file
    product_file = '/home/ubuntu/alpapies-complete-project/product_list.txt'
    products = load_product_list_from_file(product_file)
    
    # Option 2: Use sample list if no file found
    if not products:
        print("📝 No product list file found, using sample 100-product list")
        products = create_sample_product_list()
        
        # Save sample list for reference
        with open(product_file, 'w', encoding='utf-8') as f:
            for product in products:
                f.write(f"{product}\n")
        print(f"📁 Sample product list saved to: {product_file}")
    
    print(f"📊 Processing {len(products)} products...")
    
    processor = ProductListProcessor()
    
    try:
        # Process all products
        results = processor.process_product_list(products, batch_size=5)
        
        # Generate comprehensive report
        report = processor.generate_comprehensive_report(results)
        
        # Save final results
        report_file = '/home/ubuntu/alpapies-complete-project/1688_comprehensive_report.txt'
        json_file = '/home/ubuntu/alpapies-complete-project/1688_final_results.json'
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        # Save JSON results
        json_data = {}
        for product, suppliers in results.items():
            json_data[product] = [supplier.to_dict() for supplier in suppliers]
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        
        print("\n" + "=" * 60)
        print("✅ PROCESSING COMPLETE!")
        print(f"📄 Comprehensive report: {report_file}")
        print(f"📊 JSON data: {json_file}")
        print("=" * 60)
        
        # Print summary
        print(f"\n📈 SUMMARY:")
        print(f"Products processed: {len(results)}")
        products_with_suppliers = len([p for p, s in results.items() if s])
        print(f"Products with suppliers: {products_with_suppliers}")
        print(f"Success rate: {(products_with_suppliers/len(results)*100):.1f}%")
        
    except Exception as e:
        print(f"❌ Error during processing: {e}")
    finally:
        processor.cleanup()

if __name__ == "__main__":
    main()

