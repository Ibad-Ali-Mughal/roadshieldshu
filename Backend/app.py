
# from flask import Flask, jsonify, request
# from flask_socketio import SocketIO, emit
# from detection import detect_reckless_driving
# from database import init_db, add_report, get_reports, get_heatmap_data
# import cv2
# import threading
# import time

# app = Flask(__name__)

# # Configure CORS for SocketIO
# socketio = SocketIO(app, cors_allowed_origins="*")

# # Initialize database
# init_db()

# # Add CORS headers manually for HTTP requests
# @app.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#     response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
#     return response

# # Handle preflight requests
# @app.route('/api/reports', methods=['OPTIONS'])
# @app.route('/api/heatmap', methods=['OPTIONS'])
# def options_response():
#     response = jsonify({'status': 'ok'})
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
#     return response

# # Video processing function
# def process_video():
#     print("Starting video processing thread...")
#     cap = cv2.VideoCapture("data/overspeeding.mp4")
#     if not cap.isOpened():
#         print("Warning: overspeeding.mp4 not found. Falling back to webcam (0).")
#         cap = cv2.VideoCapture(0)
#         if not cap.isOpened():
#             print("Error: No video file or webcam available. Skipping video processing.")
#             return

#     try:
#         while cap.isOpened():
#             ret, frame = cap.read()
#             if not ret:
#                 print("End of input, restarting...")
#                 cap.set(cv2.CAP_PROP_POS_FRAMES, 0) if "overspeeding.mp4" in cap.getBackendName() else cap.release()
#                 cap = cv2.VideoCapture(0)
#                 continue
            
#             reckless_detected, vehicle_type, location = detect_reckless_driving(frame)
#             if reckless_detected:
#                 print(f"Alert: {vehicle_type} detected at {location}")
#                 socketio.emit('alert', {
#                     'vehicle_type': vehicle_type,
#                     'location': location,
#                     'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
#                 })
#             time.sleep(0.1)
#     except Exception as e:
#         print(f"Error in process_video: {e}")
#     finally:
#         cap.release()

# # API Endpoints
# @app.route('/api/reports', methods=['GET'])
# def get_all_reports():
#     reports = get_reports()
#     return jsonify(reports)

# @app.route('/api/reports', methods=['POST'])
# def submit_report():
#     data = request.json
#     add_report(data['location'], data['description'], data['vehicle_type'])
#     return jsonify({'message': 'Report submitted'}), 201

# @app.route('/api/heatmap', methods=['GET'])
# def get_heatmap():
#     data = get_heatmap_data()
#     return jsonify(data)

# # Test endpoint to verify CORS is working
# @app.route('/api/test', methods=['GET'])
# def test_endpoint():
#     return jsonify({'message': 'Server is working!', 'status': 'success'})

# # Add sample data endpoint
# @app.route('/api/add-sample-data', methods=['GET'])
# def add_sample_data():
#     """Add sample data for testing"""
#     sample_reports = [
#         {'location': 'University Road', 'description': 'Overspeeding car', 'vehicle_type': 'car'},
#         {'location': 'II Chundrigar Road', 'description': 'Illegal overtaking', 'vehicle_type': 'bus'},
#         {'location': 'Shahrah-e-Faisal', 'description': 'Signal jumping', 'vehicle_type': 'motorcycle'},
#         {'location': 'Gulshan-e-Iqbal', 'description': 'Wrong parking', 'vehicle_type': 'car'},
#         {'location': 'North Nazimabad', 'description': 'Rash driving', 'vehicle_type': 'motorcycle'},
#     ]
    
#     for report in sample_reports:
#         add_report(report['location'], report['description'], report['vehicle_type'])
    
#     return jsonify({'message': f'Added {len(sample_reports)} sample reports successfully!'})

# @app.route('/api/stats', methods=['GET'])
# def get_stats():
#     """Get database statistics"""
#     reports = get_reports()
#     heatmap = get_heatmap_data()
    
#     return jsonify({
#         'total_reports': len(reports),
#         'unique_locations': len(heatmap),
#         'heatmap_data': heatmap,
#         'recent_reports': reports[:3] if reports else []
#     })

# # Start video processing in background
# threading.Thread(target=process_video, daemon=True).start()

# if __name__ == '__main__':
#     print("🚀 Starting Flask server on http://localhost:5000")
#     print("📊 Test endpoints:")
#     print("   http://localhost:5000/api/test")
#     print("   http://localhost:5000/api/stats") 
#     print("   http://localhost:5000/api/heatmap")
#     print("   http://localhost:5000/api/reports")
#     print("   http://localhost:5000/api/add-sample-data")
#     socketio.run(app, debug=True, port=5000)
# from flask import Flask, jsonify, request
# from flask_socketio import SocketIO, emit
# from detection import detect_reckless_driving, CAMERA_LOCATIONS
# from database import init_db, add_report, get_reports, get_heatmap_data
# import cv2
# import threading
# import time

# app = Flask(__name__)
# socketio = SocketIO(app, cors_allowed_origins="*")

# # Initialize database
# init_db()

# # Add CORS headers manually for HTTP requests
# @app.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#     response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
#     return response

# # Video processing function for MULTIPLE cameras
# def process_video():
#     print("🚀 Starting Multi-Camera AI Monitoring System")
#     print("📹 Processing 4 different camera feeds...")
    
#     # Define all your video files with their locations
#     video_configs = [
#         {
#             "path": "data/camera1_overspeeding.mp4",
#             "camera_id": "camera1_overspeeding",
#             "name": "Shahrah-e-Faisal Camera"
#         },
#         {
#             "path": "data/camera2_lane_violation.mp4", 
#             "camera_id": "camera2_lane_violation",
#             "name": "University Road Camera"
#         },
#         {
#             "path": "data/camera3_truckspeed.mp4",
#             "camera_id": "camera3_truckspeed", 
#             "name": "II Chundrigar Road Camera"
#         },
#         {
#             "path": "data/camera4_reckless_car.mp4",
#             "camera_id": "camera4_reckless_car",
#             "name": "Gulshan-e-Iqbal Camera"
#         }
#     ]
    
#     # Start a thread for each camera
#     for config in video_configs:
#         thread = threading.Thread(target=process_single_camera, args=(config,), daemon=True)
#         thread.start()
#         print(f"📹 Started camera: {config['name']}")

# def process_single_camera(config):
#     """Process a single camera feed"""
#     cap = cv2.VideoCapture(config["path"])
    
#     if not cap.isOpened():
#         print(f"❌ Cannot open video: {config['path']}")
#         return

#     print(f"✅ Processing: {config['name']} -> {config['path']}")
    
#     try:
#         while cap.isOpened():
#             ret, frame = cap.read()
#             if not ret:
#                 # Restart video when it ends
#                 cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
#                 continue
            
#             # Process frame with this camera's specific location
#             reckless_detected, vehicle_type, location_data = detect_reckless_driving(
#                 frame, config["camera_id"]
#             )
            
#             if reckless_detected:
#                 print(f"🚨 {location_data['name']}: {vehicle_type} detected - {location_data['behavior']}")
                
#                 socketio.emit('alert', {
#                     'vehicle_type': vehicle_type,
#                     'location': location_data['coords'],  # Coordinates for map
#                     'location_name': location_data['name'],  # Location name for display
#                     'behavior': location_data['behavior'],
#                     'camera_name': config['name'],
#                     'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
#                 })
                
#                 # Add to database
#                 add_report(
#                     location_data['name'],
#                     f"{vehicle_type} - {location_data['behavior']}",
#                     vehicle_type
#                 )
            
#             # Process at reasonable rate
#             time.sleep(0.2)
            
#     except Exception as e:
#         print(f"❌ Error processing {config['name']}: {e}")
#     finally:
#         cap.release()

# # API Endpoints (keep your existing ones)
# @app.route('/api/reports', methods=['GET'])
# def get_all_reports():
#     reports = get_reports()
#     return jsonify(reports)

# @app.route('/api/reports', methods=['POST'])
# def submit_report():
#     data = request.json
#     add_report(data['location'], data['description'], data['vehicle_type'])
#     return jsonify({'message': 'Report submitted'}), 201

# @app.route('/api/heatmap', methods=['GET'])
# def get_heatmap():
#     data = get_heatmap_data()
#     return jsonify(data)

# @app.route('/api/test', methods=['GET'])
# def test_endpoint():
#     return jsonify({'message': 'Server is working!', 'status': 'success'})

# @app.route('/api/cameras', methods=['GET'])
# def get_cameras():
#     """Get camera information for the frontend"""
#     cameras = []
#     for cam_id, location in CAMERA_LOCATIONS.items():
#         cameras.append({
#             'id': cam_id,
#             'name': location['name'],
#             'lat': location['coords']['lat'],
#             'lng': location['coords']['lng'],
#             'behavior': location['behavior']
#         })
#     return jsonify(cameras)

# @app.route('/api/add-sample-data', methods=['GET'])
# def add_sample_data():
#     sample_reports = [
#         {'location': 'University Road', 'description': 'Overspeeding car', 'vehicle_type': 'car'},
#         {'location': 'II Chundrigar Road', 'description': 'Illegal overtaking', 'vehicle_type': 'bus'},
#         {'location': 'Shahrah-e-Faisal', 'description': 'Signal jumping', 'vehicle_type': 'motorcycle'},
#     ]
    
#     for report in sample_reports:
#         add_report(report['location'], report['description'], report['vehicle_type'])
    
#     return jsonify({'message': f'Added {len(sample_reports)} sample reports!'})

# @app.route('/api/stats', methods=['GET'])
# def get_stats():
#     reports = get_reports()
#     heatmap = get_heatmap_data()
    
#     return jsonify({
#         'system': 'Multi-Camera Traffic Monitoring',
#         'status': 'Active',
#         'total_reports': len(reports),
#         'active_cameras': 4,
#         'unique_locations': len(heatmap),
#         'last_updated': time.strftime("%Y-%m-%d %H:%M:%S")
#     })

# # Start multi-camera processing
# print("🚀 Starting Multi-Camera AI Monitoring System")
# print("📍 Monitoring 4 Karachi Locations:")
# print("   📹 Shahrah-e-Faisal - Overspeeding")
# print("   📹 University Road - Lane Violations") 
# print("   📹 II Chundrigar Road - Truck Monitoring")
# print("   📹 Gulshan-e-Iqbal - Reckless Driving")
# print("=" * 60)

# # Start video processing in background
# threading.Thread(target=process_video, daemon=True).start()

# if __name__ == '__main__':
#     socketio.run(app, debug=True, port=5000, use_reloader=False)


# third check

# from flask import Flask, jsonify, request
# from flask_socketio import SocketIO, emit
# from detection import detect_reckless_driving, CAMERA_LOCATIONS
# from database import init_db, add_report, get_reports, get_heatmap_data
# import cv2
# import threading
# import time
# import random

# app = Flask(__name__)
# socketio = SocketIO(app, cors_allowed_origins="*")

# # Initialize database
# init_db()

# # Add CORS headers manually for HTTP requests
# @app.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#     response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
#     return response

# # Video processing function for MULTIPLE cameras
# def process_video():
#     print("🚀 Starting Multi-Camera AI Monitoring System")
#     print("📹 Processing 4 different camera feeds...")
    
#     # Define all your video files with their locations
#     video_configs = [
#         {
#             "path": "data/camera1_overspeeding.mp4",
#             "camera_id": "camera1_overspeeding",
#             "name": "Shahrah-e-Faisal Camera"
#         },
#         {
#             "path": "data/camera2_lane_violation.mp4", 
#             "camera_id": "camera2_lane_violation",
#             "name": "University Road Camera"
#         },
#         {
#             "path": "data/camera3_truckspeed.mp4",
#             "camera_id": "camera3_truckspeed", 
#             "name": "II Chundrigar Road Camera"
#         },
#         {
#             "path": "data/camera4_reckless_car.mp4",
#             "camera_id": "camera4_reckless_car",
#             "name": "Gulshan-e-Iqbal Camera"
#         }
#     ]
    
#     # Start a thread for each camera
#     for config in video_configs:
#         thread = threading.Thread(target=process_single_camera, args=(config,), daemon=True)
#         thread.start()
#         print(f"📹 Started camera: {config['name']}")

# def process_single_camera(config):
#     """Process a single camera feed with better timing"""
#     cap = cv2.VideoCapture(config["path"])
    
#     if not cap.isOpened():
#         print(f"❌ Cannot open video: {config['path']}")
#         # Fallback to demo mode for this camera
#         run_camera_demo_mode(config)
#         return

#     print(f"✅ Processing: {config['name']} -> {config['path']}")
    
#     try:
#         frame_count = 0
#         while cap.isOpened():
#             ret, frame = cap.read()
#             if not ret:
#                 # Restart video when it ends
#                 cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
#                 frame_count = 0
#                 continue
            
#             # FIXED: Only process every 10th frame to reduce load
#             frame_count += 1
#             if frame_count % 10 != 0:
#                 time.sleep(0.1)  # Skip this frame
#                 continue
            
#             # Process frame with this camera's specific location
#             reckless_detected, vehicle_type, location_data = detect_reckless_driving(
#                 frame, config["camera_id"]
#             )
            
#             if reckless_detected:
#                 print(f"🚨 {location_data['name']}: {vehicle_type} detected - {location_data['behavior']}")
                
#                 alert_data = {
#                     'vehicle_type': vehicle_type,
#                     'location': location_data['coords'],
#                     'location_name': location_data['name'],
#                     'behavior': location_data['behavior'],
#                     'camera_name': config['name'],
#                     'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
#                 }
                
#                 socketio.emit('alert', alert_data)
                
#                 # Add to database
#                 add_report(
#                     location_data['name'],
#                     f"{vehicle_type} - {location_data['behavior']}",
#                     vehicle_type
#                 )
            
#             # FIXED: Process slower to see individual alerts
#             time.sleep(1)  # Process 1 frame per second
            
#     except Exception as e:
#         print(f"❌ Error processing {config['name']}: {e}")
#         run_camera_demo_mode(config)
#     finally:
#         if cap:
#             cap.release()

# def run_camera_demo_mode(config):
#     """Run demo mode for a camera that can't open video"""
#     print(f"🎮 Starting demo mode for {config['name']}")
    
#     location_data = CAMERA_LOCATIONS[config["camera_id"]]
#     alert_count = 0
    
#     try:
#         while True:
#             alert_count += 1
#             vehicle_type = random.choice(['car', 'truck', 'bus', 'motorcycle'])
            
#             # FIXED: Send alerts less frequently (every 10-20 seconds)
#             if alert_count % 3 == 0:  # Only send every 3rd cycle
#                 print(f"🚨 DEMO {config['name']} Alert #{alert_count}: {vehicle_type}")
                
#                 alert_data = {
#                     'vehicle_type': vehicle_type,
#                     'location': location_data['coords'],
#                     'location_name': location_data['name'],
#                     'behavior': location_data['behavior'],
#                     'camera_name': config['name'],
#                     'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
#                     'demo': True
#                 }
                
#                 socketio.emit('alert', alert_data)
                
#                 # Add to database occasionally
#                 if alert_count % 6 == 0:
#                     add_report(
#                         location_data['name'],
#                         f"{vehicle_type} - {location_data['behavior']}",
#                         vehicle_type
#                     )
            
#             # FIXED: Longer delay between cycles
#             time.sleep(10)  # Wait 10 seconds between checks
            
#     except Exception as e:
#         print(f"Demo mode error for {config['name']}: {e}")

# # API Endpoints (keep your existing ones)
# @app.route('/api/reports', methods=['GET'])
# def get_all_reports():
#     reports = get_reports()
#     return jsonify(reports)

# @app.route('/api/reports', methods=['POST'])
# def submit_report():
#     data = request.json
#     add_report(data['location'], data['description'], data['vehicle_type'])
#     return jsonify({'message': 'Report submitted'}), 201

# @app.route('/api/heatmap', methods=['GET'])
# def get_heatmap():
#     data = get_heatmap_data()
#     return jsonify(data)

# @app.route('/api/test', methods=['GET'])
# def test_endpoint():
#     return jsonify({'message': 'Server is working!', 'status': 'success'})

# @app.route('/api/cameras', methods=['GET'])
# def get_cameras():
#     """Get camera information for the frontend"""
#     cameras = []
#     for cam_id, location in CAMERA_LOCATIONS.items():
#         cameras.append({
#             'id': cam_id,
#             'name': location['name'],
#             'lat': location['coords']['lat'],
#             'lng': location['coords']['lng'],
#             'behavior': location['behavior']
#         })
#     return jsonify(cameras)

# @app.route('/api/add-sample-data', methods=['GET'])
# def add_sample_data():
#     sample_reports = [
#         {'location': 'University Road', 'description': 'Overspeeding car', 'vehicle_type': 'car'},
#         {'location': 'II Chundrigar Road', 'description': 'Illegal overtaking', 'vehicle_type': 'bus'},
#         {'location': 'Shahrah-e-Faisal', 'description': 'Signal jumping', 'vehicle_type': 'motorcycle'},
#     ]
    
#     for report in sample_reports:
#         add_report(report['location'], report['description'], report['vehicle_type'])
    
#     return jsonify({'message': f'Added {len(sample_reports)} sample reports!'})

# @app.route('/api/stats', methods=['GET'])
# def get_stats():
#     reports = get_reports()
#     heatmap = get_heatmap_data()
    
#     return jsonify({
#         'system': 'Multi-Camera Traffic Monitoring',
#         'status': 'Active',
#         'total_reports': len(reports),
#         'active_cameras': 4,
#         'unique_locations': len(heatmap),
#         'last_updated': time.strftime("%Y-%m-%d %H:%M:%S")
#     })

# # Start multi-camera processing
# print("🚀 Starting Multi-Camera AI Monitoring System")
# print("📍 Monitoring 4 Karachi Locations:")
# print("   📹 Shahrah-e-Faisal - Overspeeding")
# print("   📹 University Road - Lane Violations") 
# print("   📹 II Chundrigar Road - Truck Monitoring")
# print("   📹 Gulshan-e-Iqbal - Reckless Driving")
# print("=" * 60)

# # Start video processing in background
# threading.Thread(target=process_video, daemon=True).start()

# if __name__ == '__main__':
#     socketio.run(app, debug=True, port=5000, use_reloader=False)

# truck logic

from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from detection import detect_reckless_driving, CAMERA_LOCATIONS
from database import init_db, add_report, get_reports, get_heatmap_data
import cv2
import threading
import time
import random

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize database
init_db()

# Add CORS headers manually for HTTP requests
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Video processing function for MULTIPLE cameras
def process_video():
    print("🚀 Starting Multi-Camera AI Monitoring System")
    print("📹 Processing 4 different camera feeds...")
    
    # Define all your video files with their locations
    video_configs = [
        {
            "path": "data/camera1_overspeeding.mp4",
            "camera_id": "camera1_overspeeding",
            "name": "Shahrah-e-Faisal Camera"
        },
        {
            "path": "data/camera2_lane_violation.mp4", 
            "camera_id": "camera2_lane_violation",
            "name": "University Road Camera"
        },
        {
            "path": "data/camera3_truckspeed.mp4",
            "camera_id": "camera3_truckspeed", 
            "name": "II Chundrigar Road Camera"
        },
        {
            "path": "data/camera4_reckless_car.mp4",
            "camera_id": "camera4_reckless_car",
            "name": "Gulshan-e-Iqbal Camera"
        }
    ]
    
    # Start a thread for each camera
    for config in video_configs:
        thread = threading.Thread(target=process_single_camera, args=(config,), daemon=True)
        thread.start()
        print(f"📹 Started camera: {config['name']}")

def process_single_camera(config):
    """Process a single camera feed with better timing"""
    cap = cv2.VideoCapture(config["path"])
    
    if not cap.isOpened():
        print(f"❌ Cannot open video: {config['path']}")
        # Fallback to demo mode for this camera
        run_camera_demo_mode(config)
        return

    print(f"✅ Processing: {config['name']} -> {config['path']}")
    
    try:
        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                # Restart video when it ends
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                frame_count = 0
                continue
            
            # FIXED: Only process every 10th frame to reduce load
            frame_count += 1
            if frame_count % 10 != 0:
                time.sleep(0.1)  # Skip this frame
                continue
            
            # UPDATED: Process frame with new return parameters
            reckless_detected, vehicle_type, location_data, is_heavy_vehicle, is_speeding = detect_reckless_driving(
                frame, config["camera_id"]
            )
            
            if reckless_detected:
                # ENHANCED: Add priority information based on vehicle type
                priority = "HIGH" if is_heavy_vehicle else "MEDIUM"
                behavior_type = location_data['behavior']
                
                if is_heavy_vehicle:
                    behavior_type = f"CRITICAL: {vehicle_type} {location_data['behavior']}"
                    print(f"🚨🚛 CRITICAL ALERT: {vehicle_type} at {location_data['name']} - PRIORITY: {priority}")
                else:
                    print(f"🚨 ALERT: {vehicle_type} at {location_data['name']} - {location_data['behavior']}")
                
                alert_data = {
                    'vehicle_type': vehicle_type,
                    'location': location_data['coords'],
                    'location_name': location_data['name'],
                    'behavior': behavior_type,
                    'camera_name': config['name'],
                    'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                    'priority': priority,
                    'is_heavy_vehicle': is_heavy_vehicle,
                    'is_speeding': is_speeding
                }
                
                socketio.emit('alert', alert_data)
                
                # Add to database with enhanced information
                add_report(
                    location_data['name'],
                    f"{vehicle_type} - {behavior_type}",
                    vehicle_type,
                    priority
                )
            
            # FIXED: Process slower to see individual alerts
            time.sleep(1)  # Process 1 frame per second
            
    except Exception as e:
        print(f"❌ Error processing {config['name']}: {e}")
        run_camera_demo_mode(config)
    finally:
        if cap:
            cap.release()

def run_camera_demo_mode(config):
    """Run demo mode for a camera that can't open video"""
    print(f"🎮 Starting demo mode for {config['name']}")
    
    location_data = CAMERA_LOCATIONS[config["camera_id"]]
    alert_count = 0
    
    try:
        while True:
            alert_count += 1
            
            # UPDATED: Simulate both heavy and normal vehicles
            if alert_count % 3 == 0:  # Every 3rd alert is heavy vehicle
                vehicle_type = random.choice(['truck', 'bus'])
                is_heavy_vehicle = True
                priority = "HIGH"
            else:
                vehicle_type = random.choice(['car', 'motorcycle'])
                is_heavy_vehicle = False
                priority = "MEDIUM"
            
            # FIXED: Send alerts less frequently (every 10-20 seconds)
            if alert_count % 3 == 0:  # Only send every 3rd cycle
                behavior_type = location_data['behavior']
                if is_heavy_vehicle:
                    behavior_type = f"CRITICAL: {vehicle_type} {location_data['behavior']}"
                
                print(f"🚨 DEMO {config['name']} Alert #{alert_count}: {vehicle_type} - Priority: {priority}")
                
                alert_data = {
                    'vehicle_type': vehicle_type,
                    'location': location_data['coords'],
                    'location_name': location_data['name'],
                    'behavior': behavior_type,
                    'camera_name': config['name'],
                    'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                    'priority': priority,
                    'is_heavy_vehicle': is_heavy_vehicle,
                    'is_speeding': random.choice([True, False]),
                    'demo': True
                }
                
                socketio.emit('alert', alert_data)
                
                # Add to database occasionally
                if alert_count % 6 == 0:
                    add_report(
                        location_data['name'],
                        f"{vehicle_type} - {behavior_type}",
                        vehicle_type,
                        priority
                    )
            
            # FIXED: Longer delay between cycles
            time.sleep(10)  # Wait 10 seconds between checks
            
    except Exception as e:
        print(f"Demo mode error for {config['name']}: {e}")

# API Endpoints (updated to handle new parameters)
@app.route('/api/reports', methods=['GET'])
def get_all_reports():
    reports = get_reports()
    return jsonify(reports)

@app.route('/api/reports', methods=['POST'])
def submit_report():
    data = request.json
    priority = data.get('priority', 'MEDIUM')
    add_report(data['location'], data['description'], data['vehicle_type'], priority)
    return jsonify({'message': 'Report submitted'}), 201

@app.route('/api/heatmap', methods=['GET'])
def get_heatmap():
    data = get_heatmap_data()
    return jsonify(data)

@app.route('/api/test', methods=['GET'])
def test_endpoint():
    return jsonify({'message': 'Server is working!', 'status': 'success'})

@app.route('/api/cameras', methods=['GET'])
def get_cameras():
    """Get camera information for the frontend"""
    cameras = []
    for cam_id, location in CAMERA_LOCATIONS.items():
        cameras.append({
            'id': cam_id,
            'name': location['name'],
            'lat': location['coords']['lat'],
            'lng': location['coords']['lng'],
            'behavior': location['behavior'],
            'priority': location['priority']
        })
    return jsonify(cameras)

@app.route('/api/add-sample-data', methods=['GET'])
def add_sample_data():
    sample_reports = [
        {'location': 'University Road', 'description': 'Overspeeding truck - CRITICAL', 'vehicle_type': 'truck', 'priority': 'HIGH'},
        {'location': 'II Chundrigar Road', 'description': 'Illegal overtaking bus', 'vehicle_type': 'bus', 'priority': 'HIGH'},
        {'location': 'Shahrah-e-Faisal', 'description': 'Signal jumping car', 'vehicle_type': 'car', 'priority': 'MEDIUM'},
        {'location': 'Gulshan-e-Iqbal', 'description': 'Reckless driving motorcycle', 'vehicle_type': 'motorcycle', 'priority': 'MEDIUM'},
    ]
    
    for report in sample_reports:
        add_report(report['location'], report['description'], report['vehicle_type'], report['priority'])
    
    return jsonify({'message': f'Added {len(sample_reports)} sample reports!'})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    reports = get_reports()
    heatmap = get_heatmap_data()
    
    # Count heavy vehicle alerts
    heavy_alerts = len([r for r in reports if r.get('priority') == 'HIGH'])
    
    return jsonify({
        'system': 'Multi-Camera Traffic Monitoring',
        'status': 'Active',
        'total_reports': len(reports),
        'heavy_vehicle_alerts': heavy_alerts,
        'active_cameras': 4,
        'unique_locations': len(heatmap),
        'last_updated': time.strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route('/api/priority-alerts', methods=['GET'])
def get_priority_alerts():
    """Get only high priority alerts"""
    reports = get_reports()
    high_priority = [r for r in reports if r.get('priority') == 'HIGH']
    return jsonify(high_priority)

# Start multi-camera processing
print("🚀 Starting Enhanced Multi-Camera AI Monitoring System")
print("📍 Monitoring 4 Karachi Locations with Heavy Vehicle Priority:")
print("   📹 Shahrah-e-Faisal - Overspeeding (HIGH PRIORITY)")
print("   📹 University Road - Lane Violations (MEDIUM PRIORITY)") 
print("   📹 II Chundrigar Road - Truck Monitoring (HIGH PRIORITY)")
print("   📹 Gulshan-e-Iqbal - Reckless Driving (MEDIUM PRIORITY)")
print("=" * 60)

# Start video processing in background
threading.Thread(target=process_video, daemon=True).start()

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000, use_reloader=False)