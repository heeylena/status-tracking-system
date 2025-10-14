/**
 * Modal for changing employee status.
 */
import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import LoadingSpinner from '../common/LoadingSpinner';

const StatusChangeModal = ({ employee, onClose, onSuccess }) => {
  const [statuses, setStatuses] = useState([]);
  const [selectedStatus, setSelectedStatus] = useState('');
  const [plannedEndTime, setPlannedEndTime] = useState('');
  const [notes, setNotes] = useState('');
  const [loading, setLoading] = useState(false);
  const [loadingStatuses, setLoadingStatuses] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchStatuses();
  }, []);

  const fetchStatuses = async () => {
    try {
      const response = await api.get('/statuses/');
      // Handle paginated response - extract results array
      const statusesData = response.data.results || response.data;
      setStatuses(Array.isArray(statusesData) ? statusesData : []);
      setLoadingStatuses(false);
    } catch (err) {
      setError('Помилка завантаження статусів');
      setLoadingStatuses(false);
    }
  };

  const selectedStatusObj = statuses.find(s => s.id === parseInt(selectedStatus));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const payload = {
        status_id: parseInt(selectedStatus),
        notes,
      };

      if (plannedEndTime) {
        payload.planned_end_time = new Date(plannedEndTime).toISOString();
      }

      await api.post(`/employees/${employee.id}/change_status/`, payload);
      onSuccess();
      onClose();
    } catch (err) {
      setError(err.response?.data?.detail || 'Помилка зміни статусу');
    } finally {
      setLoading(false);
    }
  };

  if (loadingStatuses) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-lg p-6 max-w-md w-full">
          <LoadingSpinner size="small" text="Loading statuses..." />
        </div>
      </div>
    );
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Зміна статусу</h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600"
              disabled={loading}
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <p className="text-gray-600 mb-4">Співробітник: <span className="font-semibold">{employee.name}</span></p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          {error && (
            <div className="p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
              {error}
            </div>
          )}

          {/* Status Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Оберіть статус <span className="text-red-500">*</span>
            </label>
            <div className="space-y-2">
              {statuses.map((status) => (
                <label
                  key={status.id}
                  className={`flex items-center p-3 border-2 rounded-lg cursor-pointer transition-all ${
                    selectedStatus === status.id.toString()
                      ? 'border-primary bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <input
                    type="radio"
                    name="status"
                    value={status.id}
                    checked={selectedStatus === status.id.toString()}
                    onChange={(e) => setSelectedStatus(e.target.value)}
                    className="mr-3"
                    required
                  />
                  <span
                    className="px-3 py-1 rounded-full text-white text-sm font-semibold mr-2"
                    style={{ backgroundColor: status.color }}
                  >
                    {status.name}
                  </span>
                  {status.has_end_time && (
                    <span className="text-xs text-gray-500 ml-auto">Requires end time</span>
                  )}
                </label>
              ))}
            </div>
          </div>

          {/* Planned End Time (conditional) */}
          {selectedStatusObj?.has_end_time && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Плановий час завершення <span className="text-red-500">*</span>
              </label>
              <input
                type="datetime-local"
                value={plannedEndTime}
                onChange={(e) => setPlannedEndTime(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                required={selectedStatusObj?.has_end_time}
              />
              <p className="text-xs text-gray-500 mt-1">
                Коли плануєте завершити цей статус?
              </p>
            </div>
          )}

          {/* Notes */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Примітки (необов'язково)
            </label>
            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              rows="3"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent resize-none"
              placeholder="Додайте примітки про зміну статусу..."
            />
          </div>

          {/* Actions */}
          <div className="flex space-x-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              disabled={loading}
              className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg font-semibold hover:bg-gray-50 disabled:bg-gray-100 disabled:cursor-not-allowed transition-colors"
            >
              Скасувати
            </button>
            <button
              type="submit"
              disabled={loading || !selectedStatus}
              className="flex-1 px-4 py-2 bg-primary text-white rounded-lg font-semibold hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? 'Зміна статусу...' : 'Змінити статус'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default StatusChangeModal;
