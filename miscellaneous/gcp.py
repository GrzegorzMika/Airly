import os

from google.cloud import storage


def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


def download(secret, path, bucket):
    storage_client = storage.Client.from_service_account_json(find(secret, '/home'))

    files = os.listdir(path)

    blobs = storage_client.list_blobs(bucket)
    for blob in blobs:
        if blob.name not in files:
            blob.download_to_filename(os.path.join(path, blob.name))
