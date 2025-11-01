# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python app.py
```

### Step 3: Open Your Browser
Navigate to: **http://localhost:5000**

---

## 📱 First Time Setup

### 1. Register an Account
- Click "Register" in the navigation
- Fill in your details
- Click "Register" button

### 2. Add Your First Task
- Click "Add Task" in the navigation
- Enter task details:
  - **Title**: "Solve Two Sum Problem"
  - **Description**: "Complete the Two Sum problem on LeetCode"
  - **Platform**: Select "LeetCode"
- Click "Save Task"

### 3. View Your Dashboard
- Click "Dashboard" in the navigation
- See your task statistics
- View charts and analytics

### 4. Sync Platform Data (Optional)

#### GitHub Stats
1. Go to Dashboard
2. Find "GitHub Stats" card
3. Enter your GitHub username
4. Click "Sync"

#### LeetCode Stats
1. Go to Dashboard
2. Find "LeetCode Stats" card
3. Enter your LeetCode username
4. Click "Sync"

---

## 🎯 Quick Tips

### Managing Tasks
- **Mark Complete**: Click "Mark Complete" button on any task
- **Edit Task**: Click "Edit" button to modify task details
- **Delete Task**: Click "Delete" button (confirmation required)
- **Filter Tasks**: Use dropdown filters for status and platform

### Understanding Analytics
- **Weekly Completion**: Shows tasks completed in last 7 weeks
- **Platform Distribution**: Shows which platforms you use most
- **Daily Productivity**: Shows your 30-day completion trend
- **Insights**: AI-generated productivity patterns

### Best Practices
1. Add tasks regularly to track your progress
2. Mark tasks complete as you finish them
3. Use descriptive titles for better organization
4. Sync platform data weekly for accurate stats
5. Review your dashboard to identify productivity patterns

---

## 🔧 Troubleshooting

### Can't Access the Application?
- Make sure the server is running
- Check if port 5000 is available
- Try: http://127.0.0.1:5000

### Database Errors?
```bash
# Delete and recreate database
rm task_tracker.db
python app.py
```

### Import Errors?
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

---

## 📚 Learn More

- Read the full [README.md](README.md) for detailed documentation
- Check [config.py](config.py) for configuration options
- Explore [models.py](models.py) to understand the database schema

---

**Happy Tracking! 🎉**
