# Task Tracker with Multi-Platform Progress Analytics

A full-stack web application built with Flask that helps users track tasks across multiple platforms (LeetCode, GitHub, Kaggle, etc.) with comprehensive analytics and visualizations.

## 🌟 Features

### Core Functionality
- **User Authentication**: Secure registration and login with password hashing (Flask-Bcrypt)
- **Task Management**: Full CRUD operations for tasks
  - Add, edit, delete, and mark tasks as completed
  - Categorize by platform (LeetCode, GitHub, Kaggle, HackerRank, etc.)
  - Filter by status and platform
- **Analytics Dashboard**: Visual insights powered by Chart.js
  - Weekly task completion bar chart
  - Platform distribution pie chart
  - Daily productivity line chart (30-day view)
  - Key statistics cards
- **Platform Integrations**:
  - **GitHub API**: Fetch repositories, commits, stars, and followers
  - **LeetCode API**: Fetch problems solved, ranking, and difficulty breakdown
- **AI-Powered Insights**: Productivity patterns and recommendations

## 🛠️ Technology Stack

### Backend
- **Flask**: Web framework
- **Flask-Login**: User session management
- **Flask-Bcrypt**: Password hashing
- **Flask-WTF**: Form handling and validation
- **Flask-SQLAlchemy**: ORM for database operations
- **SQLite**: Database (easily switchable to PostgreSQL)

### Frontend
- **Bootstrap 5**: Responsive UI framework
- **Chart.js**: Data visualization
- **Jinja2**: Template engine
- **Vanilla JavaScript**: Interactive features

## 📁 Project Structure

```
task_tracker/
├── app.py                      # Main application file
├── config.py                   # Configuration settings
├── models.py                   # Database models
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── routes/
│   ├── __init__.py
│   ├── auth.py                # Authentication routes
│   ├── tasks.py               # Task management routes
│   ├── analytics.py           # Dashboard and analytics
│   └── api_integration.py     # External API integrations
├── templates/
│   ├── base.html              # Base template
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── tasks.html             # Task list page
│   ├── task_form.html         # Add/Edit task form
│   └── dashboard.html         # Analytics dashboard
└── static/
    ├── css/
    │   └── style.css          # Custom styles
    └── js/                    # (Reserved for custom JS)
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project
```bash
cd task_tracker
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# On Linux/Mac
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables (Optional)
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your settings
# - Add GitHub personal access token for higher API rate limits
# - Change SECRET_KEY for production
```

### Step 5: Initialize Database
The database will be automatically created when you first run the application.

### Step 6: Run the Application
```bash
python app.py
```

The application will be available at: **http://localhost:5000**

## 📖 Usage Guide

### 1. Register an Account
- Navigate to the registration page
- Create an account with username, email, and password
- Password is securely hashed using Bcrypt

### 2. Add Tasks
- Click "Add Task" in the navigation
- Fill in task details:
  - Title (required)
  - Description (optional)
  - Platform (LeetCode, GitHub, Kaggle, etc.)
- Tasks are created with "pending" status

### 3. Manage Tasks
- **View Tasks**: See all your tasks on the "My Tasks" page
- **Filter**: Filter by status (pending/completed) or platform
- **Mark Complete**: Toggle task status with one click
- **Edit**: Update task details
- **Delete**: Remove tasks permanently

### 4. View Analytics Dashboard
- Access comprehensive analytics and insights
- View statistics cards (total, completed, pending, completion rate)
- Analyze charts:
  - **Weekly Completion**: Bar chart showing tasks completed per week
  - **Platform Distribution**: Pie chart of tasks by platform
  - **Daily Productivity**: Line chart of 30-day completion trend
- Read AI-generated productivity insights

### 5. Sync Platform Data

#### GitHub Integration
1. Enter your GitHub username in the GitHub Stats card
2. Click "Sync" to fetch:
   - Public repositories count
   - Followers and following
   - Total stars across repos
   - Recent repositories
   - Recent commit activity

#### LeetCode Integration
1. Enter your LeetCode username in the LeetCode Stats card
2. Click "Sync" to fetch:
   - Total problems solved
   - Ranking
   - Problems by difficulty (Easy, Medium, Hard)

## 🔧 Configuration

### Database Configuration
By default, the app uses SQLite. To use PostgreSQL:

1. Install PostgreSQL driver:
```bash
pip install psycopg2-binary
```

2. Update `config.py`:
```python
SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/task_tracker'
```

### API Configuration

#### GitHub API
- **Without Token**: 60 requests/hour
- **With Token**: 5000 requests/hour

To add a GitHub token:
1. Generate a personal access token at: https://github.com/settings/tokens
2. Add to `.env` file:
```
GITHUB_TOKEN=your_token_here
```

#### LeetCode API
- Uses unofficial GraphQL API
- No authentication required
- May have rate limits

## 📊 Database Schema

### User Table
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `password_hash`: Bcrypt hashed password
- `created_at`: Account creation timestamp

### Task Table
- `id`: Primary key
- `user_id`: Foreign key to User
- `title`: Task title
- `description`: Task description
- `platform`: Platform category
- `status`: pending or completed
- `created_at`: Task creation timestamp
- `completed_at`: Task completion timestamp

### PlatformStats Table
- `id`: Primary key
- `user_id`: Foreign key to User
- `platform`: Platform name (github, leetcode)
- `data`: JSON string with platform-specific data
- `last_updated`: Last sync timestamp

## 🎨 Customization

### Styling
- Edit `static/css/style.css` for custom styles
- Bootstrap 5 classes can be modified in templates

### Adding New Platforms
1. Add platform to `PLATFORMS` list in `routes/tasks.py`
2. Create API integration function in `routes/api_integration.py`
3. Add sync form in `dashboard.html`

### Modifying Charts
- Chart configurations are in `dashboard.html`
- Chart.js documentation: https://www.chartjs.org/docs/

## 🔒 Security Features

- Password hashing with Bcrypt
- CSRF protection on all forms
- SQL injection prevention via SQLAlchemy ORM
- Session-based authentication
- Login required decorators on protected routes

## 🐛 Troubleshooting

### Database Issues
```bash
# Delete database and recreate
rm task_tracker.db
python app.py
```

### Import Errors
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt
```

### API Rate Limits
- GitHub: Add personal access token
- LeetCode: Wait before retrying

## 📝 Future Enhancements

- [ ] Email notifications for pending tasks
- [ ] Export data to CSV/PDF
- [ ] Mobile app version
- [ ] More platform integrations (Kaggle, CodeForces)
- [ ] Team collaboration features
- [ ] Task priorities and deadlines
- [ ] Dark mode theme

## 📄 License

This project is open-source and available for educational purposes.

## 👨‍💻 Author

Created as a comprehensive full-stack Flask application demonstrating:
- RESTful API design
- Database modeling and relationships
- User authentication and authorization
- External API integration
- Data visualization
- Responsive web design

## 🙏 Acknowledgments

- Flask documentation and community
- Bootstrap for UI components
- Chart.js for visualizations
- GitHub and LeetCode for API access

---

**Happy Task Tracking! 🚀**
