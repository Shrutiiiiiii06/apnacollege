from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length
from models import db, Task
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

# Platform choices for task categorization
PLATFORMS = [
    ('LeetCode', 'LeetCode'),
    ('GitHub', 'GitHub'),
    ('Kaggle', 'Kaggle'),
    ('HackerRank', 'HackerRank'),
    ('CodeForces', 'CodeForces'),
    ('GeeksforGeeks', 'GeeksforGeeks'),
    ('Other', 'Other')
]

# Forms
class TaskForm(FlaskForm):
    """Form for creating and editing tasks"""
    title = StringField('Task Title', validators=[
        DataRequired(),
        Length(min=3, max=200, message='Title must be between 3 and 200 characters')
    ])
    description = TextAreaField('Description', validators=[
        Length(max=1000, message='Description must not exceed 1000 characters')
    ])
    platform = SelectField('Platform', choices=PLATFORMS, validators=[DataRequired()])
    submit = SubmitField('Save Task')


# Routes
@tasks_bp.route('/')
@login_required
def index():
    """Display all tasks for the current user"""
    # Get filter parameters
    status_filter = request.args.get('status', 'all')
    platform_filter = request.args.get('platform', 'all')
    
    # Base query
    query = Task.query.filter_by(user_id=current_user.id)
    
    # Apply filters
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    if platform_filter != 'all':
        query = query.filter_by(platform=platform_filter)
    
    # Order by creation date (newest first)
    tasks = query.order_by(Task.created_at.desc()).all()
    
    # Get unique platforms for filter dropdown
    platforms = db.session.query(Task.platform).filter_by(user_id=current_user.id).distinct().all()
    platforms = [p[0] for p in platforms]
    
    return render_template('tasks.html', 
                         tasks=tasks, 
                         platforms=platforms,
                         current_status=status_filter,
                         current_platform=platform_filter)


@tasks_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """Add a new task"""
    form = TaskForm()
    
    if form.validate_on_submit():
        task = Task(
            user_id=current_user.id,
            title=form.title.data,
            description=form.description.data,
            platform=form.platform.data,
            status='pending'
        )
        
        db.session.add(task)
        db.session.commit()
        
        flash('Task added successfully!', 'success')
        return redirect(url_for('tasks.index'))
    
    return render_template('task_form.html', form=form, action='Add')


@tasks_bp.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit(task_id):
    """Edit an existing task"""
    task = Task.query.get_or_404(task_id)
    
    # Ensure the task belongs to the current user
    if task.user_id != current_user.id:
        flash('You do not have permission to edit this task.', 'danger')
        return redirect(url_for('tasks.index'))
    
    form = TaskForm(obj=task)
    
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.platform = form.platform.data
        
        db.session.commit()
        
        flash('Task updated successfully!', 'success')
        return redirect(url_for('tasks.index'))
    
    return render_template('task_form.html', form=form, action='Edit', task=task)


@tasks_bp.route('/delete/<int:task_id>', methods=['POST'])
@login_required
def delete(task_id):
    """Delete a task"""
    task = Task.query.get_or_404(task_id)
    
    # Ensure the task belongs to the current user
    if task.user_id != current_user.id:
        flash('You do not have permission to delete this task.', 'danger')
        return redirect(url_for('tasks.index'))
    
    db.session.delete(task)
    db.session.commit()
    
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('tasks.index'))


@tasks_bp.route('/toggle/<int:task_id>', methods=['POST'])
@login_required
def toggle(task_id):
    """Toggle task completion status"""
    task = Task.query.get_or_404(task_id)
    
    # Ensure the task belongs to the current user
    if task.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    task.toggle_status()
    db.session.commit()
    
    return jsonify({
        'success': True,
        'status': task.status,
        'completed_at': task.completed_at.strftime('%Y-%m-%d %H:%M:%S') if task.completed_at else None
    })
