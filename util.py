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
    lowerLimit = max(0, hue - 10), 90, 90
    upperLimit = min(179, hue + 10), 255, 255
    
    # Convert limits to numpy arrays with uint8 datatype
    lowerLimit = np.array(lowerLimit, dtype=np.uint8)
    upperLimit = np.array(upperLimit, dtype=np.uint8)   
    
    return (lowerLimit, upperLimit)

# Pre-defined HSV ranges for 16 web colors
WEB_COLOR_LIMITS = {
    'aqua':    (np.array([85, 70, 50]), np.array([95, 255, 255])),
    'black':   (np.array([0, 0, 0]), np.array([180, 255, 30])),
    'blue':    (np.array([105, 70, 50]), np.array([135, 255, 255])),
    'fuchsia': (np.array([145, 70, 50]), np.array([155, 255, 255])),
    'gray':    (np.array([0, 0, 40]), np.array([180, 30, 150])),
    'green':   (np.array([45, 70, 50]), np.array([75, 255, 255])),
    'lime':    (np.array([45, 150, 50]), np.array([75, 255, 255])),
    'maroon':  (np.array([0, 70, 20]), np.array([10, 255, 150])),
    'navy':    (np.array([105, 70, 20]), np.array([135, 255, 150])),
    'olive':   (np.array([20, 70, 20]), np.array([30, 255, 150])),
    'purple':  (np.array([145, 70, 20]), np.array([155, 255, 150])),
    'red':     (np.array([0, 70, 50]), np.array([10, 255, 255])),
    'silver':  (np.array([0, 0, 150]), np.array([180, 30, 200])),
    'teal':    (np.array([85, 70, 20]), np.array([95, 255, 150])),
    'white':   (np.array([0, 0, 200]), np.array([180, 30, 255])),
    'yellow':  (np.array([25, 70, 50]), np.array([35, 255, 255]))
}

def get_limits_limited(color):
    """
    Get HSV limits for web colors.
    
    Args:
        color: String name of one of 16 colors
    
    Returns:
        tuple: (lowerLimit, upperLimit) - HSV threshold bounds for color detection
    """
    color = color.lower()
    if color not in WEB_COLOR_LIMITS:
        raise ValueError(f"Color '{color}' not in web colors. Available colors: {', '.join(WEB_COLOR_LIMITS.keys())}")
    
    return WEB_COLOR_LIMITS[color]