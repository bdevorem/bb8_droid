import socket
import sys
from irc import *

class BB8:
  
    def __init__(self, irc, server, channel, nick, password, debug=False):  
        self.irc = irc
        self.server = server
        self.channel = channel
        self.nick = nick
        self.password = password
        self.debug = debug

    def connect(self, debug=False):
        self.irc.connect(self.server, self.channel, self.nick, self.password, debug)

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
            elif "bb8" in buff:
                self.irc.send(self.channel, "u talkin bout me bruh", debug)
            elif "@bb8" in buff:
                self.irc.send(self.channel, "u talkin to me bruh", debug)

 
