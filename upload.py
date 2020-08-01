import logging
import os

import pandas as pd
from Airly.utils import parse_upload, find, upload_gcp, list_gcp_files, compare_files


def upload():
    logdir, local_storage, bucket_name, load_break, max_tries = parse_upload(find('setup_airly.json', '..'))

    secret = find('secretgc.json', '..')

    logging.basicConfig(filename=logdir, level=logging.WARNING,
                        format='%(asctime)s %(levelname)s %(name)s %(message)s')
    logger = logging.getLogger(__name__)

    gcp_list = list_gcp_files(bucket_name, secret)
    local_list = os.listdir(local_storage)
    data_list = compare_files(local_list, gcp_list)
    for data in data_list:
        upload_gcp(pd.read_csv(os.path.join(local_storage, data)), bucket_name, secret, load_break, max_tries)


if __name__ == '__main__':
    upload()
