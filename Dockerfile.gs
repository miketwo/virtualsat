FROM python:3.6

ENV TERM xterm-256color
ENV FLASK_APP=gs.py

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app

RUN wget "https://www.celestrak.com/NORAD/elements/starlink.txt"

ENTRYPOINT ["python3"]
CMD ["gs.py"]
