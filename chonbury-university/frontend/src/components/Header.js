import React, { useState } from 'react';
import { Navbar, Nav, Container, NavDropdown } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import SchoolIcon from '@mui/icons-material/School';
import MenuIcon from '@mui/icons-material/Menu';

const Header = () => {
  const [expanded, setExpanded] = useState(false);

  return (
    <Navbar bg="primary" variant="dark" expand="lg" sticky="top" expanded={expanded}>
      <Container>
        <Navbar.Brand as={Link} to="/" onClick={() => setExpanded(false)}>
          <SchoolIcon sx={{ mr: 1, fontSize: 30 }} />
          <strong>🏛️ Chanakya University</strong>
        </Navbar.Brand>
        <Navbar.Toggle 
          aria-controls="basic-navbar-nav" 
          onClick={() => setExpanded(expanded ? false : true)}
        >
          <MenuIcon />
        </Navbar.Toggle>
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="ms-auto">
            <Nav.Link as={Link} to="/" onClick={() => setExpanded(false)}>Home</Nav.Link>
            <Nav.Link as={Link} to="/register" onClick={() => setExpanded(false)}>Register</Nav.Link>
            <NavDropdown title="Academics" id="academics-dropdown">
              <NavDropdown.Item as={Link} to="/courses" onClick={() => setExpanded(false)}>Courses</NavDropdown.Item>
              <NavDropdown.Item as={Link} to="/faculty" onClick={() => setExpanded(false)}>Faculty</NavDropdown.Item>
              <NavDropdown.Item as={Link} to="/student-faculty" onClick={() => setExpanded(false)}>Student-Faculty</NavDropdown.Item>
            </NavDropdown>
            <Nav.Link as={Link} to="/transport" onClick={() => setExpanded(false)}>Transport</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default Header;