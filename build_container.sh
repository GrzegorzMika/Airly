docker build -t miner -f Dockerfile .
docker run --mount type=bind,source=/home/grzegorz/Pulpit/Projects/airly_data,target=/home/storage miner