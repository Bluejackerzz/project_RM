from ultralytics import YOLO
import cv2

model = YOLO('models/yolov8n.pt')
vehicle_classes = ['car', 'truck', 'bus', 'motorbike']


def detect_vehicles(video_path):
    cap = cv2.VideoCapture(video_path)
    vehicle_counts = []

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        results = model(frame, conf=0.4, verbose=False)[0]
        boxes = results.boxes
        detections = []

        for box in boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            if label in vehicle_classes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2
                detections.append((cx, cy))

        vehicle_counts.append(detections)
    
    cap.release()
    return vehicle_counts
