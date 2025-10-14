#!/bin/bash

# Employee Status Tracking System - Setup Script
# This script sets up both backend and frontend

echo "=================================="
echo "Employee Status Tracking System"
echo "Setup Script"
echo "=================================="
echo ""

# Check prerequisites
echo "Checking prerequisites..."
echo ""

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ Python found: $PYTHON_VERSION"
else
    echo "✗ Python 3 is not installed. Please install Python 3.10 or higher."
    exit 1
fi

# Check Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "✓ Node.js found: $NODE_VERSION"
else
    echo "✗ Node.js is not installed. Please install Node.js 18 or higher."
    exit 1
fi

# Check npm
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo "✓ npm found: v$NPM_VERSION"
else
    echo "✗ npm is not installed."
    exit 1
fi

echo ""
echo "=================================="
echo "Setting up Backend..."
echo "=================================="
echo ""

cd backend || exit

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv

# Use virtual environment Python directly instead of activating
VENV_PYTHON="venv/bin/python"
VENV_PIP="venv/bin/pip"

# Install dependencies
echo "Installing Python dependencies..."
$VENV_PIP install --upgrade pip
$VENV_PIP install -r requirements.txt

# Copy environment file
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created. Please update it with your settings."
else
    echo "✓ .env file already exists."
fi

# Run migrations
echo "Running database migrations..."
$VENV_PYTHON manage.py makemigrations
$VENV_PYTHON manage.py migrate

# Create superuser
echo ""
echo "=================================="
echo "Create Superuser Account"
echo "=================================="
echo ""
echo "Please create an admin account to access the system."
$VENV_PYTHON manage.py createsuperuser

# Load initial data
echo ""
echo "Loading initial data (default statuses)..."
$VENV_PYTHON manage.py load_initial_data

echo ""
echo "✓ Backend setup complete!"

cd ..

echo ""
echo "=================================="
echo "Setting up Frontend..."
echo "=================================="
echo ""

cd frontend || exit

# Install dependencies
echo "Installing npm dependencies..."
npm install

# Copy environment file
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created."
else
    echo "✓ .env file already exists."
fi

echo ""
echo "✓ Frontend setup complete!"

cd ..

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "To start the application:"
echo ""
echo "1. Start the backend (in a new terminal):"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python manage.py runserver"
echo ""
echo "2. Start the frontend (in another terminal):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "3. Access the application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   Django Admin: http://localhost:8000/admin"
echo ""
echo "Optional: Start Redis and Celery for background tasks"
echo "   brew install redis"
echo "   brew services start redis"
echo "   cd backend"
echo "   celery -A config worker -l info"
echo ""
echo "Happy tracking! 🚀"
echo ""
