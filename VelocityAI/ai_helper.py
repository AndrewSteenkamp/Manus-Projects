#!/usr/bin/env python3
"""
AI Helper - Supports Multiple Cheaper AI Providers
Replaces expensive OpenAI with cost-effective alternatives
"""

import os
import requests
import json
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class AIHelper:
    def __init__(self, provider="huggingface"):
        self.provider = provider
        self.setup_providers()
        print(f"🤖 AI Helper initialized with provider: {provider}")
    
    def setup_providers(self):
        """Setup configuration for different AI providers"""
        self.providers = {
            # FREE OPTION 1: Hugging Face (Free tier: 1000 requests/month)
            "huggingface": {
                "url": "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large",
                "headers": {
                    "Authorization": f"Bearer {os.getenv('HF_API_KEY', '')}"
                },
                "cost": "FREE (1000 requests/month)"
            },
            
            # FREE OPTION 2: Google Gemini (Free tier: 60 requests/minute)
            "google": {
                "url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
                "headers": {
                    "Content-Type": "application/json"
                },
                "cost": "FREE (60 requests/minute)"
            },
            
            # CHEAP OPTION 1: Anthropic Claude (Cheaper than OpenAI)
            "anthropic": {
                "url": "https://api.anthropic.com/v1/messages",
                "headers": {
                    "x-api-key": os.getenv('ANTHROPIC_API_KEY', ''),
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json"
                },
                "payload": {
                    "model": "claude-3-haiku-20240307",  # Cheapest Claude model
                    "max_tokens": 1000
                },
                "cost": "$0.25 per 1M tokens (5x cheaper than GPT-4)"
            },
            
            # COMPLETELY FREE: Local Ollama (No API costs)
            "local": {
                "url": "http://localhost:11434/api/generate",
                "headers": {
                    "Content-Type": "application/json"
                },
                "payload": {
                    "model": "llama2",
                    "stream": False
                },
                "cost": "COMPLETELY FREE (runs on your computer)"
            },
            
            # FALLBACK: OpenAI (Most expensive)
            "openai": {
                "url": "https://api.openai.com/v1/chat/completions",
                "headers": {
                    "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY', '')}",
                    "Content-Type": "application/json"
                },
                "payload": {
                    "model": "gpt-3.5-turbo",  # Cheapest OpenAI model
                    "temperature": 0.3
                },
                "cost": "$0.50 per 1M tokens"
            }
        }
    
    def generate_response(self, prompt: str, system_message: str = None) -> str:
        """Generate a response using the configured AI provider"""
        try:
            print(f"🔄 Generating response using {self.provider}...")
            
            if self.provider == "huggingface":
                return self._call_huggingface(prompt)
            elif self.provider == "google":
                return self._call_google(prompt, system_message)
            elif self.provider == "anthropic":
                return self._call_anthropic(prompt, system_message)
            elif self.provider == "local":
                return self._call_local(prompt)
            elif self.provider == "openai":
                return self._call_openai(prompt, system_message)
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")
                
        except Exception as e:
            print(f"❌ Error calling {self.provider}: {str(e)}")
            # Fallback to simple response
            return self._create_fallback_response(prompt)
    
    def _call_huggingface(self, prompt: str) -> str:
        """Call Hugging Face API (FREE)"""
        config = self.providers["huggingface"]
        
        # Use a better model for text generation
        url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
        
        payload = {"inputs": prompt}
        
        response = requests.post(
            url,
            headers=config["headers"],
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("generated_text", prompt)
            else:
                return str(result)
        else:
            raise Exception(f"HuggingFace API error: {response.status_code}")
    
    def _call_google(self, prompt: str, system_message: str = None) -> str:
        """Call Google Gemini API (FREE)"""
        config = self.providers["google"]
        
        # Add API key to URL
        url = f"{config['url']}?key={os.getenv('GOOGLE_API_KEY', '')}"
        
        # Combine system message and prompt
        full_prompt = prompt
        if system_message:
            full_prompt = f"{system_message}\n\n{prompt}"
        
        payload = {
            "contents": [{
                "parts": [{"text": full_prompt}]
            }]
        }
        
        response = requests.post(
            url,
            headers=config["headers"],
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            raise Exception(f"Google API error: {response.status_code}")
    
    def _call_anthropic(self, prompt: str, system_message: str = None) -> str:
        """Call Anthropic API (CHEAP)"""
        config = self.providers["anthropic"]
        
        messages = [{"role": "user", "content": prompt}]
        
        payload = config["payload"].copy()
        payload["messages"] = messages
        
        if system_message:
            payload["system"] = system_message
        
        response = requests.post(
            config["url"],
            headers=config["headers"],
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["content"][0]["text"]
        else:
            raise Exception(f"Anthropic API error: {response.status_code}")
    
    def _call_local(self, prompt: str) -> str:
        """Call local Ollama API (COMPLETELY FREE)"""
        config = self.providers["local"]
        
        payload = config["payload"].copy()
        payload["prompt"] = prompt
        
        try:
            response = requests.post(
                config["url"],
                headers=config["headers"],
                json=payload,
                timeout=60  # Local models can be slower
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "No response from local model")
            else:
                raise Exception(f"Local model error: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            raise Exception("Local Ollama server not running. Start it with: ollama serve")
    
    def _call_openai(self, prompt: str, system_message: str = None) -> str:
        """Call OpenAI API (EXPENSIVE - FALLBACK ONLY)"""
        config = self.providers["openai"]
        
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})
        
        payload = config["payload"].copy()
        payload["messages"] = messages
        
        response = requests.post(
            config["url"],
            headers=config["headers"],
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            raise Exception(f"OpenAI API error: {response.status_code}")
    
    def _create_fallback_response(self, prompt: str) -> str:
        """Create fallback response when AI fails"""
        
        # Simple keyword-based responses for common UGC scenarios
        prompt_lower = prompt.lower()
        
        if "script" in prompt_lower and "video" in prompt_lower:
            return """
            {
                "hook": "Hey everyone! I have to share this amazing product with you...",
                "main_content": "I've been using this product for a few weeks now and the results are incredible. It really delivers on its promises.",
                "benefits": "The main benefits I've noticed are improved quality, ease of use, and great value for money.",
                "call_to_action": "If you're interested, check out the link in my bio. You won't regret it!",
                "full_script": "Hey everyone! I have to share this amazing product with you. I've been using it for a few weeks now and the results are incredible. It really delivers on its promises. The main benefits I've noticed are improved quality, ease of use, and great value for money. If you're interested, check out the link in my bio. You won't regret it!"
            }
            """
        
        elif "decision" in prompt_lower or "approve" in prompt_lower:
            return """
            {
                "decision": "REQUEST_MORE_INFO",
                "reasoning": "Need additional information to make an informed decision",
                "confidence_score": 50,
                "risk_assessment": "Moderate risk - requires further analysis"
            }
            """
        
        elif "qualify" in prompt_lower or "lead" in prompt_lower:
            return """
            {
                "qualification_score": 65,
                "status": "qualified",
                "reasoning": "Company meets basic qualification criteria",
                "recommended_package": "growth",
                "probability_of_closing": 60
            }
            """
        
        else:
            return "AI service temporarily unavailable. Please try again or contact support."
    
    def test_connection(self) -> bool:
        """Test if the AI provider is working"""
        try:
            test_response = self.generate_response("Hello, are you working?")
            return len(test_response) > 0
        except:
            return False
    
    def get_cost_info(self) -> str:
        """Get cost information for current provider"""
        return self.providers.get(self.provider, {}).get("cost", "Cost information not available")

# Test function
def test_ai_providers():
    """Test all available AI providers"""
    providers = ["huggingface", "google", "anthropic", "local"]
    
    print("🧪 TESTING AI PROVIDERS")
    print("=" * 50)
    
    for provider in providers:
        print(f"\n🤖 Testing {provider}...")
        
        try:
            helper = AIHelper(provider=provider)
            print(f"💰 Cost: {helper.get_cost_info()}")
            
            # Test simple prompt
            response = helper.generate_response("What is 2+2? Answer in one sentence.")
            print(f"✅ Response: {response[:100]}...")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print(f"\n🎯 RECOMMENDATION: Use 'huggingface' or 'google' for free tier")

if __name__ == "__main__":
    test_ai_providers()

