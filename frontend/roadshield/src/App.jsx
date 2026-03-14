import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import Map from './components/Map';
import ReportForm from './components/ReportForm';
import Dashboard from './components/Dashboard';
import './App.css';

function App() {
  const [alerts, setAlerts] = useState([]);

  return (
    <Router>
      <div className="App">
        <Navbar />
        <Routes>
          <Route path="/" element={<Map alerts={alerts} setAlerts={setAlerts} />} />
          <Route path="/report" element={<ReportForm />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;