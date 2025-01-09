disk.raw:
	scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null majopela@192.168.1.159:~/disk.raw .

build: disk.raw

flash: disk.raw
	j interface power off
	j interface storage write-local-file disk.raw
	j interface storage dut

boot:
	j interface power off
	sleep 1
	j interface storage dut
	j interface power on

console:
	j interface console start-console

video:
	./video_stream.py

boot-console: boot console

.PHONY: flash build boot boot-console console
