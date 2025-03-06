import React from 'react';
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward';
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward';

interface ChatTitleBarProps {
  title: string;
  minimized: boolean;
  toggleMinimize: () => void;
  onMouseDown: (e: React.MouseEvent) => void;
}

const ChatTitleBar: React.FC<ChatTitleBarProps> = ({ title, minimized, toggleMinimize, onMouseDown }) => {
  return (
    <div className="chat-titlebar" onMouseDown={onMouseDown} style={{ cursor: 'move', userSelect: 'none' }}>
      <span className="chat-title">{title}</span>
      <button className="minimize-button" onClick={toggleMinimize}>
        {minimized ? <ArrowUpwardIcon style={{ fontSize: 24 }} /> : <ArrowDownwardIcon style={{ fontSize: 24 }} />}
      </button>
    </div>
  );
};

export default ChatTitleBar; 