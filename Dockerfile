FROM python:3.6-buster

RUN apt-get update

COPY Airly/requirements.txt /home/Airly/requirements.txt

RUN pip install -r /home/Airly/requirements.txt

RUN mkdir /home/storage
RUN mkdir /home/logdir

WORKDIR /home

COPY . .

ENTRYPOINT ["python",  "-m", "Airly.main"]
