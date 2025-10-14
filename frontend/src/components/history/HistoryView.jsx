/**
 * History view component for employee status logs.
 */
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../../services/api';
import HistoryItem from './HistoryItem';
import LoadingSpinner from '../common/LoadingSpinner';

const HistoryView = () => {
  const { employeeId } = useParams();
  const navigate = useNavigate();
  
  const [employee, setEmployee] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);

  useEffect(() => {
    fetchEmployeeAndHistory();
  }, [employeeId, page]);

  const fetchEmployeeAndHistory = async () => {
    try {
      // Fetch employee details
      const empResponse = await api.get(`/employees/${employeeId}/`);
      setEmployee(empResponse.data);

      // Fetch history
      const historyResponse = await api.get(`/employees/${employeeId}/history/?page=${page}`);
      
      if (page === 1) {
        setHistory(historyResponse.data.results || historyResponse.data);
      } else {
        setHistory(prev => [...prev, ...(historyResponse.data.results || historyResponse.data)]);
      }
      
      setHasMore(!!historyResponse.data.next);
      setLoading(false);
      setError('');
    } catch (err) {
      setError('Помилка завантаження історії');
      setLoading(false);
    }
  };

  const handleLoadMore = () => {
    setPage(prev => prev + 1);
  };

  const handleBack = () => {
    navigate('/');
  };

  if (loading && page === 1) {
    return (
      <div className="min-h-screen bg-gray-100 py-8">
        <LoadingSpinner text="Завантаження історії..." />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto px-4 py-6 max-w-4xl">
        {/* Header */}
        <div className="mb-6">
          <button
            onClick={handleBack}
            className="flex items-center text-primary hover:text-blue-600 mb-4"
          >
            <svg
              className="w-5 h-5"
              fill="none"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
            </svg>
            Назад до панелі
          </button>
          
          {employee && (
            <>
              <h2 className="text-2xl font-bold text-gray-900">Історія статусів</h2>
              <p className="text-gray-600 mt-1">
                {employee.name}
              </p>
            </>
          )}
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg">
            {error}
          </div>
        )}

        {/* History Items */}
        {history.length > 0 ? (
          <>
            <div className="space-y-3">
              {history.map((log) => (
                <HistoryItem key={log.id} log={log} />
              ))}
            </div>

            {/* Load More Button */}
            {hasMore && (
              <div className="mt-6 text-center">
                <button
                  onClick={handleLoadMore}
                  className="px-6 py-2 bg-primary text-white rounded-lg font-semibold hover:bg-blue-600 transition-colors"
                >
                  {loadingMore ? 'Завантаження...' : 'Завантажити більше'}
                </button>
              </div>
            )}
          </>
        ) : (
          <div className="bg-white rounded-lg shadow-md p-8 text-center">
            <p className="text-gray-500">Історія відсутня</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default HistoryView;
