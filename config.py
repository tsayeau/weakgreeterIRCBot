# Bot configurations and passwords to be sent to weakgreeter.py
import psycopg2

server = "server"  # IRC server address
port = 6667  # port number your IRC server uses
channel = "#channel"  # Channel you wish to join
botNickName = "weakgreeter"  # Bot's nickname
password = "password"  # password you use to authenticate against the server's nickserv (optional but recommended)

# Various greetings for weakgreeter to say when a user says hi to weakgreeter
greetings = [
    "Aloha 🌸 🌺",
    "Bonjour",
    "Hola",
    "Hi",
    "Konichiwa",
    "Hei",
    "Hello",
    "G'day",
    "Privet",
    "Ni Hao",
    "Guten tag",
]
# Various answers for the .ask function
answer = [
    "yes",
    "no",
    "maybe",
    "ask SlDeviant",
    "I don't think so",
    "that's a stupid question",
    "of course",
    "??????",
    "HELL YEAH",
    "👍💯💯💯💯",
]

# Various messages of praise for the .praise function
motivation = [
    "You're doing good Work,",
    "Great job,",
    "Awesome pics. Great size. Look thick. Solid. Tight. Keep us all posted on your continued progress with any new progress pics or vid clips. Show us what you got man. Wanna see how freakn' huge, solid, thick and tight you can get. Thanks for the motivation, ",
    "We did it,",
]
# Api key for https://opencagedata.com/ for .time command
key = ""

# connect string for the sql db
con = psycopg2.connect(
    host="", user="", password="", dbname=""
)
