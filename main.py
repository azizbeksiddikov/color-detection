import cv2
import os
from datetime import datetime
from util import get_limits

def main(user_color, save=False, save_folder='output'):
    # Configuration
    FRAME_WIDTH = 640
    FRAME_HEIGHT = 480
    MIN_AREA = 5
    FPS = 20.0

    # Create output directory
    if save and not os.path.exists(save_folder):
        os.makedirs(save_folder)
    
    # Video writer setup
    out = None
    is_recording = False
    if save:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = os.path.join(save_folder, f'detection_{timestamp}.mp4')
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, FPS, (FRAME_WIDTH, FRAME_HEIGHT))
    
    
    # Calculate color limits once
    lowerLimit, upperLimit = get_limits(user_color)
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot open webcam")
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

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
        
        
        
        
        if is_recording:
            cv2.putText(frame, "REC", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                       1, (0, 0, 255), 2)
        
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
            

    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    yellow_bgr = [0, 255, 255] # put color here
    main(yellow_bgr, save=True) # set save=True to save video and press "r" to start recording