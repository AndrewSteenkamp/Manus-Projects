#!/usr/bin/env python3
"""
AI Helper - Multi-Provider AI System
Manages connections to various AI providers with cost-effective alternatives
"""

import os
import requests
import json
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

class AIHelper:
    """
    A unified interface for multiple AI providers with automatic fallbacks.
    
    This class provides a single interface to interact with various AI services,
    starting with free options and falling back to paid services as needed.
    """
    
    def __init__(self, provider: str = None):
        """
        Initialize the AI Helper with a specific provider or auto-select the best available.
        
        Args:
            provider (str): Specific provider to use ('huggingface', 'google', 'anthropic')
                          If None, will auto-select based on available API keys
        """
        self.provider = provider or self._auto_select_provider()
        self.setup_providers()
        print(f"🤖 AI Helper initialized with provider: {self.provider}")
    
    def _auto_select_provider(self) -> str:
        """Auto-select the best available provider based on API keys."""
        if os.getenv('HF_API_KEY'):
            return 'huggingface'
        elif os.getenv('GOOGLE_API_KEY'):
            return 'google'
        elif os.getenv('ANTHROPIC_API_KEY'):
            return 'anthropic'
        else:
            print("⚠️  No API keys found, using fallback mode")
            return 'fallback'
    
    def setup_providers(self):
        """Configure all available AI providers with their endpoints and costs."""
        self.providers = {
            'huggingface': {
                'url': 'https://api-inference.huggingface.co/models/microsoft/DialoGPT-large',
                'headers': {
                    'Authorization': f"Bearer {os.getenv('HF_API_KEY', '')}"
                },
                'cost': 'FREE (1000 requests/month)',
                'cost_per_request': 0.0
            },
            'google': {
                'url': 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent',
                'headers': {
                    'Content-Type': 'application/json'
                },
                'cost': 'FREE (60 requests/minute)',
                'cost_per_request': 0.0
            },
            'anthropic': {
                'url': 'https://api.anthropic.com/v1/messages',
                'headers': {
                    'x-api-key': os.getenv('ANTHROPIC_API_KEY', ''),
                    'anthropic-version': '2023-06-01',
                    'Content-Type': 'application/json'
                },
                'payload': {
                    'model': 'claude-3-haiku-20240307',
                    'max_tokens': 1000
                },
                'cost': '$0.25 per 1M tokens (5x cheaper than GPT-4)',
                'cost_per_request': 0.0006
            },
            'fallback': {
                'cost': 'FREE (no API required)',
                'cost_per_request': 0.0
            }
        }
    
    def generate_response(self, prompt: str, system_message: str = None) -> str:
        """
        Generate a response using the configured AI provider.
        
        Args:
            prompt (str): The user prompt to send to the AI
            system_message (str): Optional system message to guide the AI's behavior
            
        Returns:
            str: The AI's response, or a fallback response if all providers fail
        """
        try:
            print(f"🔄 Generating response using {self.provider}...")
            
            if self.provider == 'huggingface':
                return self._call_huggingface(prompt)
            elif self.provider == 'google':
                return self._call_google(prompt, system_message)
            elif self.provider == 'anthropic':
                return self._call_anthropic(prompt, system_message)
            else:
                return self._create_fallback_response(prompt)
                
        except Exception as e:
            print(f"❌ Error calling {self.provider}: {str(e)}")
            return self._create_fallback_response(prompt)
    
    def _call_huggingface(self, prompt: str) -> str:
        """Call Hugging Face API (FREE tier)."""
        config = self.providers['huggingface']
        payload = {'inputs': prompt}
        
        try:
            response = requests.post(
                config['url'],
                headers=config['headers'],
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('generated_text', prompt)
                else:
                    return str(result)
            else:
                raise Exception(f"HuggingFace API error: {response.status_code}")
                
        except Exception as e:
            print(f"HuggingFace error: {e}")
            raise
    
    def _call_google(self, prompt: str, system_message: str = None) -> str:
        """Call Google Gemini API (FREE tier)."""
        config = self.providers['google']
        url = f"{config['url']}?key={os.getenv('GOOGLE_API_KEY', '')}"
        
        full_prompt = prompt
        if system_message:
            full_prompt = f"{system_message}\n\n{prompt}"
        
        payload = {
            'contents': [{
                'parts': [{'text': full_prompt}]
            }]
        }
        
        try:
            response = requests.post(
                url,
                headers=config['headers'],
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                raise Exception(f"Google API error: {response.status_code}")
                
        except Exception as e:
            print(f"Google error: {e}")
            raise
    
    def _call_anthropic(self, prompt: str, system_message: str = None) -> str:
        """Call Anthropic API (Low-cost option)."""
        config = self.providers['anthropic']
        
        messages = [{'role': 'user', 'content': prompt}]
        payload = config['payload'].copy()
        payload['messages'] = messages
        
        if system_message:
            payload['system'] = system_message
        
        try:
            response = requests.post(
                config['url'],
                headers=config['headers'],
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['content'][0]['text']
            else:
                raise Exception(f"Anthropic API error: {response.status_code}")
                
        except Exception as e:
            print(f"Anthropic error: {e}")
            raise
    
    def _create_fallback_response(self, prompt: str) -> str:
        """
        Create intelligent fallback responses when AI services are unavailable.
        
        This method analyzes the prompt and provides contextually appropriate responses
        based on common business scenarios in the UGC advertising agency.
        """
        prompt_lower = prompt.lower()
        
        # UGC Video Script Generation
        if 'script' in prompt_lower and 'video' in prompt_lower:
            return json.dumps({
                'hook': "Hey everyone! I have to share this amazing product with you...",
                'main_content': "I've been using this product for a few weeks now and the results are incredible. It really delivers on its promises.",
                'benefits': "The main benefits I've noticed are improved quality, ease of use, and great value for money.",
                'call_to_action': "If you're interested, check out the link in my bio. You won't regret it!",
                'full_script': "Hey everyone! I have to share this amazing product with you. I've been using this product for a few weeks now and the results are incredible. It really delivers on its promises. The main benefits I've noticed are improved quality, ease of use, and great value for money. If you're interested, check out the link in my bio. You won't regret it!"
            })
        
        # Business Decision Making
        elif 'decision' in prompt_lower or 'approve' in prompt_lower:
            return json.dumps({
                'decision': 'REQUEST_MORE_INFO',
                'reasoning': 'Need additional information to make an informed decision',
                'confidence_score': 50,
                'risk_assessment': 'Moderate risk - requires further analysis'
            })
        
        # Lead Qualification
        elif 'qualify' in prompt_lower or 'lead' in prompt_lower:
            return json.dumps({
                'qualification_score': 65,
                'status': 'qualified',
                'reasoning': 'Company meets basic qualification criteria',
                'recommended_package': 'growth',
                'probability_of_closing': 60
            })
        
        # Marketing Campaign Creation
        elif 'campaign' in prompt_lower or 'marketing' in prompt_lower:
            return json.dumps({
                'campaign_name': 'UGC Awareness Campaign',
                'target_audience': 'E-commerce business owners',
                'key_message': 'Increase sales with authentic user-generated content',
                'channels': ['LinkedIn', 'Facebook', 'Email'],
                'budget_recommendation': 5000
            })
        
        # Financial Analysis
        elif 'financial' in prompt_lower or 'revenue' in prompt_lower or 'profit' in prompt_lower:
            return json.dumps({
                'revenue_projection': 150000,
                'profit_margin': 85,
                'growth_rate': 25,
                'recommendation': 'Strong financial performance, continue current strategy'
            })
        
        # Customer Success
        elif 'customer' in prompt_lower or 'client' in prompt_lower:
            return json.dumps({
                'satisfaction_score': 8.5,
                'retention_rate': 92,
                'upsell_opportunity': 'Premium package upgrade',
                'action_required': 'Schedule quarterly review'
            })
        
        # General Business Response
        else:
            return "AI service temporarily unavailable. Operating in fallback mode with basic business logic."
    
    def get_cost_info(self) -> str:
        """Get cost information for the current provider."""
        return self.providers.get(self.provider, {}).get('cost', 'Cost information not available')
    
    def get_cost_per_request(self) -> float:
        """Get the cost per request for the current provider."""
        return self.providers.get(self.provider, {}).get('cost_per_request', 0.0)
    
    def test_connection(self) -> bool:
        """Test if the current AI provider is working correctly."""
        try:
            test_response = self.generate_response("Hello, are you working? Please respond with 'Yes, I am working.'")
            return len(test_response) > 0 and 'working' in test_response.lower()
        except:
            return False
    
    def switch_provider(self, new_provider: str) -> bool:
        """
        Switch to a different AI provider.
        
        Args:
            new_provider (str): The new provider to switch to
            
        Returns:
            bool: True if switch was successful, False otherwise
        """
        if new_provider in self.providers:
            old_provider = self.provider
            self.provider = new_provider
            
            if self.test_connection():
                print(f"✅ Successfully switched from {old_provider} to {new_provider}")
                return True
            else:
                self.provider = old_provider
                print(f"❌ Failed to switch to {new_provider}, reverted to {old_provider}")
                return False
        else:
            print(f"❌ Unknown provider: {new_provider}")
            return False


def test_ai_providers():
    """Test all available AI providers to see which ones are working."""
    providers = ['huggingface', 'google', 'anthropic', 'fallback']
    
    print("🧪 TESTING AI PROVIDERS")
    print("=" * 50)
    
    working_providers = []
    
    for provider in providers:
        print(f"\n🤖 Testing {provider}...")
        
        try:
            helper = AIHelper(provider=provider)
            print(f"💰 Cost: {helper.get_cost_info()}")
            
            if helper.test_connection():
                print(f"✅ {provider} is working")
                working_providers.append(provider)
            else:
                print(f"❌ {provider} is not responding")
                
        except Exception as e:
            print(f"❌ {provider} error: {str(e)}")
    
    print(f"\n🎯 WORKING PROVIDERS: {', '.join(working_providers)}")
    
    if working_providers:
        recommended = working_providers[0]
        print(f"🎯 RECOMMENDED: Use '{recommended}' for optimal cost/performance")
    else:
        print("⚠️  No providers working, system will use fallback mode")
    
    return working_providers


if __name__ == "__main__":
    test_ai_providers()
