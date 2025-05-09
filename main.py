import cv2
import yaml
from ultralytics import YOLO
import time
from datetime import datetime
import sys

class Vehicle:
    def __init__(self, id, center_x, center_y):
        self.id = id
        self.center_x = center_x
        self.center_y = center_y
        self.entry_time = time.time()
        self.last_seen = time.time()

    def update_position(self, center_x, center_y):
        self.center_x = center_x
        self.center_y = center_y
        self.last_seen = time.time()

    def get_wait_time(self):
        return time.time() - self.entry_time

    def format_wait_time(self):
        wait_time = self.get_wait_time()
        minutes = int(wait_time // 60)
        seconds = int(wait_time % 60)
        return f"{minutes:02d}:{seconds:02d}"

class VehicleTracker:
    def __init__(self):
        self.vehicles = {}
        self.next_id = 1

    def add_vehicle(self, center_x, center_y):
        vehicle = Vehicle(self.next_id, center_x, center_y)
        self.vehicles[self.next_id] = vehicle
        self.next_id += 1
        return vehicle

    def update_vehicles(self, current_time, log_file):
        for vid, vehicle in list(self.vehicles.items()):
            if current_time - vehicle.last_seen > 1.0:
                log_msg = f"Vehicle {vid} waited for {vehicle.format_wait_time()}"
                print(log_msg)
                log_file.write(log_msg + '\n')
                log_file.flush()
                del self.vehicles[vid]

    def find_existing_vehicle(self, center_x, center_y):
        for vehicle in self.vehicles.values():
            if abs(center_x - vehicle.center_x) < 50 and abs(center_y - vehicle.center_y) < 50:
                return vehicle
        return None

class VideoProcessor:
    def __init__(self, config):
        self.config = config
        self.cap = cv2.VideoCapture(config['video']['source'])
        ret, first_frame = self.cap.read()
        if not ret:
            raise Exception("Failed to read video")
        
        self.frame_size = (first_frame.shape[1], first_frame.shape[0])
        # Add back ROI selection
        self.roi = self.select_roi(first_frame)
        self.model = YOLO(config['model']['name'])
        self.out = cv2.VideoWriter(
            config['video']['output'],
            cv2.VideoWriter_fourcc(*'mp4v'),
            30.0,
            self.frame_size
        )

    @staticmethod
    def select_roi(frame):
        roi = cv2.selectROI("Select ROI", frame, False)
        cv2.destroyWindow("Select ROI")
        return roi

    def process_frame(self, frame, tracker, log_file):
        results = self.model(frame, conf=self.config['model']['confidence'],
                           classes=self.config['classes']['include'],
                           verbose=False)  # Add verbose=False to suppress output

        # Draw ROI
        cv2.rectangle(frame, (int(self.roi[0]), int(self.roi[1])),
                     (int(self.roi[0] + self.roi[2]), int(self.roi[1] + self.roi[3])),
                     (0, 255, 0), 2)

        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                if self.is_in_roi(x1, y1, x2, y2):
                    center_x = (x1 + x2) / 2
                    center_y = (y1 + y2) / 2

                    vehicle = tracker.find_existing_vehicle(center_x, center_y)
                    if vehicle:
                        vehicle.update_position(center_x, center_y)
                    else:
                        vehicle = tracker.add_vehicle(center_x, center_y)

                    self.draw_vehicle_info(frame, vehicle, x1, y1, x2, y2)

        tracker.update_vehicles(time.time(), log_file)
        self.out.write(frame)
        
        # Display frame if enabled in config
        if self.config['video'].get('display', True):  # Default to True if not specified
            cv2.imshow('Vehicle Tracking', frame)
            
        return frame

    def is_in_roi(self, x1, y1, x2, y2):
        return (self.roi[0] < x1 < self.roi[0] + self.roi[2] and
                self.roi[1] < y1 < self.roi[1] + self.roi[3])

    def draw_vehicle_info(self, frame, vehicle, x1, y1, x2, y2):
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
        cv2.putText(frame, f"ID:{vehicle.id} ({vehicle.format_wait_time()})",
                    (int(x1), int(y1)-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    def release(self):
        self.cap.release()
        self.out.release()
        cv2.destroyAllWindows()

def load_config():
    with open('config.yaml', 'r') as file:
        return yaml.safe_load(file)

def main():
    config = load_config()
    processor = VideoProcessor(config)
    tracker = VehicleTracker()

    with open('output.txt', 'w') as log_file:
        while processor.cap.isOpened():
            ret, frame = processor.cap.read()
            if not ret:
                break

            frame = processor.process_frame(frame, tracker, log_file)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    processor.release()

if __name__ == "__main__":
    main()
