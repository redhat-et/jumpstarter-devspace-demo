import os
import sys
import time
import pytest

from jumpstarter_testing.pytest import JumpstarterTest
from jumpstarter_imagehash import ImageHash

class TestExample(JumpstarterTest):
    @pytest.fixture()
    def console(self, client):
        with client.interface.console.pexpect() as console:
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

    def test_devices_in_place(self, client, console):
        console.sendline("ls /dev/nv*")
        console.expect("/dev/nvhost-gpu")
