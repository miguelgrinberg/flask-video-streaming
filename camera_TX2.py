#====================================================
#   Function: Capture frames from TX2 onboard camera
#    
#   This code builds Camera class a video streaming 
#   captured from TX2 onboard camera. 
#   Reference: https://jkjung-avt.github.io/tx2-camera-with-python/
#
#   Written by Gengxin Xie <xiegx@163.com> 08/02/2018
#=====================================================

from base_camera import BaseCamera
import cv2

class Camera(BaseCamera):
    width = 640;            
    height = 480;
    gst_str = ("nvcamerasrc ! "
               "video/x-raw(memory:NVMM), width=(int)2592, height=(int)1458, format=(string)I420, framerate=(fraction)30/1 ! "
               "nvvidconv ! video/x-raw, width=(int){}, height=(int){}, format=(string)BGRx ! "
               "videoconvert ! appsink").format(width, height) 
    @staticmethod
    def set_video_para(w, h):
        Camera.width = w;
        Camera.height = h;
        Camera.gst_str = ("nvcamerasrc ! "
               "video/x-raw(memory:NVMM), width=(int)2592, height=(int)1458, format=(string)I420, framerate=(fraction)30/1 ! "
               "nvvidconv ! video/x-raw, width=(int){}, height=(int){}, format=(string)BGRx ! "
               "videoconvert ! appsink").format(w, h)

    @staticmethod
    def frames():
        cap = cv2.VideoCapture(Camera.gst_str, cv2.CAP_GSTREAMER)
        if not cap.isOpened():
            raise RuntimeError("Could not start camera.")
        
        while True:
            _, img = cap.read()     #read curent frame
            yield cv2.imencode('.jpg', img)[1].tobytes()    
