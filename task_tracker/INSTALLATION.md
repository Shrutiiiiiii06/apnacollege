# Installation Guide

## 📋 Prerequisites

Before installing Task Tracker, ensure you have:

- **Python 3.8 or higher** installed
- **pip** (Python package manager)
- **Git** (optional, for cloning)
- **Internet connection** (for downloading dependencies)

### Check Python Version
```bash
python --version
# or
python3 --version
```

## 🔧 Installation Methods

### Method 1: Automated Setup (Recommended)

#### On Linux/Mac:
```bash
cd task_tracker
chmod +x run.sh
./run.sh
```

#### On Windows:
```cmd
cd task_tracker
run.bat
```

The script will:
1. Create a virtual environment
2. Install all dependencies
3. Create .env file from template
4. Start the application

### Method 2: Manual Setup

#### Step 1: Navigate to Project Directory
```bash
cd task_tracker
```

#### Step 2: Create Virtual Environment (Recommended)
```bash
# On Linux/Mac
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Configure Environment (Optional)
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your preferred text editor
nano .env  # or vim, code, notepad, etc.
```

#### Step 5: Verify Installation
```bash
python verify_setup.py
```

#### Step 6: Run Application
```bash
python app.py
```

## 🌐 Accessing the Application

Once the application is running, open your web browser and navigate to:

```
http://localhost:5000
```

Or:

```
http://127.0.0.1:5000
```

## ⚙️ Configuration Options

### Environment Variables (.env file)

```bash
# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=1

# Database Configuration
DATABASE_URL=sqlite:///task_tracker.db

# API Keys (Optional)
GITHUB_TOKEN=your-github-token
```

### Database Configuration

#### SQLite (Default)
No additional configuration needed. Database file will be created automatically.

#### PostgreSQL (Production)
1. Install PostgreSQL driver:
```bash
pip install psycopg2-binary
```

2. Update DATABASE_URL in .env:
```bash
DATABASE_URL=postgresql://username:password@localhost/task_tracker
```

3. Create database:
```sql
CREATE DATABASE task_tracker;
```

### GitHub API Token (Optional)

To increase GitHub API rate limits:

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `public_repo`, `read:user`
4. Copy token and add to .env:
```bash
GITHUB_TOKEN=ghp_your_token_here
```

## 🐳 Docker Installation (Alternative)

### Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

### Build and Run
```bash
# Build image
docker build -t task-tracker .

# Run container
docker run -p 5000:5000 task-tracker
```

## 🔍 Troubleshooting

### Issue: Port 5000 Already in Use

**Solution 1**: Stop the process using port 5000
```bash
# On Linux/Mac
lsof -ti:5000 | xargs kill -9

# On Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Solution 2**: Use a different port
```bash
# Edit app.py and change port number
port = int(os.environ.get('PORT', 8080))
```

### Issue: Module Not Found Error

**Solution**: Reinstall dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Issue: Database Locked Error

**Solution**: Close other connections or delete database
```bash
rm task_tracker.db
python app.py
```

### Issue: Permission Denied (Linux/Mac)

**Solution**: Make scripts executable
```bash
chmod +x run.sh
chmod +x verify_setup.py
```

### Issue: Virtual Environment Not Activating

**Solution**: Use full path
```bash
# Linux/Mac
source ./venv/bin/activate

# Windows
.\venv\Scripts\activate.bat
```

## 📦 Dependency List

### Core Dependencies
- Flask==3.0.0 - Web framework
- Flask-Login==0.6.3 - User session management
- Flask-Bcrypt==1.0.1 - Password hashing
- Flask-WTF==1.2.1 - Form handling
- Flask-SQLAlchemy==3.1.1 - Database ORM
- WTForms==3.1.1 - Form validation
- email-validator==2.1.0 - Email validation
- requests==2.31.0 - HTTP requests
- python-dotenv==1.0.0 - Environment variables

### Optional Dependencies
- psycopg2-binary - PostgreSQL support
- gunicorn - Production WSGI server
- pytest - Testing framework

## 🚀 Production Deployment

### Using Gunicorn (Linux/Mac)

1. Install Gunicorn:
```bash
pip install gunicorn
```

2. Run with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Waitress (Windows)

1. Install Waitress:
```bash
pip install waitress
```

2. Create serve.py:
```python
from waitress import serve
from app import create_app

app = create_app()
serve(app, host='0.0.0.0', port=5000)
```

3. Run:
```bash
python serve.py
```

### Environment Variables for Production

```bash
SECRET_KEY=<generate-strong-random-key>
FLASK_ENV=production
FLASK_DEBUG=0
DATABASE_URL=postgresql://user:pass@host/db
```

### Generate Secret Key
```python
import secrets
print(secrets.token_hex(32))
```

## 🔒 Security Checklist for Production

- [ ] Change SECRET_KEY to a strong random value
- [ ] Set FLASK_DEBUG=0
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable HTTPS/SSL
- [ ] Set up firewall rules
- [ ] Use environment variables for sensitive data
- [ ] Implement rate limiting
- [ ] Set up logging and monitoring
- [ ] Regular security updates
- [ ] Backup database regularly

## 📊 Performance Optimization

### Database Optimization
```python
# Add indexes to frequently queried columns
# Already implemented in models.py
```

### Caching (Optional)
```bash
pip install Flask-Caching
```

### CDN for Static Files
- Bootstrap and Chart.js already use CDN
- Consider CDN for custom static files in production

## 🧪 Testing Installation

Run the verification script:
```bash
python verify_setup.py
```

Expected output:
```
✅ Python Version: PASSED
✅ Dependencies: PASSED
✅ File Structure: PASSED
✅ Python Syntax: PASSED
✅ Database: PASSED
```

## 📱 Mobile Access

To access from mobile devices on the same network:

1. Find your computer's IP address:
```bash
# Linux/Mac
ifconfig | grep "inet "

# Windows
ipconfig
```

2. Run app with host='0.0.0.0':
```python
app.run(host='0.0.0.0', port=5000)
```

3. Access from mobile:
```
http://YOUR_IP_ADDRESS:5000
```

## 🆘 Getting Help

If you encounter issues:

1. **Check Documentation**:
   - README.md - Full documentation
   - QUICKSTART.md - Quick start guide
   - PROJECT_OVERVIEW.md - Architecture details

2. **Run Verification**:
   ```bash
   python verify_setup.py
   ```

3. **Check Logs**:
   - Look for error messages in terminal
   - Check Flask debug output

4. **Common Solutions**:
   - Reinstall dependencies
   - Delete and recreate database
   - Check Python version
   - Verify file permissions

## ✅ Post-Installation Steps

After successful installation:

1. **Create First Account**:
   - Navigate to http://localhost:5000
   - Click "Register"
   - Fill in details and submit

2. **Add Sample Tasks**:
   - Click "Add Task"
   - Create a few tasks to test functionality

3. **Explore Dashboard**:
   - View analytics and charts
   - Check productivity insights

4. **Sync Platform Data**:
   - Add GitHub username and sync
   - Add LeetCode username and sync

5. **Customize Settings**:
   - Edit .env for custom configuration
   - Modify config.py for advanced settings

---

**Installation Complete! 🎉**

You're now ready to start tracking your tasks and analyzing your productivity!
