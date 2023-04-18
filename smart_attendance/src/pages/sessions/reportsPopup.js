import React, {useEffect, useState} from "react";
import './reportsPopup.css'


const ReportsPopup = ({ onClose, session })=>{
    const [reportData, setReportData] = useState([]);

    useEffect(() => {
        const fetchReportData = async () => {
          try {
            const response = await fetch(`http://192.168.20.42:5000/react/session_report/${session.session_id}`);
            const data = await response.json();
            setReportData(data);
          } catch (error) {
            console.error(`Error fetching report data: ${error.message}`);
          }
        };
    
        fetchReportData();
      }, [session]);

      return (  
        <>
        <div className="reports-popup-overlay" onClick={onClose}></div>
        <div className="reports-popup">
          
          <h2>Session Report</h2>
          <div>
            <h3>{session.session_name}</h3>
            <p>Date: {new Date(session.session_start_time).toLocaleDateString()}</p>
            <p>Start time: {new Date(session.session_start_time).toLocaleTimeString()}</p>
            <p>End time: {new Date(session.session_end_time).toLocaleTimeString()}</p>
            <p>Number of students attended: {reportData.length}</p>
          </div>
          <table>
            <thead>
              <tr>
                <th>Student Name</th>
                <th>Start Time</th>
                <th>End Time</th>
              </tr>
            </thead>
            <tbody>
              {reportData.map((student, index) => (
                <tr key={index}>
                  <td>{student.student_name}</td>
                  <td>{new Date(student.attendance_start_time).toLocaleTimeString()}</td>
                  <td>{new Date(student.attendance_end_time).toLocaleTimeString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        </>
      );

}

export default ReportsPopup;
