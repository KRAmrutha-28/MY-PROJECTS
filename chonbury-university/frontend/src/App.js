import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import Header from './components/Header';
import Footer from './components/Footer';
import HomePage from './components/HomePage';
import Registration from './components/Registration';
import CourseDetails from './components/CourseDetails';
import FacultyInfo from './components/FacultyInfo';
import TransportInfo from './components/TransportInfo';
import StudentFaculty from './components/StudentFaculty';
import InquiryPopup from './components/InquiryPopup';

function App() {
  return (
    <Router>
      <Header />
      <InquiryPopup />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/register" element={<Registration />} />
        <Route path="/courses" element={<CourseDetails />} />
        <Route path="/faculty" element={<FacultyInfo />} />
        <Route path="/student-faculty" element={<StudentFaculty />} />
        <Route path="/transport" element={<TransportInfo />} />
      </Routes>
      <Footer />
    </Router>
  );
}

export default App;