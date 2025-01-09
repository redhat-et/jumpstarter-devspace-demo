#!/bin/env python
import time

from jumpstarter.common.utils import env


with env() as client:
    while True:
        img = client.video.snapshot()
        img.save("video.jpg")
        time.sleep(0.2)
