# weakgreeter is an IRC bot written in 2022, who knew IRC would still be in use?
# weakgreet requires beautifulsoup (https://pypi.org/project/beautifulsoup4/)
# and requests (https://pypi.org/project/requests/)
# and yfinance (https://pypi.org/project/yfinance/)
# and pytz (https://pypi.org/project/pytz/)
# and opencage (https://pypi.org/project/opencage/)
# and pyscopg2 (https://pypi.org/project/psycopg2/)

# Import modules needed to weakgreeter
from email.quoprimime import quote
from operator import contains
import socket
import time
from wsgiref import headers
import config
import random
import bs4
import requests
import re
import yfinance as yf
import psycopg2


# pull the variables from the config file
from config import *
from bs4 import BeautifulSoup
from numpy import empty, true_divide
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
    talk(random.choice(motivation) + " " + name.strip() + "!")
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


# Roll a die with the amount of sides defined by the user with the .roll command ".roll 6"
# Defaults to 6 if the input is invalid
def rollTheDice(dice, name):
    if (dice.strip()).isdigit() == True and dice.strip() != "0" and dice.strip() != "":
        valDice = random.randint(1, int(dice))
        talk(
            name
            + " "
            + "rolled a "
            + str(dice).strip()
            + " sided die. It has landed on "
            + str(valDice).strip()
            + "."
        )
        if valDice == 69:
            talk("Nice.")
            print(str(valDice) + " was rolled.")
        elif valDice == 420:
            talk("Blaze it.")
            print(str(valDice) + " was rolled.")
        else:
            print(str(valDice) + " was rolled.")
    else:
        dice = 6
        valDice = random.randint(1, dice)
        talk(
            name
            + " "
            + "rolled a "
            + str(dice).strip()
            + " sided die. It has landed on "
            + str(valDice).strip()
            + "."
        )
        if valDice == 69:
            talk("Nice.")
            print("Invalid input, rolled dice as a 6")
        elif valDice == 420:
            talk("Blaze it.")
            print("Invalid input, rolled dice as a 6")
        else:
            print("Invalid input, rolled dice as a 6")


# Grab a quote from the postgresql database, if the quote number is not specified pick a random quote
def quoteFetch(quote):
    if (
        (quote.strip()).isdigit() == True
        and quote.strip() != "0"
        and quote.strip() != ""
    ):
        con
        print("Database opened successfully")
        cur = con.cursor()
        print(int(quote))
        cur.execute("select quote from quotes where quote_id = (%s)", (quote,))
        quoteGot = cur.fetchone()
        print(quoteGot)
        if quoteGot == None:
            talk("Quote not found")
        else:
            quoteGot = [i for i in quoteGot]
            talk(str(quoteGot)[1:-1].strip("'"))
            cur.close()

    else:
        con
        print("Database opened successfully")
        cur = con.cursor()
        cur.execute("select quote from quotes order by RANDOM() limit 1;")
        quoteGot = cur.fetchone()
        print(quoteGot)
        quoteGot = [i for i in quoteGot]
        talk(str(quoteGot)[1:-1].strip("'"))
        cur.close()


# Add a new quote to the database with .addquote "string"
def addQuote(newQuote):
    if newQuote.strip() != "0" and newQuote.strip() != "":
        con
        print("Database opened successfully")
        cur = con.cursor()
        cur.execute("insert into quotes(quote) values (%s)", (newQuote.strip(),))
        cur.execute("SELECT quote FROM quotes ORDER BY quote_id DESC limit 1;")
        addedQuote = cur.fetchone()
        addedQuote = [i for i in addedQuote]
        talk("Added quote: " + (str(addedQuote)[1:-1].strip("'")))
        con.commit()
        cur.close()
    else:
        talk("Can't add that.")


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
                soup = BeautifulSoup(page.text, "lxml")
                talk(name + "'s link is: " + soup.title.string.replace('"', ""))
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
            # Look for the .time command and provide the time base on the location the user has specified
            elif message.find(".time") != -1:
                city = message = ircChat.split("PRIVMSG", 1)[1].split(".time", 1)[1]
                localTime(city)
            # Look for the .roll command and roll a die based on the amount of sides the user has specified
            elif message.find(".rtd") != -1:
                dice = message = ircChat.split("PRIVMSG", 1)[1].split(".rtd", 1)[1]
                rollTheDice(dice, name)
            elif message.find(".quote") != -1:
                quote = message = ircChat.split("PRIVMSG", 1)[1].split(".quote", 1)[1]
                quoteFetch(quote)
            elif message.find(".addquote") != -1:
                newQuote = message = ircChat.split("PRIVMSG", 1)[1].split(
                    ".addquote", 1
                )[1]
                addQuote(newQuote)
            # Provide a user with a command menu when they type .help
            elif message.find(".help") != -1:
                talk("Help Menu: .help returns a list of commands.")
                talk(
                    "Stock: .stock 'Ticker Symbol' i.e. '.stock TSLA' will provide you with a stock quote."
                )
                talk(
                    "Ask: .ask '.ask are cargo shorts cool', use or between choices for the bot to select a choice '.ask apple or orange'."
                )
                talk("Praise: .praise '.praise USERNAME'.")
                talk("Time: .time '.time Dublin, Ireland'.")
                talk("Roll the Dice: .rtd '.rtd 20' will roll a 20 sided die.")
                talk(
                    "Quotes: .quote pulls a random quote from the database, .quote 1 pulls quote 1 etc., .addquote '.addquote "
                    "Thrusty: HI GUYS"
                    "' will add that quote to the database."
                )
        # Respond to PINGs from the server as they appear
        else:
            if ircChat.find("PING :") != -1:
                ping()


main()
