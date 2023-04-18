import React, { useState, useEffect } from "react";
import axios from "axios";
import "./ReportTable.css";

const ReportTable = () => {
  const [reports, setReports] = useState([]);

  useEffect(() => {
    const fetchReports = async () => {
      try {
        const response = await axios.get("http://localhost:5000/react/reports");
        setReports(response.data);
      } catch (error) {
        console.error("Error fetching reports data:", error);
      }
    };

    fetchReports();
  }, []);

  return (
    <div className="report-table">
      <table style={{ width: "100%" }}>
        <thead>
          <tr>
          <th>Attendance ID</th>
            <th>Student Name</th>
            <th>Student Registration No.</th>
            <th>Session Name</th>
            <th>Start Time</th>
            <th>End Time</th>
          </tr>
        </thead>
        <tbody>
          {reports.map((report) => (
            <tr key={report.attendance_id}>
              <td>{report.attendance_id}</td>
              <td>{report.student_name}</td>
              <td>{report.student_reg_no}</td>
              <td>{report.session_name}</td>
              <td>{report.attendance_start_time}</td>
              <td>{report.attendance_end_time}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ReportTable;