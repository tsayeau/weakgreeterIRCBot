FROM python:3

WORKDIR ./
COPY ["weakgreeter.py", "config.py", "requirements.txt", "./"]

RUN pip install -r requirements.txt

CMD python3 weakgreeter.py