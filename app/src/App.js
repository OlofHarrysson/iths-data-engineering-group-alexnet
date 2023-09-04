import React, { useState } from 'react';
import jsonData from './aggregated_articles';
import './App.css';
import Header from './Header';

function App() {
  const [darkMode, setDarkMode] = useState(false);

  const toggleDarkMode = () => {
    console.log('Toggle dark mode from App.js');
    setDarkMode(prevDarkMode => !prevDarkMode);
  };

  return (
    <div className={darkMode ? 'dark-mode' : ''}>
      <Header />

      <div className="dark-mode-toggle" onClick={toggleDarkMode}>
        <span>Toggle Dark Mode</span>
      </div>

      <div className="card-space">
        {jsonData.map((item, index) => (
          <div className={`articles-card ${darkMode ? 'dark-mode-card' : ''}`} key={index}>
            <h2>{item.title}</h2>
            <p>{item.description}</p>
            <div className="article-footer">
            <a href={item.link}>🌐 Full Article</a>
            <p>{item.published}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
