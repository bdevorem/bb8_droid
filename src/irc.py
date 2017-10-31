import socket
import sys
 
class IRC:
    irc = socket.socket()
  
    def __init__(self):  
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
    def quit(self, channel, debug=False):
        if debug:
            print "quitting " + channel + "\n"
        self.irc.send("QUIT " + " :kbye...\r\n")

    def send(self, channel, msg, debug=False):
        if debug:
            print "sending \"" + msg + "\" to " + channel + "\n"
        self.irc.send("PRIVMSG " + channel + " :" + msg + "\r\n")
 
    def connect(self, server, channel, nick, password, debug=False):
        if debug:
            print "connecting to " + server
        # TODO: error check all this
        self.irc.connect((server, 6667))
        print "here"
        self.irc.send("PASS " + password + "\r\n") 
        self.irc.send("NICK " + nick + "\r\n")
        self.irc.send("USER " + nick + " " + server + " bb8 : " + nick + "\r\n") 
        self.irc.send("JOIN " + channel + "\r\n")
 
    def pong(self, buff, debug=False):
        if buff.find('PING') != -1:
            if debug:
                print "recieved " + buff + "\n"
                print "sending " + buff.split()[1] + "\n"
            self.irc.send('PONG ' + buff.split()[1] + '\r\n') 

    def recieve(self, debug=False):
        if debug:
            print "recieving..."
        buff = self.irc.recv(2040)
        self.pong(buff, debug)
        return buff
