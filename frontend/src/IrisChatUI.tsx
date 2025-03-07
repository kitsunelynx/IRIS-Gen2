import React from 'react';
import styled from 'styled-components';
import ChatWindow from './components/ChatWindow';
import DateWidget from './components/DateWidget';
import TimeWidget from './components/TimeWidget';
import { ConnectionStatus } from './ConnectionStatus';
import YouTubeWidget from './components/YouTubeWidget';

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
  // Widget visibility state – default open for date and time; youtube starts closed
  const [widgets, setWidgets] = React.useState({
    date: true,
    time: true,
    youtube: false,
  });

  // Command handler for widget commands coming from the chat window.
  const handleWidgetCommand = (command: string): string => {
    const tokens = command.split(" ");
    if (tokens.length < 3) {
      return "Invalid widget command. Usage: widget open|close <widget_name>";
    }
    const action = tokens[1].toLowerCase();
    const widgetName = tokens[2].toLowerCase();
    if (!["date", "time", "youtube"].includes(widgetName)) {
      return `Unknown widget: ${widgetName}`;
    }
    if (action !== "open" && action !== "close") {
      return "Invalid action. Use open or close.";
    }
  
    const newState = action === "open";
    setWidgets((prev) => ({
      ...prev,
      [widgetName]: newState,
    }));
    return `${widgetName} widget ${newState ? "opened" : "closed"}.`;
  };

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
          <ChatWindow onCommand={handleWidgetCommand} />
        </ChatSection>
        {widgets.date && <DateWidget />}
        {widgets.time && <TimeWidget />}
        {widgets.youtube && <YouTubeWidget videoId="dQw4w9WgXcQ" />}
      </Container>
    </>
  );
};

export default IrisChatUI;