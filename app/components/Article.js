// Article / cards

import React from 'react';
import styles from './alexneet.module.css';

const ArticleCard = ({ cardData }) => {
  return (
    <div className={styles.article}>
      <h1>{cardData.title}</h1>
      <p>{cardData.description}</p>
      <a href="blank">Read full article</a>
    </div>
  );
};

export default ArticleCard;