// darkMode.js

// Function to set a cookie
function setCookie(name, value, days) {
    const expires = new Date(Date.now() + days * 24 * 60 * 60 * 1000).toUTCString();
    document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/`;
  }

  // Function to get a cookie value
  function getCookie(name) {
    const cookies = document.cookie.split('; ');
    for (const cookie of cookies) {
      const [cookieName, cookieValue] = cookie.split('=');
      if (cookieName === name) {
        return decodeURIComponent(cookieValue);
      }
    }
    return null;
  }

  // Function to toggle dark mode
  function toggleDarkMode() {
    const body = document.body;
    body.classList.toggle('dark-mode');

    // Save the dark mode preference to a cookie
    const darkModeEnabled = body.classList.contains('dark-mode');
    setCookie('darkMode', darkModeEnabled ? '1' : '0', 30);

    // Log the toggled message
    console.log('Dark mode toggled');
  }

  // Toggle dark mode on button click
  const toggleButton = document.getElementById('dark-mode-toggle');
  toggleButton.addEventListener('click', toggleDarkMode);

  // Check and apply dark mode preference on page load
  document.addEventListener('DOMContentLoaded', () => {
    const darkModePref = getCookie('darkMode');
    if (darkModePref === '1') {
      document.body.classList.add('dark-mode');
    }
  });