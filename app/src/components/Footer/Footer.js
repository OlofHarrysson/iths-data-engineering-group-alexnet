import React from 'react';
import { Link } from 'react-router-dom';

function Footer({ handleToggleDarkMode }) {
  return (
    <div className="bottom_footer">
      <div className="dark-mode-toggle" onClick={handleToggleDarkMode}>
        <span>Toggle Dark Mode</span>
      </div>
      <div className="example-text-column">
        <div className="example-text"><p>🌐</p></div>
      </div>
      <div className="example-text-column">
        <div className="example-text">
          {/* Add a Link to the "About" page */}
          <p><Link to="/about">About</Link></p>
        </div>
      </div>
    </div>
  );
}

export default Footer;