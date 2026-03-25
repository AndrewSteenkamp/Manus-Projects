#!/usr/bin/env python3
"""
UGC VIDEO GENERATOR - WEB INTERFACE
Simple web interface to generate UGC videos for clients
"""

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
import os
import json
from datetime import datetime
from ugc_video_generator import UGCVideoGenerator, generate_single_video, generate_video_set
import zipfile
import io

app = Flask(__name__)

# Create necessary directories
os.makedirs('ugc_videos', exist_ok=True)
os.makedirs('client_deliveries', exist_ok=True)
os.makedirs('templates', exist_ok=True)

# Initialize UGC generator
ugc_generator = UGCVideoGenerator()

@app.route('/')
def index():
    """Main page for generating UGC videos"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_videos():
    """Generate UGC videos based on form input"""
    
    try:
        # Get form data
        product_name = request.form.get('product_name', '').strip()
        product_description = request.form.get('product_description', '').strip()
        product_benefits = request.form.get('product_benefits', '').strip()
        industry = request.form.get('industry', 'general')
        num_videos = int(request.form.get('num_videos', 5))
        client_name = request.form.get('client_name', '').strip()
        
        # Validate input
        if not all([product_name, product_description, product_benefits]):
            return jsonify({
                'success': False,
                'error': 'Please fill in all required fields'
            })
        
        # Generate videos
        print(f"🎬 Generating {num_videos} videos for {product_name}")
        
        video_packages = generate_video_set(
            product_name=product_name,
            product_description=product_description,
            product_benefits=product_benefits,
            industry=industry,
            num_videos=num_videos
        )
        
        # Create client delivery package
        delivery_package = create_client_delivery(
            video_packages=video_packages,
            client_name=client_name,
            product_name=product_name
        )
        
        return jsonify({
            'success': True,
            'message': f'Successfully generated {len(video_packages)} UGC videos!',
            'num_videos': len(video_packages),
            'delivery_package': delivery_package,
            'download_url': f'/download/{delivery_package["package_id"]}'
        })
        
    except Exception as e:
        print(f"❌ Error generating videos: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Generation failed: {str(e)}'
        })

@app.route('/quick-generate', methods=['POST'])
def quick_generate():
    """Quick generate single video for testing"""
    
    try:
        data = request.get_json()
        
        product_name = data.get('product_name', 'Test Product')
        product_description = data.get('product_description', 'Amazing product that solves problems')
        
        # Generate single video
        video_package = generate_single_video(
            product_name=product_name,
            product_description=product_description,
            product_benefits="Great results, easy to use, high quality",
            industry="general"
        )
        
        return jsonify({
            'success': True,
            'video': {
                'script': video_package['script'].get('full_script', ''),
                'hook': video_package['script'].get('hook', ''),
                'duration': video_package['estimated_duration'],
                'style': video_package['video_style'],
                'avatar': video_package['avatar_type']
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/download/<package_id>')
def download_package(package_id):
    """Download client delivery package"""
    
    package_path = f'client_deliveries/{package_id}.zip'
    
    if os.path.exists(package_path):
        return send_file(package_path, as_attachment=True)
    else:
        return "Package not found", 404

@app.route('/preview/<package_id>')
def preview_package(package_id):
    """Preview client delivery package"""
    
    info_path = f'client_deliveries/{package_id}_info.json'
    
    if os.path.exists(info_path):
        with open(info_path, 'r') as f:
            package_info = json.load(f)
        
        return render_template('preview.html', package=package_info)
    else:
        return "Package not found", 404

def create_client_delivery(video_packages, client_name, product_name):
    """Create professional client delivery package"""
    
    # Generate package ID
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_client = "".join(c for c in client_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_product = "".join(c for c in product_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    package_id = f"{safe_client}_{safe_product}_{timestamp}".replace(' ', '_')
    
    # Create delivery package info
    package_info = {
        'package_id': package_id,
        'client_name': client_name,
        'product_name': product_name,
        'num_videos': len(video_packages),
        'generated_at': datetime.now().isoformat(),
        'videos': []
    }
    
    # Create ZIP file for delivery
    zip_path = f'client_deliveries/{package_id}.zip'
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        
        # Add cover letter
        cover_letter = create_cover_letter(client_name, product_name, len(video_packages))
        zipf.writestr('00_COVER_LETTER.txt', cover_letter)
        
        # Add production guide
        production_guide = create_production_guide()
        zipf.writestr('00_PRODUCTION_GUIDE.txt', production_guide)
        
        # Add each video package
        for i, video_package in enumerate(video_packages, 1):
            
            # Create video folder name
            video_style = video_package['video_style']
            avatar_type = video_package['avatar_type']
            folder_name = f"Video_{i:02d}_{video_style}_{avatar_type}"
            
            # Add script file
            script_content = create_script_file(video_package)
            zipf.writestr(f'{folder_name}/SCRIPT.txt', script_content)
            
            # Add visual instructions
            visual_content = create_visual_file(video_package)
            zipf.writestr(f'{folder_name}/VISUAL_INSTRUCTIONS.txt', visual_content)
            
            # Add avatar instructions
            avatar_content = create_avatar_file(video_package)
            zipf.writestr(f'{folder_name}/AVATAR_INSTRUCTIONS.txt', avatar_content)
            
            # Add production notes
            production_content = create_production_file(video_package)
            zipf.writestr(f'{folder_name}/PRODUCTION_NOTES.txt', production_content)
            
            # Add to package info
            package_info['videos'].append({
                'video_number': i,
                'style': video_style,
                'avatar': avatar_type,
                'duration': video_package['estimated_duration'],
                'folder': folder_name
            })
    
    # Save package info
    with open(f'client_deliveries/{package_id}_info.json', 'w') as f:
        json.dump(package_info, f, indent=2)
    
    print(f"📦 Client delivery package created: {zip_path}")
    
    return package_info

def create_cover_letter(client_name, product_name, num_videos):
    """Create professional cover letter for client"""
    
    return f"""
VELOCITYAI MEDIA - UGC VIDEO PACKAGE DELIVERY

Dear {client_name},

Thank you for choosing VelocityAI Media for your UGC video content needs!

We're excited to deliver your custom UGC video package for {product_name}.

WHAT'S INCLUDED:
✅ {num_videos} unique UGC video concepts
✅ Complete scripts for each video
✅ Detailed visual instructions
✅ Avatar/performer guidelines
✅ Production notes and tips
✅ Platform-specific formatting guide

PACKAGE CONTENTS:
Each video folder contains everything needed to produce professional UGC content:

1. SCRIPT.txt - Complete video script with timing
2. VISUAL_INSTRUCTIONS.txt - Camera angles, lighting, shots
3. AVATAR_INSTRUCTIONS.txt - Performer guidance and style
4. PRODUCTION_NOTES.txt - Technical requirements and tips

NEXT STEPS:
1. Review all video concepts
2. Choose your favorites to produce first
3. Follow the production guide for best results
4. Contact us for any questions or revisions

PRODUCTION TIMELINE:
- Each video should take 1-2 hours to film
- Allow 2-4 hours for editing per video
- Total production time: 3-6 hours per video

SUPPORT:
If you need any clarifications, revisions, or have questions about production, 
please don't hesitate to reach out to us.

We're confident these UGC videos will drive excellent results for {product_name}!

Best regards,
The VelocityAI Media Team

---
Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
Package ID: {client_name}_{product_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}
"""

def create_production_guide():
    """Create comprehensive production guide"""
    
    return """
UGC VIDEO PRODUCTION GUIDE
Complete guide to producing professional UGC content

=== EQUIPMENT NEEDED ===
ESSENTIAL:
- Smartphone with good camera (iPhone 12+ or Android equivalent)
- Stable surface or tripod
- Good lighting (natural window light or ring light)

RECOMMENDED:
- Wireless microphone or lapel mic
- Ring light (12-18 inch)
- Phone tripod with adjustable height
- Reflector or white poster board

OPTIONAL:
- Gimbal stabilizer for smooth movement
- External microphone for better audio
- Backdrop or clean wall

=== FILMING SETUP ===
CAMERA POSITION:
- Film vertically (9:16 aspect ratio) for social media
- Position camera at eye level
- Keep phone 2-3 feet away from subject
- Ensure subject fills about 2/3 of frame

LIGHTING:
- Natural light is best - film near large window
- Avoid harsh overhead lighting
- Use ring light if filming indoors
- Ensure even lighting on face (no shadows)

AUDIO:
- Film in quiet environment
- Speak clearly and at normal volume
- Test audio levels before recording
- Use external mic if available

=== FILMING TIPS ===
BEFORE RECORDING:
- Practice script until it sounds natural
- Check lighting and audio
- Clear background of distractions
- Have product easily accessible

DURING RECORDING:
- Speak conversationally (like talking to a friend)
- Use natural gestures and expressions
- Don't worry about being perfect - authenticity is key
- Film multiple takes for best result

PERFORMANCE TIPS:
- Smile genuinely when appropriate
- Use hand gestures to emphasize points
- Vary your tone and energy
- Look directly at camera (like eye contact)

=== POST-PRODUCTION ===
EDITING BASICS:
- Keep editing minimal and natural
- Cut out long pauses or mistakes
- Add captions for accessibility
- Include product close-up shots

PLATFORM SPECIFICATIONS:
Instagram Reels: 9:16, max 90 seconds, 1080x1920
TikTok: 9:16, max 60 seconds, 1080x1920
Facebook: 9:16 or 16:9, max 60 seconds
YouTube Shorts: 9:16, max 60 seconds, 1080x1920

EDITING APPS:
Free: CapCut, InShot, iMovie
Paid: Adobe Premiere Pro, Final Cut Pro

=== QUALITY CHECKLIST ===
BEFORE PUBLISHING:
✅ Video is clear and well-lit
✅ Audio is clear and audible
✅ Script sounds natural and conversational
✅ Product is clearly visible
✅ Video length is appropriate for platform
✅ Captions are accurate (if added)
✅ Call-to-action is clear

=== COMMON MISTAKES TO AVOID ===
❌ Reading script word-for-word (sounds robotic)
❌ Poor lighting (too dark or harsh shadows)
❌ Background noise or distractions
❌ Filming horizontally for social media
❌ Speaking too fast or too slow
❌ Over-editing (losing authenticity)
❌ Forgetting call-to-action

=== TROUBLESHOOTING ===
If video looks unprofessional:
- Check lighting (most common issue)
- Ensure stable camera position
- Practice script more for natural delivery
- Simplify background

If engagement is low:
- Stronger hook in first 3 seconds
- More emotional/authentic delivery
- Better call-to-action
- Test different video styles

Remember: Authenticity beats perfection in UGC content!
"""

def create_script_file(video_package):
    """Create formatted script file"""
    
    script = video_package['script']
    
    return f"""
UGC VIDEO SCRIPT
Product: {video_package['product_info']['name']}
Style: {video_package['video_style']}
Avatar: {video_package['avatar_type']}
Duration: {video_package['estimated_duration']} seconds

=== COMPLETE SCRIPT ===
{script.get('full_script', 'Script not available')}

=== SCRIPT BREAKDOWN ===

HOOK (0-3 seconds):
{script.get('hook', 'Not specified')}

MAIN CONTENT:
{script.get('main_content', 'Not specified')}

KEY BENEFITS:
{script.get('benefits', 'Not specified')}

SOCIAL PROOF:
{script.get('social_proof', 'Not specified')}

CALL TO ACTION:
{script.get('call_to_action', 'Not specified')}

=== KEY PHRASES TO EMPHASIZE ===
{json.dumps(script.get('key_phrases', []), indent=2)}

=== DELIVERY NOTES ===
- Speak conversationally, not like reading
- Pause naturally between sections
- Emphasize key benefits with enthusiasm
- End with confident call-to-action
- Sound genuine and authentic throughout
"""

def create_visual_file(video_package):
    """Create formatted visual instructions file"""
    
    visuals = video_package['visuals']
    
    return f"""
VISUAL INSTRUCTIONS
Product: {video_package['product_info']['name']}
Style: {video_package['video_style']}

=== CAMERA SETUP ===
{visuals.get('camera_setup', 'Standard setup: phone at eye level, 2-3 feet away')}

=== LIGHTING ===
{visuals.get('lighting', 'Natural window light or ring light')}

=== BACKGROUND ===
{visuals.get('background', 'Clean, simple background')}

=== SHOT SEQUENCE ===
{json.dumps(visuals.get('shots', []), indent=2)}

=== DETAILED VISUAL INSTRUCTIONS ===
{json.dumps(visuals, indent=2)}

=== PRODUCT POSITIONING ===
- Keep product visible throughout video
- Show product details clearly
- Use natural hand movements
- Demonstrate product use if applicable

=== CAMERA MOVEMENTS ===
- Keep camera stable (use tripod if available)
- Minimal camera movement for authenticity
- Focus on subject and product
- Ensure good framing throughout
"""

def create_avatar_file(video_package):
    """Create formatted avatar instructions file"""
    
    avatar = video_package['avatar_instructions']
    
    return f"""
AVATAR/PERFORMER INSTRUCTIONS
Avatar Type: {video_package['avatar_type']}
Product: {video_package['product_info']['name']}

=== CHARACTER PROFILE ===
{json.dumps(avatar, indent=2)}

=== PERFORMANCE GUIDELINES ===

TONE OF VOICE:
- Conversational and friendly
- Enthusiastic but natural
- Authentic and relatable
- Confident in product recommendation

ENERGY LEVEL:
- Match the product and audience
- Maintain consistent energy throughout
- Show genuine excitement about product
- Stay engaged and animated

MANNERISMS:
- Use natural hand gestures
- Maintain good eye contact with camera
- Smile genuinely when appropriate
- Express authentic emotions

CLOTHING/APPEARANCE:
- Dress appropriately for target audience
- Keep styling simple and not distracting
- Ensure clothing doesn't clash with product
- Look approachable and trustworthy

=== AUTHENTICITY TIPS ===
- Speak like you're talking to a friend
- Share personal experience with product
- Use natural pauses and inflections
- Don't be afraid to show personality
- React genuinely to product benefits

=== COMMON PHRASES TO USE ===
- "I have to share this with you..."
- "Honestly, I was surprised by..."
- "The thing I love most about this is..."
- "I've been using this for [timeframe] and..."
- "You guys know I'm picky about..."
"""

def create_production_file(video_package):
    """Create formatted production notes file"""
    
    production = video_package['production_notes']
    
    return f"""
PRODUCTION NOTES
Product: {video_package['product_info']['name']}
Estimated Duration: {video_package['estimated_duration']} seconds

=== EQUIPMENT CHECKLIST ===
{chr(10).join(f"✅ {item}" for item in production['equipment_needed'])}

=== SETUP TIPS ===
{chr(10).join(f"• {tip}" for tip in production['setup_tips'])}

=== EDITING GUIDELINES ===
{chr(10).join(f"• {note}" for note in production['editing_notes'])}

=== PLATFORM SPECIFICATIONS ===
{json.dumps(production['platform_specs'], indent=2)}

=== FILMING CHECKLIST ===
BEFORE FILMING:
✅ Script practiced and natural
✅ Lighting tested and adjusted
✅ Audio levels checked
✅ Background cleared and clean
✅ Product positioned and accessible
✅ Camera stable and positioned correctly

DURING FILMING:
✅ Multiple takes recorded
✅ Audio quality monitored
✅ Product clearly visible
✅ Performance feels authentic
✅ Call-to-action delivered confidently

AFTER FILMING:
✅ Best take selected
✅ Basic editing completed
✅ Captions added if needed
✅ Platform-specific format exported
✅ Quality check completed

=== DELIVERY TIMELINE ===
- Filming: 1-2 hours
- Editing: 2-4 hours  
- Review: 30 minutes
- Total: 3-6 hours per video

=== SUCCESS METRICS ===
- Clear audio throughout
- Good lighting and visibility
- Natural, authentic performance
- Product clearly showcased
- Strong call-to-action
- Appropriate length for platform
"""

# Create HTML templates
def create_html_templates():
    """Create HTML templates for the web interface"""
    
    # Main index template
    index_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UGC Video Generator - VelocityAI Media</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f7fa; color: #333; }
        .container { max-width: 800px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; margin-bottom: 40px; }
        .header h1 { color: #2c3e50; font-size: 2.5em; margin-bottom: 10px; }
        .header p { color: #7f8c8d; font-size: 1.2em; }
        .form-container { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        .form-group { margin-bottom: 25px; }
        .form-group label { display: block; margin-bottom: 8px; font-weight: 600; color: #2c3e50; }
        .form-group input, .form-group textarea, .form-group select { width: 100%; padding: 12px; border: 2px solid #ecf0f1; border-radius: 5px; font-size: 16px; }
        .form-group input:focus, .form-group textarea:focus, .form-group select:focus { outline: none; border-color: #3498db; }
        .form-group textarea { height: 100px; resize: vertical; }
        .btn { background: #3498db; color: white; padding: 15px 30px; border: none; border-radius: 5px; font-size: 18px; cursor: pointer; width: 100%; }
        .btn:hover { background: #2980b9; }
        .btn:disabled { background: #bdc3c7; cursor: not-allowed; }
        .quick-test { background: #e8f5e8; padding: 20px; border-radius: 5px; margin-bottom: 30px; }
        .quick-test h3 { color: #27ae60; margin-bottom: 15px; }
        .quick-test-form { display: flex; gap: 10px; margin-bottom: 15px; }
        .quick-test-form input { flex: 1; }
        .quick-test-btn { background: #27ae60; padding: 10px 20px; }
        .result { margin-top: 30px; padding: 20px; border-radius: 5px; }
        .result.success { background: #d4edda; border: 1px solid #c3e6cb; color: #155724; }
        .result.error { background: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; }
        .loading { display: none; text-align: center; margin-top: 20px; }
        .video-preview { background: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 15px; }
        .video-preview h4 { color: #495057; margin-bottom: 10px; }
        .video-preview p { margin-bottom: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎬 UGC Video Generator</h1>
            <p>Generate professional UGC videos for your clients in minutes</p>
        </div>

        <div class="quick-test">
            <h3>🚀 Quick Test Generator</h3>
            <p>Test the system with a simple product:</p>
            <div class="quick-test-form">
                <input type="text" id="quickProduct" placeholder="Product name (e.g., Vitamin C Serum)" value="HydroGlow Vitamin C Serum">
                <input type="text" id="quickDescription" placeholder="What it does" value="Brightens skin and reduces dark spots">
                <button class="btn quick-test-btn" onclick="quickGenerate()">Generate Test Video</button>
            </div>
            <div id="quickResult"></div>
        </div>

        <div class="form-container">
            <h2>Generate Complete UGC Video Package</h2>
            <form id="videoForm">
                <div class="form-group">
                    <label for="client_name">Client Name *</label>
                    <input type="text" id="client_name" name="client_name" required placeholder="e.g., BeautyBrand SA">
                </div>

                <div class="form-group">
                    <label for="product_name">Product Name *</label>
                    <input type="text" id="product_name" name="product_name" required placeholder="e.g., HydroGlow Vitamin C Serum">
                </div>

                <div class="form-group">
                    <label for="product_description">Product Description *</label>
                    <textarea id="product_description" name="product_description" required placeholder="Describe what the product does, how it works, key features..."></textarea>
                </div>

                <div class="form-group">
                    <label for="product_benefits">Product Benefits *</label>
                    <textarea id="product_benefits" name="product_benefits" required placeholder="List the main benefits, results customers see, problems it solves..."></textarea>
                </div>

                <div class="form-group">
                    <label for="industry">Industry Category</label>
                    <select id="industry" name="industry">
                        <option value="beauty">Beauty & Cosmetics</option>
                        <option value="health">Health & Supplements</option>
                        <option value="electronics">Electronics & Tech</option>
                        <option value="fashion">Fashion & Accessories</option>
                        <option value="fitness">Fitness & Sports</option>
                        <option value="home">Home & Garden</option>
                        <option value="food">Food & Beverage</option>
                        <option value="general">General/Other</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="num_videos">Number of Videos</label>
                    <select id="num_videos" name="num_videos">
                        <option value="3">3 Videos</option>
                        <option value="5" selected>5 Videos</option>
                        <option value="8">8 Videos</option>
                        <option value="10">10 Videos</option>
                    </select>
                </div>

                <button type="submit" class="btn" id="generateBtn">Generate UGC Video Package</button>
            </form>

            <div class="loading" id="loading">
                <p>🎬 Generating your UGC videos... This may take 2-3 minutes.</p>
            </div>

            <div id="result"></div>
        </div>
    </div>

    <script>
        function quickGenerate() {
            const product = document.getElementById('quickProduct').value;
            const description = document.getElementById('quickDescription').value;
            const resultDiv = document.getElementById('quickResult');
            
            if (!product || !description) {
                resultDiv.innerHTML = '<div class="result error">Please fill in both fields</div>';
                return;
            }
            
            resultDiv.innerHTML = '<p>🎬 Generating test video...</p>';
            
            fetch('/quick-generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    product_name: product,
                    product_description: description
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    resultDiv.innerHTML = `
                        <div class="result success">
                            <h4>✅ Test Video Generated!</h4>
                            <div class="video-preview">
                                <h4>Video Details:</h4>
                                <p><strong>Style:</strong> ${data.video.style}</p>
                                <p><strong>Avatar:</strong> ${data.video.avatar}</p>
                                <p><strong>Duration:</strong> ${data.video.duration} seconds</p>
                                <p><strong>Hook:</strong> "${data.video.hook}"</p>
                                <p><strong>Full Script:</strong></p>
                                <p style="font-style: italic; background: white; padding: 10px; border-radius: 3px;">"${data.video.script}"</p>
                            </div>
                        </div>
                    `;
                } else {
                    resultDiv.innerHTML = `<div class="result error">❌ Error: ${data.error}</div>`;
                }
            })
            .catch(error => {
                resultDiv.innerHTML = `<div class="result error">❌ Error: ${error.message}</div>`;
            });
        }

        document.getElementById('videoForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const generateBtn = document.getElementById('generateBtn');
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');
            
            // Show loading
            generateBtn.disabled = true;
            generateBtn.textContent = 'Generating...';
            loading.style.display = 'block';
            result.innerHTML = '';
            
            fetch('/generate', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                loading.style.display = 'none';
                generateBtn.disabled = false;
                generateBtn.textContent = 'Generate UGC Video Package';
                
                if (data.success) {
                    result.innerHTML = `
                        <div class="result success">
                            <h3>🎉 ${data.message}</h3>
                            <p><strong>Videos Generated:</strong> ${data.num_videos}</p>
                            <p><strong>Client:</strong> ${data.delivery_package.client_name}</p>
                            <p><strong>Product:</strong> ${data.delivery_package.product_name}</p>
                            <p style="margin-top: 20px;">
                                <a href="${data.download_url}" class="btn" style="display: inline-block; text-decoration: none;">📦 Download Client Package</a>
                            </p>
                            <p style="margin-top: 10px;">
                                <a href="/preview/${data.delivery_package.package_id}" target="_blank">👁️ Preview Package Contents</a>
                            </p>
                        </div>
                    `;
                } else {
                    result.innerHTML = `<div class="result error">❌ ${data.error}</div>`;
                }
            })
            .catch(error => {
                loading.style.display = 'none';
                generateBtn.disabled = false;
                generateBtn.textContent = 'Generate UGC Video Package';
                result.innerHTML = `<div class="result error">❌ Error: ${error.message}</div>`;
            });
        });
    </script>
</body>
</html>
    """
    
    # Preview template
    preview_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Package Preview - {{ package.client_name }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f7fa; color: #333; line-height: 1.6; }
        .container { max-width: 1000px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; margin-bottom: 40px; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        .header h1 { color: #2c3e50; margin-bottom: 10px; }
        .package-info { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); margin-bottom: 30px; }
        .video-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .video-card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        .video-card h3 { color: #3498db; margin-bottom: 15px; }
        .video-card .meta { background: #f8f9fa; padding: 10px; border-radius: 5px; margin-bottom: 15px; }
        .video-card .meta span { display: inline-block; margin-right: 15px; font-size: 14px; }
        .btn { background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 10px; }
        .btn:hover { background: #2980b9; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📦 UGC Video Package Preview</h1>
            <p>Client delivery package for {{ package.client_name }}</p>
        </div>

        <div class="package-info">
            <h2>Package Information</h2>
            <p><strong>Client:</strong> {{ package.client_name }}</p>
            <p><strong>Product:</strong> {{ package.product_name }}</p>
            <p><strong>Videos Generated:</strong> {{ package.num_videos }}</p>
            <p><strong>Generated:</strong> {{ package.generated_at }}</p>
            <p><strong>Package ID:</strong> {{ package.package_id }}</p>
        </div>

        <h2 style="margin-bottom: 20px;">Video Contents</h2>
        <div class="video-grid">
            {% for video in package.videos %}
            <div class="video-card">
                <h3>{{ video.folder }}</h3>
                <div class="meta">
                    <span><strong>Style:</strong> {{ video.style }}</span>
                    <span><strong>Avatar:</strong> {{ video.avatar }}</span>
                    <span><strong>Duration:</strong> {{ video.duration }}s</span>
                </div>
                <p>This video package includes complete script, visual instructions, avatar guidelines, and production notes.</p>
            </div>
            {% endfor %}
        </div>

        <div style="text-align: center; margin-top: 40px;">
            <a href="/download/{{ package.package_id }}" class="btn">📦 Download Complete Package</a>
        </div>
    </div>
</body>
</html>
    """
    
    # Save templates
    with open('templates/index.html', 'w') as f:
        f.write(index_html)
    
    with open('templates/preview.html', 'w') as f:
        f.write(preview_html)
    
    print("✅ HTML templates created")

if __name__ == '__main__':
    # Create templates
    create_html_templates()
    
    print("🎬 UGC VIDEO GENERATOR - WEB INTERFACE")
    print("=" * 60)
    print("Starting web interface for UGC video generation...")
    print("\nMake sure you have OPENAI_API_KEY in your .env file")
    print("\nWeb interface will be available at: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)

