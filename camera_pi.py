import io
import time
import gevent
import picamera
from base_camera import BaseCamera

STREAM_RESOLUTION = (
    832,
    624,
) 

class Camera(BaseCamera):

    def __init__(self):
        self.camera = picamera.PiCamera()
        self.stream = io.BytesIO()

        BaseCamera.__init__(self)

    def capture(self, *args, **kwargs):
        return self.camera.capture(*args, **kwargs)

    def frames(self):
        self.camera.start_recording(
            self.stream,
            format="mjpeg",
            quality=70
        )

        try:
            while True:
                self.stream.seek(0)
                self.stream.truncate()
                # to stream, read the new frame
                gevent.sleep(1 / self.camera.framerate * 0.1)
                # yield the result to be read
                frame = self.stream.getvalue()

                # ensure the size of package is right
                if len(frame) == 0:
                    pass
                else:
                    yield frame

        finally:
            self.camera.stop_recording()

