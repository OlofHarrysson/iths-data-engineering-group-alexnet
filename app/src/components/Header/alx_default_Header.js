// components/Header.js
// Default header
import React from 'react';
import styles from './alx_header.module.css';

const Header = () => {
    return (
      <header className={styles.alxHeader}>
        <div className={styles.headerContent}>
            <div className={styles.title}>
              <h1>AAIN: Alexnet AI Newsfeed</h1>
              <h2>Your Source for Intelligent News Analysis</h2>
            </div>
        </div>
      </header>
    );
  };

export default Header;

