import { useState, useEffect } from 'react';

const useArticleFilter = (articles, initialQuery = '') => {
  const [searchQuery, setSearchQuery] = useState(initialQuery);
  const [filteredArticles, setFilteredArticles] = useState(articles);

  useEffect(() => {
    const filtered = filterArticles(articles, searchQuery);
    setFilteredArticles(filtered);
  }, [articles, searchQuery]);

  const handleSearchQueryChange = (newQuery) => {
    setSearchQuery(newQuery);
  };

  return { filteredArticles, handleSearchQueryChange };
};

const filterArticles = (articles, query) => {
  if (!query) {
    return articles;
  }

  return articles.filter((article) =>
    article.title.toLowerCase().includes(query.toLowerCase())
  );
};

export default useArticleFilter;
