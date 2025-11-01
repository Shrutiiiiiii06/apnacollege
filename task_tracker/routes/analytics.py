from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from models import db, Task, PlatformStats
from datetime import datetime, timedelta
from sqlalchemy import func
from collections import defaultdict

analytics_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@analytics_bp.route('/')
@login_required
def index():
    """Display analytics dashboard"""
    # Get basic statistics
    stats = current_user.get_task_statistics()
    
    # Get platform stats from database
    platform_stats = PlatformStats.query.filter_by(user_id=current_user.id).all()
    platform_data = {ps.platform: ps.get_data() for ps in platform_stats}
    
    return render_template('dashboard.html', stats=stats, platform_data=platform_data)


@analytics_bp.route('/api/chart-data')
@login_required
def chart_data():
    """API endpoint to get chart data for visualizations"""
    
    # 1. Weekly completion data (last 7 weeks)
    weekly_data = get_weekly_completion_data()
    
    # 2. Platform distribution data
    platform_data = get_platform_distribution()
    
    # 3. Daily productivity streak (last 30 days)
    daily_data = get_daily_productivity_data()
    
    # 4. Productivity insights
    insights = generate_productivity_insights()
    
    return jsonify({
        'weekly': weekly_data,
        'platform': platform_data,
        'daily': daily_data,
        'insights': insights
    })


def get_weekly_completion_data():
    """Get tasks completed per week for the last 7 weeks"""
    weeks = []
    completed_counts = []
    
    today = datetime.utcnow().date()
    
    for i in range(6, -1, -1):
        week_start = today - timedelta(days=today.weekday() + (i * 7))
        week_end = week_start + timedelta(days=6)
        
        count = Task.query.filter(
            Task.user_id == current_user.id,
            Task.status == 'completed',
            func.date(Task.completed_at) >= week_start,
            func.date(Task.completed_at) <= week_end
        ).count()
        
        weeks.append(f"Week {7-i}")
        completed_counts.append(count)
    
    return {
        'labels': weeks,
        'data': completed_counts
    }


def get_platform_distribution():
    """Get task distribution across platforms"""
    platform_counts = db.session.query(
        Task.platform,
        func.count(Task.id)
    ).filter(
        Task.user_id == current_user.id
    ).group_by(Task.platform).all()
    
    platforms = [p[0] for p in platform_counts]
    counts = [p[1] for p in platform_counts]
    
    return {
        'labels': platforms,
        'data': counts
    }


def get_daily_productivity_data():
    """Get daily task completion for the last 30 days"""
    days = []
    completed_counts = []
    
    today = datetime.utcnow().date()
    
    for i in range(29, -1, -1):
        day = today - timedelta(days=i)
        
        count = Task.query.filter(
            Task.user_id == current_user.id,
            Task.status == 'completed',
            func.date(Task.completed_at) == day
        ).count()
        
        days.append(day.strftime('%m/%d'))
        completed_counts.append(count)
    
    return {
        'labels': days,
        'data': completed_counts
    }


def generate_productivity_insights():
    """Generate AI-based productivity insights"""
    insights = []
    
    # Analyze completion by day of week
    day_counts = defaultdict(int)
    completed_tasks = Task.query.filter_by(
        user_id=current_user.id,
        status='completed'
    ).all()
    
    for task in completed_tasks:
        if task.completed_at:
            day_name = task.completed_at.strftime('%A')
            day_counts[day_name] += 1
    
    if day_counts:
        most_productive_day = max(day_counts, key=day_counts.get)
        insights.append(f"You're most productive on {most_productive_day}s!")
    
    # Analyze favorite platform
    platform_counts = db.session.query(
        Task.platform,
        func.count(Task.id)
    ).filter(
        Task.user_id == current_user.id
    ).group_by(Task.platform).order_by(func.count(Task.id).desc()).first()
    
    if platform_counts:
        insights.append(f"Your most used platform is {platform_counts[0]} with {platform_counts[1]} tasks.")
    
    # Calculate current streak
    streak = calculate_streak()
    if streak > 0:
        insights.append(f"You're on a {streak}-day streak! Keep it up!")
    
    # Completion rate insight
    stats = current_user.get_task_statistics()
    if stats['completion_rate'] >= 80:
        insights.append(f"Excellent! You've completed {stats['completion_rate']}% of your tasks.")
    elif stats['completion_rate'] >= 50:
        insights.append(f"Good progress! {stats['completion_rate']}% completion rate.")
    else:
        insights.append(f"You have {stats['pending']} pending tasks. Time to tackle them!")
    
    return insights


def calculate_streak():
    """Calculate current daily completion streak"""
    today = datetime.utcnow().date()
    streak = 0
    
    for i in range(30):
        day = today - timedelta(days=i)
        count = Task.query.filter(
            Task.user_id == current_user.id,
            Task.status == 'completed',
            func.date(Task.completed_at) == day
        ).count()
        
        if count > 0:
            streak += 1
        else:
            break
    
    return streak
