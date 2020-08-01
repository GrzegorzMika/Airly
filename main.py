import logging
import os
import time
from datetime import date
from pathlib import Path

from Airly import AirlyDownloader
import pandas as pd
from Airly.utils import find, parse_main


def main():
    logdir, local_storage, max_distance_km, latitude, longitude = parse_main(find('setup_airly.json', '..'))
    API_key = Path(find('Airly_API_key.txt', '..')).read_text().split('\n')[0]

    logging.basicConfig(filename=logdir, level=logging.WARNING,
                        format='%(asctime)s %(levelname)s %(name)s %(message)s')
    logger = logging.getLogger(__name__)

    miner = AirlyDownloader.AirlyDownloader(API_key)
    ids = miner.get_installations_ids_location(latitude, longitude, max_distance_km)
    frames = []
    for i in ids:
        start = time.time()
        try:
            frames.append(miner.measurement_installation_id(i, 'history'))
        except Exception as err:
            logger.error(err)
        end = time.time()
        elapsed = end - start
        time.sleep(max(0, int(2 - elapsed) + 1))
        break
    data = pd.concat(frames)

    data.to_csv(os.path.join(local_storage, 'test_' + str(date.today()) + '.csv'), index_label=False)


if __name__ == '__main__':
    main()