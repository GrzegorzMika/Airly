import AirlyDownloader
from pathlib import Path
from datetime import date

API_key = Path('./Airly_API_key.txt').read_text().split('\n')[0]  # key to API obtained from https://developer.airly.eu/api

miner = AirlyDownloader.AirlyDownloader(API_key)  # connect and authorize access to API

miner.collect_measurements_in_location(latitude=50.061464, longitude=19.938000,
                                       max_distance_km=100, filename=str(date.today()) + '.csv')  # collect historical
# measurements around Cracow (latitude and longitude of Cracow main square) and up to 100 km from Cracow main square
# and save results to file with current date

# miner.get_all_installations(filename='installations.csv') # collect information about all installations and
# save results to file

# print(miner.measurement_installation_id(2339, 'current')) # print the current measurement for an installation on Wilenska
# street in Cracow
