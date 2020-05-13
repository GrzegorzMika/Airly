FROM arm32v7/python:3.6-slim

RUN apt-get update

COPY requirements.txt /home/airly/requirements.txt

WORKDIR /home/airly

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "Collect_data.py"]
