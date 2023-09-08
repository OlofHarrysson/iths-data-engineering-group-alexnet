import React from 'react';
import { Link } from 'react-router-dom';

const About = () => {
  return (
    <div>
      <h1>About Us</h1>
      <p>This is the About page content.</p>
      <Link to="/">Go back to Home</Link>
    </div>
  );
};

export default About;
