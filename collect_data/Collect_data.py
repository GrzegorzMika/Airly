import AirlyDownloader
from pathlib import Path
from datetime import date
from google.cloud import storage
import pandas as pd
from io import StringIO
import logging
import time

logging.basicConfig(filename='/home/airly/data/log.log', level=logging.WARNING,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

API_key = Path('/home/airly/Airly_API_key.txt').read_text().split('\n')[0]

latitude = 50.061464
longitude = 19.938000
max_distance_km = 100


miner = AirlyDownloader.AirlyDownloader(API_key)
ids = miner.get_installations_ids_location(latitude, longitude, max_distance_km)
frames = []
for id in ids:
    start = time.time()
    try:
        frames.append(miner.measurement_installation_id(id, 'history'))
    except Exception as err:
        logger.error(err)
    end = time.time()
    elapsed = end - start
    time.sleep(max(0, 2 - elapsed))
data = pd.concat(frames)

f = StringIO()
data.to_csv(f, index_label=False)
f.seek(0)

storage_client = storage.Client.from_service_account_json('/home/data/secretgc.json')

bucket = storage_client.bucket('airly_data')
blob = bucket.blob(str(date.today()) + '.csv')

blob.upload_from_file(f, content_type='text/csv')

