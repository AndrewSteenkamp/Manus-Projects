#!/usr/bin/env python3
"""
UGC VIDEO GENERATOR - THE CORE PRODUCT
This is what actually generates the videos you sell to clients
"""

import openai
import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class UGCVideoGenerator:
    def __init__(self):
        # OpenAI setup for script generation
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        # Video generation settings
        self.video_styles = {
            'testimonial': 'Customer sharing genuine experience with product',
            'unboxing': 'Excited customer opening and reviewing product',
            'before_after': 'Customer showing transformation/results',
            'tutorial': 'Customer demonstrating how to use product',
            'lifestyle': 'Product naturally integrated into daily life',
            'comparison': 'Customer comparing product to alternatives'
        }
        
        self.avatar_types = {
            'young_female': 'Energetic 20-something female influencer style',
            'mature_female': 'Professional 30-40s female, trustworthy',
            'young_male': 'Enthusiastic 20-something male reviewer',
            'mature_male': 'Experienced 30-40s male, authoritative',
            'fitness_enthusiast': 'Athletic person, health/fitness focused',
            'beauty_guru': 'Beauty expert, makeup/skincare focused',
            'tech_reviewer': 'Tech-savvy reviewer, gadget focused',
            'mom_blogger': 'Relatable mom, family-focused products'
        }
    
    def generate_ugc_video(self, product_info, video_style='testimonial', avatar_type='young_female'):
        """
        Generate a complete UGC video for a product
        
        Args:
            product_info (dict): Product details
            video_style (str): Type of UGC video
            avatar_type (str): Type of person/avatar
            
        Returns:
            dict: Complete video package with script, visuals, and instructions
        """
        
        print(f"🎬 Generating UGC video for: {product_info.get('name', 'Unknown Product')}")
        print(f"   Style: {video_style}")
        print(f"   Avatar: {avatar_type}")
        
        # Step 1: Generate video script
        script = self.generate_video_script(product_info, video_style, avatar_type)
        
        # Step 2: Create visual instructions
        visuals = self.create_visual_instructions(product_info, video_style, script)
        
        # Step 3: Generate avatar instructions
        avatar_instructions = self.create_avatar_instructions(avatar_type, script)
        
        # Step 4: Create production notes
        production_notes = self.create_production_notes(product_info, video_style)
        
        # Package everything together
        video_package = {
            'product_info': product_info,
            'video_style': video_style,
            'avatar_type': avatar_type,
            'script': script,
            'visuals': visuals,
            'avatar_instructions': avatar_instructions,
            'production_notes': production_notes,
            'estimated_duration': self.estimate_duration(script),
            'generated_at': datetime.now().isoformat()
        }
        
        # Save video package
        self.save_video_package(video_package)
        
        print(f"✅ UGC video generated successfully!")
        print(f"   Duration: {video_package['estimated_duration']} seconds")
        print(f"   Script length: {len(script.get('full_script', ''))} characters")
        
        return video_package
    
    def generate_video_script(self, product_info, video_style, avatar_type):
        """Generate authentic UGC video script"""
        
        context = f"""
        Create an authentic UGC video script for this product:
        
        Product: {json.dumps(product_info)}
        Video Style: {video_style} - {self.video_styles.get(video_style, '')}
        Avatar: {avatar_type} - {self.avatar_types.get(avatar_type, '')}
        
        Requirements:
        1. Sound natural and conversational (not scripted)
        2. Include specific product benefits
        3. Address common pain points
        4. Include authentic emotions and reactions
        5. 30-60 seconds total duration
        6. Include call-to-action
        7. Use casual, relatable language
        8. Include specific details about the product
        
        Format the response as JSON with:
        - hook (first 3-5 seconds to grab attention)
        - main_content (product demonstration/explanation)
        - benefits (key benefits mentioned naturally)
        - social_proof (credibility elements)
        - call_to_action (what viewer should do)
        - full_script (complete script with timing)
        - key_phrases (important phrases to emphasize)
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert UGC content creator who writes authentic, converting video scripts."},
                    {"role": "user", "content": context}
                ],
                temperature=0.7  # Higher creativity for natural scripts
            )
            
            script_text = response.choices[0].message.content
            
            try:
                script = json.loads(script_text)
                return script
            except:
                # Fallback if JSON parsing fails
                return {
                    "full_script": script_text,
                    "hook": "Hey everyone! I have to share this with you...",
                    "call_to_action": f"Check out {product_info.get('name', 'this product')} - link in bio!"
                }
                
        except Exception as e:
            print(f"❌ Script generation failed: {str(e)}")
            return self.create_fallback_script(product_info, video_style)
    
    def create_visual_instructions(self, product_info, video_style, script):
        """Create detailed visual instructions for video production"""
        
        context = f"""
        Create detailed visual instructions for this UGC video:
        
        Product: {json.dumps(product_info)}
        Video Style: {video_style}
        Script: {json.dumps(script)}
        
        Provide specific visual instructions including:
        1. Camera angles and shots
        2. Lighting requirements
        3. Background/setting
        4. Product positioning
        5. Hand gestures and movements
        6. Facial expressions
        7. Props needed
        8. Shot sequence with timing
        
        Make it detailed enough for someone to follow exactly.
        Respond in JSON format.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a video production director creating detailed visual instructions."},
                    {"role": "user", "content": context}
                ],
                temperature=0.3
            )
            
            visuals_text = response.choices[0].message.content
            
            try:
                return json.loads(visuals_text)
            except:
                return {"visual_instructions": visuals_text}
                
        except Exception as e:
            print(f"❌ Visual instructions failed: {str(e)}")
            return self.create_fallback_visuals(video_style)
    
    def create_avatar_instructions(self, avatar_type, script):
        """Create specific instructions for the avatar/person in video"""
        
        context = f"""
        Create detailed avatar/performer instructions:
        
        Avatar Type: {avatar_type} - {self.avatar_types.get(avatar_type, '')}
        Script: {json.dumps(script)}
        
        Provide specific instructions for:
        1. Tone of voice and speaking style
        2. Personality traits to convey
        3. Energy level and enthusiasm
        4. Clothing/appearance suggestions
        5. Mannerisms and gestures
        6. Emotional delivery for each part
        7. Pacing and rhythm
        8. Authenticity tips
        
        Make the person feel real and relatable.
        Respond in JSON format.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a casting director creating detailed character instructions."},
                    {"role": "user", "content": context}
                ],
                temperature=0.4
            )
            
            avatar_text = response.choices[0].message.content
            
            try:
                return json.loads(avatar_text)
            except:
                return {"avatar_instructions": avatar_text}
                
        except Exception as e:
            print(f"❌ Avatar instructions failed: {str(e)}")
            return self.create_fallback_avatar(avatar_type)
    
    def create_production_notes(self, product_info, video_style):
        """Create production notes and tips"""
        
        return {
            "equipment_needed": [
                "Smartphone with good camera (iPhone 12+ or equivalent)",
                "Ring light or natural window lighting",
                "Tripod or stable surface",
                "Wireless microphone (optional but recommended)"
            ],
            "setup_tips": [
                "Film in vertical (9:16) format for social media",
                "Ensure good lighting on face",
                "Keep background simple and clean",
                "Test audio levels before recording"
            ],
            "editing_notes": [
                "Keep cuts natural and minimal",
                "Add captions for accessibility",
                "Include product close-ups",
                "Maintain authentic feel - avoid over-editing"
            ],
            "platform_specs": {
                "instagram_reels": "9:16, max 90 seconds, 1080x1920",
                "tiktok": "9:16, max 60 seconds, 1080x1920",
                "facebook": "9:16 or 16:9, max 60 seconds",
                "youtube_shorts": "9:16, max 60 seconds, 1080x1920"
            }
        }
    
    def estimate_duration(self, script):
        """Estimate video duration based on script"""
        
        full_script = script.get('full_script', '')
        word_count = len(full_script.split())
        
        # Average speaking rate: 150-160 words per minute
        # For UGC: slightly slower, more natural pace
        words_per_second = 2.5
        
        estimated_seconds = word_count / words_per_second
        
        # Add time for pauses, product shots, etc.
        estimated_seconds *= 1.3
        
        return round(estimated_seconds)
    
    def save_video_package(self, video_package):
        """Save video package to file"""
        
        # Create output directory
        os.makedirs('ugc_videos', exist_ok=True)
        
        # Generate filename
        product_name = video_package['product_info'].get('name', 'unknown_product')
        safe_name = "".join(c for c in product_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"ugc_videos/{safe_name}_{timestamp}.json"
        
        # Save to file
        with open(filename, 'w') as f:
            json.dump(video_package, f, indent=2)
        
        print(f"💾 Video package saved to: {filename}")
        
        # Also create a readable summary
        self.create_readable_summary(video_package, filename.replace('.json', '_summary.txt'))
    
    def create_readable_summary(self, video_package, filename):
        """Create human-readable summary of video package"""
        
        summary = f"""
UGC VIDEO PRODUCTION PACKAGE
Generated: {video_package['generated_at']}

PRODUCT: {video_package['product_info'].get('name', 'Unknown')}
STYLE: {video_package['video_style']}
AVATAR: {video_package['avatar_type']}
DURATION: {video_package['estimated_duration']} seconds

=== VIDEO SCRIPT ===
{video_package['script'].get('full_script', 'Script not available')}

=== KEY ELEMENTS ===
Hook: {video_package['script'].get('hook', 'Not specified')}
Call to Action: {video_package['script'].get('call_to_action', 'Not specified')}

=== VISUAL INSTRUCTIONS ===
{json.dumps(video_package['visuals'], indent=2)}

=== AVATAR INSTRUCTIONS ===
{json.dumps(video_package['avatar_instructions'], indent=2)}

=== PRODUCTION NOTES ===
Equipment: {', '.join(video_package['production_notes']['equipment_needed'])}
Format: Vertical (9:16) for social media
Lighting: Natural or ring light
Audio: Clear, close to subject

=== NEXT STEPS ===
1. Review script and make any adjustments
2. Set up filming location with good lighting
3. Practice script delivery (should sound natural, not read)
4. Film multiple takes for best result
5. Edit with captions and product close-ups
6. Export in platform-specific formats
        """
        
        with open(filename, 'w') as f:
            f.write(summary)
        
        print(f"📄 Readable summary saved to: {filename}")
    
    def create_fallback_script(self, product_info, video_style):
        """Create fallback script if AI fails"""
        
        product_name = product_info.get('name', 'this amazing product')
        
        return {
            "hook": f"Okay, I need to tell you about {product_name}...",
            "main_content": f"I've been using {product_name} for a few weeks now and honestly, I'm impressed. It really does what it says it will do.",
            "benefits": f"The main thing I love about {product_name} is how easy it is to use and the results I'm seeing.",
            "call_to_action": f"If you're interested in {product_name}, I'll put the link in my bio. Definitely worth checking out!",
            "full_script": f"Okay, I need to tell you about {product_name}. I've been using it for a few weeks now and honestly, I'm impressed. It really does what it says it will do. The main thing I love about it is how easy it is to use and the results I'm seeing. If you're interested, I'll put the link in my bio. Definitely worth checking out!"
        }
    
    def create_fallback_visuals(self, video_style):
        """Create fallback visual instructions"""
        
        return {
            "camera_setup": "Phone camera at eye level, arm's length away",
            "lighting": "Natural light from window or ring light",
            "background": "Clean, simple background - bedroom or living room",
            "shots": [
                "Close-up of face while speaking",
                "Product in hands showing details",
                "Using/demonstrating product",
                "Final shot with product and smile"
            ]
        }
    
    def create_fallback_avatar(self, avatar_type):
        """Create fallback avatar instructions"""
        
        return {
            "tone": "Conversational and authentic",
            "energy": "Enthusiastic but natural",
            "style": "Casual, relatable",
            "delivery": "Speak like talking to a friend"
        }

# EASY-TO-USE FUNCTIONS FOR GENERATING VIDEOS

def generate_single_video(product_name, product_description, product_benefits, industry="general"):
    """
    Generate a single UGC video - SIMPLE VERSION
    
    Args:
        product_name (str): Name of the product
        product_description (str): What the product does
        product_benefits (str): Main benefits/results
        industry (str): Industry category
    
    Returns:
        dict: Complete video package
    """
    
    # Create product info
    product_info = {
        "name": product_name,
        "description": product_description,
        "benefits": product_benefits,
        "industry": industry
    }
    
    # Initialize generator
    generator = UGCVideoGenerator()
    
    # Generate video
    video_package = generator.generate_ugc_video(
        product_info=product_info,
        video_style='testimonial',  # Default to testimonial
        avatar_type='young_female'  # Default avatar
    )
    
    return video_package

def generate_video_set(product_name, product_description, product_benefits, industry="general", num_videos=5):
    """
    Generate a set of different UGC videos for one product
    
    Args:
        product_name (str): Name of the product
        product_description (str): What the product does
        product_benefits (str): Main benefits/results
        industry (str): Industry category
        num_videos (int): Number of videos to generate
    
    Returns:
        list: List of video packages
    """
    
    # Create product info
    product_info = {
        "name": product_name,
        "description": product_description,
        "benefits": product_benefits,
        "industry": industry
    }
    
    # Different combinations for variety
    video_combinations = [
        ('testimonial', 'young_female'),
        ('unboxing', 'young_male'),
        ('before_after', 'mature_female'),
        ('tutorial', 'tech_reviewer'),
        ('lifestyle', 'mom_blogger'),
        ('comparison', 'mature_male'),
        ('testimonial', 'fitness_enthusiast'),
        ('unboxing', 'beauty_guru')
    ]
    
    # Initialize generator
    generator = UGCVideoGenerator()
    
    video_packages = []
    
    for i in range(min(num_videos, len(video_combinations))):
        video_style, avatar_type = video_combinations[i]
        
        print(f"\n🎬 Generating video {i+1}/{num_videos}")
        
        video_package = generator.generate_ugc_video(
            product_info=product_info,
            video_style=video_style,
            avatar_type=avatar_type
        )
        
        video_packages.append(video_package)
    
    print(f"\n✅ Generated {len(video_packages)} UGC videos!")
    return video_packages

# EXAMPLE USAGE AND TESTING

def test_video_generation():
    """Test the video generation system"""
    
    print("🧪 TESTING UGC VIDEO GENERATION")
    print("=" * 50)
    
    # Test product
    test_product = {
        "name": "HydroGlow Vitamin C Serum",
        "description": "Advanced vitamin C serum that brightens skin and reduces dark spots",
        "benefits": "Brighter skin in 7 days, reduces dark spots, improves skin texture, anti-aging",
        "industry": "beauty"
    }
    
    # Generate single video
    print("\n📹 Generating single testimonial video...")
    video = generate_single_video(
        product_name=test_product["name"],
        product_description=test_product["description"],
        product_benefits=test_product["benefits"],
        industry=test_product["industry"]
    )
    
    print(f"✅ Video generated: {video['estimated_duration']} seconds")
    print(f"📝 Script preview: {video['script'].get('hook', 'No hook available')}")
    
    # Generate video set
    print(f"\n📹 Generating set of 3 videos...")
    video_set = generate_video_set(
        product_name=test_product["name"],
        product_description=test_product["description"],
        product_benefits=test_product["benefits"],
        industry=test_product["industry"],
        num_videos=3
    )
    
    print(f"✅ Generated {len(video_set)} videos total")
    
    return video, video_set

if __name__ == "__main__":
    print("🎬 UGC VIDEO GENERATOR - CORE PRODUCT")
    print("=" * 60)
    print("This generates the actual UGC videos you sell to clients")
    print("\nMake sure you have OPENAI_API_KEY in your .env file")
    print("\nPress Enter to run test generation...")
    input()
    
    # Run test
    single_video, video_set = test_video_generation()
    
    print("\n🎉 VIDEO GENERATION TEST COMPLETE!")
    print("\nCheck the 'ugc_videos' folder for generated video packages")
    print("Each package contains:")
    print("- Complete script")
    print("- Visual instructions") 
    print("- Avatar/performer instructions")
    print("- Production notes")
    print("- Readable summary")

