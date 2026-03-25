from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.client import Client
from src.models.project import Project
from src.models.ad import Ad
import json

project_bp = Blueprint('project', __name__)

@project_bp.route('/projects', methods=['GET'])
def get_projects():
    """Get all projects"""
    try:
        projects = Project.query.all()
        return jsonify([project.to_dict() for project in projects]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@project_bp.route('/projects', methods=['POST'])
def create_project():
    """Create a new project"""
    try:
        data = request.get_json()
        
        if not data or not data.get('client_id') or not data.get('product_name') or not data.get('product_url'):
            return jsonify({'error': 'client_id, product_name, and product_url are required'}), 400
        
        # Verify client exists
        client = Client.query.get(data['client_id'])
        if not client:
            return jsonify({'error': 'Client not found'}), 404
        
        project = Project(
            client_id=data['client_id'],
            product_name=data['product_name'],
            product_url=data['product_url'],
            product_description=data.get('product_description'),
            status='pending'
        )
        
        db.session.add(project)
        db.session.commit()
        
        return jsonify(project.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@project_bp.route('/projects/<project_id>', methods=['GET'])
def get_project(project_id):
    """Get a specific project"""
    try:
        project = Project.query.get_or_404(project_id)
        return jsonify(project.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@project_bp.route('/projects/<project_id>', methods=['PUT'])
def update_project(project_id):
    """Update a project"""
    try:
        project = Project.query.get_or_404(project_id)
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        if 'product_name' in data:
            project.product_name = data['product_name']
        if 'product_url' in data:
            project.product_url = data['product_url']
        if 'product_description' in data:
            project.product_description = data['product_description']
        if 'status' in data:
            project.status = data['status']
        if 'pain_points' in data:
            # Store pain points as JSON string
            if isinstance(data['pain_points'], (list, dict)):
                project.pain_points = json.dumps(data['pain_points'])
            else:
                project.pain_points = data['pain_points']
        
        db.session.commit()
        return jsonify(project.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@project_bp.route('/projects/<project_id>', methods=['DELETE'])
def delete_project(project_id):
    """Delete a project"""
    try:
        project = Project.query.get_or_404(project_id)
        db.session.delete(project)
        db.session.commit()
        return jsonify({'message': 'Project deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@project_bp.route('/projects/<project_id>/ads', methods=['GET'])
def get_project_ads(project_id):
    """Get all ads for a specific project"""
    try:
        project = Project.query.get_or_404(project_id)
        ads = Ad.query.filter_by(project_id=project_id).all()
        return jsonify([ad.to_dict() for ad in ads]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@project_bp.route('/projects/<project_id>/start-generation', methods=['POST'])
def start_ad_generation(project_id):
    """Start the AI ad generation process for a project"""
    try:
        project = Project.query.get_or_404(project_id)
        
        if project.status != 'pending':
            return jsonify({'error': 'Project must be in pending status to start generation'}), 400
        
        # Update project status
        project.status = 'in_progress'
        db.session.commit()
        
        # TODO: Trigger n8n workflow here
        # This would be done via a webhook call to n8n
        
        return jsonify({
            'message': 'Ad generation started',
            'project': project.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

