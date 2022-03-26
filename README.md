# weakgreeterIRCBot

A simple IRC bot written in Python.

# weakgreeter requires the following non standard modules:

-beautifulsoup (https://pypi.org/project/beautifulsoup4/) 

-requests (https://pypi.org/project/requests/)

-yfinance (https://pypi.org/project/yfinance/)

# Current Features:

-When a user says "Hi weakgreeter" weakgreeter will respond with a greeting in a random language

-When a user posts a URL in chat weakgreeter will read the webpage's title out in chat

- Commands:

- Stocks: .stock followed by a ticker symbol, weakgreeter will reply with the current price and the daily gain. ".stock FB"

- Ask: .ask followed by a question, weakgreeter will respond with a random answer to that question. Putting or between values will cause weakgreeter to select one of the values. ".ask go buy toilet paper" ".ask apples or oranges"

- Praise: .praise followed by a username, weakgreeter will respond to the listed user with a random message to praise them. ".praise username"

- Time: .time followed by a location, weakgreeter will respond with the local time of that location. ".time Toronto"

- Help: .help, weakgreeter will respond with the command menu
