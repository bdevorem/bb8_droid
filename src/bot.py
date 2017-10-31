#!/usr/bin/env python2

from irc import *
from bb8 import *
import os
import random
import yaml

config = yaml.load(open(".config.yaml"))
server = config["server"]
channel = config["channel"]
nick = config["nick"]
password = config["password"]

debug = False

if __name__ == '__main__':
    irc = IRC()
    bb8 = BB8(irc, server, channel, nick, password, debug)
    bb8.connect(debug)
     
    while True:
        buff = bb8.irc.recieve(debug)
        print buff
        bb8.respond(buff, debug)
     
