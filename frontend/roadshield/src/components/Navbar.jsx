import React from 'react';
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav className="bg-gray-800 text-white p-4">
      <div className="container mx-auto flex justify-between">
        <Link to="/" className="text-xl font-bold">RoadShield</Link>
        <div className="space-x-4">
          <Link to="/" className="hover:underline">Map</Link>
          <Link to="/report" className="hover:underline">Report Incident</Link>
          <Link to="/dashboard" className="hover:underline">Dashboard</Link>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;