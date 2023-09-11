import React from 'react';
import styles from './header.module.css';
import { Link } from 'react-router-dom';

const Header = ({ setSearchQuery, handleAddBotClick }) => {
  return (
    <header className={styles.alxHeader}>
      <div className={styles.headerContent}>
        <div className={styles.title}>
          <h1>AAIN: Alexnet AI Newsfeed</h1>
          <h2>Your Source for Intelligent News Analysis</h2>
        </div>
      </div>

      <div id="header-search-bar" className={styles.headerSearchBar}>
        <form>
          <input
            type="text"
            id="search-input"
            placeholder="Search articles..."
            onChange={(e) => setSearchQuery(e.target.value)}
            className={styles.searchInput}
          />
        </form>
      </div>
    </header>
  );
};

export default Header;
