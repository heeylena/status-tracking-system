/**
 * Real-time timer component for displaying elapsed/remaining time.
 */
import React from 'react';
import { useTimer } from '../../hooks/useTimer';
import { calculateElapsedSeconds, calculateRemainingSeconds, formatDurationHuman, isOverdue } from '../../utils/timeUtils';

const Timer = ({ startTime, plannedEndTime }) => {
  const currentTime = useTimer(1000); // Update every second

  const elapsedSeconds = calculateElapsedSeconds(startTime);
  const remainingSeconds = calculateRemainingSeconds(plannedEndTime);
  const overdue = isOverdue(plannedEndTime);

  return (
    <div className="space-y-2">
      {/* Elapsed Time */}
      <div className="flex justify-between items-center">
        <span className="text-sm font-medium text-gray-600">Минуло:</span>
        <span className="text-sm font-semibold text-gray-900">
          {formatDurationHuman(elapsedSeconds)}
        </span>
      </div>

      {/* Remaining/Overdue Time */}
      {plannedEndTime && (
        <div className="flex justify-between items-center">
          <span className="text-sm font-medium text-gray-600">
            {overdue ? 'Прострочено:' : 'Залишилось:'}
          </span>
          <span
            className={`text-sm font-semibold ${
              overdue ? 'text-red-600 pulse-red' : 'text-green-600'
            }`}
          >
            {formatDurationHuman(remainingSeconds)}
          </span>
        </div>
      )}
    </div>
  );
};

export default Timer;
