import React from 'react';
import './App.css';
import StudentRegistration from './pages/StudentRegistration'
import StudentsPage from './pages/students/StudentsPage';
import SessionsPage from './pages/sessions/SessionsPage'
import NavBar from './NavBar';
import {Routes, Route, useMatch } from 'react-router-dom';
import ReportTable from './pages/reports/Reports';
import Settings from './pages/settings/settings';



function App() {
  if (useMatch('registration')) {
    return <StudentRegistration />
  }

  return (
    <>
    <NavBar></NavBar>
        <Routes>
          <Route path='/' element={<h1>Nasser</h1>} />
          <Route path='/Students' element={<StudentsPage />} />
          <Route path='/Sessions' element={<SessionsPage />} />
          <Route path='/Reports' element={<ReportTable />} />
          <Route path='/Settings' element={<Settings />} />
          <Route path='*' element={<h1>Page NOT found</h1>}/>
        </Routes>
    </>
  );  
}

export default App;
