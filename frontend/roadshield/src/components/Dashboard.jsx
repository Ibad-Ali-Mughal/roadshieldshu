// import React, { useEffect, useState } from 'react';
// import axios from 'axios';

// function Dashboard() {
//   const [heatmapData, setHeatmapData] = useState([]);
//   const [reports, setReports] = useState([]);

//   useEffect(() => {
//     axios.get('http://localhost:5000/api/heatmap')
//       .then((response) => setHeatmapData(response.data))
//       .catch((error) => console.error('Error fetching heatmap:', error));

//     axios.get('http://localhost:5000/api/reports')
//       .then((response) => setReports(response.data))
//       .catch((error) => console.error('Error fetching reports:', error));
//   }, []);

//   return (
//     <div className="max-w-2xl mx-auto mt-8 p-4">
//       <h2 className="text-2xl font-bold mb-4">Authorities Dashboard</h2>
//       <h3 className="text-xl font-semibold mb-2">Incident Heatmap</h3>
//       <ul className="list-disc pl-5">
//         {heatmapData.map((item, idx) => (
//           <li key={idx}>{item.location}: {item.count} incidents</li>
//         ))}
//       </ul>
//       <h3 className="text-xl font-semibold mt-4 mb-2">Recent Reports</h3>
//       <ul className="list-disc pl-5">
//         {reports.map((report) => (
//           <li key={report.id}>
//             {report.vehicle_type} at {report.location}: {report.description} ({report.timestamp})
//           </li>
//         ))}
//       </ul>
//     </div>
//   );
// }

// export default Dashboard;
import React, { useEffect, useState, useMemo } from 'react';
import axios from 'axios';

function Dashboard() {
  const [heatmapData, setHeatmapData] = useState([]);
  const [reports, setReports] = useState([]);
  const [stats, setStats] = useState({});
  const [loading, setLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState('');

  // Remove duplicates based on unique combination of location, description, and timestamp
  const uniqueReports = useMemo(() => {
    const seen = new Set();
    return reports.filter(report => {
      const key = `${report.location}-${report.description}-${report.timestamp}`;
      if (seen.has(key)) {
        return false;
      }
      seen.add(key);
      return true;
    });
  }, [reports]);

  const uniqueHeatmap = useMemo(() => {
    const seen = new Set();
    return heatmapData.filter(item => {
      const key = `${item.location}-${item.count}`;
      if (seen.has(key)) {
        return false;
      }
      seen.add(key);
      return true;
    });
  }, [heatmapData]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [heatmapRes, reportsRes, statsRes] = await Promise.all([
          axios.get('http://localhost:5000/api/heatmap'),
          axios.get('http://localhost:5000/api/reports'),
          axios.get('http://localhost:5000/api/stats')
        ]);
        
        setHeatmapData(heatmapRes.data || []);
        setReports(reportsRes.data || []);
        setStats(statsRes.data || {});
        setLastUpdate(new Date().toLocaleTimeString());
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
    // Refresh data every 30 seconds
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-lg text-gray-600">Loading Dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">🚓 Traffic Monitoring Dashboard</h1>
              <p className="text-gray-600 mt-1">Real-time traffic violation analytics</p>
            </div>
            <div className="text-right">
              <p className="text-sm text-gray-500">Last updated: {lastUpdate}</p>
              <p className="text-xs text-gray-400">Auto-refreshes every 30 seconds</p>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="max-w-7xl mx-auto px-4 py-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow border p-6">
            <div className="flex items-center">
              <div className="bg-blue-100 p-3 rounded-full">
                <span className="text-2xl">📊</span>
              </div>
              <div className="ml-4">
                <p className="text-sm text-gray-600">Total Incidents</p>
                <p className="text-2xl font-bold text-gray-900">{stats.total_reports || uniqueReports.length}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow border p-6">
            <div className="flex items-center">
              <div className="bg-green-100 p-3 rounded-full">
                <span className="text-2xl">📍</span>
              </div>
              <div className="ml-4">
                <p className="text-sm text-gray-600">Active Locations</p>
                <p className="text-2xl font-bold text-gray-900">{stats.unique_locations || uniqueHeatmap.length}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow border p-6">
            <div className="flex items-center">
              <div className="bg-purple-100 p-3 rounded-full">
                <span className="text-2xl">⚡</span>
              </div>
              <div className="ml-4">
                <p className="text-sm text-gray-600">System Status</p>
                <p className="text-2xl font-bold text-green-600">Active</p>
              </div>
            </div>
          </div>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Incident Heatmap Table */}
          <div className="bg-white rounded-lg shadow border">
            <div className="bg-blue-600 text-white px-6 py-4 rounded-t-lg">
              <h2 className="text-xl font-semibold flex items-center">
                🗺️ Incident Heatmap
                <span className="ml-2 bg-blue-500 text-xs px-2 py-1 rounded-full">
                  {uniqueHeatmap.length} locations
                </span>
              </h2>
            </div>
            <div className="p-6">
              {uniqueHeatmap.length === 0 ? (
                <div className="text-center py-8 text-gray-500">
                  <p>No heatmap data available</p>
                  <p className="text-sm mt-1">Incidents will appear here as they are detected</p>
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead>
                      <tr>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Location
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Incidents
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Severity
                        </th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                      {uniqueHeatmap.map((item, idx) => (
                        <tr key={idx} className="hover:bg-gray-50 transition-colors">
                          <td className="px-4 py-3 whitespace-nowrap">
                            <div className="flex items-center">
                              <span className="text-lg">📍</span>
                              <span className="ml-2 font-medium text-gray-900">{item.location}</span>
                            </div>
                          </td>
                          <td className="px-4 py-3 whitespace-nowrap">
                            <span className="bg-red-100 text-red-800 text-sm font-medium px-2 py-1 rounded-full">
                              {item.count} incidents
                            </span>
                          </td>
                          <td className="px-4 py-3 whitespace-nowrap">
                            <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                              item.count > 5 
                                ? 'bg-red-100 text-red-800' 
                                : item.count > 2 
                                ? 'bg-orange-100 text-orange-800'
                                : 'bg-green-100 text-green-800'
                            }`}>
                              {item.count > 5 ? 'High' : item.count > 2 ? 'Medium' : 'Low'}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>

          {/* Recent Reports Table */}
          <div className="bg-white rounded-lg shadow border">
            <div className="bg-green-600 text-white px-6 py-4 rounded-t-lg">
              <h2 className="text-xl font-semibold flex items-center">
                📋 Recent Reports
                <span className="ml-2 bg-green-500 text-xs px-2 py-1 rounded-full">
                  {uniqueReports.length} reports
                </span>
              </h2>
            </div>
            <div className="p-6">
              {uniqueReports.length === 0 ? (
                <div className="text-center py-8 text-gray-500">
                  <p>No reports available</p>
                  <p className="text-sm mt-1">Reports will appear here as violations are detected</p>
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead>
                      <tr>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Vehicle & Location
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Description
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Time
                        </th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                      {uniqueReports.slice(0, 10).map((report) => (
                        <tr key={report.id} className="hover:bg-gray-50 transition-colors">
                          <td className="px-4 py-3">
                            <div>
                              <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                                report.vehicle_type === 'car' ? 'bg-blue-100 text-blue-800' :
                                report.vehicle_type === 'truck' ? 'bg-orange-100 text-orange-800' :
                                report.vehicle_type === 'bus' ? 'bg-purple-100 text-purple-800' :
                                'bg-green-100 text-green-800'
                              }`}>
                                {report.vehicle_type}
                              </span>
                              <div className="mt-1 text-sm text-gray-600 flex items-center">
                                <span>📍</span>
                                <span className="ml-1">{report.location}</span>
                              </div>
                            </div>
                          </td>
                          <td className="px-4 py-3">
                            <div className="text-sm text-gray-900 max-w-xs truncate">
                              {report.description}
                            </div>
                          </td>
                          <td className="px-4 py-3 whitespace-nowrap">
                            <div className="text-xs text-gray-500">
                              {new Date(report.timestamp).toLocaleDateString()}
                            </div>
                            <div className="text-xs text-gray-400">
                              {new Date(report.timestamp).toLocaleTimeString()}
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Vehicle Type Distribution */}
        <div className="bg-white rounded-lg shadow border mt-8">
          <div className="bg-purple-600 text-white px-6 py-4 rounded-t-lg">
            <h2 className="text-xl font-semibold">🚗 Vehicle Type Distribution</h2>
          </div>
          <div className="p-6">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {['car', 'truck', 'bus', 'motorcycle'].map(vehicleType => {
                const count = uniqueReports.filter(r => r.vehicle_type === vehicleType).length;
                return (
                  <div key={vehicleType} className="text-center p-4 bg-gray-50 rounded-lg">
                    <div className="text-2xl mb-2">
                      {vehicleType === 'car' ? '🚗' : 
                       vehicleType === 'truck' ? '🚚' : 
                       vehicleType === 'bus' ? '🚌' : '🏍️'}
                    </div>
                    <div className="font-semibold text-gray-900 capitalize">{vehicleType}</div>
                    <div className="text-2xl font-bold text-purple-600">{count}</div>
                    <div className="text-xs text-gray-500">incidents</div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-lg shadow border mt-8">
          <div className="bg-gray-600 text-white px-6 py-4 rounded-t-lg">
            <h2 className="text-xl font-semibold">⚡ Quick Actions</h2>
          </div>
          <div className="p-6">
            <div className="flex flex-wrap gap-4">
              <button 
                onClick={() => window.location.reload()}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
              >
                🔄 Refresh Data
              </button>
              <button 
                onClick={() => window.open('http://localhost:5000/api/add-sample-data', '_blank')}
                className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors"
              >
                📊 Add Sample Data
              </button>
              <button className="bg-orange-600 text-white px-4 py-2 rounded-lg hover:bg-orange-700 transition-colors">
                📧 Export Report
              </button>
              <button className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors">
                🖨️ Print Summary
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;