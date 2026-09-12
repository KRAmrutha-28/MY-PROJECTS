import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Table, Badge, Accordion } from 'react-bootstrap';
import axios from 'axios';
import DirectionsBusIcon from '@mui/icons-material/DirectionsBus';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import PlaceIcon from '@mui/icons-material/Place';

const API_BASE_URL = 'http://localhost:8000/api';

const TransportInfo = () => {
  const [transportData, setTransportData] = useState([]);

  useEffect(() => {
    fetchTransportDetails();
  }, []);

  const fetchTransportDetails = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/transport/details/`);
      setTransportData(response.data);
    } catch (error) {
      console.error('Error fetching transport details:', error);
    }
  };

  return (
    <Container className="my-5">
      <h2 className="text-center mb-4">
        <DirectionsBusIcon sx={{ mr: 2, fontSize: 40 }} />
        🚍 Transportation Facilities
      </h2>
      
      <p className="text-center mb-5">
        Chonbury University provides reliable bus transportation for students and staff across multiple routes.
        Limited seats available on first-come, first-served basis.
      </p>

      <Row>
        {transportData.map(route => (
          <Col md={12} key={route.route_number} className="mb-4">
            <Card className="shadow">
              <Card.Header className="bg-primary text-white">
                <h4 className="mb-0">
                  <PlaceIcon /> Route {route.route_number}: {route.route_name}
                </h4>
              </Card.Header>
              <Card.Body>
                <Row className="mb-3">
                  <Col md={4}>
                    <strong>🚏 Start Point:</strong> {route.start_point}
                  </Col>
                  <Col md={4}>
                    <strong>🏁 End Point:</strong> {route.end_point}
                  </Col>
                  <Col md={4}>
                    <strong>🚌 Total Buses:</strong> <Badge bg="info">{route.total_buses}</Badge>
                    {' '}
                    <strong>Active:</strong> <Badge bg="success">{route.active_buses}</Badge>
                  </Col>
                </Row>
                
                <h6>📌 Stops:</h6>
                <p className="mb-3">{route.stops}</p>

                <h6 className="mt-3">🚍 Bus Schedule & Details:</h6>
                <Table striped bordered hover responsive>
                  <thead className="bg-light">
                    <tr>
                      <th>Bus Number</th>
                      <th>Registration No.</th>
                      <th>Capacity</th>
                      <th>Driver Name</th>
                      <th>Driver Contact</th>
                      <th>Morning Departure</th>
                      <th>Evening Departure</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {route.buses.map(bus => (
                      <tr key={bus.id}>
                        <td><strong>{bus.bus_number}</strong></td>
                        <td>{bus.registration_number}</td>
                        <td>{bus.capacity} seats</td>
                        <td>{bus.driver_name}</td>
                        <td>{bus.driver_contact}</td>
                        <td><AccessTimeIcon sx={{ fontSize: 14 }} /> {bus.morning_departure}</td>
                        <td><AccessTimeIcon sx={{ fontSize: 14 }} /> {bus.evening_departure}</td>
                        <td>
                          <Badge bg={bus.status === 'ACTIVE' ? 'success' : 'warning'}>
                            {bus.status}
                          </Badge>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </Table>

                <Card className="bg-warning bg-opacity-10 mt-3">
                  <Card.Body>
                    <strong>⚠️ Important Note:</strong> Limited seats available per bus. Students need to register for 
                    transportation at the beginning of each semester. Monthly bus pass fee: ₹2500.
                  </Card.Body>
                </Card>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>

      {transportData.length === 0 && (
        <div className="text-center">
          <p>No transport routes available at the moment.</p>
        </div>
      )}
    </Container>
  );
};

export default TransportInfo;