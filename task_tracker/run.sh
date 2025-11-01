#!/bin/bash

# Task Tracker - Run Script

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   Task Tracker with Multi-Platform Progress Analytics    ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from template..."
    cp .env.example .env
    echo "✏️  Please edit .env file with your configuration"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Starting Flask application..."
echo "🌐 Access the app at: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the Flask app
export FLASK_APP=app.py
export FLASK_ENV=development
python app.py
