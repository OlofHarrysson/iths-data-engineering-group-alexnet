import React, { useState, useEffect } from 'react';
import jsonData from './aggregated_articles';
import './App.css';
import Header from './Header';
import Footer from './Footer';
import ArticleCard from './articleCard';
import { toggleDarkMode, getCookie, setCookie } from './darkMode';
import apiKeys from './api-key.json'; // Adjust the path as needed


import About from './About'; // Import your About component

function App() {
  const initialDarkModePref = getCookie('dark_mode');
  const [darkMode, setDarkMode] = useState(initialDarkModePref === '1');
  const [searchQuery, setSearchQuery] = useState('');
  const [filteredArticles, setFilteredArticles] = useState([]);

  useEffect(() => {
    const filtered = filterArticles(searchQuery);
    setFilteredArticles(filtered);
  }, [searchQuery]);

  const handleToggleDarkMode = () => {
    toggleDarkMode();
    const newDarkModeValue = !darkMode;
    setDarkMode(newDarkModeValue);
    setCookie('dark_mode', newDarkModeValue ? '1' : '0', 365);
  };

  const handleAddBotClick = () => {
    // Use the DISCORD_BOT_INVITE URL from your api-key.json
    const inviteURL = apiKeys.DISCORD_BOT_INVITE;

    // Open the invite URL in a new tab
    window.open(inviteURL, '_blank');
  };



  const filterArticles = (query) => {
    if (!query) {
      return jsonData;
    }

    return jsonData.filter((article) =>
      article.title.toLowerCase().includes(query.toLowerCase())
    );
  };

  return (
    <div className={darkMode ? 'dark-mode' : ''}>
      <Header setSearchQuery={setSearchQuery} handleAddBotClick={handleAddBotClick} />
      <div className="card-space">
        {filteredArticles.map((item, index) => (
          <ArticleCard key={index} item={item} darkMode={darkMode} />
        ))}
      </div>
      <Footer handleToggleDarkMode={handleToggleDarkMode} />
      {/* Add the "Add Discord Bot" button within the footer */}



    </div>
  );
}

export default App;
