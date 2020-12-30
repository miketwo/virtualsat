FROM python:3.6

ENV TERM xterm-256color

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app

RUN wget "https://www.celestrak.com/NORAD/elements/starlink.txt"

CMD bash
