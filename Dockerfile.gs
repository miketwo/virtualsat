FROM python:3.9

ENV TERM xterm-256color
ENV FLASK_APP=gs.py

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app

EXPOSE 5001

ENV GS_NAME="STL GroundStation"
ENV GS_LATITUDE=38.6270
ENV GS_LONGITUDE=-90.1994

CMD ["python3", "gs.py"]
