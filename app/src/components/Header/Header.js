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

        {/* Add the spacer to push the "About" button to the right */}
        <div className={styles.spacer}></div>

        <nav>
        <Link to="/about" className={`${styles.aboutButton} ${styles.aboutButtonText} ${styles.aboutButtonMargin}`}>
  About
</Link>

{/* Add the "Add Discord Bot" button */}
<div className={`discord-button`} onClick={handleAddBotClick}>
  Add Discord Bot
</div>

        </nav>
      </div>

      <div id="search-bar" className={styles.searchBar}>
        <form>
          <input
            type="text"
            id="search-input"
            placeholder="Search..."
            onChange={(e) => setSearchQuery(e.target.value)}
            className={styles.searchInput}
          />
          <button type="submit" className={styles.searchButton}>
            Search
          </button>
        </form>
      </div>
    </header>
  );
};

export default Header;
