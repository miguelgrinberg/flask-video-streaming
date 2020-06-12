#!/usr/bin/env python
#!/usr/bin/env python
from labthings import monkey

monkey.patch_all()

import os
from flask import Flask, render_template, Response

from labthings.server.quick import create_app
from labthings.server.find import find_component
from labthings.server.view import PropertyView

# import camera driver
from camera_pi import Camera
from views import MjpegStream, SnapshotStream

app, labthing = create_app(
    __name__,
    title=f"Pi Camera",
    description="Thing for Pi Camers",
    types=["org.raspberrypi.camera"],
    version="0.1.0"
)

labthing.add_component(Camera(), "org.raspberrypi.camera")

labthing.add_view(MjpegStream, "/mjpeg")
labthing.add_view(SnapshotStream, "/still")

if __name__ == "__main__":
    from labthings.server.wsgi import Server
    Server(app).run(host="::", port=5000, debug=False, zeroconf=True)
