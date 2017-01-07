#!/usr/bin/env python2

from bluepy import btle
import struct
import time
import BB8_driver
import sys

bb8 = BB8_driver.Sphero()

print "connecting...\n"
try:
    bb8.connect()
except:
    print 'dsfsfdds'
    sys.exit(1)

print "starting...\n"
bb8.start()
time.sleep(2)

print "goin red...\n"
bb8.set_rgb_led(255, 0, 0, 0, False)
time.sleep(1)

print "goin green...\n"
bb8.set_rgb_led(0, 255, 0, 0, False)
time.sleep(1)

print "goin blue...\n"
bb8.set_rgb_led(0, 0, 255, 0, False)
time.sleep(1)

print "goin neon yellow...\n"
bb8.set_rgb_led(255, 255, 0, 0, False)
time.sleep(1)

print "goin purple...\n"
bb8.set_rgb_led(255, 0, 255, 0, False)
time.sleep(1)

print "goin pink...\n"
bb8.set_rgb_led(255, 0, 127, 0, False)
time.sleep(1)

print "goin turquoise...\n"
bb8.set_rgb_led(0, 255, 255, 0, False)
time.sleep(1)

print "disconnecting...\n"
bb8.join()
bb8.disconnect()
sys.exit(1)

