import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import FacebookIcon from '@mui/icons-material/Facebook';
import TwitterIcon from '@mui/icons-material/Twitter';
import LinkedInIcon from '@mui/icons-material/LinkedIn';
import InstagramIcon from '@mui/icons-material/Instagram';
import EmailIcon from '@mui/icons-material/Email';
import PhoneIcon from '@mui/icons-material/Phone';
import LocationOnIcon from '@mui/icons-material/LocationOn';

const Footer = () => {
  return (
    <footer className="bg-dark text-white mt-5 py-4">
      <Container>
        <Row>
          <Col md={4} className="mb-3">
            <h5>🏛️ Chanakya University</h5>
            <p><LocationOnIcon sx={{ fontSize: 18, mr: 1 }} /> Knowledge Park, Vidya Vihar, City Center</p>
            <p><PhoneIcon sx={{ fontSize: 18, mr: 1 }} /> +91 1234567890</p>
            <p><EmailIcon sx={{ fontSize: 18, mr: 1 }} /> info@chanakya.edu</p>
          </Col>
          <Col md={4} className="mb-3">
            <h5>Quick Links</h5>
            <ul className="list-unstyled">
              <li><a href="/" className="text-white text-decoration-none">Home</a></li>
              <li><a href="/courses" className="text-white text-decoration-none">Courses</a></li>
              <li><a href="/faculty" className="text-white text-decoration-none">Faculty</a></li>
              <li><a href="/transport" className="text-white text-decoration-none">Transport</a></li>
            </ul>
          </Col>
          <Col md={4} className="mb-3">
            <h5>Follow Us</h5>
            <div>
              <FacebookIcon sx={{ mr: 2, cursor: 'pointer' }} />
              <TwitterIcon sx={{ mr: 2, cursor: 'pointer' }} />
              <LinkedInIcon sx={{ mr: 2, cursor: 'pointer' }} />
              <InstagramIcon sx={{ cursor: 'pointer' }} />
            </div>
            <div className="mt-3">
              <small>© 2026 Chanakya University. All rights reserved.</small>
            </div>
          </Col>
        </Row>
      </Container>
    </footer>
  );
};

export default Footer;