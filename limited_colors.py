import cv2
import os
from datetime import datetime
from util import get_limits_limited

# Available web colors for reference
WEB_COLORS = ['aqua', 'black', 'blue', 'fuchsia', 'gray', 'green', 
              'lime', 'maroon', 'navy', 'olive', 'purple', 'red', 
              'silver', 'teal', 'white', 'yellow']

def main(color_name, save=False, save_folder='output'):
    """
    Detect objects of specified web color using webcam.
    
    Args:
        color_name: String name of web color to detect
        save: Boolean to enable video saving
        save_folder: Output directory for saved videos
    """
    # Configuration
    FRAME_WIDTH = 640
    FRAME_HEIGHT = 480
    MIN_AREA = 5
    FPS = 20.0

    # Validate color name
    if color_name.lower() not in WEB_COLORS:
        raise ValueError(f"Invalid color. Choose from: {', '.join(WEB_COLORS)}")

    # Create output directory
    if save and not os.path.exists(save_folder):
        os.makedirs(save_folder)
    
    # Video writer setup
    out = None
    is_recording = False
    if save:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = os.path.join(save_folder, f'{color_name}_{timestamp}.mp4')
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, FPS, (FRAME_WIDTH, FRAME_HEIGHT))
    
    # Get color limits once
    lowerLimit, upperLimit = get_limits_limited(color_name.lower())
    
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot open webcam")
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    print(f"Detecting {color_name} objects. Press 'q' to quit, 'r' to toggle recording.")

    while True:
        ret, frame = cap.read()
        
        # Color detection
        hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)
        
        # Find and process contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Draw rectangles for all detected objects above minimum size
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > MIN_AREA:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Show recording status
        if is_recording:
            cv2.putText(frame, "REC", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 
                       1, (0, 0, 255), 2)
        
        # Show detected color name
        cv2.putText(frame, f"Detecting: {color_name}", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Save frame if recording
        if is_recording and out is not None:
            out.write(frame)
        
        cv2.imshow('Color Detection', frame)
        
        # Handle keyboard input
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r') and save:
            is_recording = not is_recording
            print("Recording:", "Started" if is_recording else "Stopped")
    
    # Cleanup
    if out is not None:
        out.release()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # aqua, black, blue, fuchsia, 
    # gray, green, lime, maroon,
    # navy, olive, purple, red, 
    # silver, teal, white, and yellow.

    # color_name = 'lime' 
    # main(color_name, save=True)
    for color in WEB_COLORS:
        main(color, save=True)