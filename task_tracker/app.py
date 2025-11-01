from flask import Flask, redirect, url_for
from flask_login import LoginManager, current_user
from config import Config
from models import db, User
from routes.auth import auth_bp, bcrypt
from routes.tasks import tasks_bp
from routes.analytics import analytics_bp
from routes.api_integration import api_bp
import os

def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(api_bp)
    
    # Root route
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.index'))
        return redirect(url_for('auth.login'))
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app


if __name__ == '__main__':
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Create and run the app
    app = create_app()
    
    # Get port from environment or use default
    port = int(os.environ.get('PORT', 5000))
    
    print(f"""
    ╔═══════════════════════════════════════════════════════════╗
    ║   Task Tracker with Multi-Platform Progress Analytics    ║
    ╚═══════════════════════════════════════════════════════════╝
    
    🚀 Application is ready!
    
    📝 To run the application:
       python app.py
    
    🌐 Access the application at:
       http://localhost:{port}
    
    📚 Features:
       ✓ User Authentication (Register/Login)
       ✓ Task Management (CRUD Operations)
       ✓ Analytics Dashboard with Chart.js
       ✓ GitHub API Integration
       ✓ LeetCode API Integration
       ✓ Productivity Insights
    
    ⚙️  Configuration:
       - Database: SQLite (task_tracker.db)
       - Copy .env.example to .env for custom settings
    
    """)
    
    # Note: Uncomment the line below to run the server
    # app.run(debug=True, host='0.0.0.0', port=port)
