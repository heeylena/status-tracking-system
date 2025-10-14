/**
 * Custom hook for polling data at regular intervals.
 */
import { useEffect, useRef } from 'react';

export const usePolling = (callback, interval = 5000, dependencies = []) => {
  const savedCallback = useRef();

  // Remember the latest callback
  useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);

  // Set up the interval
  useEffect(() => {
    function tick() {
      savedCallback.current();
    }

    if (interval !== null) {
      const id = setInterval(tick, interval);
      return () => clearInterval(id);
    }
  }, [interval, ...dependencies]);
};
