import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Badge, Form } from 'react-bootstrap';
import axios from 'axios';
import PersonIcon from '@mui/icons-material/Person';

const API_BASE_URL = 'http://localhost:8000/api';

const FacultyInfo = () => {
  const [faculty, setFaculty] = useState([]);
  const [filteredFaculty, setFilteredFaculty] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchFaculty();
  }, []);

  const fetchFaculty = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/faculty/faculty/`);
      setFaculty(response.data);
      setFilteredFaculty(response.data);
    } catch (error) {
      console.error('Error fetching faculty:', error);
    }
  };

  const handleSearch = (e) => {
    const term = e.target.value.toLowerCase();
    setSearchTerm(term);
    const filtered = faculty.filter(f => 
      f.name.toLowerCase().includes(term) ||
      f.specialization.toLowerCase().includes(term) ||
      f.designation.toLowerCase().includes(term)
    );
    setFilteredFaculty(filtered);
  };

  const getDesignationBadge = (designation) => {
    const colors = {
      'PROF': 'danger',
      'APROF': 'warning',
      'ASPROF': 'info',
      'LECT': 'secondary'
    };
    return colors[designation] || 'primary';
  };

  const getDesignationText = (designation) => {
    const texts = {
      'PROF': 'Professor',
      'APROF': 'Associate Professor',
      'ASPROF': 'Assistant Professor',
      'LECT': 'Lecturer'
    };
    return texts[designation] || designation;
  };

  return (
    <Container className="my-5">
      <h2 className="text-center mb-4">👨‍🏫 Our Esteemed Faculty</h2>
      
      <Row className="mb-4">
        <Col md={6} className="mx-auto">
          <Form.Control
            type="text"
            placeholder="🔍 Search faculty by name, specialization, or designation..."
            value={searchTerm}
            onChange={handleSearch}
          />
        </Col>
      </Row>

      <Row>
        {filteredFaculty.map(f => (
          <Col md={6} lg={4} key={f.id} className="mb-4">
            <Card className="h-100 shadow-sm">
              <Card.Body>
                <div className="text-center mb-3">
                  <div className="bg-light rounded-circle d-inline-flex p-3">
                    <PersonIcon sx={{ fontSize: 60, color: '#1976d2' }} />
                  </div>
                </div>
                <Card.Title className="text-center">{f.name}</Card.Title>
                <Card.Subtitle className="text-center text-muted mb-3">
                  <Badge bg={getDesignationBadge(f.designation)}>
                    {getDesignationText(f.designation)}
                  </Badge>
                  {f.is_hod && <Badge bg="primary" className="ms-2">Head of Department</Badge>}
                </Card.Subtitle>
                <Card.Text>
                  <strong>📧 Email:</strong> {f.email}<br/>
                  <strong>📞 Phone:</strong> {f.phone}<br/>
                  <strong>🎓 Qualification:</strong> {f.qualification}<br/>
                  <strong>🔬 Specialization:</strong> {f.specialization}<br/>
                  <strong>⭐ Experience:</strong> {f.experience_years} years<br/>
                  <strong>📅 Joined:</strong> {new Date(f.joining_date).toLocaleDateString()}
                </Card.Text>
                {f.bio && <p className="mt-2"><em>"{f.bio}"</em></p>}
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>
    </Container>
  );
};

export default FacultyInfo;