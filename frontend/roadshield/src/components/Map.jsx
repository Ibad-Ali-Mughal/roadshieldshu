// import React, { useEffect } from 'react';
// import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
// import L from 'leaflet';
// import io from 'socket.io-client';
// import 'leaflet/dist/leaflet.css';

// const socket = io('http://localhost:5000');

// function Map({ alerts, setAlerts }) {
//   const position = [24.8607, 67.0011]; // Karachi coordinates

//   useEffect(() => {
//     socket.on('alert', (data) => {
//       setAlerts((prev) => [...prev, data]);
//     });

//     return () => socket.off('alert');
//   }, [setAlerts]);

//   return (
//     <div>
//       <MapContainer center={position} zoom={13} className="map-container">
//         <TileLayer
//           url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
//           attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
//         />
//         {alerts.map((alert, idx) => (
//           <Marker key={idx} position={[alert.location.lat, alert.location.lng]}>
//             <Popup>
//               {alert.vehicle_type} detected at {alert.timestamp}
//             </Popup>
//           </Marker>
//         ))}
//       </MapContainer>
//       <div>
//         {alerts.map((alert, idx) => (
//           <div key={idx} className="alert">
//             Warning: Reckless {alert.vehicle_type} at {alert.location.lat}, {alert.location.lng}
//           </div>
//         ))}
//       </div>
//     </div>
//   );
// }

// export default Map;
import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import io from 'socket.io-client';
import 'leaflet/dist/leaflet.css';

// Fix for default markers
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Custom icons
const alertIcon = new L.Icon({
  iconUrl: 'https://cdn-icons-png.flaticon.com/512/1828/1828843.png',
  iconSize: [25, 25],
  iconAnchor: [12, 25],
  popupAnchor: [1, -25],
});

const cameraIcon = new L.Icon({
  iconUrl: 'https://cdn-icons-png.flaticon.com/512/535/535137.png',
  iconSize: [20, 20],
  iconAnchor: [10, 20],
  popupAnchor: [1, -20],
});

function Map({ alerts, setAlerts }) {
  const [cameras, setCameras] = useState([]);
  const [sidebarVisible, setSidebarVisible] = useState(true);
  const [windowSize, setWindowSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight
  });

  const position = [24.8607, 67.0011];

  useEffect(() => {
    const socket = io('http://localhost:5000');
    
    socket.on('alert', (data) => {
      console.log('📍 New alert:', data);
      setAlerts(prev => [...prev.slice(-19), data]);
    });

    fetch('http://localhost:5000/api/cameras')
      .then(res => res.json())
      .then(setCameras);

    // Handle window resize for responsive sidebar
    const handleResize = () => {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight
      });
      // Auto-hide sidebar on small screens
      setSidebarVisible(window.innerWidth > 768);
    };

    window.addEventListener('resize', handleResize);
    handleResize(); // Initial check

    return () => {
      socket.disconnect();
      window.removeEventListener('resize', handleResize);
    };
  }, [setAlerts]);

  // Determine if sidebar should be visible based on zoom level and screen size
  const shouldShowSidebar = sidebarVisible && windowSize.width > 768;

  return (
    <div className="map-container" style={{ 
      height: '100vh', 
      width: '100%', 
      position: 'relative',
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
    }}>
      <MapContainer 
        center={position} 
        zoom={12} 
        style={{ height: '100%', width: '100%' }}
        className="map-view"
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />
        
        {/* Camera Locations */}
        {cameras.map((camera, idx) => (
          <Marker 
            key={`cam-${idx}`} 
            position={[camera.lat, camera.lng]}
            icon={cameraIcon}
          >
            <Popup className="custom-popup">
              <div style={{ padding: '8px', textAlign: 'center', minWidth: '140px' }}>
                <div style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  justifyContent: 'center',
                  marginBottom: '8px'
                }}>
                  <span style={{ 
                    backgroundColor: '#10b981',
                    borderRadius: '50%',
                    width: '24px',
                    height: '24px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    marginRight: '8px'
                  }}>📹</span>
                  <strong style={{ fontSize: '14px', color: '#1f2937' }}>
                    {camera.name}
                  </strong>
                </div>
                <div style={{ 
                  fontSize: '12px', 
                  color: '#6b7280',
                  backgroundColor: '#f3f4f6',
                  padding: '4px 8px',
                  borderRadius: '4px'
                }}>
                  Monitoring: {camera.behavior}
                </div>
              </div>
            </Popup>
          </Marker>
        ))}
        
        {/* Live Alerts */}
        {alerts.map((alert, idx) => (
          <Marker 
            key={`alert-${idx}`} 
            position={[alert.location.lat, alert.location.lng]}
            icon={alertIcon}
          >
            <Popup className="custom-popup">
              <div style={{ padding: '12px', textAlign: 'center', minWidth: '180px' }}>
                <div style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  justifyContent: 'center',
                  marginBottom: '8px'
                }}>
                  <span style={{ 
                    backgroundColor: '#ef4444',
                    borderRadius: '50%',
                    width: '28px',
                    height: '28px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    marginRight: '8px',
                    color: 'white'
                  }}>🚨</span>
                  <strong style={{ fontSize: '15px', color: '#dc2626' }}>
                    {alert.vehicle_type} Alert
                  </strong>
                </div>
                
                <div style={{ textAlign: 'left', fontSize: '13px' }}>
                  <div style={{ marginBottom: '4px' }}>
                    <span style={{ color: '#6b7280' }}>📍</span>
                    <span style={{ marginLeft: '6px', color: '#374151' }}>
                      {alert.location_name}
                    </span>
                  </div>
                  <div style={{ marginBottom: '4px' }}>
                    <span style={{ color: '#6b7280' }}>⚡</span>
                    <span style={{ marginLeft: '6px', color: '#374151' }}>
                      {alert.behavior}
                    </span>
                  </div>
                  <div style={{ marginBottom: '4px' }}>
                    <span style={{ color: '#6b7280' }}>📹</span>
                    <span style={{ marginLeft: '6px', color: '#374151' }}>
                      {alert.camera_name}
                    </span>
                  </div>
                  <div style={{ 
                    marginTop: '8px',
                    padding: '4px 8px',
                    backgroundColor: '#fef2f2',
                    borderRadius: '4px',
                    fontSize: '11px',
                    color: '#dc2626'
                  }}>
                    ⏰ {alert.timestamp}
                  </div>
                </div>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>

      {/* Responsive Alerts Sidebar */}
      {shouldShowSidebar && (
        <div style={{
          position: 'absolute', 
          top: '20px', 
          right: '20px',
          background: 'rgba(255, 255, 255, 0.98)',
          backdropFilter: 'blur(10px)',
          padding: '20px',
          borderRadius: '16px',
          width: Math.min(320, windowSize.width * 0.3), // Responsive width
          maxHeight: 'calc(100vh - 40px)',
          overflowY: 'auto',
          boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
          border: '1px solid rgba(229, 231, 235, 0.8)',
          fontFamily: 'inherit',
          zIndex: 1000,
          transition: 'all 0.3s ease-in-out'
        }}>
          {/* Header with toggle button */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            marginBottom: '20px',
            paddingBottom: '16px',
            borderBottom: '2px solid #f3f4f6'
          }}>
            <div style={{ flex: 1 }}>
              <h3 style={{ 
                margin: 0, 
                fontSize: '18px',
                fontWeight: '700',
                color: '#111827',
                display: 'flex',
                alignItems: 'center',
                gap: '8px'
              }}>
                <span style={{
                  backgroundColor: '#dc2626',
                  borderRadius: '50%',
                  width: '24px',
                  height: '24px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'white',
                  fontSize: '12px'
                }}>🚨</span>
                Live Alerts
              </h3>
              <p style={{ 
                margin: '4px 0 0 0',
                fontSize: '12px',
                color: '#6b7280'
              }}>
                Real-time traffic monitoring
              </p>
            </div>
            <button
              onClick={() => setSidebarVisible(false)}
              style={{
                background: 'none',
                border: 'none',
                fontSize: '18px',
                color: '#6b7280',
                cursor: 'pointer',
                padding: '4px',
                borderRadius: '4px',
                marginLeft: '10px',
                ':hover': {
                  backgroundColor: '#f3f4f6'
                }
              }}
              title="Hide sidebar"
            >
              ✕
            </button>
          </div>

          {/* Alerts List */}
          <div style={{ maxHeight: '400px', overflowY: 'auto' }}>
            {alerts.length === 0 ? (
              <div style={{
                textAlign: 'center',
                padding: '40px 20px',
                color: '#9ca3af'
              }}>
                <div style={{ fontSize: '48px', marginBottom: '16px' }}>📡</div>
                <p style={{ margin: 0, fontSize: '14px', fontWeight: '500' }}>
                  No active alerts
                </p>
                <p style={{ margin: '4px 0 0 0', fontSize: '12px' }}>
                  Alerts will appear here in real-time
                </p>
              </div>
            ) : (
              alerts.slice(0, 8).map((alert, idx) => (
                <div key={idx} style={{
                  background: idx === 0 ? '#fef2f2' : 'white',
                  border: idx === 0 ? '2px solid #fecaca' : '1px solid #f3f4f6',
                  borderRadius: '12px',
                  padding: '16px',
                  marginBottom: '12px',
                  transition: 'all 0.2s ease-in-out',
                  cursor: 'pointer',
                  ':hover': {
                    transform: 'translateY(-1px)',
                    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.05)'
                  }
                }}>
                  <div style={{
                    display: 'flex',
                    alignItems: 'flex-start',
                    justifyContent: 'space-between',
                    marginBottom: '8px'
                  }}>
                    <div style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '8px'
                    }}>
                      <span style={{
                        backgroundColor: '#dc2626',
                        color: 'white',
                        borderRadius: '6px',
                        padding: '4px 8px',
                        fontSize: '11px',
                        fontWeight: '600'
                      }}>
                        {alert.vehicle_type}
                      </span>
                      <span style={{
                        backgroundColor: '#f59e0b',
                        color: 'white',
                        borderRadius: '6px',
                        padding: '4px 8px',
                        fontSize: '11px',
                        fontWeight: '600'
                      }}>
                        {alert.behavior}
                      </span>
                    </div>
                    {idx === 0 && (
                      <span style={{
                        backgroundColor: '#dc2626',
                        color: 'white',
                        borderRadius: '4px',
                        padding: '2px 6px',
                        fontSize: '10px',
                        fontWeight: '600'
                      }}>
                        NEW
                      </span>
                    )}
                  </div>
                  
                  <div style={{
                    fontSize: '14px',
                    fontWeight: '600',
                    color: '#1f2937',
                    marginBottom: '6px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '6px'
                  }}>
                    <span>📍</span>
                    {alert.location_name}
                  </div>
                  
                  <div style={{
                    fontSize: '12px',
                    color: '#6b7280',
                    marginBottom: '8px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '6px'
                  }}>
                    <span>📹</span>
                    {alert.camera_name}
                  </div>
                  
                  <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    fontSize: '11px',
                    color: '#9ca3af'
                  }}>
                    <span>⏰ {alert.timestamp}</span>
                    <span>{alert.location.lat.toFixed(4)}, {alert.location.lng.toFixed(4)}</span>
                  </div>
                </div>
              ))
            )}
          </div>

          {/* Footer */}
          <div style={{
            marginTop: '16px',
            paddingTop: '16px',
            borderTop: '1px solid #f3f4f6',
            fontSize: '11px',
            color: '#9ca3af',
            textAlign: 'center'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-around', marginBottom: '8px' }}>
              <span>📊 {cameras.length} Cameras</span>
              <span>⚡ Real-time</span>
              <span>🎯 AI Powered</span>
            </div>
            <p style={{ margin: 0 }}>SafeKarachi Traffic Monitoring</p>
          </div>
        </div>
      )}

      {/* Show Sidebar Button (when hidden) */}
      {!sidebarVisible && (
        <button
          onClick={() => setSidebarVisible(true)}
          style={{
            position: 'absolute',
            top: '20px',
            right: '20px',
            background: '#dc2626',
            color: 'white',
            border: 'none',
            borderRadius: '50%',
            width: '50px',
            height: '50px',
            fontSize: '20px',
            cursor: 'pointer',
            boxShadow: '0 4px 12px rgba(220, 38, 38, 0.3)',
            zIndex: 1000,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            transition: 'all 0.3s ease-in-out',
            ':hover': {
              transform: 'scale(1.1)',
              boxShadow: '0 6px 20px rgba(220, 38, 38, 0.4)'
            }
          }}
          title="Show alerts sidebar"
        >
          🚨
          {alerts.length > 0 && (
            <span style={{
              position: 'absolute',
              top: '-5px',
              right: '-5px',
              background: 'white',
              color: '#dc2626',
              borderRadius: '50%',
              width: '20px',
              height: '20px',
              fontSize: '12px',
              fontWeight: 'bold',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              border: '2px solid #dc2626'
            }}>
              {alerts.length}
            </span>
          )}
        </button>
      )}

      {/* Map Controls Overlay */}
      <div style={{
        position: 'absolute',
        bottom: '20px',
        left: '20px',
        background: 'rgba(255, 255, 255, 0.95)',
        backdropFilter: 'blur(8px)',
        padding: '12px',
        borderRadius: '12px',
        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
        border: '1px solid rgba(229, 231, 235, 0.8)',
        zIndex: 1000
      }}>
        <div style={{ fontSize: '14px', fontWeight: '600', color: '#1f2937', marginBottom: '8px' }}>
          Karachi Traffic Map
        </div>
        <div style={{ display: 'flex', gap: '8px', fontSize: '11px', color: '#6b7280' }}>
          <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
            <div style={{ width: '8px', height: '8px', backgroundColor: '#10b981', borderRadius: '50%' }}></div>
            Cameras
          </span>
          <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
            <div style={{ width: '8px', height: '8px', backgroundColor: '#dc2626', borderRadius: '50%' }}></div>
            Alerts
          </span>
        </div>
      </div>
    </div>
  );
}

export default Map;