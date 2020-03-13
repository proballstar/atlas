"""
       _______ _                _____ 
    /\|__   __| |        /\    / ____|
   /  \  | |  | |       /  \  | (___  
  / /\ \ | |  | |      / /\ \  \___ \ 
 / ____ \| |  | |____ / ____ \ ____) |
/_/    \_\_|  |______/_/    \_\_____/ 

This file is part of Atlas and Firebolt Space Agency.

Copyright 2017 - 2020 Firebolt, Inc,
Copyright 2017 - 2020 Firebolt Space Agency,
Copyright 2020 - Present Aaron Ma.
All Rights Reserved.

Licensed under the MIT License

Helper functions for PiCam on Raspberry Pi 3 B+.
This file only works on a RPi 3 B+ and compatible devices currently.
"""
#@TODO: Make it Compatible with Raspberry Pi 0 W

import cv2                              # Import cv2 library

def retrieve_webcam(mirror=False):      # Camera function
    """
    - input:
        - mirror: boolean
            By default False, but when True,
            mirror is enabled.
    """
    cam = cv2.VideoCapture(0)            # Create Camera Window
    while True:                          # While the function is called
        ret_val, img = cam.read()        # Read the current camera
        if mirror:                       # If mirror is true:
            img = cv2.flip(img, 1)       # Create a mirrored experience
        else:                            #
            pass                         # Anything else, ignore
        cv2.imshow('Stage 2 LIVE!', img) # 
        if cv2.waitKey(1) == 27:         # Wait until key 27 is pressed
            break                        # Press ESC (key 27) to quit
        else:                            # Anything else
            pass                         # Anything else, ignore 
    
    cv2.destroyAllWindows()              # Close Camera Window

def camera(mirror_status):               # Camera utility wizard function
    """
    - input:
        - mirror_status: boolean
            Takes in a boolean and if True, enable mirror,
            anything else will disable mirror.
    
    - output:
        - retrieve_webcam() Camera Window
    """
    retrieve_webcam(mirror=mirror_status) # Call the retrieve_webcam() function with the mirror_status boolean value
    
# exports camera