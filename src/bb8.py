import socket
import time
import random
import sys
from irc import *
from bluepy import btle
import struct
import BB8_driver

FASTEST = 255
VERY_FAST = 210
FAST = 160
MEDIUM = 100
SLOW = 50
VERY_SLOW = 32
SLOWEST = 8

COLORS = {
        'red': (255, 0, 0, 0, False),
        'yellow': (255, 255, 0, 0, False),
        'blue': (0, 0, 255, 0, False),
        'green': (0, 255, 0, 0, False),
        'purple': (255, 0, 255, 0, False),
        'pink': (255, 0, 127, 0, False),
        'orange': (255, 127, 0, 0, False),
        'turquoise': (0, 255, 255, 0, False)}

class BB8:
    def __init__(self, irc, server, channel, nick, password, debug=False):  
        self.irc = irc
        self.server = server
        self.channel = channel
        self.nick = nick
        self.password = password
        self.debug = debug
        self.sphero = BB8_driver.Sphero()
        self.bt = False

    def connect(self, debug=False):
        self.irc.connect(self.server, self.channel, self.nick, self.password, debug)
        if debug:
            print "connecting to irc...\n"

    def bt_connect(self, debug=True):
        if self.bt == True:
            self.irc.send(self.channel, "failure!", debug)
        else:
            try:
                self.sphero.connect()
            except:
                self.irc.send(self.channel, "failure! Droid is powered down", debug)
                return

            if debug:
                print "connecting...\n"
            # self.sphero.start()
            self.bt = True
            self.irc.send(self.channel, "success!", debug)
            time.sleep(2)

    def bt_disconnect(self, debug=True):
        if self.bt == True:
            # self.sphero.join()
            self.sphero.disconnect()
            self.bt = False
            self.irc.send(self.channel, "success!", debug)
            if debug:
                print "disconnecting...\n"
        else:
            self.irc.send(self.channel, "failure!", debug)

    def change_color(self, color, debug=True):
        if self.bt == True:
            try:
                self.sphero.set_rgb_led(*COLORS[color])
                self.irc.send(self.channel, "success!", debug)
            except KeyError:
                self.irc.send(self.channel, "failure! try !listcolors", debug)
        else:
            self.irc.send(self.channel, "u gotta connect first u idiot", debug)

    def list_colors(self, debug=False):
        for k, v in COLORS.iteritems():
            self.irc.send(self.channel, k, debug)
    
    def turn(self, direction, debug=False):
        if self.bt == True:
            try:
                if direction == 'right':
                    for _ in xrange(5):
                        self.sphero.roll(150, 90, 1, True)
                        self.sphero.set_heading(90, True)
                        time.sleep(1)
                elif direction == 'left':
                    for _ in xrange(5):
                        self.sphero.roll(150, 270, 1, True)
                        self.sphero.set_heading(270, True)
                        time.sleep(1)
        else:
            self.irc.send(self.channel, "u gotta connect first u idiot", debug)

    def stop(self, debug=False):
        if self.bt == True:
            try:
                self.sphero.roll(0, 0, 0, True)
                time.sleep(.5)
        else:
            self.irc.send(self.channel, "u gotta connect first u idiot", debug)

    def _roll(self, speed, direction, duration, debug=False):
        self.sphero.roll(speed, direction, 1, True)
        time.sleep(duration)
        self.stop()

    def roll(self, speed=SLOW, duration=1.5, direction, debug=False):
        if self.bt == True:
            try:
                if direction == 'back':
                    self._roll(speed, 180, duration) # 180 for backwards
                elif direction == 'fwd':
                    self._roll(speed, 0, duration) # 0 for fwd
                elif direction == 'left':
                    self._roll(speed, 270, duration) # 270 left
                elif direction == 'right':
                    self._roll(speed, 90, duration) # 270 right
        else:
            self.irc.send(self.channel, "u gotta connect first u idiot", debug)

    def respond(self, buff, debug=False):
        if debug or self.debug:
            print "responding...\n"
            debug = True

        # TODO: create dictionary or yaml file of responses bc this is nasty
        if "PRIVMSG" in buff and self.channel in buff:
            if "hello" in buff and "bb8" in buff:
                self.irc.send(self.channel, "I'm working!", debug)
            elif "still there" in buff and "bb8" in buff:
                self.irc.send(self.channel, "YES!", debug)
            elif "goodnight" in buff and "bb8" in buff:
                self.irc.send(self.channel, "kbye...", debug)
                self.irc.quit(self.channel, debug)
                sys.exit(0)
            elif "favorite gender" in buff and "bb8" in buff:
                self.irc.send(self.channel, "no need to get political", debug)
            elif "favorite color" in buff and "bb8" in buff:
                self.irc.send(self.channel, "orange! or green like bdevorem", debug)
            elif "favorite video game" in buff and "bb8" in buff:
                self.irc.send(self.channel, "jeffrey tells me undertale is quite good", debug)
                self.irc.send(self.channel, "i also hear a lot of talk about clash of clans", debug)
            elif "@bb8" in buff:
                self.irc.send(self.channel, "u talkin to me bruh", debug)

            cmd = ''
            arg = ''
            try:
                cmd = buff.split()[3].replace(':', '')
                arg = buff.split()[4]
            except:
                pass

            if cmd.startswith('!'):

                if cmd == '!connect':
                    self.bt_connect()
                elif cmd == '!disconnect':
                    self.bt_disconnect()
                elif cmd == '!listcolors':
                    self.list_colors()
                elif cmd == '!color' and arg:
                    self.change_color(arg)
                elif cmd == '!forward':
                    self.roll(direction='fwd')
                elif cmd == '!backward':
                    self.roll(direction='back')
                elif cmd == '!right':
                    self.roll(direction='right')
                elif cmd == '!left':
                    self.roll(direction='left')
                elif cmd == '!turn':
                    num = randrange(0, 100)
                    if num < 50:
                        self.turn(direction='left')
                    else 
                        self.turn(direction='right')
                elif cmd == '!help':
                    self.irc.send(self.channel, "I can do the following...", debug)
                    cmds = "connect, disconnect, listcolors, color, forward, backward, right, left, turn"
                    self.irc.send(self.channel, cmds, debug)

