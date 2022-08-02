import os
import numpy as np
import cv2
from base_camera import BaseCamera

class VideoCaptureRND():
    def __init__(self, size=(100, 100, 3)):
        self._size = size

    def isOpened(self):
        return True

    def read(self):
        rnd_img = np.random.randint(255, size=self._size, dtype=np.uint8)
        return True, rnd_img

class Camera(BaseCamera):
    video_source = 0

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            video_source = os.environ.get('OPENCV_CAMERA_SOURCE')
            if not video_source == "rnd":
                Camera.set_video_source(int(video_source))
            else:
                Camera.set_video_source(video_source)
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        if Camera.video_source == "rnd":
            camera = VideoCaptureRND(size=(640,640,3))
        else:
            camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # read current frame
            _, img = camera.read()

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()
