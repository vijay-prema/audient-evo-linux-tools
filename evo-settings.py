#!/usr/bin/env python3

# Run lsusb to find device (plug and unplug run twice)
# Then Get data on Audient EVO 4 audio interface:
# lsusb -v -d 2708:0006

# On Windows VM use USBPCap to capture a log then open in Wireshark
# https://wiki.wireshark.org/CaptureSetup/USB
# Or run Wireshark with USB capture option, use filters to identify the specific messages
# when actions are done on the device (e.g. button press)

import usb.core
import usb.util

def find_device():
    audient_vendor_id = 0x2708

    products = {
            0x0006: "Audient EVO4",
            0x0007: "Audient EVO8",
            0x000a: "Audient EVO16",
    }

    for product_id, product_name in products.items():
        dev = usb.core.find(idVendor=audient_vendor_id, idProduct=product_id)
        if dev is not None:
            print(f"Found {product_name}")
            return dev

    raise ValueError('Device not found')

def set_phantom_power(channel, power_on):
    # 48V (channel 1). First byte is 0x01 or 0x00 for on or off
    if power_on is True:
        dataFragment = b'\x01\x00\x00\x00'
    else:
        dataFragment = b'\x00\x00\x00\x00'

    assert dev.ctrl_transfer(0x21, 1, 0x0000, 0x3a00, dataFragment) == len(dataFragment)

dev = find_device()

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

set_phantom_power(1, True)

# Mic (channel 1) Volume. 2nd byte in data is volume level from 0x00 to 0x31
dataFragment = b'\x00\x61\x00\x00'
assert dev.ctrl_transfer(0x21, 1, 0x0100, 0x3a00, dataFragment) == len(dataFragment)


# This is needed to release interface, otherwise attach_kernel_driver fails 
# due to "Resource busy"
usb.util.dispose_resources(dev)

# Return control back to kernel driver
# It may raise USBError if there's e.g. no kernel driver loaded at all
if reattach:
    dev.attach_kernel_driver(0)
