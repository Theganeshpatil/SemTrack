import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import {
  AppBar,
  Toolbar,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@mui/material";

const Dashboard = () => {
  const [attendance, setAttendance] = useState(null);

  useEffect(() => {
    const fetchAttendance = async () => {
      const jwtToken = localStorage.getItem("jwt_token");
      const response = await fetch(
        `http://127.0.0.1:8000/get_attendance?jwt_token=${jwtToken}`,
        {
          headers: {
            accept: "application/json",
          },
        }
      );
      const data = await response.json();
      setAttendance(data.attendance);
    };

    fetchAttendance();
  }, []);

  return (
    <div>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6">SemTrack</Typography>
        </Toolbar>
      </AppBar>

      <h1>Dashboard Page</h1>

      {/* Attendance Report */}
      {attendance && (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Course</TableCell>
                <TableCell align="right">Total Sessions</TableCell>
                <TableCell align="right">Attended Sessions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {Object.entries(attendance.total_session).map(([key, value]) => (
                <TableRow key={key}>
                  <TableCell component="th" scope="row">
                    {key}
                  </TableCell>
                  <TableCell align="right">{value}</TableCell>
                  <TableCell align="right">
                    {attendance.attended_session[key]}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </div>
  );
};

export default Dashboard;
