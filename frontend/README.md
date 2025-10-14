# Employee Status Tracking System - Frontend

React-based mobile-first frontend for the employee status tracking system.

## Features

- **Mobile-First Design** - No horizontal scrolling, optimized for touch devices
- **Real-Time Updates** - Timers update every second, data polls every 5 seconds
- **JWT Authentication** - Secure login with automatic token refresh
- **Status Management** - Easy status changes with modal interface
- **History View** - Complete status history with pagination
- **Overdue Alerts** - Visual indicators and animations for overdue statuses
- **Excel Export** - Download comprehensive reports

## Technology Stack

- React 18.2
- Vite (fast build tool)
- Tailwind CSS (utility-first styling)
- Axios (HTTP client with interceptors)
- React Router (navigation)
- date-fns (date utilities)

## Setup Instructions

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env if your backend runs on a different URL
```

Default configuration connects to `http://localhost:8000/api`

### 3. Run Development Server

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

### 4. Build for Production

```bash
npm run build
```

The production build will be in the `dist/` folder.

### 5. Preview Production Build

```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── auth/
│   │   │   └── LoginForm.jsx
│   │   ├── common/
│   │   │   ├── Navbar.jsx
│   │   │   └── LoadingSpinner.jsx
│   │   ├── employees/
│   │   │   ├── EmployeeCard.jsx
│   │   │   ├── EmployeeList.jsx
│   │   │   ├── StatusChangeModal.jsx
│   │   │   └── Timer.jsx
│   │   ├── history/
│   │   │   ├── HistoryView.jsx
│   │   │   └── HistoryItem.jsx
│   │   └── reports/
│   │       └── ExcelReportButton.jsx
│   ├── context/
│   │   └── AuthContext.jsx
│   ├── hooks/
│   │   ├── useAuth.js
│   │   ├── useTimer.js
│   │   └── usePolling.js
│   ├── services/
│   │   ├── api.js
│   │   └── auth.js
│   ├── utils/
│   │   └── timeUtils.js
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── index.html
├── package.json
├── vite.config.js
└── tailwind.config.js
```

## Key Components

### EmployeeList
Main dashboard displaying all employees with their current status. Updates via polling every 5 seconds.

### EmployeeCard
Individual employee card with:
- Employee name and email
- Current status with color-coded badge
- Real-time elapsed/remaining timers
- Overdue warnings with pulse animation
- Quick action buttons

### StatusChangeModal
Modal for changing employee status with:
- Radio button status selection
- Conditional datetime picker for statuses requiring end time
- Optional notes field
- Validation

### Timer
Real-time timer component that:
- Updates every second
- Shows elapsed time since status start
- Shows remaining/overdue time
- Applies red pulse animation when overdue

### HistoryView
Complete status history with:
- Chronological list of status changes
- Duration and overdue information
- Pagination (load more)
- Notes and metadata

## Mobile Optimization

### Design Principles
- **Vertical Stack Layout** - All content stacks vertically
- **No Horizontal Scroll** - Content fits within viewport width
- **Touch-Friendly** - Minimum 44x44px tap targets
- **Responsive Cards** - Cards expand to full width on mobile
- **Large Text** - Readable font sizes (14px minimum)

### Tested On
- iPhone SE (375px width)
- iPhone 12 Pro (390px width)
- iPad (768px width)

## Authentication Flow

1. User visits protected route
2. Check for valid access token
3. If no token, redirect to `/login`
4. On login, store JWT tokens in localStorage
5. Add access token to all API requests via interceptor
6. On 401 error, attempt token refresh
7. If refresh fails, clear tokens and redirect to login

## Real-Time Updates

### Local Timer Updates
Timers update every 1 second using `useTimer` hook for smooth countdown.

### Server Polling
Employee data refreshes every 5 seconds using `usePolling` hook to get latest status changes.

## Overdue Display Logic

When a status is overdue:
- Timer shows negative value (e.g., `-02:15:30`)
- Text color changes to red (`text-red-600`)
- Pulse animation applied (`pulse-red`)
- Warning icon displayed
- Alert banner shown on employee card

## Error Handling

- **Network Errors** - Displayed in error banners
- **401 Unauthorized** - Automatic token refresh attempt
- **Failed Refresh** - Logout and redirect to login
- **Validation Errors** - Inline form validation messages

## Performance Optimizations

- **React.memo** - Employee cards memoized to prevent unnecessary re-renders
- **Lazy Loading** - History items load on demand (pagination)
- **Debounced Polling** - 5-second intervals prevent server overload
- **Optimized Bundles** - Vite tree-shaking and code splitting

## Development Tips

### Hot Module Replacement
Vite provides instant HMR - changes appear immediately without full reload.

### Tailwind CSS IntelliSense
Install the Tailwind CSS IntelliSense VS Code extension for autocompletion.

### React DevTools
Use React DevTools browser extension to inspect component state and props.

## Troubleshooting

### CORS Errors
Ensure backend has frontend URL in `CORS_ALLOWED_ORIGINS`.

### Token Refresh Loop
Check that backend `/api/auth/refresh/` endpoint is working correctly.

### Timer Not Updating
Verify `useTimer` hook is properly cleaning up intervals on unmount.

### Styling Issues
Run `npm run build` to ensure Tailwind purges unused styles correctly.

## Future Enhancements

- **Dark Mode** - Add theme toggle
- **Notifications** - Browser push notifications for overdue statuses
- **Filters** - Filter employees by status
- **Search** - Search employees by name
- **PWA** - Progressive Web App for offline capability
- **WebSockets** - Real-time updates without polling

## License

MIT License
