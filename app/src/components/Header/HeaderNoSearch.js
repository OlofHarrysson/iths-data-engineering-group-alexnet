import React from 'react';
import styles from './header.module.css';
import { Link } from 'react-router-dom';

const HeaderSansSearch = () => {
  return (
    <header className={styles.alxHeader}>
      <Link to="/" className={styles.headerLink}>
        <div className={styles.headerContent}>
          <div className={styles.title}>
            <h1>ANN: AlexNet News</h1>
            <h2>Your Source for Intelligent News Analysis</h2>
          </div>
        </div>
      </Link>
    </header>
  );
};

export default HeaderSansSearch;
