# Library to provide some simple controller functions for BB-8
# From https://github.com/jchadwhite/SpheroBB8-python

import pygame
import time
import BB8_driver

# Define arbitrary speeds
FASTEST = 255
VERY_FAST = 210
FAST = 160
MEDIUM = 100
SLOW = 50
VERY_SLOW = 32
SLOWEST = 8


class BB8Controller(object):
    """Simplified controller for BB-8"""

    def __init__(self):
        pygame.mixer.init()
#        pygame.mixer.music.load('sounds/connect.mp3')
#        pygame.mixer.music.play()

        self.bb8 = BB8_driver.Sphero()
        self.bb8.connect()
        self.bb8.start()
        time.sleep(2)
        self.flash_green(ntimes=2)

    def flash_color(self, color=(255, 255, 255), ntimes=3):
        """Flash light with given with 1 second intervals"""

        for _ in xrange(ntimes):
            self.bb8.set_rgb_led(color[0], color[1], color[2], 0, False)
            time.sleep(1)
            self.bb8.join()
            self.bb8.set_rgb_led(0, 0, 0, 0, False)
            time.sleep(1)
            self.bb8.join()

    def flash_red(self, ntimes=3):
        """Flash red light"""

        self.flash_color(color=(255, 0, 0), ntimes=ntimes)

    def flash_green(self, ntimes=3):
        """Flash green light"""

        self.flash_color(color=(0, 255, 0), ntimes=ntimes)

    def flash_blue(self, ntimes=3):
        """Flash blue light"""

        self.flash_color(color=(0, 0, 255), ntimes=ntimes)

    def turn_right(self):
        """Turn sphero right"""

        pygame.mixer.music.load('sounds/turn.mp3')
        pygame.mixer.music.play()
        time.sleep(1)
        
        for _ in xrange(5):
            self.bb8.roll(150, 90, 1, True)
            self.bb8.set_heading(90, True)
            time.sleep(.1)

    def turn_left(self):
        """Turn sphero left"""

        pygame.mixer.music.load('sounds/turn.mp3')
        pygame.mixer.music.play()
        time.sleep(1)

        for _ in xrange(5):
            self.bb8.roll(150, 270, 1, True)
            self.bb8.set_heading(270, True)
            time.sleep(.1)

    def displace(self, speed, direction, duration):
        """Move and stop"""

        pygame.mixer.music.load('sounds/roll.mp3')
        pygame.mixer.music.play()

        self.bb8.roll(speed, direction, 1, True)
        time.sleep(duration)
        self.bb8.join()
        self.stop()

    def stop(self):
        """Stop moving"""

        self.bb8.roll(0, 0, 0, True)
        time.sleep(.5)
        self.bb8.join()

    def go_forward(self, speed=SLOW, duration=1.5):
        """Move forward"""

        self.displace(speed, 0, duration)

    def go_back(self, speed=SLOW, duration=1.5):
        """Move back"""

        self.displace(speed, 180, duration)

    def go_right(self, speed=SLOW, duration=1.5):
        """Move right"""

        self.displace(speed, 90, duration)

    def go_left(self, speed=SLOW, duration=1.5):
        """Move left"""
        self.displace(speed, 270, duration)

    def disconnect(self):
        """Disconnect from BB-8"""
        pygame.mixer.music.load('sounds/disconnect.mp3')
        pygame.mixer.music.play()

        self.bb8.disconnect()
        time.sleep(2)
        self.bb8.join()

        print("Disconnected from BB-8")
