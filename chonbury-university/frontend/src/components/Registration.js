import React, { useState, useEffect } from 'react';
import { Container, Form, Button, Row, Col, Alert, Card } from 'react-bootstrap';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const Registration = () => {
  const [formData, setFormData] = useState({
    student_name: '',
    email: '',
    phone: '',
    course_interested: '',
    comment: ''
  });
  const [courses, setCourses] = useState([]);
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchCourses();
  }, []);

  const fetchCourses = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/courses/courses/`);
      setCourses(response.data);
    } catch (error) {
      console.error('Error fetching courses:', error);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await axios.post(`${API_BASE_URL}/inquiries/create/`, formData);
      setSubmitted(true);
      setFormData({
        student_name: '',
        email: '',
        phone: '',
        course_interested: '',
        comment: ''
      });
      setTimeout(() => setSubmitted(false), 3000);
    } catch (error) {
      setError('Registration failed. Please try again.');
      setTimeout(() => setError(''), 3000);
    }
  };

  return (
    <Container className="my-5">
      <Row className="justify-content-center">
        <Col md={8}>
          <Card className="shadow">
            <Card.Header as="h3" className="text-center bg-primary text-white">
              📝 Student Registration Form
            </Card.Header>
            <Card.Body>
              {submitted && <Alert variant="success">✅ Registration successful! We'll contact you soon.</Alert>}
              {error && <Alert variant="danger">{error}</Alert>}
              <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3">
                  <Form.Label>Full Name *</Form.Label>
                  <Form.Control
                    type="text"
                    name="student_name"
                    value={formData.student_name}
                    onChange={handleChange}
                    required
                    placeholder="Enter your full name"
                  />
                </Form.Group>

                <Form.Group className="mb-3">
                  <Form.Label>Email Address *</Form.Label>
                  <Form.Control
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    placeholder="Enter your email"
                  />
                </Form.Group>

                <Form.Group className="mb-3">
                  <Form.Label>Phone Number *</Form.Label>
                  <Form.Control
                    type="tel"
                    name="phone"
                    value={formData.phone}
                    onChange={handleChange}
                    required
                    placeholder="Enter your phone number"
                  />
                </Form.Group>

                <Form.Group className="mb-3">
                  <Form.Label>Course Interested In *</Form.Label>
                  <Form.Select
                    name="course_interested"
                    value={formData.course_interested}
                    onChange={handleChange}
                    required
                  >
                    <option value="">Select a course</option>
                    {courses.map(course => (
                      <option key={course.id} value={course.id}>
                        {course.name} - {course.specialization}
                      </option>
                    ))}
                  </Form.Select>
                </Form.Group>

                <Form.Group className="mb-3">
                  <Form.Label>Additional Comments / Questions</Form.Label>
                  <Form.Control
                    as="textarea"
                    rows={4}
                    name="comment"
                    value={formData.comment}
                    onChange={handleChange}
                    placeholder="Any specific questions about course curriculum, faculty, facilities, or admission process?"
                  />
                </Form.Group>

                <Button variant="primary" type="submit" className="w-100" size="lg">
                  Register Now
                </Button>
              </Form>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default Registration;