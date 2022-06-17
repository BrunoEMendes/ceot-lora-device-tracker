LHT65_FIELDS = {
    'battery (V)':'device_frmpayload_data_BatV',
    'humidity (%)':'device_frmpayload_data_Hum_SHT',
    'temperature (ºC)':'device_frmpayload_data_TempC_SHT',
    'illumination (lux)':'device_frmpayload_data_ILL_lux'
}

MAX_LHT65_DEVICES = 25


LSE01_FIELDS = {
    'battery (V)': 'device_frmpayload_data_Bat',
    'soil water content (%)': 'device_frmpayload_data_water_SOIL',
    'soil conductivity (uS/cm)': 'device_frmpayload_data_conduct_SOIL',
    'soil temperature (ºC)':'device_frmpayload_data_temp_SOIL'
}

MAX_LSE01_DEVICES = 6


SIGNAL_FIELDS = ['rssi', 'snr']

MEASUREMENT_OPTIONS = ['mean', 'max', 'min', 'median', 'stddev']


WS_FIELDS = {
    'temperature (ºC)': 'device_frmpayload_data_OUTSIDETEMPERATURE',
    'humidity (%)': 'device_frmpayload_data_OUTSIDEHUMIDITY',
    'solar radiation (W/m2)'  : 'device_frmpayload_data_SOLARADIATION',
    'pressure (hPa)'  : 'device_frmpayload_data_PRESSURE',
    'daily rain (mm/h)'   : 'device_frmpayload_data_DAYRAIN',
    'wind speed (m/s)' : 'device_frmpayload_data_WINDSPEED',
    'wind direction (º)'   : 'device_frmpayload_data_WINDDIRECTION',
    '10minavg_windspeed (m/s)'  : 'device_frmpayload_data_TENMINUTESAVGWINDSPEED',
}