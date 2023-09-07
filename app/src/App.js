import React, { useState, useEffect } from 'react';
import jsonData from './aggregated_articles'; // Import jsonData
import './App.css';
import Header from './Header';
import Footer from './Footer';
import ArticleCard from './articleCard'; // Import ArticleCard
import { toggleDarkMode, getCookie, setCookie } from './darkMode'; // Import setCookie

function App() {
  // Retrieve the dark mode preference from the cookie
  const initialDarkModePref = getCookie('dark_mode');
  const [darkMode, setDarkMode] = useState(initialDarkModePref === '1'); // Set initial state based on cookie

  const handleToggleDarkMode = () => {
    toggleDarkMode(); // Call toggleDarkMode function from darkMode.js
    const newDarkModeValue = !darkMode;
    setDarkMode(newDarkModeValue);

    // Update the dark mode preference in the cookie
    setCookie('dark_mode', newDarkModeValue ? '1' : '0', 365);
  };

  useEffect(() => {
    // This effect runs when the component mounts
    // You can use it for other initializations if needed
  }, []);

  return (
    <div className={darkMode ? 'dark-mode' : ''}>
      <Header />

      {/* Add the Search bar */}
      <div id="search-bar">
        <form>
          <input
            type="text"
            id="search-input"
            placeholder="Search..."
          />
          <button type="submit">Search</button>
        </form>
      </div>

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
