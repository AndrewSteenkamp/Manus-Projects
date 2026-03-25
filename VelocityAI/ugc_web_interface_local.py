#!/usr/bin/env python3
"""
UGC VIDEO GENERATOR - LOCAL WEB INTERFACE
Simple web interface using cheaper AI alternatives
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import json
from datetime import datetime
from ugc_video_generator_local import UGCVideoGenerator, generate_single_video, generate_video_set

app = Flask(__name__)

# Create necessary directories
os.makedirs('ugc_videos', exist_ok=True)
os.makedirs('templates', exist_ok=True)

@app.route('/')
def index():
    """Main page for generating UGC videos"""
    
    # Create simple HTML template
    html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>UGC Video Generator - Local</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, textarea, select { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        textarea { height: 100px; }
        button { background: #007bff; color: white; padding: 15px 30px; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .result { margin-top: 20px; padding: 15px; border-radius: 5px; }
        .success { background: #d4edda; border: 1px solid #c3e6cb; }
        .error { background: #f8d7da; border: 1px solid #f5c6cb; }
        .provider-info { background: #e7f3ff; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <h1>🎬 UGC Video Generator - Local Version</h1>
    
    <div class="provider-info">
        <h3>💰 Cost-Effective AI Providers</h3>
        <p><strong>Current Provider:</strong> <span id="currentProvider">Loading...</span></p>
        <p><strong>Cost:</strong> <span id="providerCost">Loading...</span></p>
        <p>This local version uses cheaper AI alternatives instead of expensive OpenAI!</p>
    </div>
    
    <form id="videoForm">
        <div class="form-group">
            <label for="ai_provider">AI Provider:</label>
            <select id="ai_provider" name="ai_provider">
                <option value="huggingface">Hugging Face (FREE - 1000 requests/month)</option>
                <option value="google">Google Gemini (FREE - 60 requests/minute)</option>
                <option value="anthropic">Anthropic Claude (CHEAP - 5x cheaper than OpenAI)</option>
                <option value="local">Local Ollama (COMPLETELY FREE)</option>
            </select>
        </div>
        
        <div class="form-group">
            <label for="product_name">Product Name:</label>
            <input type="text" id="product_name" name="product_name" required placeholder="e.g., HydroGlow Vitamin C Serum">
        </div>
        
        <div class="form-group">
            <label for="product_description">Product Description:</label>
            <textarea id="product_description" name="product_description" required placeholder="Describe what the product does..."></textarea>
        </div>
        
        <div class="form-group">
            <label for="product_benefits">Product Benefits:</label>
            <textarea id="product_benefits" name="product_benefits" required placeholder="List the main benefits and results..."></textarea>
        </div>
        
        <div class="form-group">
            <label for="industry">Industry:</label>
            <select id="industry" name="industry">
                <option value="beauty">Beauty & Cosmetics</option>
                <option value="health">Health & Supplements</option>
                <option value="electronics">Electronics & Tech</option>
                <option value="fashion">Fashion & Accessories</option>
                <option value="fitness">Fitness & Sports</option>
                <option value="general">General/Other</option>
            </select>
        </div>
        
        <div class="form-group">
            <label for="num_videos">Number of Videos:</label>
            <select id="num_videos" name="num_videos">
                <option value="1">1 Video (Quick Test)</option>
                <option value="3">3 Videos</option>
                <option value="5" selected>5 Videos</option>
                <option value="8">8 Videos</option>
            </select>
        </div>
        
        <button type="submit">Generate UGC Videos</button>
    </form>
    
    <div id="result"></div>
    
    <script>
        // Update provider info
        document.getElementById('ai_provider').addEventListener('change', function() {
            const provider = this.value;
            const costs = {
                'huggingface': 'FREE (1000 requests/month)',
                'google': 'FREE (60 requests/minute)',
                'anthropic': '$0.25 per 1M tokens (5x cheaper than GPT-4)',
                'local': 'COMPLETELY FREE (runs on your computer)'
            };
            
            document.getElementById('currentProvider').textContent = provider;
            document.getElementById('providerCost').textContent = costs[provider] || 'Unknown';
        });
        
        // Trigger initial update
        document.getElementById('ai_provider').dispatchEvent(new Event('change'));
        
        // Handle form submission
        document.getElementById('videoForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const resultDiv = document.getElementById('result');
            
            // Show loading
            resultDiv.innerHTML = '<div class="result">🎬 Generating videos... This may take 1-2 minutes.</div>';
            
            fetch('/generate', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    resultDiv.innerHTML = `
                        <div class="result success">
                            <h3>✅ ${data.message}</h3>
                            <p><strong>Videos Generated:</strong> ${data.num_videos}</p>
                            <p><strong>AI Provider:</strong> ${data.ai_provider}</p>
                            <p><strong>Generation Cost:</strong> ${data.cost}</p>
                            <p><strong>Files Saved:</strong> Check 'ugc_videos' folder</p>
                        </div>
                    `;
                } else {
                    resultDiv.innerHTML = `<div class="result error">❌ ${data.error}</div>`;
                }
            })
            .catch(error => {
                resultDiv.innerHTML = `<div class="result error">❌ Error: ${error.message}</div>`;
            });
        });
    </script>
</body>
</html>
    """
    
    return html_template

@app.route('/generate', methods=['POST'])
def generate_videos():
    """Generate UGC videos using local AI"""
    
    try:
        # Get form data
        product_name = request.form.get('product_name', '').strip()
        product_description = request.form.get('product_description', '').strip()
        product_benefits = request.form.get('product_benefits', '').strip()
        industry = request.form.get('industry', 'general')
        num_videos = int(request.form.get('num_videos', 1))
        ai_provider = request.form.get('ai_provider', 'huggingface')
        
        # Validate input
        if not all([product_name, product_description, product_benefits]):
            return jsonify({
                'success': False,
                'error': 'Please fill in all required fields'
            })
        
        # Generate videos
        print(f"🎬 Generating {num_videos} videos for {product_name} using {ai_provider}")
        
        if num_videos == 1:
            video_package = generate_single_video(
                product_name=product_name,
                product_description=product_description,
                product_benefits=product_benefits,
                industry=industry,
                ai_provider=ai_provider
            )
            video_packages = [video_package]
        else:
            video_packages = generate_video_set(
                product_name=product_name,
                product_description=product_description,
                product_benefits=product_benefits,
                industry=industry,
                num_videos=num_videos,
                ai_provider=ai_provider
            )
        
        return jsonify({
            'success': True,
            'message': f'Successfully generated {len(video_packages)} UGC videos!',
            'num_videos': len(video_packages),
            'ai_provider': ai_provider,
            'cost': video_packages[0].get('generation_cost', 'Unknown') if video_packages else 'Unknown'
        })
        
    except Exception as e:
        print(f"❌ Error generating videos: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Generation failed: {str(e)}'
        })

if __name__ == '__main__':
    print("🎬 UGC VIDEO GENERATOR - LOCAL WEB INTERFACE")
    print("=" * 60)
    print("Using cost-effective AI alternatives")
    print("\nWeb interface will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)

