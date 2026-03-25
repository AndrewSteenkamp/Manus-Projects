#!/usr/bin/env python3
"""
UGC VIDEO GENERATOR - LOCAL VERSION WITH CHEAP AI
Uses cost-effective AI alternatives instead of expensive OpenAI
"""

import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
from ai_helper import AIHelper

load_dotenv()

class UGCVideoGenerator:
    def __init__(self, ai_provider="huggingface"):
        # Initialize with cheaper AI provider
        self.ai_helper = AIHelper(provider=ai_provider)
        
        print(f"🎬 UGC Video Generator initialized")
        print(f"🤖 AI Provider: {ai_provider}")
        print(f"💰 Cost: {self.ai_helper.get_cost_info()}")
        
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
        """Generate a complete UGC video for a product"""
        
        print(f"🎬 Generating UGC video for: {product_info.get('name', 'Unknown Product')}")
        print(f"   Style: {video_style}")
        print(f"   Avatar: {avatar_type}")
        
        try:
            # Step 1: Generate video script using cheaper AI
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
                'generated_at': datetime.now().isoformat(),
                'ai_provider': self.ai_helper.provider,
                'generation_cost': self.ai_helper.get_cost_info()
            }
            
            # Save video package
            self.save_video_package(video_package)
            
            print(f"✅ UGC video generated successfully!")
            print(f"   Duration: {video_package['estimated_duration']} seconds")
            print(f"   AI Provider: {video_package['ai_provider']}")
            
            return video_package
            
        except Exception as e:
            print(f"❌ Video generation failed: {str(e)}")
            return self.create_fallback_video_package(product_info, video_style, avatar_type)
    
    def generate_video_script(self, product_info, video_style, avatar_type):
        """Generate authentic UGC video script using cheaper AI"""
        
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
            system_message = "You are an expert UGC content creator who writes authentic, converting video scripts."
            script_text = self.ai_helper.generate_response(context, system_message)
            
            try:
                script = json.loads(script_text)
                return script
            except:
                # Fallback if JSON parsing fails
                return self.create_fallback_script(product_info, video_style)
                
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
            system_message = "You are a video production director creating detailed visual instructions."
            visuals_text = self.ai_helper.generate_response(context, system_message)
            
            try:
                return json.loads(visuals_text)
            except:
                return self.create_fallback_visuals(video_style)
                
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
            system_message = "You are a casting director creating detailed character instructions."
            avatar_text = self.ai_helper.generate_response(context, system_message)
            
            try:
                return json.loads(avatar_text)
            except:
                return self.create_fallback_avatar(avatar_type)
                
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
AI Provider: {video_package['ai_provider']}
Generation Cost: {video_package['generation_cost']}

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
    
    def create_fallback_video_package(self, product_info, video_style, avatar_type):
        """Create fallback video package when AI completely fails"""
        
        return {
            'product_info': product_info,
            'video_style': video_style,
            'avatar_type': avatar_type,
            'script': self.create_fallback_script(product_info, video_style),
            'visuals': self.create_fallback_visuals(video_style),
            'avatar_instructions': self.create_fallback_avatar(avatar_type),
            'production_notes': self.create_production_notes(product_info, video_style),
            'estimated_duration': 45,
            'generated_at': datetime.now().isoformat(),
            'ai_provider': 'fallback',
            'generation_cost': 'FREE (fallback mode)'
        }

# EASY-TO-USE FUNCTIONS

def generate_single_video(product_name, product_description, product_benefits, industry="general", ai_provider="huggingface"):
    """Generate a single UGC video with cheaper AI"""
    
    product_info = {
        "name": product_name,
        "description": product_description,
        "benefits": product_benefits,
        "industry": industry
    }
    
    generator = UGCVideoGenerator(ai_provider=ai_provider)
    
    video_package = generator.generate_ugc_video(
        product_info=product_info,
        video_style='testimonial',
        avatar_type='young_female'
    )
    
    return video_package

def generate_video_set(product_name, product_description, product_benefits, industry="general", num_videos=5, ai_provider="huggingface"):
    """Generate a set of different UGC videos using cheaper AI"""
    
    product_info = {
        "name": product_name,
        "description": product_description,
        "benefits": product_benefits,
        "industry": industry
    }
    
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
    
    generator = UGCVideoGenerator(ai_provider=ai_provider)
    
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

# TEST FUNCTION

def test_local_video_generation():
    """Test the local video generation system"""
    
    print("🧪 TESTING LOCAL UGC VIDEO GENERATION")
    print("=" * 60)
    
    # Test product
    test_product = {
        "name": "HydroGlow Vitamin C Serum",
        "description": "Advanced vitamin C serum that brightens skin and reduces dark spots",
        "benefits": "Brighter skin in 7 days, reduces dark spots, improves skin texture, anti-aging",
        "industry": "beauty"
    }
    
    # Test different AI providers
    providers_to_test = ["huggingface", "google"]  # Start with free options
    
    for provider in providers_to_test:
        print(f"\n🤖 Testing with {provider} provider...")
        
        try:
            # Generate single video
            video = generate_single_video(
                product_name=test_product["name"],
                product_description=test_product["description"],
                product_benefits=test_product["benefits"],
                industry=test_product["industry"],
                ai_provider=provider
            )
            
            print(f"✅ Video generated with {provider}")
            print(f"   Duration: {video['estimated_duration']} seconds")
            print(f"   Cost: {video['generation_cost']}")
            print(f"   Script preview: {video['script'].get('hook', 'No hook available')[:100]}...")
            
        except Exception as e:
            print(f"❌ Failed with {provider}: {str(e)}")
    
    return True

if __name__ == "__main__":
    print("🎬 UGC VIDEO GENERATOR - LOCAL VERSION")
    print("=" * 60)
    print("Using cost-effective AI alternatives instead of expensive OpenAI")
    print("\nPress Enter to run test generation...")
    input()
    
    # Run test
    test_local_video_generation()
    
    print("\n🎉 LOCAL VIDEO GENERATION TEST COMPLETE!")
    print("\nCheck the 'ugc_videos' folder for generated video packages")

