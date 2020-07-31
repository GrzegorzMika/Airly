import json
import os
import logging
import time
from io import StringIO
from datetime import date
from google.cloud import storage


def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


def parse_main(path):
    with open(path, 'r') as f:
        setup = json.load(f)

    logdir = os.path.join(setup.get('logdir', '.'), 'log.log')
    local_storage = setup.get('local_storage')
    max_distance_km = setup.get('max_distance_km')
    latitude = setup.get('latitude')
    longitude = setup.get('longitude')

    return logdir, local_storage, max_distance_km, latitude, longitude


def parse_upload(path):
    with open(path, 'r') as f:
        setup = json.load(f)

    logdir = os.path.join(setup.get('logdir', '.'), 'log.log')
    local_storage = setup.get('local_storage')
    bucket = setup.get('bucket')
    load_break = setup.get('load_break')
    max_tries = setup.get('max_tries')
    return logdir, local_storage, bucket, load_break, max_tries


def download(secret, path, bucket):
    storage_client = storage.Client.from_service_account_json(find(secret, '/home'))

    files = os.listdir(path)

    blobs = storage_client.list_blobs(bucket)
    for blob in blobs:
        if blob.name not in files:
            blob.download_to_filename(os.path.join(path, blob.name))


def upload(data, secret, load_break, max_tries):
    f = StringIO()
    data.to_csv(f, index_label=False)
    f.seek(0)

    for _ in range(max_tries):
        try:
            storage_client = storage.Client.from_service_account_json(find(secret, '/home'))
            bucket = storage_client.bucket('airly_data')
            blob = bucket.blob(str(date.today()) + '.csv')
            blob.upload_from_file(f, content_type='text/csv')
            break
        except Exception as err:
            logging.error(err)
            time.sleep(load_break)
