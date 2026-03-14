import React, { useState } from 'react';
import axios from 'axios';

function ReportForm() {
  const [location, setLocation] = useState('');
  const [description, setDescription] = useState('');
  const [vehicleType, setVehicleType] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:5000/api/reports', {
        location,
        description,
        vehicle_type: vehicleType,
      });
      alert('Report submitted successfully!');
      setLocation('');
      setDescription('');
      setVehicleType('');
    } catch (error) {
      alert('Error submitting report');
    }
  };

  return (
    <div className="max-w-md mx-auto mt-8 p-4">
      <h2 className="text-2xl font-bold mb-4">Report an Incident</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium">Location</label>
          <input
            type="text"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            placeholder="e.g., Clifton Road, Karachi"
            className="mt-1 p-2 border rounded w-full"
          />
        </div>
        <div>
          <label className="block text-sm font-medium">Description</label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Describe the incident"
            className="mt-1 p-2 border rounded w-full"
          />
        </div>
        <div>
          <label className="block text-sm font-medium">Vehicle Type</label>
          <input
            type="text"
            value={vehicleType}
            onChange={(e) => setVehicleType(e.target.value)}
            placeholder="e.g., Truck, Bus"
            className="mt-1 p-2 border rounded w-full"
          />
        </div>
        <button type="submit" className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600">
          Submit Report
        </button>
      </form>
    </div>
  );
}

export default ReportForm;