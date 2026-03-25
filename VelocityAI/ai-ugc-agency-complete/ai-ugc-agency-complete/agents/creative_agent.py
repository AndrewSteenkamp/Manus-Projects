#!/usr/bin/env python3
"""
Creative Agent - UGC Video Content Creation
Autonomous creative operations for UGC video production and content strategy
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import sys
import os

# Add the services directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services'))
from ai_helper import AIHelper

class CreativeAgent:
    """
    The Creative Agent handles all aspects of UGC video content creation and production.
    
    Responsibilities:
    - UGC video script creation
    - Visual direction and shot planning
    - Avatar casting and direction
    - Content strategy development
    - Brand voice and messaging
    - Creative campaign planning
    - Quality assurance and review
    - Content optimization for platforms
    - Trend analysis and incorporation
    - Creative asset management
    
    The Creative Agent ensures all UGC content is engaging, authentic,
    and optimized for maximum conversion and brand alignment.
    """
    
    def __init__(self, ai_provider: str = None):
        """
        Initialize the Creative Agent with AI capabilities.
        
        Args:
            ai_provider (str): Preferred AI provider for creative generation
        """
        self.ai_helper = AIHelper(provider=ai_provider)
        self.agent_id = "CREATIVE-001"
        self.name = "Maya Thompson"
        self.role = "Creative Director"
        
        # Creative configuration
        self.video_styles = [
            "testimonial", "unboxing", "before_after", "tutorial", 
            "lifestyle", "comparison", "day_in_life", "transformation"
        ]
        
        self.avatar_types = [
            "young_female", "mature_female", "young_male", "mature_male",
            "fitness_enthusiast", "beauty_guru", "tech_reviewer", "mom_blogger"
        ]
        
        self.platform_specs = {
            "instagram_reels": {"duration": "15-30s", "aspect_ratio": "9:16", "style": "trendy"},
            "tiktok": {"duration": "15-60s", "aspect_ratio": "9:16", "style": "authentic"},
            "youtube_shorts": {"duration": "15-60s", "aspect_ratio": "9:16", "style": "engaging"},
            "facebook": {"duration": "30-60s", "aspect_ratio": "1:1", "style": "informative"}
        }
        
        # Creative metrics tracking
        self.creative_metrics = {
            "videos_created": 0,
            "scripts_generated": 0,
            "campaigns_developed": 0,
            "avg_engagement_rate": 0,
            "conversion_improvement": 0,
            "client_satisfaction": 0,
            "revision_rate": 0
        }
        
        # Content database
        self.content_library = []
        self.active_projects = []
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(f"CREATIVE-{self.agent_id}")
        
        print(f"🎨 Creative Agent '{self.name}' initialized")
        print(f"   Role: {self.role}")
        print(f"   AI Provider: {self.ai_helper.provider}")
        print(f"   Video Styles: {len(self.video_styles)} available")
        print(f"   Avatar Types: {len(self.avatar_types)} available")
    
    def create_ugc_video_package(self, project_brief: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a complete UGC video package with scripts, visuals, and production guidelines.
        
        Args:
            project_brief (Dict): Client project requirements and product information
            
        Returns:
            Dict: Complete video package with all production materials
        """
        client_name = project_brief.get("client_name", "Unknown Client")
        product_name = project_brief.get("product_name", "Unknown Product")
        video_count = project_brief.get("video_count", 3)
        
        self.logger.info(f"Creating UGC video package for {client_name}: {product_name} ({video_count} videos)")
        
        context_prompt = f"""
        As a creative director, create a comprehensive UGC video package:
        
        PROJECT BRIEF:
        {json.dumps(project_brief, indent=2)}
        
        PACKAGE REQUIREMENTS:
        - Number of videos: {video_count}
        - Target platforms: Instagram Reels, TikTok, YouTube Shorts
        - Video length: 15-60 seconds each
        - Style: Authentic, engaging, conversion-focused
        
        CREATIVE STRATEGY:
        - Focus on authentic user experiences
        - Highlight key product benefits
        - Include social proof elements
        - Create emotional connection
        - Drive clear call-to-action
        
        For each video, create:
        1. Video concept and hook
        2. Complete script (30-60 seconds)
        3. Visual shot list and directions
        4. Avatar casting requirements
        5. Props and setup instructions
        6. Platform-specific optimizations
        7. Performance expectations
        
        Also include:
        - Overall campaign strategy
        - Brand voice guidelines
        - Hashtag recommendations
        - Testing and optimization plan
        
        Make each video unique while maintaining brand consistency.
        Respond in JSON format with detailed video specifications.
        """
        
        system_message = """You are Maya Thompson, an award-winning creative director with 10 years experience in digital content and UGC campaigns. 
        You specialize in creating authentic, high-converting video content that resonates with target audiences. 
        You balance creativity with performance marketing principles."""
        
        try:
            response = self.ai_helper.generate_response(context_prompt, system_message)
            video_package = self._parse_video_package_response(response)
            
            # Create project record
            project_record = {
                "id": f"PROJ-{len(self.active_projects) + 1:04d}",
                "client_name": client_name,
                "product_name": product_name,
                "brief": project_brief,
                "package": video_package,
                "created_date": datetime.now().isoformat(),
                "status": "created",
                "delivery_date": (datetime.now() + timedelta(hours=48)).isoformat()
            }
            
            self.active_projects.append(project_record)
            
            # Update metrics
            self.creative_metrics["videos_created"] += video_count
            self.creative_metrics["scripts_generated"] += video_count
            self.creative_metrics["campaigns_developed"] += 1
            
            self.logger.info(f"UGC video package created: {video_count} videos for {client_name}")
            return project_record
            
        except Exception as e:
            self.logger.error(f"Error creating UGC video package: {str(e)}")
            return self._create_fallback_video_package(project_brief)
    
    def generate_video_script(self, script_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a detailed UGC video script with timing and directions.
        
        Args:
            script_requirements (Dict): Script specifications and product details
            
        Returns:
            Dict: Complete video script with timing and production notes
        """
        product_name = script_requirements.get("product_name", "Unknown Product")
        video_style = script_requirements.get("video_style", "testimonial")
        
        self.logger.info(f"Generating video script: {product_name} ({video_style} style)")
        
        context_prompt = f"""
        As a creative director, write a compelling UGC video script:
        
        SCRIPT REQUIREMENTS:
        {json.dumps(script_requirements, indent=2)}
        
        SCRIPT STRUCTURE:
        
        HOOK (0-3 seconds):
        - Attention-grabbing opening
        - Pattern interrupt or curiosity gap
        - Visual or verbal hook
        
        PROBLEM/SETUP (3-8 seconds):
        - Identify viewer's pain point
        - Create relatability
        - Set up the solution
        
        SOLUTION/PRODUCT (8-25 seconds):
        - Introduce the product naturally
        - Show product in use
        - Highlight key benefits
        - Include social proof if applicable
        
        RESULTS/TRANSFORMATION (25-40 seconds):
        - Show the outcome/results
        - Before/after if applicable
        - Emotional payoff
        
        CALL TO ACTION (40-50 seconds):
        - Clear next step
        - Create urgency if appropriate
        - Include discount/offer if available
        
        SCRIPT ELEMENTS:
        - Natural, conversational tone
        - Authentic language (avoid sales-speak)
        - Emotional triggers
        - Visual cues and directions
        - Timing markers
        - Platform-specific optimizations
        
        Provide:
        1. Complete script with timing
        2. Visual directions for each segment
        3. Props and setup requirements
        4. Avatar performance notes
        5. Platform variations (Instagram vs TikTok)
        6. Alternative hooks for A/B testing
        
        Respond in JSON format.
        """
        
        try:
            response = self.ai_helper.generate_response(context_prompt)
            script = self._parse_script_response(response)
            
            # Add to content library
            script_record = {
                "id": f"SCRIPT-{len(self.content_library) + 1:04d}",
                "product_name": product_name,
                "video_style": video_style,
                "script": script,
                "created_date": datetime.now().isoformat(),
                "usage_count": 0
            }
            
            self.content_library.append(script_record)
            self.creative_metrics["scripts_generated"] += 1
            
            self.logger.info(f"Video script generated: {product_name} ({video_style})")
            return script_record
            
        except Exception as e:
            self.logger.error(f"Error generating video script: {str(e)}")
            return self._create_fallback_script(script_requirements)
    
    def develop_creative_strategy(self, campaign_brief: Dict[str, Any]) -> Dict[str, Any]:
        """
        Develop comprehensive creative strategy for a UGC campaign.
        
        Args:
            campaign_brief (Dict): Campaign objectives and brand information
            
        Returns:
            Dict: Complete creative strategy with guidelines and recommendations
        """
        brand_name = campaign_brief.get("brand_name", "Unknown Brand")
        campaign_goal = campaign_brief.get("goal", "increase_conversions")
        
        self.logger.info(f"Developing creative strategy for {brand_name}: {campaign_goal}")
        
        context_prompt = f"""
        As a creative strategist, develop a comprehensive UGC creative strategy:
        
        CAMPAIGN BRIEF:
        {json.dumps(campaign_brief, indent=2)}
        
        STRATEGIC FRAMEWORK:
        
        BRAND ANALYSIS:
        - Brand personality and voice
        - Target audience psychographics
        - Competitive landscape
        - Unique value propositions
        
        CREATIVE POSITIONING:
        - Core message architecture
        - Emotional drivers
        - Rational benefits
        - Social proof strategy
        
        CONTENT STRATEGY:
        - Video style mix and ratios
        - Avatar diversity and casting
        - Storytelling approaches
        - Visual style guidelines
        
        PLATFORM OPTIMIZATION:
        - Platform-specific adaptations
        - Format and timing considerations
        - Hashtag and discovery strategy
        - Community engagement approach
        
        PERFORMANCE OPTIMIZATION:
        - A/B testing framework
        - Success metrics and KPIs
        - Iteration and improvement process
        - Scaling strategies
        
        Develop strategy including:
        1. Creative brief and guidelines
        2. Content calendar recommendations
        3. Avatar casting specifications
        4. Visual style guide
        5. Messaging framework
        6. Testing and optimization plan
        7. Success metrics and benchmarks
        8. Budget allocation recommendations
        
        Respond in JSON format.
        """
        
        try:
            response = self.ai_helper.generate_response(context_prompt)
            strategy = self._parse_strategy_response(response)
            
            # Create strategy record
            strategy_record = {
                "id": f"STRAT-{len(self.active_projects) + 1:04d}",
                "brand_name": brand_name,
                "campaign_goal": campaign_goal,
                "brief": campaign_brief,
                "strategy": strategy,
                "created_date": datetime.now().isoformat(),
                "status": "active"
            }
            
            self.creative_metrics["campaigns_developed"] += 1
            
            self.logger.info(f"Creative strategy developed for {brand_name}")
            return strategy_record
            
        except Exception as e:
            self.logger.error(f"Error developing creative strategy: {str(e)}")
            return self._create_fallback_strategy(campaign_brief)
    
    def optimize_content_performance(self, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze content performance and provide optimization recommendations.
        
        Args:
            performance_data (Dict): Video performance metrics and analytics
            
        Returns:
            Dict: Optimization recommendations and next steps
        """
        self.logger.info("Optimizing content performance based on analytics")
        
        context_prompt = f"""
        As a creative director, analyze content performance and provide optimization recommendations:
        
        PERFORMANCE DATA:
        {json.dumps(performance_data, indent=2)}
        
        ANALYSIS FRAMEWORK:
        
        ENGAGEMENT METRICS:
        - View rates and completion rates
        - Like, comment, share ratios
        - Click-through rates
        - Conversion rates
        
        CONTENT ANALYSIS:
        - Top-performing video styles
        - Most effective hooks and CTAs
        - Optimal video length and pacing
        - Avatar performance comparison
        
        PLATFORM PERFORMANCE:
        - Platform-specific insights
        - Audience behavior differences
        - Timing and posting optimization
        - Algorithm performance factors
        
        CREATIVE INSIGHTS:
        - Visual elements that drive engagement
        - Messaging that resonates
        - Emotional triggers that convert
        - Authenticity factors
        
        Provide recommendations for:
        1. Content optimization priorities
        2. Creative direction adjustments
        3. Avatar and casting improvements
        4. Script and messaging refinements
        5. Visual and production upgrades
        6. Platform-specific adaptations
        7. Testing and iteration plan
        8. Performance benchmarking
        
        Focus on actionable insights that will improve conversion rates.
        Respond in JSON format.
        """
        
        try:
            response = self.ai_helper.generate_response(context_prompt)
            optimization = self._parse_optimization_response(response)
            
            # Update performance metrics
            if "avg_engagement_rate" in performance_data:
                self.creative_metrics["avg_engagement_rate"] = performance_data["avg_engagement_rate"]
            
            if "conversion_improvement" in performance_data:
                self.creative_metrics["conversion_improvement"] = performance_data["conversion_improvement"]
            
            self.logger.info("Content performance optimization complete")
            return optimization
            
        except Exception as e:
            self.logger.error(f"Error optimizing content performance: {str(e)}")
            return self._create_fallback_optimization()
    
    def manage_creative_quality(self, content_review: Dict[str, Any]) -> Dict[str, Any]:
        """
        Review and ensure quality standards for all creative content.
        
        Args:
            content_review (Dict): Content to review and quality criteria
            
        Returns:
            Dict: Quality assessment and approval/revision recommendations
        """
        content_id = content_review.get("content_id", "Unknown")
        content_type = content_review.get("content_type", "video_script")
        
        self.logger.info(f"Reviewing creative quality for {content_id} ({content_type})")
        
        context_prompt = f"""
        As a creative director, review this content for quality and brand alignment:
        
        CONTENT REVIEW:
        {json.dumps(content_review, indent=2)}
        
        QUALITY CRITERIA:
        
        CREATIVE EXCELLENCE:
        - Originality and creativity
        - Emotional impact and engagement
        - Visual appeal and production value
        - Storytelling effectiveness
        
        BRAND ALIGNMENT:
        - Brand voice and tone consistency
        - Message clarity and accuracy
        - Visual brand guidelines adherence
        - Target audience appropriateness
        
        PERFORMANCE POTENTIAL:
        - Conversion optimization
        - Platform best practices
        - Call-to-action effectiveness
        - Social proof integration
        
        TECHNICAL QUALITY:
        - Script clarity and flow
        - Visual direction completeness
        - Production feasibility
        - Platform specifications compliance
        
        Provide assessment including:
        1. Overall quality score (0-100)
        2. Strengths and creative highlights
        3. Areas for improvement
        4. Specific revision recommendations
        5. Brand alignment assessment
        6. Performance predictions
        7. Approval status (APPROVED/REVISIONS_NEEDED/REJECTED)
        8. Next steps and timeline
        
        Be constructive but maintain high standards.
        Respond in JSON format.
        """
        
        try:
            response = self.ai_helper.generate_response(context_prompt)
            quality_review = self._parse_quality_response(response)
            
            # Track revision rates
            if quality_review.get("approval_status") == "REVISIONS_NEEDED":
                self.creative_metrics["revision_rate"] += 1
            
            self.logger.info(f"Quality review complete for {content_id}: {quality_review.get('approval_status', 'Unknown')}")
            return quality_review
            
        except Exception as e:
            self.logger.error(f"Error reviewing creative quality: {str(e)}")
            return self._create_fallback_quality_review()
    
    def get_creative_dashboard(self) -> Dict[str, Any]:
        """
        Generate creative performance dashboard.
        
        Returns:
            Dict: Comprehensive creative dashboard data
        """
        return {
            "timestamp": datetime.now().isoformat(),
            "creative_metrics": self.creative_metrics,
            "active_projects": len(self.active_projects),
            "content_library_size": len(self.content_library),
            "video_styles_available": len(self.video_styles),
            "avatar_types_available": len(self.avatar_types),
            "platform_specs": list(self.platform_specs.keys()),
            "recent_projects": [
                {
                    "id": project["id"],
                    "client": project["client_name"],
                    "status": project["status"],
                    "created": project["created_date"]
                }
                for project in self.active_projects[-5:]  # Last 5 projects
            ],
            "ai_provider": self.ai_helper.provider,
            "cost_per_video": self.ai_helper.get_cost_per_request() * 3  # Estimated cost per video
        }
    
    def _parse_video_package_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response for video package creation."""
        try:
            return json.loads(response)
        except:
            return self._create_fallback_video_package({})
    
    def _parse_script_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response for script generation."""
        try:
            return json.loads(response)
        except:
            return self._create_fallback_script({})
    
    def _parse_strategy_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response for strategy development."""
        try:
            return json.loads(response)
        except:
            return self._create_fallback_strategy({})
    
    def _parse_optimization_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response for performance optimization."""
        try:
            return json.loads(response)
        except:
            return self._create_fallback_optimization()
    
    def _parse_quality_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response for quality review."""
        try:
            return json.loads(response)
        except:
            return self._create_fallback_quality_review()
    
    def _create_fallback_video_package(self, brief: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback video package when AI is unavailable."""
        video_count = brief.get("video_count", 3)
        
        return {
            "id": f"PROJ-{len(self.active_projects) + 1:04d}",
            "client_name": brief.get("client_name", "Unknown Client"),
            "product_name": brief.get("product_name", "Unknown Product"),
            "package": {
                "video_count": video_count,
                "videos": [
                    {
                        "id": f"VIDEO-{i+1}",
                        "style": "testimonial",
                        "script": "AI unavailable - manual script creation required",
                        "duration": "30 seconds",
                        "platform": "Instagram Reels"
                    }
                    for i in range(video_count)
                ],
                "strategy": "Focus on authentic user experiences and clear benefits"
            },
            "status": "needs_manual_review"
        }
    
    def _create_fallback_script(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback script when AI is unavailable."""
        return {
            "id": f"SCRIPT-{len(self.content_library) + 1:04d}",
            "product_name": requirements.get("product_name", "Unknown Product"),
            "script": {
                "hook": "Hey everyone! I have to share this with you...",
                "problem": "I was struggling with [problem]...",
                "solution": "Then I found [product] and everything changed...",
                "results": "Now I [positive outcome]...",
                "cta": "Check it out using my link below!",
                "full_script": "AI unavailable - manual script creation required"
            },
            "status": "needs_manual_completion"
        }
    
    def _create_fallback_strategy(self, brief: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback strategy when AI is unavailable."""
        return {
            "id": f"STRAT-{len(self.active_projects) + 1:04d}",
            "brand_name": brief.get("brand_name", "Unknown Brand"),
            "strategy": {
                "core_message": "Authentic experiences with real results",
                "target_audience": "Primary demographic interested in the product",
                "content_mix": "70% testimonials, 20% tutorials, 10% lifestyle",
                "success_metrics": ["Engagement rate", "Conversion rate", "Brand awareness"]
            },
            "status": "needs_manual_development"
        }
    
    def _create_fallback_optimization(self) -> Dict[str, Any]:
        """Create fallback optimization when AI is unavailable."""
        return {
            "recommendations": [
                "Review top-performing content manually",
                "A/B test different hooks and CTAs",
                "Optimize video length based on platform",
                "Improve avatar casting and diversity"
            ],
            "priority_actions": [
                "Analyze engagement metrics",
                "Test new creative approaches",
                "Optimize for platform algorithms"
            ]
        }
    
    def _create_fallback_quality_review(self) -> Dict[str, Any]:
        """Create fallback quality review when AI is unavailable."""
        return {
            "quality_score": 75,
            "approval_status": "NEEDS_MANUAL_REVIEW",
            "strengths": ["Creative concept", "Brand alignment"],
            "improvements": ["Manual review required", "Check technical specifications"],
            "next_steps": ["Conduct manual quality assessment", "Verify brand guidelines"]
        }


def test_creative_agent():
    """Test the Creative Agent functionality."""
    print("🧪 Testing Creative Agent...")
    
    # Initialize Creative Agent
    creative = CreativeAgent()
    
    # Test UGC video package creation
    project_brief = {
        "client_name": "VitaBoost Supplements",
        "product_name": "Omega-3 Fish Oil",
        "product_category": "Health & Supplements",
        "video_count": 3,
        "target_audience": "Health-conscious adults 25-45",
        "key_benefits": ["Heart health", "Brain function", "Joint support"],
        "brand_voice": "Trustworthy, scientific, approachable"
    }
    
    video_package = creative.create_ugc_video_package(project_brief)
    print(f"✅ Video Package Created: {video_package['id']} for {video_package['client_name']}")
    
    # Test script generation
    script_requirements = {
        "product_name": "Omega-3 Fish Oil",
        "video_style": "testimonial",
        "duration": "30 seconds",
        "platform": "instagram_reels",
        "key_message": "Improved energy and focus"
    }
    
    script = creative.generate_video_script(script_requirements)
    print(f"✅ Script Generated: {script['id']} ({script['video_style']} style)")
    
    # Test creative dashboard
    dashboard = creative.get_creative_dashboard()
    print(f"✅ Creative Dashboard: {dashboard['active_projects']} active projects")
    
    print("🎨 Creative Agent test complete!")
    return creative


if __name__ == "__main__":
    test_creative_agent()
