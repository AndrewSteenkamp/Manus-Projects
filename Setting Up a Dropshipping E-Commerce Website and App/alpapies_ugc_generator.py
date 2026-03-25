#!/usr/bin/env python3
"""
Alpapies UGC Ad Generator
Custom script to generate UGC-style video ads for Alpapies phone accessories
Using the AI automation service for electronics category
"""

import json
import time
from typing import List, Dict, Any
import openai
from openai import OpenAI

class AlpapiesUGCGenerator:
    def __init__(self):
        self.openai_client = OpenAI()
        
        # Alpapies product configurations
        self.alpapies_products = {
            "iPhone 16 Pro Premium Shield Case": {
                "category": "electronics",
                "description": "Premium protection case with Camera Control compatibility, MagSafe ready, drop protection",
                "price": "$24.99",
                "original_price": "$39.99",
                "features": ["Camera Control Compatible", "MagSafe Ready", "Drop Protection"],
                "target_audience": "iPhone 16 Pro users",
                "pain_points": ["expensive phone needs protection", "camera button accessibility", "wireless charging compatibility"]
            },
            "Samsung Galaxy S25 Ultra Wireless Charger": {
                "category": "electronics", 
                "description": "15W fast wireless charger with Qi compatibility and LED indicator",
                "price": "$29.99",
                "original_price": "$49.99",
                "features": ["15W Fast Charging", "Qi Compatible", "LED Indicator"],
                "target_audience": "Samsung Galaxy S25 users",
                "pain_points": ["slow charging", "cable clutter", "charging convenience"]
            },
            "Universal Tempered Glass Screen Protector": {
                "category": "electronics",
                "description": "9H hardness tempered glass with bubble-free installation",
                "price": "$12.99", 
                "original_price": "$24.99",
                "features": ["9H Hardness", "Bubble-Free", "Easy Install"],
                "target_audience": "smartphone users",
                "pain_points": ["cracked screens", "expensive repairs", "screen scratches"]
            },
            "20000mAh Fast Charging Power Bank": {
                "category": "electronics",
                "description": "High capacity power bank with USB-C PD and wireless charging",
                "price": "$34.99",
                "original_price": "$59.99", 
                "features": ["USB-C PD", "Wireless Charging", "Digital Display"],
                "target_audience": "heavy phone users",
                "pain_points": ["dead battery", "travel charging", "multiple device charging"]
            },
            "Magnetic Car Mount with Wireless Charging": {
                "category": "electronics",
                "description": "360° rotation car mount with wireless charging capability",
                "price": "$19.99",
                "original_price": "$34.99",
                "features": ["360° Rotation", "One-Hand Operation", "Strong Magnet"],
                "target_audience": "drivers",
                "pain_points": ["phone falling", "navigation visibility", "hands-free charging"]
            },
            "Premium Bluetooth Earbuds": {
                "category": "electronics",
                "description": "ANC earbuds with 30H battery and IPX7 waterproof rating",
                "price": "$39.99",
                "original_price": "$79.99",
                "features": ["ANC Technology", "30H Battery", "IPX7 Waterproof"],
                "target_audience": "music lovers",
                "pain_points": ["poor audio quality", "short battery life", "noise interference"]
            }
        }
        
        # UGC script templates for electronics/phone accessories
        self.ugc_templates = {
            "problem_solution": """
            Hook: "I was so frustrated with [PAIN_POINT]..."
            Problem: "My [DEVICE] kept [SPECIFIC_PROBLEM] and it was driving me crazy."
            Discovery: "Then I found this [PRODUCT_NAME] from Alpapies..."
            Solution: "Now I have [BENEFIT] and [SPECIFIC_RESULT]!"
            Call to Action: "Get yours at Alpapies.com - they source directly from 1688.com so you get premium quality at amazing prices!"
            """,
            
            "before_after": """
            Hook: "Before vs After using [PRODUCT_NAME]"
            Before: "I used to struggle with [PAIN_POINT] every day..."
            After: "Now with this [PRODUCT_NAME] from Alpapies, [POSITIVE_RESULT]"
            Features: "It has [FEATURE_1], [FEATURE_2], and [FEATURE_3]"
            Value: "Only [PRICE] instead of [ORIGINAL_PRICE] - that's [DISCOUNT]% off!"
            CTA: "Check out Alpapies.com for more premium accessories sourced from 1688.com"
            """,
            
            "unboxing_review": """
            Hook: "Unboxing this [PRODUCT_NAME] from Alpapies..."
            First Impression: "The packaging looks premium and the quality feels amazing"
            Testing: "Let me test the [KEY_FEATURE]... wow, [POSITIVE_RESULT]!"
            Comparison: "This is so much better than [COMPETITOR] and costs way less"
            Value: "Only [PRICE] for something that usually costs [ORIGINAL_PRICE]"
            CTA: "Alpapies sources directly from 1688.com - same suppliers as Temu but with quality guarantee!"
            """,
            
            "lifestyle_integration": """
            Hook: "How [PRODUCT_NAME] changed my daily routine..."
            Scenario: "Every morning I [DAILY_ACTIVITY] and this makes it so much easier"
            Benefit: "Now I can [SPECIFIC_BENEFIT] without worrying about [PAIN_POINT]"
            Features: "The [KEY_FEATURE] is a game-changer for [USE_CASE]"
            Social Proof: "My friends keep asking where I got it!"
            CTA: "Get yours at Alpapies.com - premium quality from 1688.com suppliers"
            """
        }
    
    def generate_ugc_script(self, product_name: str, template_type: str = "problem_solution") -> str:
        """
        Generate a UGC script for a specific Alpapies product
        """
        if product_name not in self.alpapies_products:
            return f"Product '{product_name}' not found in Alpapies catalog"
        
        product = self.alpapies_products[product_name]
        template = self.ugc_templates.get(template_type, self.ugc_templates["problem_solution"])
        
        # Create personalized script using OpenAI
        prompt = f"""
        Create a natural, authentic UGC-style video script for the product: {product_name}
        
        Product Details:
        - Description: {product['description']}
        - Price: {product['price']} (was {product['original_price']})
        - Features: {', '.join(product['features'])}
        - Target Audience: {product['target_audience']}
        - Pain Points: {', '.join(product['pain_points'])}
        
        Template Structure:
        {template}
        
        Requirements:
        1. Sound natural and conversational (like a real customer)
        2. Highlight the 1688.com sourcing advantage (same suppliers as Temu/Shein)
        3. Emphasize the quality + price value proposition
        4. Include specific product features and benefits
        5. Keep it under 60 seconds when spoken
        6. End with clear CTA to visit Alpapies.com
        
        Make it feel authentic, not overly promotional.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a UGC content creator who makes authentic, relatable video scripts for phone accessories. Your scripts should sound like real customers sharing genuine experiences."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating script: {str(e)}"
    
    def generate_video_concept(self, product_name: str) -> Dict[str, Any]:
        """
        Generate a complete video concept including script, visual directions, and technical specs
        """
        if product_name not in self.alpapies_products:
            return {"error": f"Product '{product_name}' not found"}
        
        product = self.alpapies_products[product_name]
        
        # Generate multiple script variations
        scripts = {}
        for template_type in self.ugc_templates.keys():
            scripts[template_type] = self.generate_ugc_script(product_name, template_type)
        
        # Create visual directions
        visual_concept = f"""
        VISUAL CONCEPT for {product_name}:
        
        Setting: Modern, clean background (home office or bedroom)
        Lighting: Natural lighting or ring light for clear visibility
        Props: {product_name}, smartphone, clean surface
        
        Shot Sequence:
        1. Close-up of creator speaking to camera (hook)
        2. Product showcase - hands holding/demonstrating
        3. Feature demonstration (specific to {', '.join(product['features'])})
        4. Before/after comparison if applicable
        5. Final product shot with Alpapies branding
        
        Creator Profile:
        - Age: 25-35
        - Style: Casual, relatable
        - Tone: Enthusiastic but authentic
        - Setting: Personal space (not studio)
        """
        
        return {
            "product_name": product_name,
            "product_details": product,
            "scripts": scripts,
            "visual_concept": visual_concept,
            "technical_specs": {
                "duration": "45-60 seconds",
                "format": "Vertical (9:16) for TikTok/Instagram",
                "resolution": "1080x1920",
                "frame_rate": "30fps"
            },
            "platform_variations": {
                "TikTok": "Focus on trending sounds, quick cuts, younger audience",
                "Instagram Reels": "Aesthetic visuals, lifestyle integration",
                "Facebook": "Longer form, more detailed explanation",
                "YouTube Shorts": "Educational angle, feature breakdown"
            }
        }
    
    def generate_campaign_batch(self, num_videos: int = 5) -> List[Dict[str, Any]]:
        """
        Generate a batch of video concepts for a complete Alpapies marketing campaign
        """
        products = list(self.alpapies_products.keys())
        campaign = []
        
        for i in range(min(num_videos, len(products))):
            product = products[i]
            concept = self.generate_video_concept(product)
            campaign.append(concept)
        
        return campaign
    
    def save_campaign_to_file(self, campaign: List[Dict[str, Any]], filename: str = "alpapies_ugc_campaign.json"):
        """
        Save the generated campaign to a JSON file
        """
        try:
            with open(filename, 'w') as f:
                json.dump(campaign, f, indent=2)
            return f"Campaign saved to {filename}"
        except Exception as e:
            return f"Error saving campaign: {str(e)}"

def main():
    """
    Main function to generate Alpapies UGC campaign
    """
    print("🎬 Alpapies UGC Ad Generator")
    print("=" * 50)
    
    generator = AlpapiesUGCGenerator()
    
    # Generate campaign for all products
    print("Generating UGC campaign for Alpapies products...")
    campaign = generator.generate_campaign_batch(6)  # All 6 products
    
    # Save to file
    filename = "/home/ubuntu/alpapies_ugc_campaign.json"
    result = generator.save_campaign_to_file(campaign, filename)
    print(f"✅ {result}")
    
    # Display summary
    print(f"\n📊 Campaign Summary:")
    print(f"Total videos generated: {len(campaign)}")
    print(f"Products covered:")
    for i, concept in enumerate(campaign, 1):
        print(f"  {i}. {concept['product_name']}")
    
    print(f"\n🎯 Next Steps:")
    print(f"1. Review the generated scripts in {filename}")
    print(f"2. Use MakeUGC.ai or similar tool to create actual videos")
    print(f"3. Test ads on TikTok, Instagram, and Facebook")
    print(f"4. Track performance and optimize")
    
    return campaign

if __name__ == "__main__":
    main()

