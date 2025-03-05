import React, { useState, useEffect, useRef } from 'react';
import styled from 'styled-components';
import { useWebSocket } from './hooks/useWebSocket';
import { ConnectionStatus } from './ConnectionStatus';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export interface Message {
    id: number;
    text: string;
    sender: 'user' | 'iris';
    isStatus?: boolean;
  }
  
  export interface WebSocketResponse {
    text: string;
    sender: 'iris';
  }

// Add new interface for WebSocket messages
interface WebSocketMessage {
  type: 'message' | 'status';
  text: string;
  sender: 'iris';
}

const Container = styled.div`
  display: flex;
  height: 100vh;
  background-color: #0d1b2a;
  font-family: 'Exo 2', sans-serif;
`;

const IrisSection = styled.div`
  width: 400px;
  display: flex;
  justify-content: center;
  align-items: center;
  border-right: 1px solid #2a4b6d;
`;

const ChatSection = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: #1b2a3f;
`;

const MessageContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
`;

const MessageList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 10px;
`;

const MarkdownMessage = styled.div`
  pre {
    background-color: #1e2a3a;
    padding: 10px;
    border-radius: 5px;
    overflow-x: auto;
  }
  code {
    background-color: #1e2a3a;
    padding: 2px 5px;
    border-radius: 3px;
  }
  table {
    border-collapse: collapse;
    width: 100%;
    margin: 10px 0;
  }
  th, td {
    border: 1px solid #2a4b6d;
    padding: 8px;
    text-align: left;
  }
  th {
    background-color: #1e2a3a;
  }
  blockquote {
    border-left: 3px solid #2a4b6d;
    margin: 0;
    padding-left: 10px;
    color: #a0aec0;
  }
  img {
    max-width: 100%;
    height: auto;
  }
  a {
    color: #00ffff;
    text-decoration: none;
    &:hover {
      text-decoration: underline;
    }
  }
`;

const Message = styled.div<{ sender: 'user' | 'iris' }>`
  padding: 10px;
  border-radius: 10px;
  max-width: 70%;
  word-wrap: break-word;
  align-self: ${props => props.sender === 'user' ? 'flex-end' : 'flex-start'};
  background-color: ${props => props.sender === 'user' ? '#2c3e50' : '#34495e'};
  color: #ecf0f1;
  font-family: 'Exo 2', sans-serif;

  ${MarkdownMessage} {
    color: inherit;
  }
`;

// Add styled component for status messages
const StatusMessage = styled.div`
  padding: 8px;
  margin: 5px 0;
  color: #00ffff;
  font-style: italic;
  text-align: center;
`;

const InputContainer = styled.div`
  display: flex;
  padding: 20px;
  border-top: 1px solid #2a4b6d;
`;

const Input = styled.input`
  flex: 1;
  padding: 10px;
  background-color: #2c3e50;
  color: #ecf0f1;
  border: none;
  border-radius: 5px;
  margin-right: 10px;
  font-family: 'Exo 2', sans-serif;
  font-size: 1em;
`;

const SendButton = styled.button`
  padding: 10px 20px;
  background-color: #00ffff;
  color: #0d1b2a;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-family: 'Exo 2', sans-serif;
  font-weight: 600;
  font-size: 1em;
`;

const IrisCircle = styled.div`
  position: relative;
  width: 300px;
  height: 300px;
`;

const CircleOuter = styled.div`
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 5px solid #ffffff;
  background: transparent;
  animation: rotate 5s linear infinite;
  transform-origin: center;

  @keyframes rotate {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;

const CircleInner = styled.div`
  position: absolute;
  top: 50px;
  left: 50px;
  right: 50px;
  bottom: 50px;
  border-radius: 50%;
  border: 5px solid #00ffff;
  background: transparent;
  animation: pulse 2s ease-in-out infinite;
  transform-origin: center;

  @keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(0.95); }
  }
`;

const IrisText = styled.div`
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 2.5em;
  color: #ffffff;
  font-family: 'Exo 2', sans-serif;
  font-weight: 600;
  text-align: center;
  z-index: 10;
`;

const LoadingDots = styled.span`
  &::after {
    content: '...';
    animation: dots 1.5s steps(5, end) infinite;
  }

  @keyframes dots {
    0%, 20% { content: '.'; }
    40% { content: '..'; }
    60%, 100% { content: '...'; }
  }
`;

const IrisChatUI: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    { id: 1, text: "Hello, I'm IRIS. How can I help you today?", sender: 'iris' }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const { isConnected, sendMessage, ws } = useWebSocket('ws://localhost:8000/ws');

  // Modify the useEffect hook that handles WebSocket messages
  useEffect(() => {
    if (ws) {
      ws.onmessage = (event) => {
        const response = JSON.parse(event.data) as WebSocketMessage;
        
        if (response.type === 'status') {
          // Add status message
          setMessages(prev => [...prev, {
            id: prev.length + 1,
            text: response.text,
            sender: 'iris',
            isStatus: true
          }]);
        } else {
          // Add regular message
          setMessages(prev => [...prev, {
            id: prev.length + 1,
            text: response.text,
            sender: 'iris',
            isStatus: false
          }]);
        }
      };
    }
  }, [ws]);

  const handleSendMessage = () => {
    if (inputMessage.trim() === '' || !isConnected) return;

    const newMessage: Message = {
      id: messages.length + 1,
      text: inputMessage,
      sender: 'user' as const
    };

    setMessages(prev => [...prev, newMessage]);
    sendMessage(inputMessage);
    setInputMessage('');
  };

  return (
    <>
      <link 
        rel="stylesheet" 
        href="https://fonts.googleapis.com/css2?family=Exo+2:wght@400;500;600&display=swap" 
      />
      <Container>
        <ConnectionStatus isConnected={isConnected} />
        <IrisSection>
          <IrisCircle>
            <CircleOuter />
            <CircleInner />
            <IrisText>IRIS</IrisText>
          </IrisCircle>
        </IrisSection>
        <ChatSection>
          <MessageContainer>
            <MessageList>
              {messages.map((msg) => (
                msg.isStatus ? (
                  <StatusMessage key={msg.id}>
                    {msg.text}
                  </StatusMessage>
                ) : (
                  <Message key={msg.id} sender={msg.sender}>
                    {msg.sender === 'iris' ? (
                      <MarkdownMessage>
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>
                          {msg.text}
                        </ReactMarkdown>
                      </MarkdownMessage>
                    ) : (
                      msg.text
                    )}
                  </Message>
                )
              ))}
            </MessageList>
          </MessageContainer>
          <InputContainer>
            <Input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              placeholder="Type a message..."
            />
            <SendButton onClick={handleSendMessage}>
              Send
            </SendButton>
          </InputContainer>
        </ChatSection>
      </Container>
    </>
  );
};

export default IrisChatUI;