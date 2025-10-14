# Quick Start Guide

Get the Employee Status Tracking System running in 5 minutes!

## Automated Setup

Run the setup script to automatically configure both backend and frontend:

```bash
./setup.sh
```

The script will:
- ✅ Check prerequisites (Python, Node.js)
- ✅ Create Python virtual environment
- ✅ Install all dependencies
- ✅ Set up database
- ✅ Create admin account
- ✅ Load default statuses

## Manual Setup

If you prefer manual setup:

### Backend (Terminal 1)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py load_initial_data
python manage.py runserver
```

### Frontend (Terminal 2)

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

## Access the Application

- **Frontend Dashboard**: http://localhost:3000
- **Django Admin**: http://localhost:8000/admin
- **API Docs**: http://localhost:8000/api/

## First Steps

1. **Login** with your superuser credentials at http://localhost:3000
2. **Add Employees** via Django Admin (http://localhost:8000/admin)
3. **Set Initial Status** for each employee (e.g., "Ready")
4. **View Dashboard** to see real-time status updates
5. **Change Status** by clicking on employee cards
6. **Download Report** using the Excel button

## Default Statuses

The system comes with 6 pre-configured statuses:

- 🟢 **Ready** - No end time required
- 🔵 **Repair** - Requires planned end time
- 🟠 **Vacation** - Requires planned end time
- 🔴 **Sick Leave** - Requires planned end time
- 🟣 **Business Trip** - Requires planned end time
- ⚪ **Rest** - Requires planned end time

You can add more statuses via Django Admin.

## Key Features to Try

### 1. Real-Time Timers
Watch the timers update every second showing elapsed time.

### 2. Overdue Detection
Set a status with a planned end time in the past - it will show in red with a pulse animation.

### 3. Status History
Click "View History" on any employee to see their complete status log.

### 4. Excel Reports
Click "Download Excel Report" to export all status data.

### 5. Django Admin
Powerful admin interface with:
- Custom filters (overdue, date range)
- Excel export actions
- Inline editing
- Rich status displays

## Test Scenario

Try this to see all features:

1. Create an employee: "John Doe"
2. Set status to "Ready" (no end time needed)
3. After a minute, change to "Repair" with end time 5 minutes from now
4. Wait until overdue to see red timer and alerts
5. Change back to "Ready"
6. View history to see all changes with overdue duration
7. Download Excel report

## Troubleshooting

### Backend won't start
- Ensure Python 3.10+ is installed
- Check virtual environment is activated
- Run migrations: `python manage.py migrate`

### Frontend won't start
- Ensure Node.js 18+ is installed
- Delete `node_modules` and run `npm install` again
- Check `.env` file exists

### Can't login
- Verify superuser was created: `python manage.py createsuperuser`
- Check credentials match

### CORS errors
- Ensure backend is running on port 8000
- Check `CORS_ALLOWED_ORIGINS` in backend settings

## Optional: Celery Setup

For background tasks (email reports, cleanup):

```bash
# Install Redis (macOS)
brew install redis
brew services start redis

# Start Celery worker (new terminal)
cd backend
source venv/bin/activate
celery -A config worker -l info

# Start Celery beat (another terminal)
celery -A config beat -l info
```

## Next Steps

- **Customize Statuses**: Add/modify statuses in Django Admin
- **Add Employees**: Bulk import or add via admin
- **Configure Email**: Set up email settings for Celery notifications
- **Deploy**: See `DEPLOYMENT.md` for production setup

## Need Help?

- **README.md** - Comprehensive project documentation
- **backend/README.md** - Backend-specific details
- **frontend/README.md** - Frontend-specific details
- **DEPLOYMENT.md** - Production deployment guide

## Success Checklist

After setup, verify:
- ✅ Backend running at http://localhost:8000
- ✅ Frontend running at http://localhost:3000
- ✅ Can login to dashboard
- ✅ Can access Django Admin
- ✅ Default statuses loaded
- ✅ Timers updating in real-time
- ✅ Can change employee status
- ✅ Can view history
- ✅ Can download Excel report

## Demo Data

Want to test with sample employees?

When running `python manage.py load_initial_data`, answer "yes" to create 5 sample employees:
- John Smith
- Maria Garcia
- David Chen
- Sarah Johnson
- Michael Brown

All will start with "Ready" status.

---

**Ready to track!** 🚀

For detailed information, see the main README.md file.
