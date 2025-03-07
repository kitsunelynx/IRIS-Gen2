import React, { useState, useEffect, useRef } from 'react';
import SendIcon from '@mui/icons-material/Send';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import '../components/ChatWindow.css';
import { useWebSocket } from '../hooks/useWebSocket';
import ChatTitleBar from './ChatTitleBar';
import { getNextZIndex } from '../utils/stackManager';

interface Message {
  id: number;
  text: string;
  sender: 'user' | 'iris';
  isStatus?: boolean;
}

interface ChatWindowProps {
  onCommand?: (command: string) => string;
}

const ChatWindow: React.FC<ChatWindowProps> = ({ onCommand }) => {
  const [minimized, setMinimized] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    { id: 1, text: "Hello, I'm IRIS. How can I help you today?", sender: 'iris' }
  ]);
  const [inputMessage, setInputMessage] = useState('');

  // State for dragging
  const [position, setPosition] = useState({ x: 100, y: 500 });
  const [dragging, setDragging] = useState(false);
  const [offset, setOffset] = useState({ x: 0, y: 0 });
  const [zIndex, setZIndex] = useState(1);

  const { isConnected, sendMessage, ws } = useWebSocket('ws://localhost:8000/ws');

  // Create a ref for the chat window DOM element
  const chatWindowRef = useRef<HTMLDivElement>(null);

  const [storedHeight, setStoredHeight] = useState<string | null>(null);

  const handleMouseDown = (e: React.MouseEvent) => {
    setZIndex(getNextZIndex());
    setDragging(true);
    setOffset({
      x: e.clientX - position.x,
      y: e.clientY - position.y
    });
  };

  const handleMouseMove = (e: MouseEvent) => {
    if (dragging) {
      setPosition({
        x: e.clientX - offset.x,
        y: e.clientY - offset.y
      });
    }
  };

  const handleMouseUp = () => {
    setDragging(false);
  };

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

  useEffect(() => {
    if (ws) {
      ws.onmessage = (event) => {
        const response = JSON.parse(event.data);
        if (response.type === 'status') {
          setMessages(prev => [...prev, { id: prev.length + 1, text: response.text, sender: 'iris', isStatus: true }]);
        } else {
          setMessages(prev => [...prev, { id: prev.length + 1, text: response.text, sender: 'iris', isStatus: false }]);
        }
      };
    }
  }, [ws]);

  const toggleMinimize = () => {
    if (!minimized) {
      // About to minimize: store current height
      if (chatWindowRef.current) {
        const currentHeight = chatWindowRef.current.style.height || chatWindowRef.current.clientHeight + "px";
        setStoredHeight(currentHeight);
      }
      setMinimized(true);
    } else {
      // Restoring maximized window; restore height if stored
      setMinimized(false);
      if (chatWindowRef.current && storedHeight) {
        chatWindowRef.current.style.height = storedHeight;
      }
    }
  };

  const handleSendMessage = () => {
    if (inputMessage.trim() === '' || !isConnected) return;
    
    // Check if this is a widget command message
    if (inputMessage.trim().toLowerCase().startsWith("widget ")) {
      if (onCommand) {
        const commandResponse = onCommand(inputMessage.trim());
        if (commandResponse) {
          // Display the response from command handling as a status message:
          setMessages(prev => [...prev, {
            id: prev.length + 1,
            text: commandResponse,
            sender: 'iris',
            isStatus: true
          }]);
        }
      }
      setInputMessage(''); // Clear the input and don't send to websocket
      return;
    }
    
    // send message normally:
    const newMessage: Message = {
      id: messages.length + 1,
      text: inputMessage,
      sender: 'user'
    };
    setMessages(prev => [...prev, newMessage]);
    sendMessage(inputMessage);
    setInputMessage('');
  };

  // When minimized, force the height to 'snap' to the titlebar height even if resized
  useEffect(() => {
    if (minimized && chatWindowRef.current) {
      chatWindowRef.current.style.height = "50px";
    }
  }, [minimized]);

  // Also observe resize changes to keep snapped height when minimized
  useEffect(() => {
    if (minimized && chatWindowRef.current) {
      const observer = new ResizeObserver((entries) => {
        for (let entry of entries) {
          if (entry.target instanceof HTMLElement) {
            entry.target.style.height = "50px";
          }
        }
      });
      observer.observe(chatWindowRef.current);
      return () => observer.disconnect();
    }
  }, [minimized]);

  return (
    <div ref={chatWindowRef} className={`chat-window ${minimized ? 'minimized' : ''}`} style={{ position: 'absolute', left: position.x, top: position.y, zIndex: zIndex }}>
      <ChatTitleBar title="CHAT" minimized={minimized} toggleMinimize={toggleMinimize} onMouseDown={handleMouseDown} />
      
      {!minimized && (
        <div className="chat-content">
          <div className="message-list">
            {messages.map((msg) =>
              msg.isStatus ? (
                <div key={msg.id} className="status-message">
                  {msg.text}
                </div>
              ) : (
                <div key={msg.id} className={`message ${msg.sender}`}>
                  {msg.sender === 'iris' ? (
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                      {msg.text}
                    </ReactMarkdown>
                  ) : (
                    msg.text
                  )}
                </div>
              )
            )}
          </div>
          <div className="input-container">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              placeholder="Type a message..."
            />
            <button onClick={handleSendMessage}>
              <SendIcon style={{ fontSize: 24 }} />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatWindow; 