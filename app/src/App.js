import React, { useState } from 'react';
import jsonData from './aggregated_articles';
import './App.css';
import Header from './Header';
import ArticleCard from './articleCard'; // Import the new component

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
          <ArticleCard key={index} item={item} darkMode={darkMode} />
        ))}
      </div>
    </div>
  );
}

export default App;
