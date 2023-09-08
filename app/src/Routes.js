import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import App from './App';
import About from './About'; // Import your About component

const AppRoutes = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </Router>
  );
};

export default AppRoutes;
