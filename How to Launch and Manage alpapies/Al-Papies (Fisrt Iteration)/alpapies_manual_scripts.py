#!/usr/bin/env python3
"""
Alpapies Manual UGC Scripts
Pre-written UGC-style video scripts for Alpapies phone accessories
Demonstrating the AI UGC platform capabilities
"""

import json

def create_alpapies_ugc_scripts():
    """
    Create authentic UGC scripts for all Alpapies products
    """
    
    scripts = {
        "iPhone 16 Pro Premium Shield Case": {
            "product_details": {
                "price": "$24.99",
                "original_price": "$39.99",
                "discount": "38% OFF",
                "features": ["Camera Control Compatible", "MagSafe Ready", "Drop Protection"]
            },
            "scripts": {
                "problem_solution": """
🎬 SCRIPT: iPhone 16 Pro Case - Problem/Solution

HOOK: "I was SO stressed about protecting my new iPhone 16 Pro..."

PROBLEM: "I just spent $1,200 on this phone and I was terrified of dropping it. Plus, I needed something that wouldn't block the new Camera Control button - most cases I found either didn't fit right or cost like $60!"

DISCOVERY: "Then I found this Premium Shield Case from Alpapies for only $24.99..."

SOLUTION: "Now I have full protection, the Camera Control works perfectly, and my MagSafe charger still connects! I've dropped it twice already and not even a scratch!"

VALUE: "And get this - it was originally $39.99 but Alpapies sources directly from 1688.com (same suppliers as Temu!) so I got it for 38% off!"

CTA: "Check out Alpapies.com - they have all the latest iPhone 16 accessories with premium quality at amazing prices!"

[Duration: 45 seconds]
                """,
                
                "unboxing_review": """
🎬 SCRIPT: iPhone 16 Pro Case - Unboxing Review

HOOK: "Unboxing this iPhone 16 Pro case from Alpapies..."

FIRST IMPRESSION: "Okay, the packaging actually looks really premium - not what I expected for $24.99!"

TESTING: "Let me test the Camera Control button... *click click* - wow, it's so responsive! And the MagSafe... *snap* - perfect alignment!"

COMPARISON: "I was looking at Apple's case for $59, but this has the same features for literally half the price!"

FEATURES: "It's got 9H drop protection, perfect cutouts, and this matte finish feels amazing in hand."

VALUE: "Only $24.99 instead of $39.99 - that's because Alpapies sources from 1688.com, the same suppliers that Temu uses!"

CTA: "Definitely check out Alpapies.com if you need iPhone 16 accessories - quality is insane for the price!"

[Duration: 50 seconds]
                """,
                
                "lifestyle_integration": """
🎬 SCRIPT: iPhone 16 Pro Case - Lifestyle

HOOK: "How this $25 case changed my daily phone routine..."

SCENARIO: "Every morning I grab my phone, wallet, and keys. Before, I was always paranoid about dropping my phone."

BENEFIT: "Now with this Alpapies case, I can actually use my phone normally! The Camera Control works perfectly for quick photos, and I don't stress about drops."

FEATURES: "The MagSafe compatibility means I just slap it on my car mount or wireless charger - no fumbling with cables."

SOCIAL PROOF: "My friends keep asking where I got it because it looks way more expensive than $25!"

VALUE: "Alpapies sources directly from 1688.com manufacturers, so you get premium quality without the markup."

CTA: "Get yours at Alpapies.com - they have all the latest phone accessories!"

[Duration: 40 seconds]
                """
            }
        },
        
        "Samsung Galaxy S25 Ultra Wireless Charger": {
            "product_details": {
                "price": "$29.99", 
                "original_price": "$49.99",
                "discount": "40% OFF",
                "features": ["15W Fast Charging", "Qi Compatible", "LED Indicator"]
            },
            "scripts": {
                "problem_solution": """
🎬 SCRIPT: Wireless Charger - Problem/Solution

HOOK: "I was so tired of cable clutter on my nightstand..."

PROBLEM: "My Galaxy S25 Ultra came with this tiny cable, and I was constantly plugging and unplugging it. Plus, the cable kept falling behind my bed!"

DISCOVERY: "Then I got this 15W wireless charger from Alpapies for $29.99..."

SOLUTION: "Now I just drop my phone on it and it charges super fast! The LED indicator shows me it's working, and my nightstand looks so clean."

FEATURES: "It's Qi compatible so it works with my phone case, and the 15W charging is actually faster than I expected!"

VALUE: "Originally $49.99 but Alpapies gets these from 1688.com suppliers - same quality, way better price!"

CTA: "Check out Alpapies.com for more wireless charging solutions!"

[Duration: 45 seconds]
                """,
                
                "before_after": """
🎬 SCRIPT: Wireless Charger - Before/After

HOOK: "Before vs After getting this wireless charger..."

BEFORE: "My desk was a mess of cables, I was always searching for my charger, and my phone would die at the worst times."

AFTER: "Now I have this clean setup where I just place my Galaxy S25 on the charger. The LED shows it's working, and I never have a dead phone!"

FEATURES: "15W fast charging means it's not slow like old wireless chargers, and it works through my case perfectly."

VALUE: "Only $29.99 instead of $49.99 - 40% off because Alpapies sources directly from 1688.com!"

CONVENIENCE: "Best part? No more wear on my charging port from constantly plugging in cables."

CTA: "Get yours at Alpapies.com - they have wireless chargers for every phone!"

[Duration: 40 seconds]
                """
            }
        },
        
        "Universal Tempered Glass Screen Protector": {
            "product_details": {
                "price": "$12.99",
                "original_price": "$24.99", 
                "discount": "48% OFF",
                "features": ["9H Hardness", "Bubble-Free", "Easy Install"]
            },
            "scripts": {
                "problem_solution": """
🎬 SCRIPT: Screen Protector - Problem/Solution

HOOK: "I cracked my last phone screen and it cost $300 to fix..."

PROBLEM: "I swore I'd never go without a screen protector again, but every one I tried either had bubbles, felt weird, or was super expensive."

DISCOVERY: "Then I found these tempered glass protectors from Alpapies for only $12.99..."

SOLUTION: "Installation was actually easy - no bubbles! And the 9H hardness means I've dropped my phone multiple times with zero damage."

FEATURES: "It feels just like the original screen, no loss in touch sensitivity, and it's crystal clear."

VALUE: "Was $24.99 but Alpapies sources from 1688.com so I got it for 48% off!"

CTA: "Don't risk a cracked screen - get yours at Alpapies.com!"

[Duration: 40 seconds]
                """,
                
                "installation_demo": """
🎬 SCRIPT: Screen Protector - Installation Demo

HOOK: "Installing a screen protector without bubbles..."

SETUP: "Okay, so I got this tempered glass protector from Alpapies. Let me show you how easy this is."

PROCESS: "Clean the screen, align it carefully... and press down. Look at that - no bubbles at all!"

TESTING: "Let me test the touch sensitivity... perfect! And you can barely tell it's there."

QUALITY: "This 9H hardness means it's basically like having a second screen protecting your real screen."

VALUE: "Only $12.99 instead of $24.99 - Alpapies gets these from the same 1688.com suppliers as major brands!"

CTA: "Save your screen and your wallet at Alpapies.com!"

[Duration: 35 seconds]
                """
            }
        },
        
        "20000mAh Fast Charging Power Bank": {
            "product_details": {
                "price": "$34.99",
                "original_price": "$59.99",
                "discount": "42% OFF", 
                "features": ["USB-C PD", "Wireless Charging", "Digital Display"]
            },
            "scripts": {
                "problem_solution": """
🎬 SCRIPT: Power Bank - Problem/Solution

HOOK: "My phone died during a 12-hour flight..."

PROBLEM: "I was stuck with no entertainment, couldn't check my boarding pass, and felt completely disconnected. I needed a power bank that could handle multiple charges."

DISCOVERY: "Found this 20000mAh power bank from Alpapies for $34.99..."

SOLUTION: "This thing charges my phone 4-5 times! Plus it has wireless charging so I can charge my earbuds too. The digital display shows exactly how much power is left."

FEATURES: "USB-C PD means it charges my laptop too, and it's way smaller than I expected for 20000mAh."

VALUE: "Was $59.99 but Alpapies sources from 1688.com manufacturers - same quality, better price!"

CTA: "Never have a dead device again - check out Alpapies.com!"

[Duration: 45 seconds]
                """
            }
        },
        
        "Magnetic Car Mount with Wireless Charging": {
            "product_details": {
                "price": "$19.99",
                "original_price": "$34.99",
                "discount": "43% OFF",
                "features": ["360° Rotation", "One-Hand Operation", "Strong Magnet"]
            },
            "scripts": {
                "problem_solution": """
🎬 SCRIPT: Car Mount - Problem/Solution

HOOK: "I was using GPS and my phone kept falling..."

PROBLEM: "My old car mount was flimsy, my phone would slide out during turns, and the battery would die during long drives."

DISCOVERY: "Got this magnetic car mount with wireless charging from Alpapies for $19.99..."

SOLUTION: "Now my phone snaps on instantly, charges while I drive, and the 360° rotation means perfect viewing angle. One-hand operation is a game changer!"

FEATURES: "The magnet is super strong - I've hit speed bumps and it doesn't budge. Plus wireless charging means no cables!"

VALUE: "Was $34.99 but Alpapies sources from 1688.com - 43% off for the same quality!"

CTA: "Make driving safer and easier - get yours at Alpapies.com!"

[Duration: 40 seconds]
                """
            }
        },
        
        "Premium Bluetooth Earbuds": {
            "product_details": {
                "price": "$39.99",
                "original_price": "$79.99", 
                "discount": "50% OFF",
                "features": ["ANC Technology", "30H Battery", "IPX7 Waterproof"]
            },
            "scripts": {
                "problem_solution": """
🎬 SCRIPT: Bluetooth Earbuds - Problem/Solution

HOOK: "I was spending $200+ on earbuds that kept breaking..."

PROBLEM: "Either the battery died quickly, they weren't waterproof for workouts, or the noise cancellation was terrible. I was tired of overpaying for mediocre quality."

DISCOVERY: "Found these premium earbuds from Alpapies for only $39.99..."

SOLUTION: "The ANC actually blocks out my noisy office, 30-hour battery lasts all week, and they survived my sweaty workouts thanks to IPX7 waterproof rating!"

FEATURES: "Sound quality rivals my old $200 pair, and the case is so compact it fits in my pocket."

VALUE: "Was $79.99 but Alpapies sources from 1688.com manufacturers - 50% off for premium quality!"

CTA: "Upgrade your audio experience at Alpapies.com!"

[Duration: 45 seconds]
                """
            }
        }
    }
    
    return scripts

def save_scripts_to_file():
    """
    Save all scripts to a formatted file
    """
    scripts = create_alpapies_ugc_scripts()
    
    # Create a comprehensive campaign document
    campaign = {
        "campaign_name": "Alpapies UGC Video Ad Campaign",
        "campaign_overview": {
            "objective": "Create authentic UGC-style video ads for Alpapies phone accessories",
            "target_audience": "Smartphone users aged 18-45",
            "key_messaging": [
                "Premium quality from 1688.com suppliers",
                "Same suppliers as Temu/Shein but with quality guarantee", 
                "Significant savings vs retail prices",
                "Latest phone compatibility (iPhone 16, Galaxy S25)"
            ],
            "platforms": ["TikTok", "Instagram Reels", "Facebook", "YouTube Shorts"],
            "total_videos": len(scripts) * 3  # 3 script variations per product
        },
        "products": scripts,
        "production_notes": {
            "creator_profile": "Age 25-35, casual style, authentic tone",
            "setting": "Personal space (bedroom, home office, car)",
            "lighting": "Natural or ring light",
            "duration": "30-60 seconds per video",
            "format": "Vertical 9:16 for mobile platforms"
        },
        "next_steps": [
            "Select top 3 products for initial video production",
            "Source UGC creators or use AI avatar generation",
            "Create videos using MakeUGC.ai or similar platform",
            "A/B test different script variations",
            "Track performance and optimize based on results"
        ]
    }
    
    # Save to file
    filename = "/home/ubuntu/alpapies_complete_ugc_campaign.json"
    with open(filename, 'w') as f:
        json.dump(campaign, f, indent=2)
    
    return filename, campaign

def main():
    """
    Generate and save the complete Alpapies UGC campaign
    """
    print("🎬 Alpapies Complete UGC Campaign Generator")
    print("=" * 60)
    
    filename, campaign = save_scripts_to_file()
    
    print(f"✅ Complete campaign saved to: {filename}")
    print(f"\n📊 Campaign Summary:")
    print(f"   • Products: {len(campaign['products'])}")
    print(f"   • Total script variations: {campaign['campaign_overview']['total_videos']}")
    print(f"   • Target platforms: {', '.join(campaign['campaign_overview']['platforms'])}")
    
    print(f"\n🎯 Featured Products:")
    for i, product in enumerate(campaign['products'].keys(), 1):
        product_data = campaign['products'][product]
        print(f"   {i}. {product}")
        print(f"      Price: {product_data['product_details']['price']} (was {product_data['product_details']['original_price']})")
        print(f"      Scripts: {len(product_data['scripts'])} variations")
    
    print(f"\n🚀 Ready for Production!")
    print(f"   This demonstrates the AI UGC platform's capability to create")
    print(f"   authentic, conversion-focused video ad scripts at scale.")
    
    return campaign

if __name__ == "__main__":
    main()

