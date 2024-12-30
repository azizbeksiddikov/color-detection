import numpy as np
import cv2

def get_limits(color):
    """
    Calculate HSV color range limits for a given BGR color value.
    
    Args:
        color: BGR color value as a list/tuple of 3 integers
    
    Returns:
        tuple: (lowerLimit, upperLimit) - HSV threshold bounds for color detection
    """
    # Convert BGR to HSV
    c = np.uint8([[color]])
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)
    
    # HSV tolerances
    hue = hsvC[0][0][0]
    lowerLimit = max(0, hue - 10), 100, 100
    upperLimit = min(179, hue + 10), 255, 255
    
    # Convert limits to numpy arrays with uint8 datatype
    lowerLimit = np.array(lowerLimit, dtype=np.uint8)
    upperLimit = np.array(upperLimit, dtype=np.uint8)   
    
    return lowerLimit, upperLimit