import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button, Modal, Table, Badge, Spinner } from 'react-bootstrap';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const CourseDetails = () => {
  const [courses, setCourses] = useState([]);
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [faculty, setFaculty] = useState([]);
  const [rooms, setRooms] = useState([]);
  const [loading, setLoading] = useState(false);

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

  const fetchCourseDetails = async (courseId) => {
    setLoading(true);
    try {
      // Fetch faculty for this course
      const facultyRes = await axios.get(`http://localhost:8000/api/faculty/by-course/${courseId}/`);
      setFaculty(facultyRes.data);
      
      // Fetch course details including rooms
      const courseRes = await axios.get(`${API_BASE_URL}/courses/courses/${courseId}/`);
      setRooms(courseRes.data.rooms || []);
      setSelectedCourse(courseRes.data);
      setShowModal(true);
    } catch (error) {
      console.error('Error fetching course details:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container className="my-5">
      <h2 className="text-center mb-4">📚 Course Details</h2>
      <Row>
        {courses.map(course => (
          <Col md={6} lg={4} key={course.id} className="mb-4">
            <Card className="h-100 shadow">
              <Card.Body>
                <Card.Title>{course.name}</Card.Title>
                <Card.Subtitle className="mb-2 text-muted">{course.specialization}</Card.Subtitle>
                <Card.Text>
                  <strong>Course Type:</strong> {course.course_type}<br/>
                  <strong>Duration:</strong> {course.duration} years<br/>
                  <strong>Campus:</strong> {course.campus_name}<br/>
                  <strong>Fee:</strong> ₹{course.fee?.toLocaleString()}/year<br/>
                  <strong>Description:</strong> {course.description.substring(0, 100)}...
                </Card.Text>
                <Badge bg="primary" className="me-1">{course.course_type}</Badge>
                <Badge bg="info">UG/PG</Badge>
                <div className="mt-3">
                  <Button 
                    variant="outline-primary" 
                    size="sm"
                    onClick={() => fetchCourseDetails(course.id)}
                  >
                    View Faculty & Facilities
                  </Button>
                </div>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>

      <Modal show={showModal} onHide={() => setShowModal(false)} size="lg">
        <Modal.Header closeButton className="bg-primary text-white">
          <Modal.Title>Course Details - Faculty & Facilities</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {loading ? (
            <div className="text-center">
              <Spinner animation="border" />
              <p>Loading details...</p>
            </div>
          ) : (
            <>
              <h5>👨‍🏫 Faculty Members ({faculty.length})</h5>
              <Table striped bordered hover responsive>
                <thead className="bg-light">
                  <tr>
                    <th>Name</th>
                    <th>Designation</th>
                    <th>Qualification</th>
                    <th>Experience</th>
                    <th>HOD</th>
                  </tr>
                </thead>
                <tbody>
                  {faculty.map(f => (
                    <tr key={f.id}>
                      <td><strong>{f.name}</strong></td>
                      <td>{f.get_designation_display || f.designation}</td>
                      <td>{f.qualification}</td>
                      <td>{f.experience_years} years</td>
                      <td>{f.is_hod ? '✅ Yes' : '❌ No'}</td>
                    </tr>
                  ))}
                </tbody>
              </Table>

              <h5 className="mt-4">🏛️ Rooms & Facilities ({rooms.length})</h5>
              <Table striped bordered hover responsive>
                <thead className="bg-light">
                  <tr>
                    <th>Room Number</th>
                    <th>Room Type</th>
                    <th>Capacity</th>
                    <th>AC Available</th>
                    <th>Projector</th>
                    <th>Facilities</th>
                  </tr>
                </thead>
                <tbody>
                  {rooms.map(room => (
                    <tr key={room.id}>
                      <td>{room.room_number}</td>
                      <td>{room.room_type}</td>
                      <td>{room.capacity}</td>
                      <td>{room.is_ac_available ? '✅' : '❌'}</td>
                      <td>{room.has_projector ? '✅' : '❌'}</td>
                      <td>{room.facilities}</td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </>
          )}
        </Modal.Body>
      </Modal>
    </Container>
  );
};

export default CourseDetails;