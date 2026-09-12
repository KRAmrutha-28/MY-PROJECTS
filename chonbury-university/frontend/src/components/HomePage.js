import React, { useEffect, useState } from 'react';
import { Container, Row, Col, Card, Badge, Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const HomePage = () => {
  const [admissions, setAdmissions] = useState([]);
  const [courses, setCourses] = useState([]);

  useEffect(() => {
    fetchAdmissionStatus();
    fetchCourses();
  }, []);

  const fetchAdmissionStatus = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/admissions/status/`);
      setAdmissions(response.data);
    } catch (error) {
      console.error('Error fetching admissions:', error);
    }
  };

  const fetchCourses = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/courses/courses/`);
      setCourses(response.data);
    } catch (error) {
      console.error('Error fetching courses:', error);
    }
  };

  const getStatusColor = (status) => {
    switch(status) {
      case 'OPEN': return 'success';
      case 'CLOSED': return 'danger';
      case 'COMING_SOON': return 'warning';
      default: return 'secondary';
    }
  };

  return (
    <div>
      {/* Hero Section with Background Image */}
      <div style={{
        backgroundImage: 'url("https://images.unsplash.com/photo-1541339907198-e08756dedf3f?ixlib=rb-4.0.3")',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        height: '500px',
        position: 'relative'
      }}>
        <div style={{
          background: 'rgba(0, 0, 0, 0.6)',
          height: '100%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}>
          <Container className="text-center text-white">
            <h1 className="display-3 fw-bold">Welcome to Chanakya University</h1>      
            <p className="lead">Excellence in Education Since 1995 | Shaping Future Leaders</p>
            <p className="mb-4">UG & PG Courses | State-of-the-art Facilities | Industry Experts</p>
            <Button as={Link} to="/register" variant="primary" size="lg" className="me-2">
              Apply Now
            </Button>
            <Button as={Link} to="/courses" variant="outline-light" size="lg">
              Explore Courses
            </Button>
          </Container>
        </div>
      </div>

      <Container className="my-5">
        <h2 className="text-center mb-4">📢 Admission Status 2026</h2>
        <Row className="mb-5">
          {admissions.map(admission => (
            <Col md={4} key={admission.id} className="mb-3">
              <Card className="h-100 shadow-sm">
                <Card.Body>
                  <Card.Title>{admission.course_details?.name} - {admission.course_details?.specialization}</Card.Title>
                  <Card.Text>
                    <strong>Status:</strong> <Badge bg={getStatusColor(admission.status)}>{admission.status}</Badge><br/>
                    <strong>Last Date:</strong> {new Date(admission.last_date).toLocaleDateString()}<br/>
                    <strong>Application Fee:</strong> ₹{admission.application_fee}
                  </Card.Text>
                  <Button variant="outline-primary" size="sm">Apply Now</Button>
                </Card.Body>
              </Card>
            </Col>
          ))}
        </Row>

        <h2 className="text-center mb-4">🎓 Our Popular Courses</h2>
        <Row>
          {courses.slice(0, 6).map(course => (
            <Col md={4} key={course.id} className="mb-4">
              <Card className="h-100 shadow-sm">
                <Card.Body>
                  <Card.Title>{course.name}</Card.Title>
                  <Card.Subtitle className="mb-2 text-muted">{course.specialization}</Card.Subtitle>
                  <Card.Text>
                    <strong>Type:</strong> {course.course_type}<br/>
                    <strong>Duration:</strong> {course.duration} years<br/>
                    <strong>Campus:</strong> {course.campus_name}<br/>
                    <strong>Fee:</strong> ₹{course.fee?.toLocaleString()}/year
                  </Card.Text>
                  <Badge bg="info" className="me-1">{course.course_type}</Badge>
                  <Badge bg="secondary">Seats Available</Badge>
                </Card.Body>
              </Card>
            </Col>
          ))}
        </Row>

        {/* BTech Section */}
        <Row className="mt-5">
          <Col md={6}>
            <Card className="bg-light border-0 shadow">
              <Card.Body>
                <Card.Title className="text-primary">💻 BTech Computer Science</Card.Title>
                <Card.Text>
                  <strong>Duration:</strong> 4 Years<br/>
                  <strong>Specializations:</strong> AI & ML, Cloud Computing, Cybersecurity, Data Science<br/>
                  <strong>Eligibility:</strong> 10+2 with 60% aggregate in PCM<br/>
                  <strong>Total Seats:</strong> 120<br/>
                  <strong>Available Seats:</strong> 45
                </Card.Text>
                <Button variant="primary">Learn More</Button>
              </Card.Body>
            </Card>
          </Col>
          <Col md={6}>
            <Card className="bg-light border-0 shadow">
              <Card.Body>
                <Card.Title className="text-primary">📡 BTech Electronics & Communication</Card.Title>
                <Card.Text>
                  <strong>Duration:</strong> 4 Years<br/>
                  <strong>Specializations:</strong> VLSI Design, Embedded Systems, IoT, Robotics<br/>
                  <strong>Eligibility:</strong> 10+2 with 60% aggregate in PCM<br/>
                  <strong>Total Seats:</strong> 90<br/>
                  <strong>Available Seats:</strong> 30
                </Card.Text>
                <Button variant="primary">Learn More</Button>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default HomePage;