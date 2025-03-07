import React, { useState, useEffect } from 'react';
import '../components/ChatWindow.css';
import { getNextZIndex } from '../utils/stackManager';

const YouTubeWidget: React.FC<{ videoId: string }> = ({ videoId }) => {
  const [minimized, setMinimized] = useState(false);
  const [position, setPosition] = useState({ x: 450, y: 400 }); // initial coordinates
  const [dragging, setDragging] = useState(false);
  const [offset, setOffset] = useState({ x: 0, y: 0 });
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

  return (
    <div
      className={`chat-window ${minimized ? 'widget-popout' : 'widget-popup'}`}
      style={{
        position: 'absolute',
        left: position.x,
        top: position.y,
        width: '640px',
        height: minimized ? '40px' : '360px',
        zIndex: zIndex,
      }}
    >
      <div
        className="chat-titlebar"
        onMouseDown={handleMouseDown}
        style={{ cursor: 'move', userSelect: 'none' }}
      >
        <span className="chat-title">YOUTUBE</span>
        <button className="minimize-button" onClick={toggleMinimize}>
          {minimized ? <span style={{ fontSize: 24 }}>+</span> : <span style={{ fontSize: 24 }}>–</span>}
        </button>
      </div>
      {!minimized && (
        <div
          className="chat-content"
          style={{
            padding: 0,
            background: '#000',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
          }}
        >
          <iframe
            width="640"
            height="360"
            src={`https://www.youtube.com/embed/${videoId}`}
            title="YOUTUBE"
            frameBorder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          ></iframe>
        </div>
      )}
    </div>
  );
};

export default YouTubeWidget; 