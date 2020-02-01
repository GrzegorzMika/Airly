import asyncio
import aiohttp
import airly
import sys
import time
import pandas as pd


class AirlyDownloader:

    def __init__(self, key):
        self.key = key

    def __extract_data_installation(self, installation):
        """
        Function to collect infos for an installment in a robust way
        :param installation: coroutine representing an installment object returned by function load_installation_...
        :return: dictionary with data for a given installment
        """
        data = {
            'installation_id': installation['id'],
            'airly_sensor': installation['airly']
        }
        try:
            data['sponsor'] = installation['sponsor']['name']
        except:
            data['sponsor'] = 'None'
        try:
            data['elevation'] = installation['elevation']
        except:
            data['elevation'] = 'None'
        try:
            data['geolocation_latitude'] = installation['location']['latitude']
            data['geolocation_longitude'] = installation['location']['longitude']
        except:
            data['geolocation_longitude'] = 'None'
            data['geolocation_latitude'] = 'None'
        try:
            data['address_country'] = installation['address']['country']
            data['address_city'] = installation['address']['city']
            data['address_street'] = installation['address']['street']
            data['address_number'] = installation['address']['number']
        except:
            data['address_country'] = 'None'
            data['address_city'] = 'None'
            data['address_street'] = 'None'
            data['address_number'] = 'None'
        return data

    def __extract_data_measurement(self, measurement):
        """
        Function to collect measurements in a robust way
        :param measurement: coroutine representing a measurement object returned by function create_measurements_session_...
        :return: dictionary with a measurement data
        """
        data = {
            'start_date': measurement['fromDateTime'],
            'end_date': measurement['tillDateTime'],
            'air_quality_index_name': measurement['indexes'][0]['name'],
            'air_quality_index_value': measurement['indexes'][0]['value'],
            'air_quality_index_level': measurement['indexes'][0]['level'],
            'air_quality_index_desc': measurement['indexes'][0]['description'],
            'air_quality_index_advice': measurement['indexes'][0]['advice'],
            'air_quality_index_colour': measurement['indexes'][0]['color']
        }
        names = [measurement['values'][i]['name'] for i in range(0, len(measurement['values']))]
        try:
            pos = names.index('PM1')
            data['PM1'] = measurement['values'][pos]['value']
        except:
            data['PM1'] = 'None'
        try:
            pos = names.index('PM25')
            data['PM25'] = measurement['values'][pos]['value']
        except:
            data['PM25'] = 'None'
        try:
            pos = names.index('PM10')
            data['PM10'] = measurement['values'][pos]['value']
        except:
            data['PM10'] = 'None'
        try:
            pos = names.index('PRESSURE')
            data['Pressure'] = measurement['values'][pos]['value']
        except:
            data['Pressure'] = 'None'
        try:
            pos = names.index('HUMIDITY')
            data['Humidity'] = measurement['values'][pos]['value']
        except:
            data['Humidity'] = 'None'
        try:
            pos = names.index('TEMPERATURE')
            data['Temperature'] = measurement['values'][pos]['value']
        except:
            data['Temperature'] = 'None'
        try:
            pos = names.index('NO2')
            data['NO2'] = measurement['values'][pos]['value']
        except:
            data['NO2'] = 'None'
        try:
            pos = names.index('CO')
            data['CO'] = measurement['values'][pos]['value']
        except:
            data['CO'] = 'None'
        try:
            pos = names.index('O3')
            data['O3'] = measurement['values'][pos]['value']
        except:
            data['O3'] = 'None'
        try:
            pos = names.index('SO2')
            data['SO2'] = measurement['values'][pos]['value']
        except:
            data['SO2'] = 'None'
        return data

    async def __installation_async(self, installation_id):
        """
        Private function to retrieve information about a specific installation by given installation_id
        :param installation_id: int representing the indicator of installation
        :return: pandas DataFrame with installation infos (coroutine)
        """
        async with aiohttp.ClientSession() as http_session:
            airly_api = airly.Airly(self.key, http_session)
            installation = await airly_api.load_installation_by_id(installation_id)
            data = self.__extract_data_installation(installation)
            data = pd.DataFrame(data, index=[0])
        return data

    def installation(self, installation_id, filename=None):
        """
        Wrapper for installation_async function to perform coroutine
        :param installation_id: int representing the indicator of installation
        :param filename: if not none, string representing the (path + ) filename to save the info
        :return: pandas DataFrame with installation infos
        """
        loop = asyncio.get_event_loop()
        data = loop.run_until_complete(self.__installation_async(installation_id))
        #data = asyncio.run(self.__installation_async(installation_id))
        if filename is not None:
            data.to_csv(filename)
        return data

    async def __installations_nearest_async(self, latitude, longitude, max_distance_km, max_results):
        """
        Private function to retrieve the information about available installations around given location within given
        distance and limited to a given number of results
        :param latitude: float representing latitude of location
        :param longitude: float representing a longitude of location
        :param max_distance_km: float representing maximal distance within which to look for installations
        :param max_results: int representing maximal number of results to be returned
        :return: pandas DataFrame with the installations infos (coroutine)
        """
        async with aiohttp.ClientSession() as http_session:
            airly_api = airly.Airly(self.key, http_session)
            sys.stdout.flush()
            installation_list = await airly_api.load_installation_nearest(latitude=latitude, longitude=longitude,
                                                                          max_distance_km=max_distance_km,
                                                                          max_results=max_results)
            sys.stdout.flush()
            installation_ids = [loc['id'] for loc in installation_list]
            data = {}
            for installation_id in range(0, len(installation_ids)):
                data[installation_id] = []
                data[installation_id].append(self.__extract_data_installation(installation_list[installation_id]))
            data = pd.concat([pd.DataFrame(data[i]) for i in data]).reset_index(drop=True)
        return data

    def installations_nearest(self, latitude, longitude, max_distance_km=1, max_results=-1, filename=None):
        """
        Wrapper function for function installations_nearest_async to perform coroutine
        :param latitude: float representing latitude of location
        :param longitude: float representing a longitude of location
        :param max_distance_km: float representing maximal distance within which to look for installations
        :param max_results: int representing maximal number of results to be returned
        :param filename: if not none, string representing the (path + ) filename to save the info
        :return: pandas DataFrame with the installations infos
        """
        loop = asyncio.get_event_loop()
        data = loop.run_until_complete(self.__installations_nearest_async(latitude, longitude, max_distance_km, max_results))
        # data = asyncio.run(self.__installations_nearest_async(latitude, longitude, max_distance_km, max_results))
        if filename is not None:
            data.to_csv(filename)
        return data

    async def __measurement_installation_id_async_current(self, installation_id):
        """
        Private function to get current measurement for an installation with a given installation_id
        :param installation_id: int representing an installation ID
        :return: pandas DataFrame with measurement (coroutine)
        """
        async with aiohttp.ClientSession() as http_session:
            airly_api = airly.Airly(self.key, http_session)
            measurement = airly_api.create_measurements_session_installation(installation_id)
            sys.stdout.flush()
            await measurement.update()
            sys.stdout.flush()
            current = measurement.current
            data = self.__extract_data_measurement(current)
            data = pd.DataFrame(data, index=[0])
        return data

    async def __measurement_installation_id_async_history(self, installation_id):
        """
        Private function to get measurements for a last 24 hour (historical) for an installation with a given installation_id
        :param installation_id: int representing an installation ID
        :return: pandas DataFrame with measurement (coroutine)
        """
        async with aiohttp.ClientSession() as http_session:
            airly_api = airly.Airly(self.key, http_session)
            measurement = airly_api.create_measurements_session_installation(installation_id)
            sys.stdout.flush()
            await measurement.update()
            sys.stdout.flush()
            history = measurement.history
            data = {}
            for i in range(0, 24):
                data[i] = []
                data[i].append(self.__extract_data_measurement(history[i]))
            data = pd.concat([pd.DataFrame(data[i]) for i in data]).reset_index(drop=True)
        return data

    async def __measurement_installation_id_async_forecast(self, installation_id):
        """
        Private function to get measurements for a next 24 hours (forecast) for an installation with a given installation_id
        :param installation_id: int representing an installation ID
        :return: pandas DataFrame with measurement (coroutine)
        """
        async with aiohttp.ClientSession() as http_session:
            airly_api = airly.Airly(self.key, http_session)
            measurement = airly_api.create_measurements_session_installation(installation_id)
            sys.stdout.flush()
            await measurement.update()
            sys.stdout.flush()
            forecast = measurement.forecast
            data = {}
            for i in range(0, 24):
                data[i] = []
                data[i].append(self.__extract_data_measurement(forecast[i]))
            data = pd.concat([pd.DataFrame(data[i]) for i in data]).reset_index(drop=True)
        return data

    def measurement_installation_id(self, installation_id, measurement_type, filename=None):
        """
        Wrapper function for functions measurement_installation_id_async_current,
        measurement_installation_id_async_history and measurement_installation_id_async_forecast to retrieve
        (respectively) current, historical or forecasted measurements for an installation with a given ID
        :param installation_id: int representing installation ID
        :param measurement_type: string representing a requested measurement type;
        possible values: current, history, forecast
        :param filename: if not none, string representing the (path + ) filename to save the info
        :return: pandas DataFrame with the measurement info
        """
        loop = asyncio.get_event_loop()
        if measurement_type == 'current':
            data = loop.run_until_complete(self.__measurement_installation_id_async_current(installation_id))
            # data = asyncio.run(self.__measurement_installation_id_async_current(installation_id))
        elif measurement_type == 'history':
            data = loop.run_until_complete(self.__measurement_installation_id_async_history(installation_id))
            # data = asyncio.run(self.__measurement_installation_id_async_history(installation_id))
        elif measurement_type == 'forecast':
            data = loop.run_until_complete(self.__measurement_installation_id_async_forecast(installation_id))
            # data = asyncio.run(self.__measurement_installation_id_async_forecast(installation_id))
        else:
            raise Exception('Wrong type of measurement!')
        data['installation_id'] = installation_id
        if filename is not None:
            data.to_csv(filename)
        return data

    async def __measurement_nearest_async_current(self, latitude, longitude, max_distance_km):
        """
        Private function to retrieve current measurement for an installation closest to the given coordinates
        :param latitude: float representing the latitude of a given location
        :param longitude: float representing the longitude of a given location
        :param max_distance_km: float representing the maximal range (in KM) to look for an installation
        :return: pandas DataFrame with measurements (coroutine)
        """
        async with aiohttp.ClientSession() as http_session:
            airly_api = airly.Airly(self.key, http_session)
            measurement = airly_api.create_measurements_session_nearest(latitude, longitude, max_distance_km)
            sys.stdout.flush()
            await measurement.update()
            sys.stdout.flush()
            current = measurement.current
            data = self.__extract_data_measurement(current)
            data = pd.DataFrame(data, index=[0])
        return data

    async def __measurement_nearest_async_history(self, latitude, longitude, max_distance_km):
        """
        Private function to retrieve measurements for a last 24 hours (historical) for an installation closest
        to the given coordinates
        :param latitude: float representing the latitude of a given location
        :param longitude: float representing the longitude of a given location
        :param max_distance_km: float representing the maximal range (in KM) to look for an installation
        :return: pandas DataFrame with measurements (coroutine)
        """
        async with aiohttp.ClientSession() as http_session:
            airly_api = airly.Airly(self.key, http_session)
            measurement = airly_api.create_measurements_session_nearest(latitude, longitude, max_distance_km)
            sys.stdout.flush()
            await measurement.update()
            sys.stdout.flush()
            history = measurement.history
            data = {}
            for i in range(0, 24):
                data[i] = []
                data[i].append(self.__extract_data_measurement(history[i]))
            data = pd.concat([pd.DataFrame(data[i]) for i in data]).reset_index(drop=True)
        return data

    async def __measurement_nearest_async_forecast(self, latitude, longitude, max_distance_km):
        """
        Private function to retrieve measurements for a next 24 hours (forecast) for an installation closest
        to the given coordinates
        :param latitude: float representing the latitude of a given location
        :param longitude: float representing the longitude of a given location
        :param max_distance_km: float representing the maximal range (in KM) to look for an installation
        :return: pandas DataFrame with measurements (coroutine)
        """
        async with aiohttp.ClientSession() as http_session:
            airly_api = airly.Airly(self.key, http_session)
            measurement = airly_api.create_measurements_session_nearest(latitude, longitude, max_distance_km)
            sys.stdout.flush()
            await measurement.update()
            sys.stdout.flush()
            forecast = measurement.forecast
            data = {}
            for i in range(0, 24):
                data[i] = []
                data[i].append(self.__extract_data_measurement(forecast[i]))
            data = pd.concat([pd.DataFrame(data[i]) for i in data]).reset_index(drop=True)
        return data

    def measurement_nearest(self, latitude, longitude, measurement_type, max_distance_km=3, filename=None):
        """
        Wrapper function for functions measurement_nearest_async_current, measurement_nearest_async_history and
        measurement_nearest_async_forecast to retrieve (respectively) current, historical and forecasted measurements for
        a installation closest to the given coordinates (and within given range)
        :param latitude: float representing the latitude of a given location
        :param longitude: float representing the longitude of a given location
        :param measurement_type: string representing a requested measurement type;
        possible values: current, history, forecast
        :param max_distance_km: float representing the maximal range (in KM) to look for an installation
        :param filename: if not none, string representing the (path + ) filename to save the info
        :return: pandas DataFrame with the measurements info
        """
        loop = asyncio.get_event_loop()
        if measurement_type == 'current':
            data = loop.run_until_complete(self.__measurement_nearest_async_current(latitude, longitude, max_distance_km))
            # data = asyncio.run(self.__measurement_nearest_async_current(latitude, longitude, max_distance_km))
        elif measurement_type == 'history':
            data = loop.run_until_complete(self.__measurement_nearest_async_history(latitude, longitude, max_distance_km))
            # data = asyncio.run(self.__measurement_nearest_async_history(latitude, longitude, max_distance_km))
        elif measurement_type == 'forecast':
            data = loop.run_until_complete(self.__measurement_nearest_async_forecast(latitude, longitude, max_distance_km))
            # data = asyncio.run(self.__measurement_nearest_async_forecast(latitude, longitude, max_distance_km))
        else:
            raise Exception('Wrong type of measurement!')
        if filename is not None:
            data.to_csv(filename)
        return data

    async def __measurement_location_async_current(self, latitude, longitude):
        """
        Private function to retrieve a current and interpolated measurement for a given coordinates
        :param latitude: float representing the latitude of a given location
        :param longitude: float representing a longitude of a given location
        :return: pandas DataFrame with measurement info (coroutine)
        """
        async with aiohttp.ClientSession() as http_session:
            airly_api = airly.Airly(self.key, http_session)
            measurement = airly_api.create_measurements_session_point(latitude, longitude)
            sys.stdout.flush()
            await measurement.update()
            sys.stdout.flush()
            current = measurement.current
            data = self.__extract_data_measurement(current)
            data = pd.DataFrame(data, index=[0])
        return data

    async def __measurement_location_async_history(self, latitude, longitude):
        """
        Private function to retrieve interpolated measurements for a last 24 hours (historical) for a given coordinates
        :param latitude: float representing the latitude of a given location
        :param longitude: float representing a longitude of a given location
        :return: pandas DataFrame with measurement info (coroutine)
        """
        async with aiohttp.ClientSession() as http_session:
            airly_api = airly.Airly(self.key, http_session)
            measurement = airly_api.create_measurements_session_point(latitude, longitude)
            sys.stdout.flush()
            await measurement.update()
            sys.stdout.flush()
            history = measurement.history
            data = {}
            for i in range(0, 24):
                data[i] = []
                data[i].append(self.__extract_data_measurement(history[i]))
            data = pd.concat([pd.DataFrame(data[i]) for i in data]).reset_index(drop=True)
        return data

    async def __measurement_location_async_forecast(self, latitude, longitude):
        """
        Private function to retrieve interpolated measurements for a nest 24 hours (forecast) for a given coordinates
        :param latitude: float representing the latitude of a given location
        :param longitude: float representing a longitude of a given location
        :return: pandas DataFrame with measurement info (coroutine)
        """
        async with aiohttp.ClientSession() as http_session:
            airly_api = airly.Airly(self.key, http_session)
            measurement = airly_api.create_measurements_session_point(latitude, longitude)
            sys.stdout.flush()
            await measurement.update()
            sys.stdout.flush()
            forecast = measurement.forecast
            data = {}
            for i in range(0, 24):
                data[i] = []
                data[i].append(self.__extract_data_measurement(forecast[i]))
            data = pd.concat([pd.DataFrame(data[i]) for i in data]).reset_index(drop=True)
        return data

    def measurement_location(self, latitude, longitude, measurement_type, filename=None):
        """
        Wrapper function for functions measurement_location_async_current, measurement_location_async_history and
        measurement_location_async_forecast to retrieve (respectively) current, historical and forecasted interpolated
        measurements for a given location
        :param latitude: float representing the latitude of a given location
        :param longitude: float representing a longitude of a given location
        :param measurement_type: string representing a requested measurement type;
        possible values: current, history, forecast
        :param filename: if not none, string representing the (path + ) filename to save the info
        :return: pandas DataFrame with the measurements infos
        """
        loop = asyncio.get_event_loop()
        if measurement_type == 'current':
            data = loop.run_until_complete(self.__measurement_location_async_current(latitude, longitude))
            # data = asyncio.run(self.__measurement_location_async_current(latitude, longitude))
        elif measurement_type == 'history':
            data = loop.run_until_complete(self.__measurement_location_async_history(latitude, longitude))
            # data = asyncio.run(self.__measurement_location_async_history(latitude, longitude))
        elif measurement_type == 'forecast':
            data = loop.run_until_complete(self.__measurement_location_async_forecast(latitude, longitude))
            # data = asyncio.run(self.__measurement_location_async_forecast(latitude, longitude))
        else:
            raise Exception('Wrong type of measurement!')
        if filename is not None:
            data.to_csv(filename)
        return data

    def get_installation_ids(self):
        """
        Get list of IDs of all available Airly and non-Airly installations
        :return: list with IDs
        """
        loop = asyncio.get_event_loop()
        data = loop.run_until_complete(self.__installations_nearest_async(0, 0, 40000, -1))
        # data = asyncio.run(self.__installations_nearest_async(0, 0, 40000, -1))
        return data['installation_id'].tolist()

    def get_all_installations(self, filename=None):
        """
        Get infos about all available Airly and non-Airly installations
        :param filename: if not none, string representing the (path + ) filename to save the info
        :return: pandas DataFrame with infos about installations
        """
        loop = asyncio.get_event_loop()
        data = loop.run_until_complete(self.__installations_nearest_async(0, 0, 40000, -1))
        # data = asyncio.run(self.__installations_nearest_async(0, 0, 40000, -1))
        if filename is not None:
            data.to_csv(filename)
        return data

    def get_installations_ids_location(self, latitude, longitude, max_distance_km):
        """
        Get a list IDs of all Airly and non-Airly installations around given location
        :param latitude: float representing a latitude of a given location
        :param longitude: float representing longitude of a given location
        :param max_distance_km: maximal range (in KM) within which to look for installations
        :return: list with IDs
        """
        loop = asyncio.get_event_loop()
        data = loop.run_until_complete(self.__installations_nearest_async(latitude, longitude, max_distance_km, -1))
        # data = asyncio.run(self.__installations_nearest_async(latitude, longitude, max_distance_km, -1))
        return data['installation_id'].tolist()

    def collect_measurements(self, filename=None):
        """
        Collect historical (last 24 hours) measurements for all available installations (maximal number of API requests
        per day is 1000)
        :param filename: if not none, string representing the (path + ) filename to save the info
        :return: pandas DataFrame with the measurements
        """
        ids = self.get_installation_ids()
        frames = []
        for id in ids:
            print(str(id))
            start = time.time()
            frames.append(self.measurement_installation_id(id, 'history'))
            end = time.time()
            elapsed = end - start
            time.sleep(max(0, 2 - elapsed))
        data = pd.concat(frames)
        if filename is not None:
            data.to_csv(filename)
        return data

    def collect_measurements_in_location(self, latitude, longitude, max_distance_km, filename=None):
        """
        Collect historical (last 24 hours) measurements for all installations within a given range from a given coordinates
        :param latitude: float representing a latitude of a given location
        :param longitude: float representing longitude of a given location
        :param max_distance_km: maximal range (in KM) within which to look for installations
        :param filename: if not none, string representing the (path + ) filename to save the info
        :return: pandas DataFrame with the measurements
        """
        ids = self.get_installations_ids_location(latitude, longitude, max_distance_km)
        frames = []
        for id in ids:
            print(str(id))
            start = time.time()
            frames.append(self.measurement_installation_id(id, 'history'))
            end = time.time()
            elapsed = end - start
            time.sleep(max(0, 2 - elapsed))
        data = pd.concat(frames)
        if filename is not None:
            data.to_csv(filename)
        return data
