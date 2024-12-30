# Real-Time Color Detection

This project uses OpenCV and NumPy to detect objects of a specific color from a live webcam feed. It draws bounding boxes around detected objects, and optionally saves the video to an MP4 file.

## Features

- Real-time detection of a target color
- Draws bounding boxes around detected objects
- Adjustable minimum area threshold to filter noise
- Optional MP4 video saving with timestamp
- Simple keyboard controls:
  - Press **r** to start/stop recording (if saving is enabled)
  - Press **q** to quit

## Requirements

- opencv-python>=4.8.0
- numpy>=1.23.4,<2.0.0

Install these dependencies using:

```bash
pip install -r requirements.txt
```

## Usage

1. Clone or download this repository.
2. Install dependencies.
3. Run the main script:

```bash
python main.py
```

4.  Pass arguments to configure color and saving:

- user_color: BGR color list, e.g. [0,255,255] (yellow).
- save: Boolean indicating whether to save video.
- save_folder: The folder where output is saved (default "output").

Example:

```bash
python main.py "[0, 255, 255]" True
```

When running:

- Press r to start/stop recording (if save=True).
- Press q to quit.

## File Overview

main.py:

- Captures webcam frames.
- Converts frames to HSV and creates a mask for the target color.
- Finds contours and draws bounding boxes for all objects above a minimum area.
- Optionally writes frames to an output video.

util.py:

- Contains get_limits(color), which calculates HSV lower/upper thresholds for a given BGR color.

## Example

![Real-Time Detection Example](public/example.jpg)
