# weakgreeter is an IRC bot written in 2022, who knew IRC would still be in use?
# weakgreet requires beautifulsoup (https://pypi.org/project/beautifulsoup4/) 
# and requests (https://pypi.org/project/requests/)

# Import modules needed to weakgreeter
import socket
import time
import config
import random
import bs4
import requests
import re

# pull the variables from the config file
from config import *
from bs4 import BeautifulSoup

# Connect to IRC server and authenticate with nickserv
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((server, port))
irc.send(bytes("USER "+ botNickName +" "+ botNickName +" "+ botNickName + " " + "WeakGreeterIRCBOT" + "\n", "UTF-8"))
irc.send(bytes("NICK "+ botNickName +"\n", "UTF-8"))
irc.send(bytes('NICK ' + botNickName + '\r\n', "UTF-8"))
irc.send(bytes("NICKSERV IDENTIFY " + password + "\n", "UTF-8"))
# Join channel
def joinChannel(channel):
    ircChat = ""
    irc.send(bytes("JOIN "+ channel +"\n", "UTF-8"))
    ircChat = irc.recv(1024).decode("UTF-8")
    ircChat = ircChat.strip('\n\r')
    print(ircChat)

# Respond to IRC server pings and keep bot alive
def ping():
  irc.send(bytes("PONG \n", "UTF-8"))
  print("Pong sent!")
# Identify URLs in the IRC chat stream
def getUrl(string):
    
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string)      
    return [x[0] for x in url]
# Send messages to the IRC Channel
def talk(msg):
    irc.send(bytes("PRIVMSG "+ channel +" :"+ msg +"\n", "UTF-8"))

def main():
    joinChannel(channel)
    while 1:
        ircChat= ""
        ircChat = irc.recv(1024).decode("UTF-8")
        ircChat = ircChat.strip('\n\r')
        print(ircChat)

        if ircChat.find("PRIVMSG") != -1:
            # Grab user's nick and split from the rest of the message
            name = ircChat.split('!',1)[0][1:]
            # Grab user's message and split from nick
            message = ircChat.split('PRIVMSG',1)[1].split(':',1)[1]
            # If someone says hi don't be rude, say hi back!
            if message.find("Hi " + botNickName) and name == "trefirefem" != -1 or message.find("hi " + botNickName) and name == "trefirefem"!= -1:
                talk("Hei trefirefem! Have you got your dad strength yet, or do you still not bench 2pl8?")
            elif message.find("Hi " + botNickName) != -1 or message.find("hi " + botNickName) != -1:
                talk(random.choice(greetings) +" " + name)
            # Look for links in chat and use BeautifulSoup to get the title back
            elif message.find("https://") != -1:
                url = message = ircChat.split('PRIVMSG',1)[1].split(':',1)[1]
                page = requests.get((','.join(getUrl(url))))
                soup = BeautifulSoup(page.text, 'html.parser')
                for title in soup.find_all('title'):
                    talk(name +"'s link is: " + title.get_text())
        
        # Respond to PINGs from the server as they appear        
        else:
            if ircChat.find("PING :") != -1:
                ping()      
main()