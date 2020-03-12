"""
Helper functions for PiCam on Raspberry Pi 3 B+.
This file only works on a RPi 3 B+ and compatible devices currently.
"""
import cv2

def retrieve_webcam(mirror=False):
    cam = cv2.VideoCapture(0)
    while True:
        ret_val, img = cam.read()
        if mirror: 
            img = cv2.flip(img, 1)
        else:
            pass
        cv2.imshow('Stage 2 LIVE!', img)
        if cv2.waitKey(1) == 27: 
            break  # esc to quit
        else:
            pass
    cv2.destroyAllWindows()

def camera(mirror_status):
    retrieve_webcam(mirror=mirror_status)
    
# exports camera