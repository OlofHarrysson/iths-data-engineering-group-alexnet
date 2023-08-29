// Not used as of now. Can be used to enlarge summary text.

import React from 'react';
import styles from './alexneet.module.css';

const ArticleDetails = () => {
  return (
    <div className={styles.articleDetails}>
      <h2 id="article-title"></h2>
      <p id="article-summary"></p>
    </div>
  );
};

export default ArticleDetails;