import time
import gevent
from labthings.core.event import ClientEvent


class BaseCamera(object):
    def __init__(self):
        """Start the background camera thread if it isn't running yet."""
        self.thread = None  # background thread that reads frames from camera
        self.frame = None  # current frame is stored here by background thread

        self.last_access = 0  # time of last client access to the camera
        self.event = ClientEvent()

        self.start_worker()

    def start_worker(self, timeout: int = 5):
        if self.thread is None:
            self.last_access = time.time()

            # start background frame thread
            self.thread = gevent.spawn(self._thread)

            # wait until frames are available
            timeout_time = time.time() + timeout
            while self.get_frame() is None:
                if time.time() > timeout_time:
                    raise TimeoutError("Timeout waiting for frames.")
                else:
                    gevent.sleep()

    def get_frame(self):
        """Return the current camera frame."""
        self.last_access = time.time()

        # wait for a signal from the camera thread
        self.event.wait()
        self.event.clear()

        return self.frame

    def frames(self):
        """"Generator that returns frames from the camera."""
        raise RuntimeError('Must be implemented by subclasses.')

    def _thread(self):
        """Camera background thread."""
        print('Starting camera thread.')

        frames_iterator = self.frames()
        for frame in frames_iterator:
            self.frame = frame
            self.event.set()  # send signal to clients
            gevent.sleep()

            # if there hasn't been any clients asking for frames in
            # the last 10 seconds then stop the thread
            if time.time() - self.last_access > 10:
                frames_iterator.close()
                print('Stopping camera thread due to inactivity.')
                break

        self.thread = None
