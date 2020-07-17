import json
import logging
import time
import pandas as pd
from .AirlyDownloader import AirlyDownloader
from .utils import find, upload


def mine(API_key, latitude, longitude, max_distance_km):
    miner = AirlyDownloader(API_key)
    ids = miner.get_installations_ids_location(latitude, longitude, max_distance_km)
    frames = []
    for i in ids:
        start = time.time()
        try:
            frames.append(miner.measurement_installation_id(i, 'history'))
        except Exception as err:
            logging.error(err)
        end = time.time()
        elapsed = end - start
        time.sleep(max(0, int(2 - elapsed) + 1))
    data = pd.concat(frames)
    return data


def main():
    logging.basicConfig(filename='/home/airly/data/log.log', level=logging.WARNING,
                        format='%(asctime)s %(levelname)s %(name)s %(message)s')
    logger = logging.getLogger(__name__)

    with open(find('Airly_API_key.json', '/')) as f:
        key = json.load(f)

    API_key = key.get('key')

    latitude = 50.061464
    longitude = 19.938000
    max_distance_km = 100
    max_tries = 12
    load_break = 15 * 60

    data = mine(API_key, latitude, longitude, max_distance_km)
    upload(data, 'secretgc.json', load_break, max_tries)
