/**
 * Single history item component.
 */
import React from 'react';
import { formatDate, formatDurationHuman } from '../../utils/timeUtils';

const HistoryItem = ({ log }) => {
  const {
    status_name,
    status_color,
    start_time,
    end_time,
    planned_end_time,
    overdue_duration,
    duration_seconds,
    notes,
    created_by_username,
  } = log;

  const isActive = !end_time;
  const wasOverdue = overdue_duration > 0;

  return (
    <div className="bg-white rounded-lg shadow-md p-4 mb-3">
      {/* Header */}
      <div className="flex justify-between items-start mb-3">
        <div className="flex items-center space-x-2">
          <span
            className="px-3 py-1 rounded-full text-white text-sm font-semibold"
            style={{ backgroundColor: status_color }}
          >
            {status_name}
          </span>
          {isActive && (
            <span className="px-2 py-1 bg-green-100 text-green-700 text-xs font-semibold rounded">
              АКТИВНИЙ
            </span>
          )}
          {wasOverdue && !isActive && (
            <span className="px-2 py-1 bg-red-100 text-red-700 text-xs font-semibold rounded">
              БУВ ПРОСТРОЧЕНИЙ
            </span>
          )}
        </div>
        <div className="text-sm text-gray-600">
          Тривалість: <span className="font-semibold">{formatDurationHuman(duration_seconds)}</span>
        </div>
      </div>

      {/* Time Information */}
      <div className="space-y-2 text-sm">
        <div className="flex justify-between">
          <span className="text-xs text-gray-500">Почато</span>
          <span className="font-medium text-gray-900">{formatDate(start_time)}</span>
        </div>

        {end_time && (
          <div className="flex justify-between">
            <span className="text-xs text-gray-500">Завершено</span>
            <span className="font-medium text-gray-900">{formatDate(end_time)}</span>
          </div>
        )}

        {planned_end_time && (
          <div className="flex justify-between">
            <span className="text-xs text-gray-500">Плановане завершення</span>
            <span className="font-medium text-gray-900">{formatDate(planned_end_time)}</span>
          </div>
        )}

        {wasOverdue && (
          <div className="flex justify-between">
            <span className="text-xs text-red-600">Прострочено</span>
            <span className="font-semibold text-red-600">
              {formatDurationHuman(overdue_duration)}
            </span>
          </div>
        )}

        {created_by_username && (
          <div className="flex justify-between">
            <span className="text-gray-600">Змінено:</span>
            <span className="font-medium text-gray-900">{created_by_username}</span>
          </div>
        )}
      </div>

      {/* Notes */}
      {notes && (
        <div className="mt-3 p-2 bg-blue-50 rounded-lg">
          <p className="text-sm text-gray-700">
            <span className="font-medium">Примітки:</span> {notes}
          </p>
        </div>
      )}
    </div>
  );
};

export default HistoryItem;
