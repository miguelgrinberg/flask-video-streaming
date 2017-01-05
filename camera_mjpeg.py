# Credit goes to Zaw Lin (http://stackoverflow.com/a/21844162/4258196)
# for the code that reads jpegs from an mjpeg stream - I just cleaned
# it up a little

# Note: This method of returning an error is not ideal, as the error
# image will continue to stream to the browser as an mjpeg stream. A
# better way would be to return something like "False" from get_frame()
# to the generator, and have the generator raise a StopIteration exception
# if this happens, so that the stream stops after the browser gets
# an error

import urllib


class Camera(object):
    def __init__(self):

        # Error flag
        self.error = None

        # The image to return if there was an error
        # Note: This loads the image into RAM right away - you may want
        # to read the image just before it needs to be returned instead
        self.error_image = open("error_image.jpg", "rb").read()

        # URL of mjpeg feed
        #   Eg:
        #       http://my_camera/Streaming/channels/102/httpPreview
        #   Eg with username, password and port:
        #       http://username:password@my_camera:port/Streaming/channels/102/httpPreview
        # Different cameras have different mjpeg URLs
        URL = ''

        # Try to connect to the stream
        try:
            self.stream = urllib.urlopen(URL)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.error = True
            return

    def get_frame(self):
        # If error flag was set, return error image
        if self.error is True:
            return self.error_image

        # Data we'll be reading
        data = ''

        # Read first part of header, and ignore it
        self.stream.read(62)

        # Read content length
        content_length = ''

        while True:
            content_length += self.stream.read(1)

            if '\r' in content_length:
                content_length = int(content_length[:-1])
                break

        # Skip the next 3 bytes
        self.stream.read(3)

        # Read content_length bytes (the jpeg data)
        data = self.stream.read(content_length)

        # Return the image
        return data
