import React, { useState } from 'react';
import jsonData from './aggregated_articles';
import './App.css';
import Header from './Header';
import Footer from './Footer';
import ArticleCard from './articleCard';

import { toggleDarkMode } from './darkMode';

function App() {
  const [darkMode, setDarkMode] = useState(false);

  const handleToggleDarkMode = () => {
    toggleDarkMode(); // Call toggleDarkMode function from darkMode.js
    setDarkMode(prevDarkMode => !prevDarkMode);
  };

  return (
    <div className={darkMode ? 'dark-mode' : ''}>
      <Header />

      <div className="card-space">
        {jsonData.map((item, index) => (
          <ArticleCard key={index} item={item} darkMode={darkMode} />
        ))}
      </div>

      <Footer handleToggleDarkMode={handleToggleDarkMode} />
    </div>
  );
}

export default App;
