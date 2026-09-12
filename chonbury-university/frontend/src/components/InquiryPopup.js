import React, { useState, useEffect } from 'react';
import { Modal, Button, Form, Alert } from 'react-bootstrap';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const InquiryPopup = () => {
  const [show, setShow] = useState(false);
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
    const timer = setTimeout(() => {
      const hasSeenPopup = localStorage.getItem('hasSeenPopup');
      if (!hasSeenPopup) {
        setShow(true);
        localStorage.setItem('hasSeenPopup', 'true');
      }
    }, 2000);

    fetchCourses();
    return () => clearTimeout(timer);
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
      setTimeout(() => {
        setShow(false);
        setSubmitted(false);
      }, 2000);
    } catch (error) {
      setError('Failed to submit inquiry. Please try again.');
    }
  };

  return (
    <Modal show={show} onHide={() => setShow(false)} size="lg">
      <Modal.Header closeButton className="bg-primary text-white">
        <Modal.Title>📢 Get Information About Courses</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {submitted ? (
          <Alert variant="success">
            <Alert.Heading>Thank you for your inquiry!</Alert.Heading>
            <p>We will contact you soon with all the details about the course.</p>
          </Alert>
        ) : (
          <Form onSubmit={handleSubmit}>
            {error && <Alert variant="danger">{error}</Alert>}
            <Form.Group className="mb-3">
              <Form.Label>Student Name *</Form.Label>
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
              <Form.Label>Additional Comments</Form.Label>
              <Form.Control
                as="textarea"
                rows={3}
                name="comment"
                value={formData.comment}
                onChange={handleChange}
                placeholder="Any specific questions about the course, faculty, or facilities?"
              />
            </Form.Group>
            <Button variant="primary" type="submit" className="w-100">
              Submit Inquiry
            </Button>
          </Form>
        )}
      </Modal.Body>
    </Modal>
  );
};

export default InquiryPopup;