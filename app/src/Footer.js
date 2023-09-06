import React from 'react';

function Footer({ handleToggleDarkMode }) { // Destructure the prop
  return (
    <div className="bottom_footer">
      <div className="dark-mode-toggle" onClick={handleToggleDarkMode}>
        <span>Toggle Dark Mode</span>
      </div>
      <div className="example-text-column">
        <div className="example-text"><p>Example column: 3 items</p></div>
        <div className="example-text"><p>Example data: 20 ms</p></div>
        <div className="example-text"><p>What stats we want here?</p></div>
      </div>
      <div className="example-text-column">
        <div className="example-text"><p>Example column: 1 item</p></div>
      </div>
    </div>
  );
}

export default Footer;
