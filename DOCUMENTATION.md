# Vehicle Wait Timer - Computer Vision Documentation

## Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Pipeline Flow](#pipeline-flow)
4. [Installation](#installation)
5. [Docker Setup](#docker-setup)
6. [Usage](#usage)
7. [Configuration](#configuration)
8. [Algorithm Details](#algorithm-details)
9. [Performance Optimization](#performance-optimization)
10. [Edge Cases & Solutions](#edge-cases--solutions)

## Overview
This application processes video input to detect and track vehicles within a specified Region of Interest (ROI), calculating their wait times. The system uses YOLOv8 for object detection and custom tracking algorithms for vehicle monitoring.

## System Architecture
```
┌─────────────────┐     ┌──────────────┐     ┌────────────────┐
│   Video Input   │────▶│ YOLOv8       │────▶│ Vehicle        │
│   (input.mp4)   │     │ Detection    │     │ Tracking       │
└─────────────────┘     └──────────────┘     └────────────────┘
                                                      │
┌─────────────────┐     ┌──────────────┐            ▼
│   Output Video  │◀────│ Visualization │◀───┌────────────────┐
│   (output.mp4)  │     │              │    │ Wait Time      │
└─────────────────┘     └──────────────┘    │ Calculation    │
                                            └────────────────┘
```

## Pipeline Flow
1. **Video Input Processing**
   - Load video from input.mp4
   - Extract frames
   - Define ROI (Region of Interest)

2. **Object Detection**
   - YOLOv8 model processes each frame
   - Detects vehicles with confidence scores
   - Filters detections within ROI

3. **Vehicle Tracking**
   - Assigns unique IDs to vehicles
   - Tracks vehicle positions across frames
   - Maintains vehicle state information

4. **Wait Time Calculation**
   - Monitors vehicle presence in ROI
   - Calculates cumulative wait time
   - Updates per-vehicle timing data

5. **Visualization**
   - Draws bounding boxes
   - Displays ROI
   - Shows wait times (MM:SS format)
   - Generates output video

## Installation

### Prerequisites
- Docker Desktop
- Input video file (input.mp4)
- YOLO model file (yolov8n.pt)
- Configuration file (config.yaml)

### Repository Setup
```bash
git clone [repository-url]
cd vehicle-wait-timer-cv
```

## Docker Setup

### Project Structure
```
vehicle-wait-timer-cv/
├── Dockerfile
├── docker-compose.yml
├── main.py
├── requirements.txt
├── config.yaml
├── input.mp4
└── yolov8n.pt
```

### Building the Docker Image
```bash
docker compose build
```

### Running the Container
```bash
docker compose up
```

### Volume Mappings
The docker-compose.yml configures the following mappings:
```yaml
volumes:
  - ./input.mp4:/app/input.mp4
  - ./config.yaml:/app/config.yaml
  - ./output.txt:/app/output.txt
  - ./yolov8n.pt:/app/yolov8n.pt
  - ./output.mp4:/app/output.mp4
```

## Usage

1. **Prepare Input Files**
   - Place input video as `input.mp4`
   - Ensure YOLO model `yolov8n.pt` is present
   - Configure `config.yaml`

2. **Run the Application**
   ```bash
   docker compose up
   ```

3. **Check Output**
   - Generated video: output.mp4
   - Wait time logs: output.txt

## Configuration

### config.yaml Options
```yaml
video:
  source: "input.mp4"
  output: "output.mp4"
  display: false  # Set to true for visual output

model:
  name: "yolov8n.pt"
  confidence: 0.25
  device: "cpu"    # Use "cuda" for GPU

classes:
  include: [2]     # Vehicle class
```

## Algorithm Details

### Vehicle Detection
- Uses YOLOv8 nano model
- Confidence threshold: 0.25
- Focuses on vehicle class (2)

### Vehicle Tracking
- Center point tracking algorithm
- Distance-based association
- Timeout mechanism for lost tracks

### Wait Time Calculation
```python
def update_wait_time(self):
    current_time = time.time()
    if self.is_in_roi:
        self.total_wait_time += (current_time - self.last_update)
    self.last_update = current_time
```

## Performance Optimization

### CPU Mode Optimizations
1. Frame Resolution Management
2. Batch Processing
3. ROI-based Processing
4. Efficient Memory Management

### Memory Usage
- Proper cleanup of processed frames
- Minimized copy operations
- Stream-based video processing

## Edge Cases & Solutions

1. **Occlusion Handling**
   - Solution: Predictive tracking
   - State maintenance during brief disappearance

2. **Lighting Changes**
   - Solution: Adaptive confidence thresholds
   - Multiple detection attempts

3. **Multiple Vehicle Scenarios**
   - Solution: Enhanced tracking logic
   - Unique ID maintenance

4. **Border Cases**
   - Solution: ROI buffer zones
   - Entry/exit validation

## Troubleshooting

### Common Issues
1. **Docker Permission Issues**
   - Solution: Check volume permissions
   - Ensure proper file ownership

2. **Performance Issues**
   - Solution: Adjust batch size
   - Reduce frame resolution

3. **Memory Issues**
   - Solution: Enable garbage collection
   - Monitor memory usage

### Error Codes
- E001: Video file not found
- E002: Model loading error
- E003: GPU not available