import React from 'react';
import styled from 'styled-components';

const WindowContainer = styled.div`
  border: 1px solid #ccc;
  background: #fff;
  width: 300px;
  box-shadow: 2px 2px 8px rgba(0,0,0,0.2);
  margin: 10px;
`;

const TitleBar = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #333;
  color: #fff;
  padding: 5px;
`;

const ControlButtons = styled.div`
  display: flex;
  gap: 5px;
`;

const Button = styled.button`
  background: transparent;
  border: none;
  color: #fff;
  font-size: 1em;
  cursor: pointer;
`;

interface WidgetWindowProps {
  title: string;
  onClose: () => void;
  onMinimize?: () => void; // optional minimize handler
  children: React.ReactNode;
}

const WidgetWindow: React.FC<WidgetWindowProps> = ({ title, onClose, onMinimize, children }) => {
  return (
    <WindowContainer>
      <TitleBar>
        <span>{title}</span>
        <ControlButtons>
          {onMinimize && <Button onClick={onMinimize}>_</Button>}
          <Button onClick={onClose}>×</Button>
        </ControlButtons>
      </TitleBar>
      <div>
        {children}
      </div>
    </WindowContainer>
  );
};

export default WidgetWindow; 