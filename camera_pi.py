import io
import time
import picamera
from base_camera import BaseCamera

STREAM_RESOLUTION = (
    832,
    624,
) 

class Camera(BaseCamera):
    @staticmethod
    def frames():
        with picamera.PiCamera() as camera:
            # let camera warm up
            time.sleep(2)

            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, 'jpeg', resize=STREAM_RESOLUTION, use_video_port=True):
                # return current frame
                stream.seek(0)
                yield stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()
