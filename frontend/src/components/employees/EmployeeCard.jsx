/**
 * Employee card component displaying status and timer.
 */
import React, { memo } from 'react';
import Timer from './Timer';
import { formatDate } from '../../utils/timeUtils';

const EmployeeCard = ({ employee, onChangeStatus, onViewHistory }) => {
  const { name, email, current_status } = employee;

  return (
    <div className="bg-white rounded-lg shadow-md p-4 mb-4 hover:shadow-lg transition-shadow">
      {/* Employee Info */}
      <div className="flex justify-between items-start mb-3">
        <div>
          <h3 className="text-lg font-bold text-gray-900">{name}</h3>
          {email && <p className="text-sm text-gray-500">{email}</p>}
        </div>
      </div>

      {/* Current Status */}
      {current_status ? (
        <div className="space-y-3">
          {/* Status Badge */}
          <div className="flex items-center space-x-2">
            <span
              className="px-3 py-1 rounded-full text-white text-sm font-semibold"
              style={{ backgroundColor: current_status.status_color }}
            >
              {current_status.status_name}
            </span>
          </div>

          {/* Start Time */}
          <div className="text-sm text-gray-600">
            <span className="font-medium">Почато:</span>{' '}
            {formatDate(current_status.start_time)}
          </div>

          {/* Planned End Time */}
          {current_status.planned_end_time && (
            <div className="text-sm text-gray-600">
              <span className="font-medium">Планове завершення:</span>{' '}
              {formatDate(current_status.planned_end_time)}
            </div>
          )}

          {/* Timer */}
          <div className="bg-gray-50 rounded-lg p-3">
            <Timer
              startTime={current_status.start_time}
              plannedEndTime={current_status.planned_end_time}
            />
          </div>

          {/* Overdue Warning */}
          {current_status.is_overdue && (
            <div className="flex items-center space-x-2 bg-red-50 border border-red-200 rounded-lg p-2">
              <svg
                className="w-5 h-5 text-red-600"
                fill="none"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
              </svg>
              <span className="text-xs text-red-600 font-semibold">Прострочено</span>
            </div>
          )}

          {/* Notes */}
          {current_status.notes && (
            <div className="text-sm text-gray-600 bg-blue-50 rounded-lg p-2">
              <span className="font-medium">Примітки:</span> {current_status.notes}
            </div>
          )}
        </div>
      ) : (
        <div className="text-gray-500 text-center py-4">Немає активного статусу</div>
      )}

      {/* Action Buttons */}
      <div className="mt-4 grid grid-cols-2 gap-2">
        <button
          onClick={() => onChangeStatus(employee)}
          className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg transition duration-200 font-medium"
        >
          Змінити статус
        </button>
        <button
          onClick={() => onViewHistory(employee)}
          className="flex-1 bg-gray-600 hover:bg-gray-700 text-white py-2 px-4 rounded-lg transition duration-200 font-medium"
        >
          Історія
        </button>
      </div>
    </div>
  );
};

// Use React.memo to prevent unnecessary re-renders
export default memo(EmployeeCard);
