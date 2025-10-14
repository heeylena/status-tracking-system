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

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- Redis (optional, for Celery tasks)

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load initial data (statuses)
python manage.py load_initial_data

# Run development server
python manage.py runserver
```

Backend will be available at `http://localhost:8000`

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env

# Run development server
npm run dev
```

Frontend will be available at `http://localhost:3000`

## Default Login

After creating a superuser, use those credentials to login.

Example:
- Username: `admin`
- Password: `your-secure-password`

## Usage

### Dashboard
- View all employees with their current status
- Real-time timers update every second
- Overdue statuses highlighted in red with pulse animation
- Click "Change Status" to update employee status
- Click "View History" to see complete status log

### Changing Status
1. Click "Change Status" on employee card
2. Select new status (color-coded)
3. If required, set planned end time
4. Add optional notes
5. Confirm change

### Viewing History
- Complete chronological log of all status changes
- Shows duration, overdue time, and notes
- Paginated for performance (50 items per page)

### Excel Reports
- Click "Download Excel Report" on dashboard
- Includes all status logs with durations and overdue times
- Automatically downloads to your device

### Django Admin
Access at `http://localhost:8000/admin`
- Manage employees and statuses
- View detailed status logs with filters
- Export data to Excel
- Custom overdue filter
- Inline editing

## Project Structure

```
status-tracking-system/
├── backend/              # Django REST API
│   ├── config/          # Project settings
│   ├── employees/       # Main app
│   └── requirements.txt
├── frontend/            # React app
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── hooks/       # Custom hooks
│   │   ├── services/    # API and auth
│   │   └── utils/       # Helper functions
│   └── package.json
└── README.md
```

## API Documentation

### Authentication
- `POST /api/auth/login/` - Login
- `POST /api/auth/refresh/` - Refresh token

### Employees
- `GET /api/employees/` - List employees
- `GET /api/employees/{id}/` - Employee detail
- `POST /api/employees/{id}/change-status/` - Change status
- `GET /api/employees/{id}/history/` - Status history
- `GET /api/employees/{id}/statistics/` - Time statistics

### Statuses
- `GET /api/statuses/` - List statuses
- `POST /api/statuses/` - Create status

### Reports
- `GET /api/reports/excel/` - Download Excel report

## Optional: Celery Setup

For background tasks (email reports, cleanup):

```bash
# Install Redis (macOS)
brew install redis
brew services start redis

# Start Celery worker (in backend directory)
celery -A config worker -l info

# Start Celery beat for scheduled tasks
celery -A config beat -l info
```

## Testing

### Backend Tests
```bash
cd backend
python manage.py test
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## Production Deployment

### Backend
1. Set `DEBUG=False` in `.env`
2. Configure secure `SECRET_KEY`
3. Set proper `ALLOWED_HOSTS`
4. Use PostgreSQL instead of SQLite
5. Configure static files serving
6. Use production WSGI server (gunicorn)

### Frontend
1. Build production bundle: `npm run build`
2. Serve from CDN or static file server
3. Update `VITE_API_BASE_URL` to production API URL

## Database Migration (SQLite → PostgreSQL)

See `backend/README.md` for detailed PostgreSQL migration instructions.

## Troubleshooting

### CORS Errors
Add frontend URL to `CORS_ALLOWED_ORIGINS` in backend settings.

### Token Expired
Access tokens expire after 1 hour. The system automatically refreshes them.

### Timers Not Updating
Check browser console for JavaScript errors. Ensure polling is working.

### Excel Download Fails
Check backend logs. Ensure openpyxl is installed correctly.

## Success Criteria

✅ Admin can log in securely with JWT  
✅ All 10 employees visible on mobile without horizontal scrolling  
✅ Timers update in real-time every second  
✅ Overdue statuses display with negative timer in red  
✅ Status changes log overdue duration correctly  
✅ History view shows complete status log with overdue times  
✅ Django admin provides filtering and reporting capabilities  
✅ API responses under 200ms for employee list  
✅ No console errors in browser  
✅ Code is clean, documented, and follows best practices  

## Key Business Logic

### Status Change Flow
1. Get current active status log (where `end_time` is NULL)
2. If `planned_end_time` exists and is in the past:
   - Calculate `overdue_duration = now() - planned_end_time`
   - Store in closing log
3. Set `end_time = now()` on current log
4. Create new status log with new status and optional `planned_end_time`

### Real-Time Calculations
- `elapsed_time = now() - start_time`
- `remaining_time = planned_end_time - now()` (if planned_end_time exists)
- `is_overdue = planned_end_time < now()` (if planned_end_time exists)
- `overdue_seconds = now() - planned_end_time` (if overdue)

### No Automatic Status Changes
- Employees remain in overdue status until manually changed
- Overdue timer continues counting negatively

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

## Acknowledgments

Built with Django REST Framework, React, and Tailwind CSS.
