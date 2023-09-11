// ArticleCard.js
import React from 'react';

const ArticleCard = ({ item, darkMode }) => {
  return (
    <div className={`articles-card ${darkMode ? 'dark-mode-card' : ''}`}>
      <h2>{item.title}</h2>
      <p>{item.description}</p>
      <div className="article-footer">
        <a href={item.link}>🌐 Full Article</a>
        <p>{item.published}</p>
      </div>
    </div>
  );
}

export default ArticleCard;
