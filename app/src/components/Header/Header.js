import React from 'react';
import styles from './header.module.css';
import { Link } from 'react-router-dom';

const Header = ({ setSearchQuery, handleAddBotClick }) => {
  return (
    <header className={styles.alxHeader}>

      {/* Title and subtitle wrapped in a Link */}
      <Link to="/" className={styles.headerLink}>
        <div className={styles.headerContent}>
          <div className={styles.title}>
            <h1>ANN: AlexNet News</h1>
            <h2>Your Source for Intelligent News Analysis</h2>
          </div>
        </div>
      </Link>

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
