FROM arm32v7/python:3.6-buster

RUN mkdir /home/airly
RUN mkdir /home/airly/data

COPY __init__.py /home/airly/__init__.py
COPY AirlyDownloader.py /home/airly/AirlyDownloader.py
COPY Collect_data.py /home/airly/Collect_data.py
COPY Airly_API_key.txt /home/airly/Airly_API_key.txt
COPY requirements.txt /home/airly/requirements.txt
COPY secretgc.json /home/airly/secretgc.json

WORKDIR /home/airly

RUN pip install -r requirements.txt

CMD ["python", "Collect_data.py"]
