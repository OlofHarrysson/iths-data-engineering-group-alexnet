// pages/index.js
import React from 'react';
import Header from '../components/Header';
import ArticleList from '../components/ArticleList';
import ArticleDetails from '../components/ArticleDetails';

const data = [
  {
    title: "Article #1",
    description: "wubadubadub wubalub dub."
  },
  {
    title: "Article #2",
    description: "Another interesting article."
  },
  {
    title: "Article #3",
    description: "A third article to showcase."
  },
  {
    title: "Article #4",
    description: "A fourth article to showcase."
  },
  {
    title: "Article #5",
    description: "A fifth article to showcase."
  }
];

const Home = () => {
  return (
    <div>
      <Header />
      <main>
        <div class="article-list">
        <ArticleList data={data} />
        <ArticleDetails />
        </div>
      </main>
    </div>
  );
};

export default Home;
