FROM python:3-onbuild
FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y \
	python3-pip

RUN mkdir /home/airly
RUN mkdir /home/airly/data

COPY Data_postprocessing.py /home/airly/Data_postprocessing.py
COPY requirements.txt /home/airly/requirements.txt

WORKDIR /home/airly

RUN pip3 install -r /home/airly/requirements.txt

EXPOSE 5000

CMD ["python3", "/home/airly/Data_postprocessing.py"]
