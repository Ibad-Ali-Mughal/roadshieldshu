# import cv2
# from ultralytics import YOLO

# # Load pre-trained YOLO model
# model = YOLO('yolov8n.pt')

# def detect_reckless_driving(frame):
#     """
#     Detect reckless driving behaviors in a video frame.
#     For prototyping, simulate detection with basic rules.
#     """
#     try:
#         if frame is None:
#             print("Error: Received None frame.")
#             return False, None, None

#         # Resize frame to reduce processing load
#         frame = cv2.resize(frame, (640, 480))

#         # Run YOLO to detect vehicles with lower confidence threshold
#         results = model(frame, conf=0.3)  # Lowered from 0.5
#         vehicles = [r for r in results[0].boxes if r.conf > 0.3 and int(r.cls) in [2, 5, 7]]  # Car, bus, truck

#         if vehicles:
#             print(f"Detected vehicles: {len(vehicles)}, classes: {[model.names[int(r.cls)] for r in vehicles]}")

#         # Simulate reckless detection
#         reckless_detected = len(vehicles) > 0  # Trigger on any vehicle
#         vehicle_type = 'truck' if vehicles else None
#         location = {'lat': 24.8607, 'lng': 67.0011}  # Mock Karachi coordinates

#         return reckless_detected, vehicle_type, location
#     except Exception as e:
#         print(f"Error in detection: {e}")
#         return False, None, None
# #
# import cv2
# from ultralytics import YOLO
# import random

# # Load pre-trained YOLO model
# model = YOLO('yolov8n.pt')

# # Different locations for each camera video
# CAMERA_LOCATIONS = {
#     "camera1_overspeeding": {
#         "name": "Shahrah-e-Faisal", 
#         "coords": {"lat": 24.8607, "lng": 67.0011},
#         "behavior": "Overspeeding"
#     },
#     "camera2_lane_violation": {
#         "name": "University Road", 
#         "coords": {"lat": 24.9285, "lng": 67.1180},
#         "behavior": "Lane Violation"
#     },
#     "camera3_truckspeed": {
#         "name": "II Chundrigar Road", 
#         "coords": {"lat": 24.8500, "lng": 67.0050},
#         "behavior": "Truck Overspeeding"
#     },
#     "camera4_reckless_car": {
#         "name": "Gulshan-e-Iqbal", 
#         "coords": {"lat": 24.9130, "lng": 67.1186},
#         "behavior": "Reckless Driving"
#     }
# }

# def detect_reckless_driving(frame, camera_id="camera1_overspeeding"):
#     """
#     Detect reckless driving behaviors with camera-specific locations.
#     """
#     try:
#         if frame is None:
#             print("Error: Received None frame.")
#             return False, None, None

#         # Resize frame to reduce processing load
#         frame = cv2.resize(frame, (640, 480))

#         # Run YOLO to detect vehicles
#         results = model(frame, conf=0.3)
#         vehicles = [r for r in results[0].boxes if r.conf > 0.3 and int(r.cls) in [2, 5, 7]]  # Car, bus, truck

#         if vehicles:
#             vehicle_names = [model.names[int(r.cls)] for r in vehicles]
#             print(f"✅ {camera_id}: Detected {len(vehicles)} vehicles - {vehicle_names}")

#         # Simulate reckless detection - trigger on any vehicle
#         reckless_detected = len(vehicles) > 0
#         vehicle_type = model.names[int(vehicles[0].cls)] if vehicles else 'car'
#         location_data = CAMERA_LOCATIONS[camera_id]

#         return reckless_detected, vehicle_type, location_data
        
#     except Exception as e:
#         print(f"Error in detection: {e}")
#         return False, None, None

# thrid check

# import cv2
# from ultralytics import YOLO
# import random
# import time

# # Load pre-trained YOLO model
# model = YOLO('yolov8n.pt')

# # Different locations for each camera video
# CAMERA_LOCATIONS = {
#     "camera1_overspeeding": {
#         "name": "Shahrah-e-Faisal", 
#         "coords": {"lat": 24.8607, "lng": 67.0011},
#         "behavior": "Overspeeding"
#     },
#     "camera2_lane_violation": {
#         "name": "University Road", 
#         "coords": {"lat": 24.9285, "lng": 67.1180},
#         "behavior": "Lane Violation"
#     },
#     "camera3_truckspeed": {
#         "name": "II Chundrigar Road", 
#         "coords": {"lat": 24.8500, "lng": 67.0050},
#         "behavior": "Truck Overspeeding"
#     },
#     "camera4_reckless_car": {
#         "name": "Gulshan-e-Iqbal", 
#         "coords": {"lat": 24.9130, "lng": 67.1186},
#         "behavior": "Reckless Driving"
#     }
# }

# # Track last detection time for each camera to avoid spam
# last_detection_time = {}

# def detect_reckless_driving(frame, camera_id="camera1_overspeeding"):
#     """
#     Detect reckless driving behaviors with camera-specific locations.
#     """
#     try:
#         if frame is None:
#             print("Error: Received None frame.")
#             return False, None, None

#         # Resize frame to reduce processing load
#         frame = cv2.resize(frame, (640, 480))

#         # Run YOLO to detect vehicles
#         results = model(frame, conf=0.3)
        
#         # FIXED: Check if boxes exist to avoid errors
#         vehicles = []
#         if results[0].boxes is not None:
#             vehicles = [r for r in results[0].boxes if r.conf > 0.3 and int(r.cls) in [2, 5, 7]]  # Car, bus, truck

#         if vehicles:
#             vehicle_names = [model.names[int(r.cls)] for r in vehicles]
#             print(f"✅ {camera_id}: Detected {len(vehicles)} vehicles - {vehicle_names}")

#         # FIXED: Only trigger detection occasionally, not every frame
#         current_time = time.time()
#         last_time = last_detection_time.get(camera_id, 0)
        
#         # Only send alert if enough time has passed since last detection (5 seconds)
#         if len(vehicles) > 0 and (current_time - last_time) > 5:
#             last_detection_time[camera_id] = current_time
#             vehicle_type = model.names[int(vehicles[0].cls)]
#             location_data = CAMERA_LOCATIONS[camera_id]
            
#             print(f"🚨 ALERT SENT: {vehicle_type} at {location_data['name']}")
#             return True, vehicle_type, location_data
#         else:
#             if len(vehicles) > 0:
#                 print(f"⏳ Detection suppressed (cooldown): {camera_id}")
#             return False, None, None
        
#     except Exception as e:
#         print(f"Error in detection: {e}")
#         return False, None, None
    
    # for truck alerts
import cv2
from ultralytics import YOLO
import random
import time

# Load pre-trained YOLO model
model = YOLO('yolov8n.pt')

# Different locations for each camera video
CAMERA_LOCATIONS = {
    "camera1_overspeeding": {
        "name": "Shahrah-e-Faisal", 
        "coords": {"lat": 24.8607, "lng": 67.0011},
        "behavior": "Overspeeding",
        "priority": "high"  # Highway - critical for heavy vehicles
    },
    "camera2_lane_violation": {
        "name": "University Road", 
        "coords": {"lat": 24.9285, "lng": 67.1180},
        "behavior": "Lane Violation",
        "priority": "medium"  # Educational area
    },
    "camera3_truckspeed": {
        "name": "II Chundrigar Road", 
        "coords": {"lat": 24.8500, "lng": 67.0050},
        "behavior": "Truck Overspeeding", 
        "priority": "high"  # Commercial area - heavy truck traffic
    },
    "camera4_reckless_car": {
        "name": "Gulshan-e-Iqbal", 
        "coords": {"lat": 24.9130, "lng": 67.1186},
        "behavior": "Reckless Driving",
        "priority": "medium"  # Residential area
    }
}

# Track last detection time for each camera to avoid spam
last_detection_time = {}
last_heavy_vehicle_alert = {}

# Define heavy vehicles that cause fatal accidents
HEAVY_VEHICLE_CLASSES = [5, 7]  # Bus = 5, Truck = 7 (YOLO class IDs)
NORMAL_VEHICLE_CLASSES = [2, 3]  # Car = 2, Motorcycle = 3

def detect_reckless_driving(frame, camera_id="camera1_overspeeding"):
    """
    Detect reckless driving behaviors with SPECIAL FOCUS ON HEAVY VEHICLES.
    Priority monitoring for trucks and buses that cause fatal accidents.
    """
    try:
        if frame is None:
            print("Error: Received None frame.")
            return False, None, None, False, False

        # Resize frame to reduce processing load
        frame = cv2.resize(frame, (640, 480))

        # Run YOLO to detect vehicles
        results = model(frame, conf=0.3)
        
        # SEPARATE DETECTION FOR HEAVY vs NORMAL VEHICLES
        heavy_vehicles = []
        normal_vehicles = []
        all_vehicles = []
        
        if results[0].boxes is not None:
            for r in results[0].boxes:
                cls = int(r.cls)
                conf = float(r.conf)
                
                if conf > 0.3:
                    all_vehicles.append(r)
                    
                    # PRIORITY: Heavy vehicle detection (trucks, buses)
                    if cls in HEAVY_VEHICLE_CLASSES:
                        heavy_vehicles.append(r)
                        print(f"⚠️ HEAVY VEHICLE DETECTED: {model.names[cls]} (confidence: {conf:.2f})")
                    
                    # Normal vehicles
                    elif cls in NORMAL_VEHICLE_CLASSES:
                        normal_vehicles.append(r)

        if all_vehicles:
            vehicle_names = [model.names[int(r.cls)] for r in all_vehicles]
            print(f"✅ {camera_id}: Detected {len(all_vehicles)} vehicles - {vehicle_names}")
            
            # SPECIFIC LOGGING FOR HEAVY VEHICLES
            if heavy_vehicles:
                heavy_names = [model.names[int(r.cls)] for r in heavy_vehicles]
                print(f"🚛 CRITICAL: {len(heavy_vehicles)} heavy vehicles - {heavy_names}")

        # FIXED: Different cooldown for heavy vs normal vehicles
        current_time = time.time()
        last_time = last_detection_time.get(camera_id, 0)
        last_heavy_time = last_heavy_vehicle_alert.get(camera_id, 0)
        
        # PRIORITY 1: HEAVY VEHICLE DETECTION (More frequent alerts due to danger)
        heavy_vehicle_detected = len(heavy_vehicles) > 0
        normal_vehicle_detected = len(normal_vehicles) > 0
        
        # Special alert for heavy vehicles (2-second cooldown for immediate response)
        if heavy_vehicle_detected and (current_time - last_heavy_time) > 2:
            last_heavy_vehicle_alert[camera_id] = current_time
            vehicle_type = model.names[int(heavy_vehicles[0].cls)]
            location_data = CAMERA_LOCATIONS[camera_id]
            
            print(f"🚨🚛 CRITICAL ALERT: {vehicle_type} detected at {location_data['name']}")
            print(f"   🚨 IMMEDIATE ACTION REQUIRED - Potential fatal accident risk!")
            
            return True, vehicle_type, location_data, True, False  # heavy_vehicle, not_speeding
        
        # PRIORITY 2: NORMAL VEHICLE DETECTION (5-second cooldown)
        elif normal_vehicle_detected and (current_time - last_time) > 5:
            last_detection_time[camera_id] = current_time
            vehicle_type = model.names[int(normal_vehicles[0].cls)]
            location_data = CAMERA_LOCATIONS[camera_id]
            
            print(f"🚨 ALERT: {vehicle_type} detected at {location_data['name']}")
            return True, vehicle_type, location_data, False, False  # not_heavy, not_speeding
        
        else:
            if heavy_vehicle_detected:
                print(f"⏳ Heavy vehicle monitoring active: {camera_id}")
            elif normal_vehicle_detected:
                print(f"⏳ Detection suppressed (cooldown): {camera_id}")
            
            return False, None, None, False, False
        
    except Exception as e:
        print(f"Error in detection: {e}")
        return False, None, None, False, False


def analyze_vehicle_behavior(vehicles, frame, camera_id):
    """
    Advanced analysis specifically for heavy vehicle behavior detection
    """
    try:
        if not vehicles:
            return False, False, False
            
        reckless_behavior = False
        speeding_detected = False
        lane_violation = False
        
        for vehicle in vehicles:
            cls = int(vehicle.cls)
            conf = float(vehicle.conf)
            
            # HEAVY VEHICLE SPECIFIC CHECKS
            if cls in HEAVY_VEHICLE_CLASSES:
                vehicle_type = model.names[cls]
                
                # Check for common heavy vehicle violations
                if conf > 0.6:  # High confidence detection
                    # Simulate behavior analysis (in real implementation, use tracking)
                    if random.random() < 0.3:  # 30% chance of violation for demo
                        reckless_behavior = True
                        print(f"🚨 {vehicle_type} reckless behavior detected!")
                        
                        # Specific violation types for heavy vehicles
                        violation_types = [
                            "overspeeding", "illegal_lane_change", 
                            "overloading", "signal_violation"
                        ]
                        violation = random.choice(violation_types)
                        print(f"   🚔 Violation type: {violation}")
                        
                        if violation == "overspeeding":
                            speeding_detected = True
                        elif violation == "illegal_lane_change":
                            lane_violation = True
                
        return reckless_behavior, speeding_detected, lane_violation
        
    except Exception as e:
        print(f"Behavior analysis error: {e}")
        return False, False, False


def get_heavy_vehicle_risk_assessment(vehicle_type, location, count):
    """
    Risk assessment specifically for heavy vehicles
    """
    risk_level = "low"
    recommendation = "Normal monitoring"
    
    if vehicle_type in ["truck", "bus"]:
        if count > 2:  # Multiple heavy vehicles
            risk_level = "high"
            recommendation = "IMMEDIATE: Deploy traffic control"
        elif location in ["Shahrah-e-Faisal", "II Chundrigar Road"]:
            risk_level = "medium"
            recommendation = "Alert nearby patrol units"
        else:
            risk_level = "elevated" 
            recommendation = "Increase monitoring frequency"
    
    return {
        "risk_level": risk_level,
        "recommendation": recommendation,
        "response_time": "immediate" if risk_level == "high" else "monitor"
    }