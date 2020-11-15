# Run lsusb to find device (plug and unplug run twice)
# Then Get data on Audient EVO 4 audio interface:
# lsusb -v -d 2708:0006

# On Windows VM use USBPCap to capture a log then open in Wireshark
# https://wiki.wireshark.org/CaptureSetup/USB
# Or run Wireshark with USB capture option, use filters to identify the specific messages
# when actions are done on the device (e.g. button press)

import usb.core
import usb.util

# find our device
dev = usb.core.find(idVendor=0x2708, idProduct=0x0006)

# was it found?
if dev is None:
    raise ValueError('Device not found')

reattach = False
if dev.is_kernel_driver_active(0):
    reattach = True
    dev.detach_kernel_driver(0)

usb.util.claim_interface(dev, 0)
dev.reset()
# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()

# SEND CONTROL DATA
# Params are: bmRequestType, bmRequest, wValue, wIndex, dataFragment
# Copy these from the Wireshark recording
# Assert return value is length of bytes sent (length of dataFragment)

# Headphone Volume. 2nd byte in data is volume level from 0x00 to 0xff
dataFragment = b'\x00\xf0\xff\xff'
assert dev.ctrl_transfer(0x21, 1, 0x0000, 0x3b00, dataFragment) == len(dataFragment)
# 48V (channel 1). First byte is 0x01 or 0x00 for on or off
dataFragment = b'\x01\x00\x00\x00'
assert dev.ctrl_transfer(0x21, 1, 0x0000, 0x3a00, dataFragment) == len(dataFragment)
# Mic (channel 1) Volume. 2nd byte in data is volume level from 0x00 to 0x31
dataFragment = b'\x00\x1f\x00\x00'
assert dev.ctrl_transfer(0x21, 1, 0x0100, 0x3a00, dataFragment) == len(dataFragment)


# This is needed to release interface, otherwise attach_kernel_driver fails 
# due to "Resource busy"
usb.util.dispose_resources(dev)

# Return control back to kernel driver
# It may raise USBError if there's e.g. no kernel driver loaded at all
if reattach:
    dev.attach_kernel_driver(0)
