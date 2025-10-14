/**
 * Main employee list component (dashboard).
 */
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';
import { usePolling } from '../../hooks/usePolling';
import EmployeeCard from './EmployeeCard';
import StatusChangeModal from './StatusChangeModal';
import LoadingSpinner from '../common/LoadingSpinner';

const EmployeeList = () => {
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedEmployee, setSelectedEmployee] = useState(null);
  const [showStatusModal, setShowStatusModal] = useState(false);
  
  const navigate = useNavigate();

  const fetchEmployees = async () => {
    try {
      const response = await api.get('/employees/');
      // Handle paginated response - extract results array
      const employeesData = response.data.results || response.data;
      setEmployees(employeesData);
      setLoading(false);
      setError('');
    } catch (err) {
      setError('Помилка завантаження співробітників');
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEmployees();
  }, []);

  // Poll server every 5 seconds
  usePolling(fetchEmployees, 5000);

  const handleChangeStatus = (employee) => {
    setSelectedEmployee(employee);
    setShowStatusModal(true);
  };

  const handleViewHistory = (employee) => {
    navigate(`/history/${employee.id}`);
  };

  const handleStatusChangeSuccess = () => {
    fetchEmployees();
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 py-8">
        <LoadingSpinner text="Завантаження співробітників..." />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto px-4 py-6 max-w-4xl">
        {/* Header */}
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-gray-900">Панель статусів співробітників</h2>
          <p className="text-gray-600 mt-1">Відстеження статусів у реальному часі</p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg">
            {error}
          </div>
        )}

        {/* Employee Cards */}
        {employees.length > 0 ? (
          <div className="space-y-4">
            {employees.map((employee) => (
              <EmployeeCard
                key={employee.id}
                employee={employee}
                onChangeStatus={handleChangeStatus}
                onViewHistory={handleViewHistory}
              />
            ))}
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow-md p-8 text-center">
            <p className="text-gray-500">Співробітників не знайдено</p>
          </div>
        )}

        {/* Status Change Modal */}
        {showStatusModal && selectedEmployee && (
          <StatusChangeModal
            employee={selectedEmployee}
            onClose={() => setShowStatusModal(false)}
            onSuccess={handleStatusChangeSuccess}
          />
        )}
      </div>
    </div>
  );
};

export default EmployeeList;
