// src/App.jsx
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import Chat from "./pages/Chat";
import { useTheme } from './contexts/ThemeContext';
import Header from "./components/Header";


function App() {
  const { theme } = useTheme();

  return (
    <Router>
      <div className={`min-h-screen flex flex-col ${theme} transition-colors duration-500`}>
        <Header />
        <main className="flex-1 ">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/chat" element={<Chat />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
