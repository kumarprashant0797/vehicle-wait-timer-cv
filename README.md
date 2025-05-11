# Vehicle Wait Timer

A computer vision application that tracks vehicles and measures their wait times using YOLOv8 object detection.

## Features

- Real-time vehicle detection using YOLOv8
- Vehicle tracking with unique IDs
- Wait time measurement for each vehicle
- Output logging to text file
- Configurable via YAML file

## Prerequisites

- Python 3.x
- Dependencies listed in requirements.txt:
  - opencv-python >= 4.5.0
  - numpy >= 1.20.0
  - pyyaml >= 6.0
  - ultralytics >= 8.0.0
  - matplotlib >= 3.5.0

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd vehicle-wait-timer-cv
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Download the YOLOv8 model (yolov8n.pt should be in the root directory)

## Configuration

The application uses a `config.yaml` file for configuration settings. Modify this file to adjust:
- ROI (Region of Interest) settings
- Video input source
- Detection parameters

## Usage

1. Configure your settings in `config.yaml`

2. Run the main application:
```bash
python main.py
```

3. To quit the application, press 'q' while the video window is in focus

The application will generate an `output.txt` file containing wait time logs for each detected vehicle.

## Project Structure

- `main.py`: Main application script with vehicle tracking logic
- `select_roi.py`: Utility for selecting regions of interest
- `config.yaml`: Configuration settings
- `requirements.txt`: Project dependencies
- `output.txt`: Generated log file with vehicle wait times

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.