# weakgreeter is an IRC bot written in 2022, who knew IRC would still be in use?
# weakgreet requires beautifulsoup (https://pypi.org/project/beautifulsoup4/)
# and requests (https://pypi.org/project/requests/)
# and yfinance (https://pypi.org/project/yfinance/)

# Import modules needed to weakgreeter
import socket
import time
import config
import random
import bs4
import requests
import re
import yfinance as yf


# pull the variables from the config file
from config import *
from bs4 import BeautifulSoup
from numpy import empty
from datetime import datetime
from pytz import timezone
from opencage.geocoder import OpenCageGeocode
from ast import Return

# Connect to IRC server and authenticate with nickserv
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((server, port))
irc.send(
    bytes(
        "USER "
        + botNickName
        + " "
        + botNickName
        + " "
        + botNickName
        + " "
        + "weakGreeterIRCBOT"
        + "\n",
        "UTF-8",
    )
)
irc.send(bytes("NICK " + botNickName + "\n", "UTF-8"))
irc.send(bytes("NICK " + botNickName + "\r\n", "UTF-8"))
irc.send(bytes("NICKSERV IDENTIFY " + password + "\n", "UTF-8"))
# Join channel
def joinChannel(channel):
    ircChat = ""
    irc.send(bytes("JOIN " + channel + "\n", "UTF-8"))
    ircChat = irc.recv(1024).decode("UTF-8")
    ircChat = ircChat.strip("\n\r")
    print(ircChat)


# Respond to IRC server pings and keep bot alive
def ping():
    irc.send(bytes("PONG \n", "UTF-8"))
    print("Pong sent!")


# Identify URLs in the IRC chat stream
def getUrl(string):

    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    return [x[0] for x in url]


# Send messages to the IRC Channel
def talk(msg):
    irc.send(bytes("PRIVMSG " + channel + " :" + msg + "\n", "UTF-8"))


# Provide stock quotes to the IRC Channel
def stockMarket(quote):
    stock = yf.Ticker(str(quote))
    today = stock.history(period="1d")
    currentPrice = today["Close"]
    if currentPrice.empty != 1:
        today = stock.history(period="1d")
        yesterday = stock.history(period="2d")
        currentPrice = today["Close"][0]
        openPrice = yesterday["Close"][0]
        companyName = stock.info["shortName"]
        dailyGrowth = (float(currentPrice) - float(openPrice)) / float(openPrice) * 100
        talk(
            quote
            + ", "
            + companyName
            + " "
            + "Current Price: "
            + str((round(float(currentPrice), 2)))
            + " "
            + "Daily Gain: "
            + str((round(float(dailyGrowth), 2)))
            + " %"
        )
        print("Stock was found, sending to IRC Channel")
    else:
        talk("idk that stock u paper handed fool")
        print("Stock not found")
    Return(quote)


# If a user asks a question with .ask weakgreeter will respond with a random answer in the config.py file
# If a user asks a question with multiple values weakgreeter will randomize the values and spit out an answer
def ask(name, question):
    if " or " in question:
        question = re.split(r"or", question)
        talk(random.choice(question) + " " + name.strip())
        print("Choice made and sent to " + name.strip())
    else:
        talk(random.choice(answer) + " " + name.strip())
        print("Random answer sent to " + name.strip())


# Praise the user selected by the person running the command with a random message of praise in the config.py file
def praise(name):
    talk(random.choice(motivation) + name.strip() + "!")
    print("Praise sent to " + name.strip())


# Get the time of a city specificed by the user running the .time command
# uses api key in config.py for https://opencagedata.com/
# Grabs the users location and outputs the timezone
def localTime(city):
    geocoder = OpenCageGeocode(key)
    results = geocoder.geocode(city)
    if results != []:
        tzString = timezone(results[0]["annotations"]["timezone"]["name"])
        tzString = datetime.now(tzString)
        onlyCity = city.split(",")
        city = onlyCity[0]
        talk("The time in " + city.strip() + " is " + tzString.strftime("%H:%M."))
        print("Local time sent for " + city.strip())
    else:
        talk("Sorry, can't find " + city.strip())
        print("Local time not found  for " + city.strip())


def main():
    joinChannel(channel)
    while 1:
        ircChat = ""
        ircChat = irc.recv(1024).decode("UTF-8")
        ircChat = ircChat.strip("\n\r")
        print(ircChat)

        if ircChat.find("PRIVMSG") != -1:
            # Grab user's nick and split from the rest of the message
            name = ircChat.split("!", 1)[0][1:]
            # Grab user's message and split from nick
            message = ircChat.split("PRIVMSG", 1)[1].split(":", 1)[1]
            # If someone says hi don't be rude, say hi back!
            if (
                message.find("Hi " + botNickName) != -1
                and name == "trefirefem" != -1
                or message.find("hi " + botNickName) != -1
                and name == "trefirefem" != -1
            ):
                talk(
                    "Hei trefirefem! Have you got your dad strength yet, or do you still not bench 2pl8?"
                )
                print("Greeting sent to trefirefem")
            elif (
                message.find("Hi " + botNickName) != -1
                or message.find("hi " + botNickName) != -1
            ):
                talk(random.choice(greetings) + " " + name)
                print("Greeting sent to " + name)

            # Look for links in chat and use BeautifulSoup to get the title back
            elif message.find("https://") != -1:
                url = message = ircChat.split("PRIVMSG", 1)[1].split(":", 1)[1]
                page = requests.get((",".join(getUrl(url))))
                soup = BeautifulSoup(page.text, "html.parser")
                for title in soup.find_all("title"):
                    talk(name + "'s link is: " + title.get_text())
                print("URL title sent")

            # Look for stock quotes using the .stock command
            elif message.find(".stock") != -1:
                stonk = message = ircChat.split("PRIVMSG", 1)[1].split(".stock", 1)[1]
                stockMarket(stonk.lstrip())
            # Look for the .ask command and respond
            elif message.find(".ask") != -1:
                question = message = ircChat.split("PRIVMSG", 1)[1].split(".ask", 1)[1]
                ask(name, question)
            # Look for the .praise command and praise the users specified
            elif message.find(".praise") != -1:
                name = message = ircChat.split("PRIVMSG", 1)[1].split(".praise", 1)[1]
                praise(name)
            elif message.find(".time") != -1:
                city = message = ircChat.split("PRIVMSG", 1)[1].split(".time", 1)[1]
                localTime(city)
        # Respond to PINGs from the server as they appear
        else:
            if ircChat.find("PING :") != -1:
                ping()


main()
