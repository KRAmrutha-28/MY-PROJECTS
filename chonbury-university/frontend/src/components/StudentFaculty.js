import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Form, Table, Badge } from 'react-bootstrap';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const StudentFaculty = () => {
  const [courses, setCourses] = useState([]);
  const [selectedCourse, setSelectedCourse] = useState('');
  const [faculty, setFaculty] = useState([]);
  const [allFaculty, setAllFaculty] = useState([]);

  useEffect(() => {
    fetchCourses();
    fetchAllFaculty();
  }, []);

  const fetchCourses = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/courses/courses/`);
      setCourses(response.data);
    } catch (error) {
      console.error('Error fetching courses:', error);
    }
  };

  const fetchAllFaculty = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/faculty/faculty/`);
      setAllFaculty(response.data);
    } catch (error) {
      console.error('Error fetching faculty:', error);
    }
  };

  const handleCourseChange = async (e) => {
    const courseId = e.target.value;
    setSelectedCourse(courseId);
    if (courseId) {
      try {
        const response = await axios.get(`http://localhost:8000/api/faculty/by-course/${courseId}/`);
        setFaculty(response.data);
      } catch (error) {
        console.error('Error fetching faculty for course:', error);
      }
    } else {
      setFaculty([]);
    }
  };

  const getHOD = () => {
    return faculty.find(f => f.is_hod);
  };

  return (
    <Container className="my-5">
      <h2 className="text-center mb-4">👥 Student-Faculty Information</h2>
      
      <Row className="mb-4">
        <Col md={6} className="mx-auto">
          <Form.Select 
            value={selectedCourse} 
            onChange={handleCourseChange}
            className="form-select-lg"
          >
            <option value="">Select a course to view faculty members</option>
            {courses.map(course => (
              <option key={course.id} value={course.id}>
                {course.name} - {course.specialization}
              </option>
            ))}
          </Form.Select>
        </Col>
      </Row>

      {selectedCourse && (
        <>
          <Row className="mb-4">
            <Col md={6} className="mx-auto">
              <Card className="bg-info text-white text-center">
                <Card.Body>
                  <Card.Title>📌 Head of Department</Card.Title>
                  {getHOD() ? (
                    <>
                      <h3>{getHOD().name}</h3>
                      <p>{getHOD().qualification} | {getHOD().experience_years}+ years experience</p>
                      <p>📧 {getHOD().email} | 📞 {getHOD().phone}</p>
                    </>
                  ) : (
                    <p>No HOD assigned yet</p>
                  )}
                </Card.Body>
              </Card>
            </Col>
          </Row>

          <h4 className="mb-3">Faculty Members ({faculty.length})</h4>
          <Table striped bordered hover responsive>
            <thead className="bg-primary text-white">
              <tr>
                <th>#</th>
                <th>Faculty Name</th>
                <th>Designation</th>
                <th>Qualification</th>
                <th>Specialization</th>
                <th>Experience</th>
                <th>Contact</th>
              </tr>
            </thead>
            <tbody>
              {faculty.map((f, index) => (
                <tr key={f.id}>
                  <td>{index + 1}</td>
                  <td>
                    <strong>{f.name}</strong>
                    {f.is_hod && <Badge bg="primary" className="ms-2">HOD</Badge>}
                  </td>
                  <td>{f.designation}</td>
                  <td>{f.qualification}</td>
                  <td>{f.specialization}</td>
                  <td>{f.experience_years} years</td>
                  <td>
                    <small>{f.email}<br/>{f.phone}</small>
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>

          <Card className="mt-4 bg-light">
            <Card.Body>
              <h5>📊 Faculty Statistics</h5>
              <Row>
                <Col md={3}>
                  <div className="text-center">
                    <h3>{faculty.length}</h3>
                    <p>Total Faculty</p>
                  </div>
                </Col>
                <Col md={3}>
                  <div className="text-center">
                    <h3>{faculty.filter(f => f.designation === 'PROF').length}</h3>
                    <p>Professors</p>
                  </div>
                </Col>
                <Col md={3}>
                  <div className="text-center">
                    <h3>{faculty.filter(f => f.designation === 'APROF').length}</h3>
                    <p>Associate Professors</p>
                  </div>
                </Col>
                <Col md={3}>
                  <div className="text-center">
                    <h3>{faculty.reduce((sum, f) => sum + (f.experience_years || 0), 0)}</h3>
                    <p>Total Experience (Years)</p>
                  </div>
                </Col>
              </Row>
            </Card.Body>
          </Card>
        </>
      )}
    </Container>
  );
};

export default StudentFaculty;