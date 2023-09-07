import React from 'react';
import styles from './header.module.css';

const Header = ({ setSearchQuery }) => {
  return (
    <header className={styles.alxHeader}>
      <div className={styles.headerContent}>
        <div className={styles.title}>
          <h1>AAIN: Alexnet AI Newsfeed</h1>
          <h2>Your Source for Intelligent News Analysis</h2>
        </div>

        {/* Add the Search bar */}
        <div id="search-bar">
          <form>
            <input
              type="text"
              id="search-input"
              placeholder="Search..."
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <button type="submit">Search</button>
          </form>
        </div>
      </div>
    </header>
  );
};

export default Header;
