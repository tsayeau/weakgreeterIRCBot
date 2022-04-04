# weakgreeterIRCBot

A simple IRC bot written in Python, using a PostgreSQL database.

# Current Features:

-When a user says "Hi weakgreeter" weakgreeter will respond with a greeting in a random language.

-When a user posts a URL in chat weakgreeter will display that webpage's title out in chat.


Commands:

- Stocks: .stock followed by a ticker symbol, weakgreeter will reply with the current price and the daily gain. ".stock FB".

- Ask: .ask followed by a question, weakgreeter will respond with a random answer to that question. Putting or between values will cause weakgreeter to select one of the values. ".ask go buy toilet paper" ".ask apples or oranges".

- Praise: .praise followed by a username, weakgreeter will respond to the listed user with a random message to praise them. ".praise username".

- Time: .time followed by a location, weakgreeter will respond with the local time of that location. ".time Toronto".

- Quote: .quote will pull a random quote from the database, .quote followed by a number will pull that specified quote from the database

- AddQuote: .addquote will add a new string of text to the quote database. ".addquote trefirefem: WE DID IT REDDIT!"

- Wiki: .wiki searchs wikipedia and provides a 2 sentance summary of the page. '.wiki Canada'.

- Help: .help, weakgreeter will respond with a link to the command menu.

# weakgreeter requires the following non standard modules:

-beautifulsoup (https://pypi.org/project/beautifulsoup4/) 

-requests (https://pypi.org/project/requests/)

-yfinance (https://pypi.org/project/yfinance/)

-pytz (https://pypi.org/project/pytz/)

-opencage (https://pypi.org/project/opencage/)

-psycopg2 (https://pypi.org/project/psycopg2/)

-wikipedia (https://pypi.org/project/wikipedia/)
