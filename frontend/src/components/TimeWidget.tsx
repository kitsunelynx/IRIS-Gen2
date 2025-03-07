import React, { useState, useEffect, useCallback } from 'react';
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward';
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward';
import '../components/ChatWindow.css';
import { getNextZIndex } from '../utils/stackManager';

const TimeWidget: React.FC = () => {
  const [minimized, setMinimized] = useState(false);
  const [position, setPosition] = useState({ x: 450, y: 300 });
  const [dragging, setDragging] = useState(false);
  const [offset, setOffset] = useState({ x: 0, y: 0 });
  const [time, setTime] = useState(new Date());
  const [zIndex, setZIndex] = useState(1);

  const toggleMinimize = () => setMinimized(!minimized);

  const handleMouseDown = (e: React.MouseEvent) => {
    setZIndex(getNextZIndex());
    setDragging(true);
    setOffset({
      x: e.clientX - position.x,
      y: e.clientY - position.y,
    });
  };

  const handleMouseMove = useCallback((e: MouseEvent) => {
    if (dragging) {
      setPosition({
        x: e.clientX - offset.x,
        y: e.clientY - offset.y,
      });
    }
  }, [dragging, offset]);

  const handleMouseUp = useCallback(() => setDragging(false), []);

  useEffect(() => {
    if (dragging) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
    } else {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    }
    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [dragging, handleMouseMove, handleMouseUp]);

  useEffect(() => {
    const timer = setInterval(() => {
      setTime(new Date());
    }, 60 * 1000);
    return () => clearInterval(timer);
  }, []);

  const formattedTime = time.toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit' });

  return (
    <div
      className={`chat-window ${minimized ? 'widget-popout' : 'widget-popup'}`}
      style={{
        position: 'absolute',
        left: position.x,
        top: position.y,
        width: '200px',
        height: minimized ? '40px' : '80px',
        zIndex: zIndex,
      }}
    >
      <div
        className="chat-titlebar"
        onMouseDown={handleMouseDown}
        style={{ cursor: 'move', userSelect: 'none', padding: '5px 10px' }}
      >
        <span className="chat-title" style={{ fontSize: '0.9rem' }}>TIME</span>
        <button className="minimize-button" onClick={toggleMinimize}>
          {minimized ? <span style={{ fontSize: 20 }}>+</span> : <span style={{ fontSize: 20 }}>–</span>}
        </button>
      </div>
      {!minimized && (
        <div
          className="chat-content"
          style={{
            padding: '10px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            background: '#15202b',
          }}
        >
          <div style={{ fontSize: '1.2rem', color: '#f1f1f1', textAlign: 'center' }}>
            {formattedTime}
          </div>
        </div>
      )}
    </div>
  );
};

export default TimeWidget; 