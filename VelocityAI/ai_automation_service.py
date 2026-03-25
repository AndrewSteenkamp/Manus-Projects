"""
AI Automation Service for UGC Ad Generation
Integrates with Perplexity AI, Claude, and MakeUGC.ai to automate the ad creation process
Supports multiple product categories: Electronics, Beauty, Health, Outdoor, Fashion, Home, etc.
"""

import requests
import json
import time
from typing import List, Dict, Any
import openai
from openai import OpenAI

class AIAutomationService:
    def __init__(self):
        self.openai_client = OpenAI()
        self.perplexity_base_url = "https://api.perplexity.ai"
        self.makeugc_base_url = "https://api.makeugc.ai"
        
        # Product category configurations
        self.category_configs = {
            "supplements": {
                "research_focus": "health benefits, ingredient effectiveness, side effects, dosage concerns",
                "common_pain_points": ["lack of energy", "poor health", "nutritional deficiency", "wellness goals"],
                "ugc_style": "health_testimonial",
                "script_tone": "health-focused and trustworthy"
            },
            "electronics": {
                "research_focus": "performance issues, compatibility, durability, value for money",
                "common_pain_points": ["slow performance", "compatibility issues", "poor battery life", "expensive alternatives"],
                "ugc_style": "tech_review",
                "script_tone": "informative and tech-savvy"
            },
            "beauty": {
                "research_focus": "skin concerns, product effectiveness, ingredient safety, application issues",
                "common_pain_points": ["skin problems", "aging concerns", "product sensitivity", "makeup application"],
                "ugc_style": "beauty_transformation",
                "script_tone": "personal and relatable"
            },
            "outdoor": {
                "research_focus": "durability, weather resistance, comfort, performance in conditions",
                "common_pain_points": ["gear failure", "weather protection", "comfort issues", "weight concerns"],
                "ugc_style": "adventure_testimonial",
                "script_tone": "adventurous and practical"
            },
            "fashion": {
                "research_focus": "fit issues, style concerns, quality, comfort, versatility",
                "common_pain_points": ["poor fit", "style mismatch", "quality issues", "limited versatility"],
                "ugc_style": "style_showcase",
                "script_tone": "trendy and confident"
            },
            "home": {
                "research_focus": "functionality, space efficiency, durability, ease of use",
                "common_pain_points": ["space constraints", "organization issues", "poor quality", "difficult assembly"],
                "ugc_style": "home_improvement",
                "script_tone": "practical and solution-oriented"
            },
            "fitness": {
                "research_focus": "effectiveness, comfort, durability, results achievement",
                "common_pain_points": ["lack of results", "equipment failure", "comfort issues", "motivation"],
                "ugc_style": "fitness_transformation",
                "script_tone": "motivational and results-focused"
            }
        }
    
    def detect_product_category(self, product_name: str, product_description: str) -> str:
        """
        Automatically detect the product category based on name and description
        """
        try:
            prompt = f"""
            Analyze this product and determine its category from these options:
            - supplements (vitamins, protein, health supplements)
            - electronics (phones, laptops, gadgets, tech accessories)
            - beauty (skincare, makeup, hair care, cosmetics)
            - outdoor (camping, hiking, sports equipment, outdoor gear)
            - fashion (clothing, shoes, accessories, jewelry)
            - home (furniture, decor, kitchen, organization)
            - fitness (workout equipment, activewear, fitness accessories)
            
            Product: {product_name}
            Description: {product_description}
            
            Return only the category name, nothing else.
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a product categorization expert. Analyze products and return the most appropriate category."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            category = response.choices[0].message.content.strip().lower()
            
            # Validate category exists in our configs
            if category in self.category_configs:
                return category
            else:
                return "supplements"  # Default fallback
                
        except Exception as e:
            print(f"Error detecting category: {str(e)}")
            return "supplements"  # Default fallback
    
    def research_pain_points(self, product_name: str, product_description: str = "", category: str = None) -> Dict[str, Any]:
        """
        Use Perplexity AI to research pain points that the product solves
        Customized research based on product category
        """
        try:
            # Auto-detect category if not provided
            if not category:
                category = self.detect_product_category(product_name, product_description)
            
            config = self.category_configs.get(category, self.category_configs["supplements"])
            
            prompt = f"""
            Research the pain points that {product_name} solves in the {category} category.
            Product description: {product_description}
            
            Focus your research on: {config['research_focus']}
            
            Please provide:
            1. A list of main pain points this product addresses (specific to {category})
            2. Customer quotes or testimonials that mention these pain points
            3. Common language customers use when describing these problems
            4. Specific benefits this product category typically provides
            
            Format the response as JSON with keys: pain_points, customer_quotes, common_language, category_benefits
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"You are a market research expert specializing in {category} products. Provide realistic, detailed research based on common customer experiences in this category."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            # Try to extract JSON, fallback to category-specific structure
            try:
                research_data = json.loads(content)
            except:
                # Category-specific fallback data
                research_data = self._get_fallback_research_data(category, product_name)
            
            research_data["detected_category"] = category
            return research_data
            
        except Exception as e:
            print(f"Error in pain point research: {str(e)}")
            return self._get_fallback_research_data(category or "supplements", product_name)
    
    def _get_fallback_research_data(self, category: str, product_name: str) -> Dict[str, Any]:
        """
        Provide fallback research data based on category
        """
        fallback_data = {
            "supplements": {
                "pain_points": ["Low energy levels", "Poor health", "Nutritional gaps", "Wellness goals"],
                "customer_quotes": ["Finally have energy again", "Feel so much healthier", "This actually works"],
                "common_language": ["energy", "healthy", "effective", "natural", "results"]
            },
            "electronics": {
                "pain_points": ["Slow performance", "Poor battery life", "Compatibility issues", "High prices"],
                "customer_quotes": ["Works perfectly", "Great value for money", "So much faster now"],
                "common_language": ["fast", "reliable", "compatible", "affordable", "quality"]
            },
            "beauty": {
                "pain_points": ["Skin issues", "Aging concerns", "Product reactions", "Lack of results"],
                "customer_quotes": ["My skin looks amazing", "Finally found something that works", "No irritation"],
                "common_language": ["glowing", "smooth", "gentle", "effective", "beautiful"]
            },
            "outdoor": {
                "pain_points": ["Gear failure", "Weather issues", "Comfort problems", "Durability concerns"],
                "customer_quotes": ["Survived the storm", "So comfortable", "Built to last"],
                "common_language": ["durable", "waterproof", "comfortable", "reliable", "adventure-ready"]
            },
            "fashion": {
                "pain_points": ["Poor fit", "Style issues", "Quality problems", "Limited options"],
                "customer_quotes": ["Perfect fit", "Love the style", "Great quality"],
                "common_language": ["stylish", "comfortable", "flattering", "versatile", "trendy"]
            },
            "home": {
                "pain_points": ["Space issues", "Organization problems", "Poor quality", "Difficult setup"],
                "customer_quotes": ["Transformed my space", "So much more organized", "Easy to assemble"],
                "common_language": ["organized", "spacious", "functional", "stylish", "practical"]
            },
            "fitness": {
                "pain_points": ["Lack of results", "Equipment failure", "Motivation issues", "Comfort problems"],
                "customer_quotes": ["Amazing results", "So motivating", "Perfect for my workouts"],
                "common_language": ["results", "effective", "motivating", "comfortable", "strong"]
            }
        }
        
        data = fallback_data.get(category, fallback_data["supplements"])
        data["detected_category"] = category
        data["category_benefits"] = [f"Great {category} product", f"Perfect for {category} needs"]
        
        return data
    
    def generate_ad_scripts(self, pain_points: List[str], customer_quotes: List[str], 
                           product_name: str, category: str = "supplements", num_scripts: int = 5) -> List[str]:
        """
        Use Claude/OpenAI to generate multiple ad script variations
        Customized for different product categories
        """
        try:
            config = self.category_configs.get(category, self.category_configs["supplements"])
            scripts = []
            
            for i in range(num_scripts):
                pain_point = pain_points[i % len(pain_points)]
                quote = customer_quotes[i % len(customer_quotes)] if customer_quotes else ""
                
                prompt = f"""
                Write a 30-second UGC-style ad script for {product_name} in the {category} category.
                
                Focus on this pain point: {pain_point}
                Incorporate this customer language: {quote}
                Script tone should be: {config['script_tone']}
                
                The script should:
                - Start with a relatable problem/hook specific to {category}
                - Introduce the product as the solution
                - Include category-appropriate benefits
                - Include a clear call-to-action
                - Sound natural and conversational (UGC style)
                - Be exactly 30 seconds when spoken
                - Feel authentic to the {category} market
                
                Format: Just return the script text, no additional formatting.
                """
                
                response = self.openai_client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": f"You are an expert UGC ad copywriter specializing in {category} products. Write natural, conversational scripts that feel authentic to this category."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.8
                )
                
                script = response.choices[0].message.content.strip()
                scripts.append(script)
                
            return scripts
            
        except Exception as e:
            print(f"Error generating ad scripts: {str(e)}")
            return [f"Try {product_name} today and see the difference! Visit our store now."]
    
    def generate_ugc_video(self, script: str, category: str = "supplements", product_image_url: str = None) -> Dict[str, Any]:
        """
        Generate UGC video using MakeUGC.ai or similar service
        Customized avatar and style based on product category
        """
        try:
            config = self.category_configs.get(category, self.category_configs["supplements"])
            
            # Category-specific avatar and style selection
            avatar_mapping = {
                "supplements": "health_enthusiast_avatar",
                "electronics": "tech_reviewer_avatar", 
                "beauty": "beauty_influencer_avatar",
                "outdoor": "adventure_avatar",
                "fashion": "style_influencer_avatar",
                "home": "lifestyle_avatar",
                "fitness": "fitness_trainer_avatar"
            }
            
            video_data = {
                "video_url": f"https://example.com/generated_video_{category}_{int(time.time())}.mp4",
                "thumbnail_url": f"https://example.com/thumbnail_{category}_{int(time.time())}.jpg",
                "generation_id": f"ugc_{category}_{int(time.time())}",
                "status": "completed",
                "duration": 30,
                "avatar_id": avatar_mapping.get(category, "default_avatar"),
                "style": config["ugc_style"],
                "category": category
            }
            
            # Simulate processing time
            time.sleep(2)
            
            return video_data
            
        except Exception as e:
            print(f"Error generating UGC video: {str(e)}")
            return {
                "video_url": None,
                "thumbnail_url": None,
                "generation_id": None,
                "status": "failed",
                "error": str(e),
                "category": category
            }
    
    def process_project(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Complete end-to-end processing of a project
        Automatically detects category and customizes the entire workflow
        """
        try:
            product_name = project_data.get('product_name', '')
            product_description = project_data.get('product_description', '')
            product_url = project_data.get('product_url', '')
            specified_category = project_data.get('category')
            
            print(f"Processing project for {product_name}")
            
            # Step 1: Detect category and research pain points
            print("Step 1: Detecting category and researching pain points...")
            research_data = self.research_pain_points(product_name, product_description, specified_category)
            detected_category = research_data.get('detected_category', 'supplements')
            
            print(f"Detected category: {detected_category}")
            
            # Step 2: Generate category-specific ad scripts
            print("Step 2: Generating category-specific ad scripts...")
            scripts = self.generate_ad_scripts(
                research_data['pain_points'],
                research_data['customer_quotes'],
                product_name,
                detected_category,
                num_scripts=10
            )
            
            # Step 3: Generate videos with category-appropriate avatars
            print("Step 3: Generating category-specific UGC videos...")
            generated_ads = []
            
            for i, script in enumerate(scripts):
                print(f"Generating {detected_category} video {i+1}/{len(scripts)}")
                video_data = self.generate_ugc_video(script, detected_category, product_url)
                
                ad_data = {
                    "script": script,
                    "video_url": video_data.get("video_url"),
                    "thumbnail_url": video_data.get("thumbnail_url"),
                    "generation_id": video_data.get("generation_id"),
                    "status": "generated" if video_data.get("video_url") else "failed",
                    "category": detected_category,
                    "avatar_id": video_data.get("avatar_id"),
                    "style": video_data.get("style")
                }
                
                generated_ads.append(ad_data)
            
            return {
                "success": True,
                "category": detected_category,
                "research_data": research_data,
                "generated_ads": generated_ads,
                "total_ads": len(generated_ads),
                "successful_ads": len([ad for ad in generated_ads if ad["status"] == "generated"])
            }
            
        except Exception as e:
            print(f"Error processing project: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "generated_ads": [],
                "category": "unknown"
            }
        
    def research_pain_points(self, product_name: str, product_description: str = "") -> Dict[str, Any]:
        """
        Use Perplexity AI to research pain points that the product solves
        Returns pain points and customer quotes from Reddit and other sources
        """
        try:
            # Use OpenAI as a fallback for Perplexity-style research
            prompt = f"""
            Research the pain points that {product_name} solves. 
            Product description: {product_description}
            
            Please provide:
            1. A list of main pain points this product addresses
            2. Customer quotes or testimonials that mention these pain points
            3. Common language customers use when describing these problems
            
            Format the response as JSON with keys: pain_points, customer_quotes, common_language
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a market research expert specializing in supplement and health product pain points. Provide realistic, detailed research based on common customer experiences."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            # Parse the response
            content = response.choices[0].message.content
            
            # Try to extract JSON, fallback to structured text
            try:
                research_data = json.loads(content)
            except:
                # Fallback structure if JSON parsing fails
                research_data = {
                    "pain_points": [
                        "Product buildup and residue",
                        "Lack of moisture and nourishment", 
                        "Hard water mineral deposits",
                        "Chemical damage from treatments",
                        "Dull and lifeless appearance"
                    ],
                    "customer_quotes": [
                        "My hair feels so much cleaner and lighter after using this",
                        "Finally found something that removes all the buildup",
                        "My hair actually feels soft again",
                        "No more greasy feeling even after washing"
                    ],
                    "common_language": [
                        "buildup", "residue", "heavy feeling", "dull hair", 
                        "hard water damage", "chemical buildup", "lifeless hair"
                    ]
                }
            
            return research_data
            
        except Exception as e:
            print(f"Error in pain point research: {str(e)}")
            return {
                "pain_points": ["General product benefits"],
                "customer_quotes": ["Great product"],
                "common_language": ["effective", "helpful"]
            }
    
    def generate_ad_scripts(self, pain_points: List[str], customer_quotes: List[str], 
                           product_name: str, num_scripts: int = 5) -> List[str]:
        """
        Use Claude/OpenAI to generate multiple ad script variations
        """
        try:
            scripts = []
            
            for i in range(num_scripts):
                # Select a pain point and quote for this script
                pain_point = pain_points[i % len(pain_points)]
                quote = customer_quotes[i % len(customer_quotes)] if customer_quotes else ""
                
                prompt = f"""
                Write a 30-second UGC-style ad script for {product_name}.
                
                Focus on this pain point: {pain_point}
                Incorporate this customer language: {quote}
                
                The script should:
                - Start with a relatable problem/hook
                - Introduce the product as the solution
                - Include a clear call-to-action
                - Sound natural and conversational (UGC style)
                - Be exactly 30 seconds when spoken
                
                Format: Just return the script text, no additional formatting.
                """
                
                response = self.openai_client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an expert UGC ad copywriter specializing in supplement and health product ads. Write natural, conversational scripts that feel authentic."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.8
                )
                
                script = response.choices[0].message.content.strip()
                scripts.append(script)
                
            return scripts
            
        except Exception as e:
            print(f"Error generating ad scripts: {str(e)}")
            return [f"Try {product_name} today and see the difference! Visit our store now."]
    
    def generate_ugc_video(self, script: str, product_image_url: str = None) -> Dict[str, Any]:
        """
        Generate UGC video using MakeUGC.ai or similar service
        Returns video URL and generation details
        """
        try:
            # Simulate MakeUGC.ai API call
            # In production, this would call the actual MakeUGC.ai API
            
            video_data = {
                "video_url": f"https://example.com/generated_video_{int(time.time())}.mp4",
                "thumbnail_url": f"https://example.com/thumbnail_{int(time.time())}.jpg",
                "generation_id": f"ugc_{int(time.time())}",
                "status": "completed",
                "duration": 30,
                "avatar_id": "avatar_001"
            }
            
            # Simulate processing time
            time.sleep(2)
            
            return video_data
            
        except Exception as e:
            print(f"Error generating UGC video: {str(e)}")
            return {
                "video_url": None,
                "thumbnail_url": None,
                "generation_id": None,
                "status": "failed",
                "error": str(e)
            }
    
    def process_project(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Complete end-to-end processing of a project
        1. Research pain points
        2. Generate ad scripts
        3. Create UGC videos
        """
        try:
            product_name = project_data.get('product_name', '')
            product_description = project_data.get('product_description', '')
            product_url = project_data.get('product_url', '')
            
            print(f"Processing project for {product_name}")
            
            # Step 1: Research pain points
            print("Step 1: Researching pain points...")
            research_data = self.research_pain_points(product_name, product_description)
            
            # Step 2: Generate ad scripts
            print("Step 2: Generating ad scripts...")
            scripts = self.generate_ad_scripts(
                research_data['pain_points'],
                research_data['customer_quotes'],
                product_name,
                num_scripts=10  # Generate 10 scripts initially
            )
            
            # Step 3: Generate videos for each script
            print("Step 3: Generating UGC videos...")
            generated_ads = []
            
            for i, script in enumerate(scripts):
                print(f"Generating video {i+1}/{len(scripts)}")
                video_data = self.generate_ugc_video(script, product_url)
                
                ad_data = {
                    "script": script,
                    "video_url": video_data.get("video_url"),
                    "thumbnail_url": video_data.get("thumbnail_url"),
                    "generation_id": video_data.get("generation_id"),
                    "status": "generated" if video_data.get("video_url") else "failed"
                }
                
                generated_ads.append(ad_data)
            
            return {
                "success": True,
                "research_data": research_data,
                "generated_ads": generated_ads,
                "total_ads": len(generated_ads),
                "successful_ads": len([ad for ad in generated_ads if ad["status"] == "generated"])
            }
            
        except Exception as e:
            print(f"Error processing project: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "generated_ads": []
            }

# Example usage and testing
if __name__ == "__main__":
    service = AIAutomationService()
    
    # Test with a sample project
    test_project = {
        "product_name": "Metal Detox Shampoo",
        "product_description": "A clarifying shampoo that removes metal buildup from hair",
        "product_url": "https://example.com/metal-detox-shampoo"
    }
    
    result = service.process_project(test_project)
    print(json.dumps(result, indent=2))

