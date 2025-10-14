/**
 * Utility functions for time formatting and calculations.
 */

/**
 * Format seconds into a readable duration string (HH:MM:SS).
 */
export const formatDuration = (seconds) => {
  if (seconds === null || seconds === undefined) return '--:--:--';
  
  const absSeconds = Math.abs(seconds);
  const hours = Math.floor(absSeconds / 3600);
  const minutes = Math.floor((absSeconds % 3600) / 60);
  const secs = Math.floor(absSeconds % 60);
  
  const formatted = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
  
  return seconds < 0 ? `-${formatted}` : formatted;
};

/**
 * Format seconds into a human-readable string (e.g., "2г 30хв 15с").
 */
export const formatDurationHuman = (seconds) => {
  if (seconds === null || seconds === undefined) return 'N/A';
  
  const absSeconds = Math.abs(seconds);
  const days = Math.floor(absSeconds / 86400);
  const hours = Math.floor((absSeconds % 86400) / 3600);
  const minutes = Math.floor((absSeconds % 3600) / 60);
  const secs = Math.floor(absSeconds % 60);
  
  const parts = [];
  if (days > 0) parts.push(`${days}д`);
  if (hours > 0) parts.push(`${hours}г`);
  if (minutes > 0) parts.push(`${minutes}хв`);
  if (secs > 0 || parts.length === 0) parts.push(`${secs}с`);
  
  const formatted = parts.join(' ');
  return seconds < 0 ? `-${formatted}` : formatted;
};

/**
 * Format a date string to a readable format (Ukrainian locale, 24-hour).
 */
export const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  const date = new Date(dateString);
  return date.toLocaleString('uk-UA', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
  });
};

/**
 * Calculate elapsed seconds from a start time to now.
 */
export const calculateElapsedSeconds = (startTime) => {
  const start = new Date(startTime);
  const now = new Date();
  return Math.floor((now - start) / 1000);
};

/**
 * Calculate remaining seconds from now to a planned end time.
 */
export const calculateRemainingSeconds = (plannedEndTime) => {
  if (!plannedEndTime) return null;
  const end = new Date(plannedEndTime);
  const now = new Date();
  return Math.floor((end - now) / 1000);
};

/**
 * Check if a status is overdue based on planned end time.
 */
export const isOverdue = (plannedEndTime) => {
  if (!plannedEndTime) return false;
  return new Date(plannedEndTime) < new Date();
};

/**
 * Get a color class for overdue status.
 */
export const getOverdueColorClass = (isOverdue) => {
  return isOverdue ? 'text-red-600' : 'text-gray-700';
};

/**
 * Convert a date to ISO string for API requests.
 */
export const toISOString = (date) => {
  return date ? new Date(date).toISOString() : null;
};
