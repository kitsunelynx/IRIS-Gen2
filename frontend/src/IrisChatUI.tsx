import React from 'react';
import styled from 'styled-components';
import ChatWindow from './components/ChatWindow';
import DateWidget from './components/DateWidget';
import TimeWidget from './components/TimeWidget';
import { ConnectionStatus } from './ConnectionStatus';

const Container = styled.div`
  display: flex;
  height: 100vh;
  background-color: #0d1b2a;
  font-family: 'Exo 2', sans-serif;
  position: relative;
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
  justify-content: center;
  align-items: center;
  background-color: #1b2a3f;
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

const IrisChatUI: React.FC = () => {
  return (
    <>
      <link 
        rel="stylesheet" 
        href="https://fonts.googleapis.com/css2?family=Exo+2:wght@400;500;600&display=swap" 
      />
      <Container>
        <ConnectionStatus isConnected={true} />
        <IrisSection>
          <IrisCircle>
            <CircleOuter />
            <CircleInner />
            <IrisText>IRIS</IrisText>
          </IrisCircle>
        </IrisSection>
        <ChatSection>
          <ChatWindow />
        </ChatSection>
        <DateWidget />
        <TimeWidget />
      </Container>
    </>
  );
};

export default IrisChatUI;