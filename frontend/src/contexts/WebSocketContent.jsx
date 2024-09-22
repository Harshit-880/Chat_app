import React, { createContext, useContext, useEffect, useRef, useState } from "react";
import axios from "axios";

const WebSocketContext = createContext(null);

export const useWebSocket = () => {
  return useContext(WebSocketContext);
};

export const WebSocketProvider = ({ children }) => {
  // No WebSocket connection made yet
  return (
    <WebSocketContext.Provider value={null}>
      {children}
    </WebSocketContext.Provider>
  );
};
export default WebSocketProvider;