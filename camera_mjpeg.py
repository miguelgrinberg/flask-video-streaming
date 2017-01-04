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

        # The data we will be reading
        self.data = ''

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

        # See if the data looks like an mjpeg stream
        self.data += self.stream.read(1024)

        if '\xff\xd8' not in self.data or 'Content-Type: image/jpeg' not in self.data:
            self.error = True

    def get_frame(self):
        # If error flag was set, return error image
        if self.error is True:
            return self.error_image

        # Read data until we get a single, full jpg image from the
        # mjpeg stream that we can return
        while True:
            self.data += self.stream.read(1024)

            # Individual jpegs in an mjpeg stream start with '\xff\xd8'
            # and end with '\xff\xd9'

            start = self.data.find('\xff\xd8')
            end = self.data.find('\xff\xd9')

            # Check if we've read enough data to put together a single
            # jpg image
            if start != -1 and end != -1: 
                # Pull out just the data representing our image
                jpg = self.data[start:end+2]

                # Truncate the data to forget the image we just read
                # from memory
                self.data = self.data[end+2:]
    
                # Return the image
                return jpg
