// This file should contain minimal code that focuses on rendering the root component.

import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// ------ Metrics ------ // TODO: Move this to other script

// Get browser and OS information
const userAgent = navigator.userAgent;
const browserInfo = {
  name: 'Unknown',
  version: 'Unknown',
};
const osInfo = {
  name: 'Unknown',
  version: 'Unknown',
};

// Browser
if (userAgent.includes('Chrome')) {
  browserInfo.name = 'Chrome';
  const versionStart = userAgent.indexOf('Chrome') + 7;
  browserInfo.version = userAgent.substring(versionStart, versionStart + 2);
} else if (userAgent.includes('Firefox')) {
  browserInfo.name = 'Firefox';
  const versionStart = userAgent.indexOf('Firefox') + 8;
  browserInfo.version = userAgent.substring(versionStart, versionStart + 2);
}

// OS
if (userAgent.includes('Windows NT')) {
  osInfo.name = 'Windows';
  const versionStart = userAgent.indexOf('Windows NT') + 11;
  osInfo.version = userAgent.substring(versionStart, versionStart + 6);
} else if (userAgent.includes('Mac OS X')) {
  osInfo.name = 'macOS';
  const versionStart = userAgent.indexOf('Mac OS X') + 9;
  osInfo.version = userAgent.substring(versionStart, versionStart + 5);
}

console.log('Browser Info:', browserInfo);
console.log('OS Info:', osInfo);
