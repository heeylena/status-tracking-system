# Deployment Guide

This guide provides instructions for deploying the Employee Status Tracking System to production.

## Prerequisites

- Production server (Ubuntu 20.04+ recommended)
- Domain name with DNS configured
- SSL certificate (Let's Encrypt recommended)
- PostgreSQL database
- Redis server
- Nginx web server

## Backend Deployment

### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3-pip python3-venv postgresql postgresql-contrib nginx redis-server -y

# Install supervisor for process management
sudo apt install supervisor -y
```

### 2. PostgreSQL Setup

```bash
# Create database and user
sudo -u postgres psql

CREATE DATABASE status_tracking;
CREATE USER status_admin WITH PASSWORD 'your-secure-password';
ALTER ROLE status_admin SET client_encoding TO 'utf8';
ALTER ROLE status_admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE status_admin SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE status_tracking TO status_admin;
\q
```

### 3. Application Setup

```bash
# Clone repository
cd /var/www
sudo git clone https://github.com/yourusername/status-tracking-system.git
sudo chown -R $USER:$USER status-tracking-system
cd status-tracking-system/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn psycopg2-binary

# Configure environment
cp .env.example .env
nano .env
```

### 4. Environment Configuration

Edit `.env` file:

```env
SECRET_KEY=your-very-secure-random-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=status_tracking
DATABASE_USER=status_admin
DATABASE_PASSWORD=your-secure-password
DATABASE_HOST=localhost
DATABASE_PORT=5432

CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

DEFAULT_FROM_EMAIL=noreply@yourdomain.com
ADMIN_EMAIL=admin@yourdomain.com
```

### 5. Django Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load initial data
python manage.py load_initial_data

# Collect static files
python manage.py collectstatic --noinput
```

### 6. Gunicorn Configuration

Create `/etc/supervisor/conf.d/status-tracking.conf`:

```ini
[program:status-tracking]
directory=/var/www/status-tracking-system/backend
command=/var/www/status-tracking-system/backend/venv/bin/gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 3
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/status-tracking/gunicorn.log
```

Create log directory:
```bash
sudo mkdir -p /var/log/status-tracking
sudo chown www-data:www-data /var/log/status-tracking
```

### 7. Celery Configuration

Create `/etc/supervisor/conf.d/status-tracking-celery.conf`:

```ini
[program:status-tracking-celery]
directory=/var/www/status-tracking-system/backend
command=/var/www/status-tracking-system/backend/venv/bin/celery -A config worker -l info
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/status-tracking/celery.log

[program:status-tracking-celery-beat]
directory=/var/www/status-tracking-system/backend
command=/var/www/status-tracking-system/backend/venv/bin/celery -A config beat -l info
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/status-tracking/celery-beat.log
```

### 8. Start Services

```bash
# Update supervisor
sudo supervisorctl reread
sudo supervisorctl update

# Start services
sudo supervisorctl start status-tracking
sudo supervisorctl start status-tracking-celery
sudo supervisorctl start status-tracking-celery-beat

# Check status
sudo supervisorctl status
```

### 9. Nginx Configuration

Create `/etc/nginx/sites-available/status-tracking`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Backend API
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Django Admin
    location /admin/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files
    location /static/ {
        alias /var/www/status-tracking-system/backend/staticfiles/;
        expires 30d;
    }

    # Media files
    location /media/ {
        alias /var/www/status-tracking-system/backend/media/;
        expires 30d;
    }

    # Frontend (React build)
    location / {
        root /var/www/status-tracking-system/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/status-tracking /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Frontend Deployment

### 1. Build Frontend

```bash
cd /var/www/status-tracking-system/frontend

# Install dependencies
npm install

# Update API URL
echo "VITE_API_BASE_URL=https://yourdomain.com/api" > .env

# Build for production
npm run build
```

The built files will be in the `dist/` directory and served by Nginx.

## SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal is configured automatically
sudo certbot renew --dry-run
```

## Database Backup

### Automated Backups

Create `/usr/local/bin/backup-status-tracking.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/status-tracking"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup database
pg_dump -U status_admin status_tracking > $BACKUP_DIR/db_$DATE.sql

# Backup media files
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /var/www/status-tracking-system/backend/media

# Keep only last 30 days
find $BACKUP_DIR -name "db_*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "media_*.tar.gz" -mtime +30 -delete
```

Make executable and add to crontab:
```bash
sudo chmod +x /usr/local/bin/backup-status-tracking.sh
sudo crontab -e

# Add line (daily at 2 AM):
0 2 * * * /usr/local/bin/backup-status-tracking.sh
```

## Monitoring

### 1. Application Logs

```bash
# Gunicorn logs
sudo tail -f /var/log/status-tracking/gunicorn.log

# Celery logs
sudo tail -f /var/log/status-tracking/celery.log

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 2. Service Status

```bash
# Check all services
sudo supervisorctl status

# Restart services
sudo supervisorctl restart status-tracking
sudo supervisorctl restart status-tracking-celery
```

## Updates and Maintenance

### Update Application

```bash
cd /var/www/status-tracking-system

# Pull latest changes
git pull origin main

# Backend updates
cd backend
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput

# Frontend updates
cd ../frontend
npm install
npm run build

# Restart services
sudo supervisorctl restart status-tracking
sudo supervisorctl restart status-tracking-celery
```

## Security Checklist

- [ ] Strong SECRET_KEY configured
- [ ] DEBUG=False in production
- [ ] ALLOWED_HOSTS properly configured
- [ ] CORS_ALLOWED_ORIGINS restricted to your domain
- [ ] PostgreSQL with strong password
- [ ] SSL certificate installed and auto-renewal configured
- [ ] Firewall configured (UFW recommended)
- [ ] Database backups automated
- [ ] Application logs monitored
- [ ] Regular security updates applied

## Scaling Considerations

### Horizontal Scaling
- Use load balancer (HAProxy, AWS ALB)
- Multiple Gunicorn instances
- Separate Celery workers
- Redis Cluster for high availability

### Performance Optimization
- Enable Redis caching for API responses
- Use CDN for static files
- Database query optimization
- Connection pooling (pgbouncer)

## Troubleshooting

### 502 Bad Gateway
Check Gunicorn is running: `sudo supervisorctl status status-tracking`

### Database Connection Errors
Verify PostgreSQL is running: `sudo systemctl status postgresql`

### Celery Tasks Not Running
Check Celery worker status: `sudo supervisorctl status status-tracking-celery`

### Static Files Not Loading
Run collectstatic: `python manage.py collectstatic --noinput`

## Support

For deployment issues, check logs first, then consult:
- Django deployment documentation
- Gunicorn documentation
- Nginx documentation
- Supervisor documentation
