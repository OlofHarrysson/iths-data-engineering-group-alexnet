import React from 'react';
import { Link } from 'react-router-dom';
import './About.css';

const About = () => {
  return (
    <div>
      <div className="header">
        <h1>About Us</h1>
      </div>
      <div className="content">
        <p>Welcome to the AI Newsfeed "About" Page</p>
        <h2>Introduction:</h2>
        <p>At AI Newsfeed, we are passionate about bringing you the latest insights into the world of artificial intelligence and machine learning. Our mission is to empower individuals, businesses, and technology enthusiasts with knowledge about the cutting-edge developments, trends, and innovations in AI.</p>
        <h2>Mission and Vision:</h2>
        <p>Our mission is to make AI accessible and understandable to everyone. We believe that AI has the potential to transform industries, improve lives, and shape the future. Our vision is to be your trusted source for intelligent news analysis, fostering a community of AI enthusiasts, and promoting informed decision-making.</p>
        <h2>History:</h2>
        <p>AI Newsfeed was founded in [Year] by a team of dedicated AI experts and technology enthusiasts. What started as a passion project has grown into a leading platform for AI-related news and insights. Our journey has been marked by a commitment to providing accurate, up-to-date, and informative content to our readers.</p>
        <Link to="/">Go back to Home</Link>
      </div>
      <div className="Team">
      // Team with images?
      </div>
      <div className="Values">

      </div>

    </div>
  );
};

export default About;
