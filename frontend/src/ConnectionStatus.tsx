import React from 'react';
import styled from 'styled-components';

interface Props {
  isConnected: boolean;
}

const StatusIndicator = styled.div<{ isConnected: boolean }>`
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 5px 10px;
  border-radius: 5px;
  background-color: ${props => props.isConnected ? '#2ecc71' : '#e74c3c'};
  color: white;
  font-size: 12px;
`;

export const ConnectionStatus: React.FC<Props> = ({ isConnected }) => {
  return (
    <StatusIndicator isConnected={isConnected}>
      {isConnected ? 'Connected to IRIS' : 'Disconnected'}
    </StatusIndicator>
  );
};