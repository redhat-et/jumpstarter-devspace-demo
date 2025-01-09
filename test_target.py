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
        #image.save("expected.jpg")
        hasher = ImageHash(client.video)
        hasher.assert_snapshot("expected.jpg")
