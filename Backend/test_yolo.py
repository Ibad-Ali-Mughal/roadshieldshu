import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')

# Open the video file or webcam
cap = cv2.VideoCapture('data/overspeeding.mp4')
if not cap.isOpened():
    print("Warning: sample_video.mp4 not found. Falling back to webcam (0).")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: No video file or webcam available.")
        exit()

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("End of input, restarting...")
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0) if "overspeeding.mp4" in cap.getBackendName() else cap.release()
            cap = cv2.VideoCapture(0)
            continue

        frame = cv2.resize(frame, (640, 480))

        results = model(frame, conf=0.5)

        for r in results:
            boxes = r.boxes
            for box in boxes:
                cls = int(box.cls)
                conf = float(box.conf)
                if conf > 0.5 and cls in [2, 5, 7]:  # Car, bus, truck
                    label = model.names[cls]
                    print(f"Detected: {label}, confidence: {conf:.2f}")

        annotated_frame = results[0].plot()
        cv2.imshow('YOLO Detection', annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Script interrupted by user.")
finally:
    cap.release()
    cv2.destroyAllWindows()