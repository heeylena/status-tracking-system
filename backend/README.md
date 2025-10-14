# Employee Status Tracking System - Backend

Django REST API for managing employee statuses with real-time tracking and reporting.

## Features

- **JWT Authentication** with token refresh
- **Employee Management** with soft delete
- **Status Tracking** with time calculations
- **Overdue Detection** and logging
- **Excel Reports** generation
- **Django Admin** with custom filters and actions
- **Celery Tasks** for background processing

## Technology Stack

- Django 5.0.1
- Django REST Framework
- SimpleJWT for authentication
- Celery + Redis for task queue
- SQLite (PostgreSQL ready)
- openpyxl for Excel generation

## Setup Instructions

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
cp .env.example .env
# Edit .env with your settings
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
# Username: admin
# Password: (your secure password)
```

### 6. Load Initial Data

```bash
python manage.py load_initial_data
```

This will create default statuses (Ready, Repair, Vacation, etc.) and optionally create sample employees.

### 7. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

### 8. Access Django Admin

Navigate to `http://localhost:8000/admin` and login with your superuser credentials.

## Optional: Celery Setup

### 1. Install and Start Redis

```bash
# macOS
brew install redis
brew services start redis

# Ubuntu
sudo apt-get install redis-server
sudo systemctl start redis
```

### 2. Start Celery Worker

```bash
celery -A config worker -l info
```

### 3. Start Celery Beat (for scheduled tasks)

```bash
celery -A config beat -l info
```

## API Endpoints

### Authentication
- `POST /api/auth/login/` - Login and get JWT tokens
- `POST /api/auth/refresh/` - Refresh access token

### Employees
- `GET /api/employees/` - List all employees with current status
- `GET /api/employees/{id}/` - Employee details
- `POST /api/employees/{id}/change-status/` - Change employee status
- `GET /api/employees/{id}/history/` - Status history
- `GET /api/employees/{id}/statistics/` - Time statistics

### Statuses
- `GET /api/statuses/` - List all active statuses
- `POST /api/statuses/` - Create new status

### Reports
- `GET /api/reports/excel/` - Download Excel report
- `POST /api/reports/excel/` - Generate custom filtered report

## Running Tests

```bash
python manage.py test
```

## Database Migration to PostgreSQL

To migrate from SQLite to PostgreSQL:

1. Update `.env`:
```
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=status_tracking
DATABASE_USER=postgres
DATABASE_PASSWORD=your-password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

2. Update `config/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DATABASE_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.getenv('DATABASE_NAME', BASE_DIR / 'db.sqlite3'),
        'USER': os.getenv('DATABASE_USER', ''),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', ''),
        'HOST': os.getenv('DATABASE_HOST', ''),
        'PORT': os.getenv('DATABASE_PORT', ''),
    }
}
```

3. Run migrations again:
```bash
python manage.py migrate
python manage.py load_initial_data
```

## Production Deployment

1. Set `DEBUG=False` in `.env`
2. Set secure `SECRET_KEY`
3. Configure `ALLOWED_HOSTS`
4. Set up proper database (PostgreSQL recommended)
5. Configure static files serving
6. Set up Redis for Celery
7. Use a production WSGI server (gunicorn, uwsgi)

## Project Structure

```
backend/
├── config/              # Project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── celery.py
├── employees/           # Main app
│   ├── models.py       # Employee, Status, StatusLog
│   ├── serializers.py  # DRF serializers
│   ├── views.py        # API views
│   ├── admin.py        # Django admin customization
│   ├── tasks.py        # Celery tasks
│   └── tests.py        # Unit tests
├── manage.py
└── requirements.txt
```

## Troubleshooting

### CORS Issues
Ensure `CORS_ALLOWED_ORIGINS` in settings includes your frontend URL.

### Database Locked (SQLite)
This can happen with concurrent writes. Consider upgrading to PostgreSQL for production.

### Celery Not Working
Ensure Redis is running: `redis-cli ping` should return `PONG`

## License

MIT License
