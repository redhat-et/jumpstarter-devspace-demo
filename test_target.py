import os
import sys
import time
import pytest

from jumpstarter.testing.pytest import JumpstarterTest
from jumpstarter.client.adapters import PexpectAdapter
from jumpstarter_imagehash import ImageHash

class TestExample(JumpstarterTest):
    @pytest.fixture()
    def console(self, client):
        with PexpectAdapter(client=client.interface.console) as console:
            if os.environ.get("DEBUG_CONSOLE"):
                console.logfile_read = sys.stdout.buffer
            yield console

    def test_boot_login(self, client, console):
        client.interface.power.off()
        time.sleep(1)
        client.interface.storage.dut()
        client.interface.power.on()
        console.expect("login:", timeout=240)
        console.sendline("redhat")
        console.expect("Password:", timeout=30)
        console.sendline("redhat")

    def test_boot_image(self, client):
        # at this point the target is booted, we just take the image
        #image = client.video.snapshot()
        #image.save("test.jpg")
        hasher = ImageHash(client.video)
        hasher.assert_snapshot("test.jpg")

    def test_video_boot(self, client):
        client.interface.power.off()
        time.sleep(1)
        client.interface.storage.dut()
        client.interface.power.on()
        for _ in range(240):
            img = client.video.snapshot()
            img.save("video.jpg")
            time.sleep(0.2)
