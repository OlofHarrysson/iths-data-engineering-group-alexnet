// darkMode.js

// Set a cookie with a specified name, value, and optional expiration period in days
export function setCookie(name, value, days) {
  const expires = new Date(Date.now() + days * 86400000); // 86400000 milliseconds / day
  document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires.toUTCString()}; path=/`;
}

// Get a cookie value by name
export function getCookie(name) {

  // Splits the document's cookies into an array
  const cookies = document.cookie.split('; ');

  // Iterate through the array, very similar to Python
  for (const cookie of cookies) {
    const [cookieName, cookieValue] = cookie.split('=');
    if (cookieName === name) {
      return decodeURIComponent(cookieValue);
    }
  }
  return null;
}

// Toggle dark mode
export function toggleDarkMode() {
  const body = document.body;
  body.classList.toggle('dark-mode');

  // Save dark mode preference to a cookie
  const darkModeEnabled = body.classList.contains('dark-mode');
  const darkModePref = darkModeEnabled ? '1' : '0';
  setCookie('dark_mode', darkModePref, 365);

  console.log('Dark mode toggled');
}

// Initialize dark mode on page load
document.addEventListener('DOMContentLoaded', () => {
  const darkModePref = getCookie('dark_mode');
  if (darkModePref === '1') {
    document.body.classList.add('dark-mode');
  }
});

// Toggle dark mode on button click
const toggleButton = document.getElementById('dark-mode-toggle');
if (toggleButton) {
  toggleButton.addEventListener('click', toggleDarkMode);
}
