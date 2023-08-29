import React from 'react';
import Article from './Article';
import styles from './alexneet.module.css';

const ArticleList = ({ data }) => {
  return (
    <div className={styles.articleList}>
      {data.map((card, index) => (
        <Article key={index} cardData={card} />
      ))}
    </div>
  );
};

export default ArticleList;
