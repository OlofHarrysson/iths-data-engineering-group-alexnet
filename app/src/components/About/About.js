import React from 'react';
import { Link } from 'react-router-dom';
import './About.css';
import Footer from '../Footer/Footer';
import HeaderSansSearch from '../Header/HeaderNoSearch';


const About = () => {
  return (
    <div>
      <HeaderSansSearch />
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
    <div className="image-container">
      <img src="https://img.freepik.com/premium-photo/collaboration-diversity-team-success-accounting-corporate-business-people-standing-together-support-portrait-smile-finance-employees-partnership-law-agency-office_590464-85793.jpg?w=2000" alt="Team" className="srs-image" />
    </div>

  <div className="center-container">
    <div className="team-text">
      We are:
      <li>Driven.</li>
      <li>Unlimited.</li>
      <li>Moral.</li>
      <li>Business.</li>
    </div>
  </div>


</div>

      <Footer />

    </div>
  );
};

export default About;
