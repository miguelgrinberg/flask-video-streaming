#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response

# import camera driver
from camera_pi import Camera

app = Flask(__name__)
main_camera = Camera()

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/mjpeg')
def mjpeg():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(main_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/still')
def still():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(main_camera.get_frame(), mimetype="image/jpeg")


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
