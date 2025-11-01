from flask import Blueprint, jsonify, flash, redirect, url_for, request
from flask_login import login_required, current_user
from models import db, PlatformStats
import requests
from datetime import datetime

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/sync/<platform>', methods=['POST'])
@login_required
def sync_platform(platform):
    """Sync data from external platform APIs"""
    
    if platform == 'github':
        success, data = fetch_github_stats()
    elif platform == 'leetcode':
        success, data = fetch_leetcode_stats()
    else:
        return jsonify({'error': 'Unsupported platform'}), 400
    
    if success:
        # Store or update platform stats
        platform_stat = PlatformStats.query.filter_by(
            user_id=current_user.id,
            platform=platform
        ).first()
        
        if platform_stat:
            platform_stat.set_data(data)
        else:
            platform_stat = PlatformStats(
                user_id=current_user.id,
                platform=platform
            )
            platform_stat.set_data(data)
            db.session.add(platform_stat)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{platform.capitalize()} data synced successfully',
            'data': data
        })
    else:
        return jsonify({
            'success': False,
            'error': data
        }), 500


def fetch_github_stats():
    """Fetch GitHub statistics using GitHub API"""
    try:
        # Get GitHub username from request or use a default
        github_username = request.args.get('username') or request.form.get('username')
        
        if not github_username:
            return False, 'GitHub username not provided'
        
        # Fetch user data
        user_url = f'https://api.github.com/users/{github_username}'
        headers = {}
        
        # Add token if available (for higher rate limits)
        from flask import current_app
        github_token = current_app.config.get('GITHUB_TOKEN')
        if github_token:
            headers['Authorization'] = f'token {github_token}'
        
        user_response = requests.get(user_url, headers=headers, timeout=10)
        
        if user_response.status_code != 200:
            return False, f'GitHub API error: {user_response.status_code}'
        
        user_data = user_response.json()
        
        # Fetch repositories
        repos_url = f'https://api.github.com/users/{github_username}/repos?sort=updated&per_page=10'
        repos_response = requests.get(repos_url, headers=headers, timeout=10)
        
        repos_data = repos_response.json() if repos_response.status_code == 200 else []
        
        # Fetch recent events (commits, etc.)
        events_url = f'https://api.github.com/users/{github_username}/events/public?per_page=10'
        events_response = requests.get(events_url, headers=headers, timeout=10)
        
        events_data = events_response.json() if events_response.status_code == 200 else []
        
        # Process and structure the data
        github_stats = {
            'username': github_username,
            'name': user_data.get('name', 'N/A'),
            'public_repos': user_data.get('public_repos', 0),
            'followers': user_data.get('followers', 0),
            'following': user_data.get('following', 0),
            'total_stars': sum(repo.get('stargazers_count', 0) for repo in repos_data),
            'recent_repos': [
                {
                    'name': repo.get('name'),
                    'description': repo.get('description', 'No description'),
                    'stars': repo.get('stargazers_count', 0),
                    'language': repo.get('language', 'N/A'),
                    'updated_at': repo.get('updated_at')
                }
                for repo in repos_data[:5]
            ],
            'recent_commits': len([e for e in events_data if e.get('type') == 'PushEvent']),
            'last_updated': datetime.utcnow().isoformat()
        }
        
        return True, github_stats
        
    except requests.exceptions.RequestException as e:
        return False, f'Network error: {str(e)}'
    except Exception as e:
        return False, f'Error fetching GitHub stats: {str(e)}'


def fetch_leetcode_stats():
    """Fetch LeetCode statistics using unofficial API"""
    try:
        # Get LeetCode username from request
        leetcode_username = request.args.get('username') or request.form.get('username')
        
        if not leetcode_username:
            return False, 'LeetCode username not provided'
        
        # Use LeetCode GraphQL API
        url = 'https://leetcode.com/graphql'
        
        query = """
        query getUserProfile($username: String!) {
            matchedUser(username: $username) {
                username
                profile {
                    ranking
                    reputation
                }
                submitStats {
                    acSubmissionNum {
                        difficulty
                        count
                    }
                }
            }
        }
        """
        
        response = requests.post(
            url,
            json={'query': query, 'variables': {'username': leetcode_username}},
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code != 200:
            return False, f'LeetCode API error: {response.status_code}'
        
        data = response.json()
        
        if 'errors' in data or not data.get('data', {}).get('matchedUser'):
            return False, 'User not found or API error'
        
        user_data = data['data']['matchedUser']
        
        # Process submission stats
        submission_stats = user_data.get('submitStats', {}).get('acSubmissionNum', [])
        
        problems_solved = {
            'total': 0,
            'easy': 0,
            'medium': 0,
            'hard': 0
        }
        
        for stat in submission_stats:
            difficulty = stat.get('difficulty', '').lower()
            count = stat.get('count', 0)
            
            if difficulty == 'all':
                problems_solved['total'] = count
            elif difficulty in problems_solved:
                problems_solved[difficulty] = count
        
        leetcode_stats = {
            'username': leetcode_username,
            'ranking': user_data.get('profile', {}).get('ranking', 'N/A'),
            'reputation': user_data.get('profile', {}).get('reputation', 0),
            'problems_solved': problems_solved,
            'last_updated': datetime.utcnow().isoformat()
        }
        
        return True, leetcode_stats
        
    except requests.exceptions.RequestException as e:
        return False, f'Network error: {str(e)}'
    except Exception as e:
        return False, f'Error fetching LeetCode stats: {str(e)}'


@api_bp.route('/platform-stats')
@login_required
def get_platform_stats():
    """Get all platform stats for current user"""
    platform_stats = PlatformStats.query.filter_by(user_id=current_user.id).all()
    
    stats_data = {}
    for ps in platform_stats:
        stats_data[ps.platform] = {
            'data': ps.get_data(),
            'last_updated': ps.last_updated.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    return jsonify(stats_data)
