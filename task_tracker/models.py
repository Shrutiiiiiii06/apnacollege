from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication and task ownership"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    tasks = db.relationship('Task', backref='owner', lazy='dynamic', cascade='all, delete-orphan')
    platform_stats = db.relationship('PlatformStats', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def get_task_statistics(self):
        """Calculate user's task statistics"""
        total_tasks = self.tasks.count()
        completed_tasks = self.tasks.filter_by(status='completed').count()
        pending_tasks = self.tasks.filter_by(status='pending').count()
        
        return {
            'total': total_tasks,
            'completed': completed_tasks,
            'pending': pending_tasks,
            'completion_rate': round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 1)
        }


class Task(db.Model):
    """Task model for tracking user tasks across different platforms"""
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    platform = db.Column(db.String(50), nullable=False, index=True)  # LeetCode, GitHub, Kaggle, etc.
    status = db.Column(db.String(20), default='pending', index=True)  # pending, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<Task {self.title}>'
    
    def to_dict(self):
        """Convert task to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'platform': self.platform,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'completed_at': self.completed_at.strftime('%Y-%m-%d %H:%M:%S') if self.completed_at else None
        }
    
    def toggle_status(self):
        """Toggle task status between pending and completed"""
        if self.status == 'pending':
            self.status = 'completed'
            self.completed_at = datetime.utcnow()
        else:
            self.status = 'pending'
            self.completed_at = None


class PlatformStats(db.Model):
    """Model for storing API data from various platforms"""
    __tablename__ = 'platform_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    platform = db.Column(db.String(50), nullable=False, index=True)  # github, leetcode, kaggle
    data = db.Column(db.Text, nullable=False)  # JSON string containing platform-specific data
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<PlatformStats {self.platform} for user {self.user_id}>'
    
    def get_data(self):
        """Parse and return JSON data"""
        try:
            return json.loads(self.data)
        except:
            return {}
    
    def set_data(self, data_dict):
        """Set data from dictionary"""
        self.data = json.dumps(data_dict)
        self.last_updated = datetime.utcnow()
