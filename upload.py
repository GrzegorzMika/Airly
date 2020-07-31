from Airly.utils import parse_upload


def upload():
    logdir, local_storage, bucket, load_break, max_tries = parse_upload('setup.json')

