FROM arm32v7/python:3.6-buster

RUN mkdir /home/airly
RUN mkdir /home/airly/data

COPY AirlyDownloader.py /home/airly/AirlyDownloader.py
COPY Collect_data.py /home/airly/Collect_data.py
COPY Airly_API_key.txt /home/airly/Airly_API_key.txt
COPY requirements.txt /home/airly/requirements.txt
COPY secretgc.json /home/data

WORKDIR /home/airly

RUN pip install -r /home/airly/requirements.txt

CMD ["python", "/home/airly/Collect_data.py"]
