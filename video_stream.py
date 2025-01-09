#!/bin/env python
import sys
import time

from jumpstarter.common.utils import env


with env() as client:
    while True:
        img = client.video.snapshot()
        img.save("video.jpg")
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(0.2)
