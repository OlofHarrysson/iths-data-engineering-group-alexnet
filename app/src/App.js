import React, { useState } from 'react';
import jsonData from './aggregated_articles';
import './App.css';
import Header from './Header';
import ArticleCard from './ArticleCard'; // Import the new component

function App() {
  const [darkMode, setDarkMode] = useState(false);

  const toggleDarkMode = () => {
    console.log('Toggle dark mode from App.js');
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
    <div className="bottom_footer">
      <div className="dark-mode-toggle" onClick={toggleDarkMode}>
        <span>Toggle Dark Mode</span>
    </div>
  <div className="example-text-column">
    <div className="example-text"><p>Example column: 3 items</p></div>
    <div className="example-text"><p>Example data: 20 ms</p></div>
    <div className="example-text"><p>What stats we want here?</p></div>

  </div>
  <div className="example-text-column">
    <div className="example-text"><p>Example column: 1 item</p></div>

  </div>
</div>




    </div>
  );
}

export default App;
