import React from 'react';
import './Footer.css';
import { Link } from 'react-router-dom';

function Footer({ handleToggleDarkMode }) {
  return (
    <div className="bottom_footer">
      <div className="dark-mode-toggle" onClick={handleToggleDarkMode}>
        <span>Toggle Dark Mode</span>
      </div>
      <div className="example-text-column">
        <div className="footer-text">
          <p><Link to="/about">About AlexNet</Link></p>
        </div>
      </div>
    </div>
  );
}

export default Footer;