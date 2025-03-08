import React, { useState, useEffect } from 'react';
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward';
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward';
import '../components/ChatWindow.css';
import { getNextZIndex } from '../utils/stackManager';

const ArrowUp: React.FC<{ size?: number }> = ({ size }) => <ArrowUpwardIcon style={{ fontSize: size }} />;
const ArrowDown: React.FC<{ size?: number }> = ({ size }) => <ArrowDownwardIcon style={{ fontSize: size }} />;

interface DateWidgetProps {
  onClose?: () => void;
}

const DateWidget: React.FC<DateWidgetProps> = (props) => {
  const [minimized, setMinimized] = useState(false);
  const [position, setPosition] = useState({ x: 450, y: 200 });
  const [dragging, setDragging] = useState(false);
  const [offset, setOffset] = useState({ x: 0, y: 0 });
  const [date, setDate] = useState(new Date());
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

  const handleMouseMove = (e: MouseEvent) => {
    if (dragging) {
      setPosition({
        x: e.clientX - offset.x,
        y: e.clientY - offset.y,
      });
    }
  };

  const handleMouseUp = () => setDragging(false);

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
  }, [dragging, offset]);

  // Update the date every minute (actual change only occurs at midnight)
  useEffect(() => {
    const timer = setInterval(() => {
      setDate(new Date());
    }, 60 * 1000);
    return () => clearInterval(timer);
  }, []);

  const formattedDate = date.toLocaleDateString();

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
        <span className="chat-title" style={{ fontSize: '0.9rem' }}>DATE</span>
        <button className="minimize-button" onClick={toggleMinimize}>
          {minimized ? <span style={{ fontSize: 20 }}>+</span> : <span style={{ fontSize: 20 }}>–</span>}
        </button>
        {props.onClose && (
          <button
            className="close-button"
            onClick={props.onClose}
            style={{
              marginLeft: '8px',
              background: 'inherit',
              color: '#ffffff',
              border: 'none',
              cursor: 'pointer',
              padding: '0',
              fontSize: 'inherit'
            }}
          >
            X
          </button>
        )}
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
          <div style={{ fontSize: '1rem', color: '#f1f1f1', textAlign: 'center' }}>
            {formattedDate}
          </div>
        </div>
      )}
    </div>
  );
};

export default DateWidget; 