import './NavBar.css';
import React from 'react';
import {Link, useMatch } from "react-router-dom";

const NavBar = () => {
  const homeMatch = useMatch('/');
  const studentsMatch = useMatch('/Students');
  const sessionsMatch = useMatch('/Sessions');
  const reportsMatch = useMatch('/Reports');
  const settingsMatch = useMatch('/Settings');

  return (
    <div className="app-container">
      <div className="nav-container">
        <div className="nav-title">
          <h1>SAS</h1>
        </div>
        <div className="nav-subtitle">
          <h2>Smart Attendance System</h2>
        </div>
        <div>
            <nav className="nav-links">
                <Link className={homeMatch? "active":''} exact={"true"} to="/">Home</Link>
                <Link className={studentsMatch? "active":''} to="/Students">Student Management</Link>
                <Link className={sessionsMatch? "active":''} to="/Sessions">Session Management</Link>
                <Link className={reportsMatch? "active":''} to="/Reports">Reports</Link>
                <Link className={settingsMatch? "active":''} to="/Settings">Settings</Link>
            </nav>
        </div>
      </div>
    </div>
  );
};

export default NavBar;

