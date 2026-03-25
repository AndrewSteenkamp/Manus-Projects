from flask_sqlalchemy import SQLAlchemy
from src.models.user import db
import uuid
from datetime import datetime

class Ad(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = db.Column(db.String(36), db.ForeignKey('project.id'), nullable=False)
    script = db.Column(db.Text, nullable=False)
    video_url = db.Column(db.String(500), nullable=True)
    thumbnail_url = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(50), default='pending_generation', nullable=False)  # pending_generation, generated, pending_review, approved, rejected
    ai_avatar_id = db.Column(db.String(100), nullable=True)  # ID from MakeUGC.ai
    generation_job_id = db.Column(db.String(100), nullable=True)  # Job ID for tracking generation
    feedback = db.Column(db.Text, nullable=True)  # Client feedback if rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Ad {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'script': self.script,
            'video_url': self.video_url,
            'thumbnail_url': self.thumbnail_url,
            'status': self.status,
            'ai_avatar_id': self.ai_avatar_id,
            'generation_job_id': self.generation_job_id,
            'feedback': self.feedback,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

