# Employee Status Tracking System

A mobile-first employee status tracking system for managing up to 10 employees with real-time timers, overdue alerts, and comprehensive history logging.

## Features

- 📱 **Mobile-First Design** - Fully responsive with no horizontal scrolling
- ⏱️ **Real-Time Timers** - Live status duration tracking with overdue detection
- 📊 **Status Management** - Customizable statuses with color coding
- 📈 **History Logging** - Complete status change history with overdue tracking
- 📑 **Excel Reports** - Export status reports with date filtering
- 🔒 **JWT Authentication** - Secure admin access with token refresh
- ⚡ **Background Tasks** - Celery integration for async report generation

## Technology Stack

### Backend
- Django 5.x + Django REST Framework
- SimpleJWT for authentication
- Celery + Redis for background tasks
- SQLite (PostgreSQL-ready)
- openpyxl for Excel generation

### Frontend
- React 18+ with Hooks
- Tailwind CSS
- Axios for API calls
- Context API for state management
