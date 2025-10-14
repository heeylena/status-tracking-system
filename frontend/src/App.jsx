/**
 * Main App component with routing.
 */
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { useAuth } from './hooks/useAuth';
import LoginForm from './components/auth/LoginForm';
import Navbar from './components/common/Navbar';
import EmployeeList from './components/employees/EmployeeList';
import HistoryView from './components/history/HistoryView';
import ExcelReportButton from './components/reports/ExcelReportButton';

// Protected route wrapper
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">Loading...</div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

// Main dashboard with employee list and export button
const Dashboard = () => {
  return (
    <>
      <Navbar />
      <div className="container mx-auto px-4 py-6 max-w-4xl">
        <ExcelReportButton />
        <EmployeeList />
      </div>
    </>
  );
};

// History page with navbar
const History = () => {
  return (
    <>
      <Navbar />
      <HistoryView />
    </>
  );
};

function App() {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<LoginForm />} />
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/history/:employeeId"
            element={
              <ProtectedRoute>
                <History />
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;
