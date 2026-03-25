from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
import sys
import os

# Import our custom modules from the src directory
from src.keyword_generator import generate_keywords
from src.guide_content_generator import generate_youtube_guide_content
from src.guide_formatter import convert_markdown_to_pdf

niche_agent_bp = Blueprint('niche_agent', __name__)

@niche_agent_bp.route('/suggest-niches', methods=['POST'])
@cross_origin()
def suggest_niches():
    """Endpoint to suggest YouTube niches based on user's hobby."""
    try:
        data = request.json
        hobby = data.get('hobby', '').strip()
        
        if not hobby:
            return jsonify({'error': 'Hobby is required'}), 400
        
        # Generate keywords for the hobby
        keywords = generate_keywords(hobby)
        
        # For demonstration purposes, we'll create mock niche suggestions
        # In a real implementation, this would involve calling omni_search
        # and analyzing the results using the agent's capabilities
        mock_suggestions = [
            {
                'name': f'{hobby.title()} for Beginners',
                'description': f'A beginner-friendly approach to {hobby}, perfect for those just starting out.',
                'potential': 'High demand for beginner content',
                'competition': 'Moderate',
                'monetization': 'Affiliate marketing, courses, equipment reviews'
            },
            {
                'name': f'Advanced {hobby.title()} Techniques',
                'description': f'Deep-dive tutorials and advanced techniques for experienced {hobby} enthusiasts.',
                'potential': 'Engaged niche audience',
                'competition': 'Low to moderate',
                'monetization': 'Premium courses, consulting, advanced equipment'
            },
            {
                'name': f'{hobby.title()} Product Reviews',
                'description': f'Honest reviews and comparisons of {hobby}-related products and equipment.',
                'potential': 'High affiliate potential',
                'competition': 'Moderate to high',
                'monetization': 'Affiliate marketing, sponsored reviews'
            }
        ]
        
        return jsonify({
            'hobby': hobby,
            'suggestions': mock_suggestions,
            'keywords_generated': len(keywords)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@niche_agent_bp.route('/capture-lead', methods=['POST'])
@cross_origin()
def capture_lead():
    """Endpoint to capture user email for lead magnet."""
    try:
        data = request.json
        email = data.get('email', '').strip()
        hobby = data.get('hobby', '').strip()
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        # In a real implementation, this would:
        # 1. Store the email in a database
        # 2. Send the lead magnet via email
        # 3. Add to email automation sequence
        
        # For now, we'll just return a success message
        return jsonify({
            'message': 'Lead captured successfully',
            'email': email,
            'hobby': hobby,
            'lead_magnet': 'YouTube Niche Selection Checklist sent to your email'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@niche_agent_bp.route('/generate-guide', methods=['POST'])
@cross_origin()
def generate_guide():
    """Endpoint to generate the YouTube channel guide."""
    try:
        data = request.json
        niche_details = data.get('niche_details')
        
        # Generate the guide content
        guide_content = generate_youtube_guide_content(niche_details)
        
        # Create a temporary markdown file
        temp_md_path = '/tmp/youtube_guide.md'
        temp_pdf_path = '/tmp/youtube_guide.pdf'
        
        with open(temp_md_path, 'w') as f:
            f.write(guide_content)
        
        # Convert to PDF
        convert_markdown_to_pdf(temp_md_path, temp_pdf_path)
        
        # In a real implementation, this would:
        # 1. Store the PDF in a secure location
        # 2. Generate a download link
        # 3. Send the download link via email
        # 4. Process payment if required
        
        return jsonify({
            'message': 'Guide generated successfully',
            'guide_ready': True,
            'niche': niche_details.get('name') if niche_details else 'Generic'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@niche_agent_bp.route('/purchase-product', methods=['POST'])
@cross_origin()
def purchase_product():
    """Endpoint to handle product purchases."""
    try:
        data = request.json
        product_type = data.get('product_type')  # 'document' or 'automated_guideline'
        email = data.get('email', '').strip()
        payment_info = data.get('payment_info', {})
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        if not product_type:
            return jsonify({'error': 'Product type is required'}), 400
        
        # In a real implementation, this would:
        # 1. Process payment using a payment gateway (Stripe, PayPal, etc.)
        # 2. Generate and deliver the purchased product
        # 3. Send confirmation email
        # 4. Present upsell if applicable
        
        product_info = {
            'document': {
                'name': 'Guide to Starting a YouTube Channel',
                'price': 29.99,
                'description': 'Comprehensive step-by-step guide'
            },
            'automated_guideline': {
                'name': 'Automated Guideline Product',
                'price': 99.99,
                'description': 'Guide plus automation tools and templates'
            }
        }
        
        selected_product = product_info.get(product_type)
        if not selected_product:
            return jsonify({'error': 'Invalid product type'}), 400
        
        return jsonify({
            'message': 'Purchase processed successfully',
            'product': selected_product,
            'email': email,
            'delivery_status': 'Product will be delivered to your email within 5 minutes',
            'upsell_available': product_type == 'document'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@niche_agent_bp.route('/health', methods=['GET'])
@cross_origin()
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'service': 'YouTube Niche Agent'})

