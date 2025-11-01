@echo off
echo ╔═══════════════════════════════════════════════════════════╗
echo ║   Task Tracker with Multi-Platform Progress Analytics    ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -q -r requirements.txt

REM Check if .env exists
if not exist ".env" (
    echo ⚙️  Creating .env file from template...
    copy .env.example .env
    echo ✏️  Please edit .env file with your configuration
)

echo.
echo ✅ Setup complete!
echo.
echo 🚀 Starting Flask application...
echo 🌐 Access the app at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

REM Run the Flask app
set FLASK_APP=app.py
set FLASK_ENV=development
python app.py

pause
