from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly
import plotly.express as px

import pandas as pd
import pathlib
from app import app
import datetime

from .modules.device import DeviceProfile, Device
from datetime import datetime
from .modules.client import Client
import config as config
import secret


START = int(datetime(2022,3,12,7,30,0, tzinfo=None).timestamp())






layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                list(config.LHT65_FIELDS.keys()),
                list(config.LHT65_FIELDS.keys())[0],
                id='xaxis-column'
            ),
        ], style={'width': '48%', 'display': 'inline-block'}),

    ]),

    dcc.Graph(id='indicator-graphic'),

    # dcc.Slider(
    #     df['Year'].min(),
    #     df['Year'].max(),
    #     step=None,
    #     id='year--slider',
    #     value=df['Year'].max(),
    #     marks={str(year): str(year) for year in df['Year'].unique()},
    # )
])



@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('xaxis-column', 'value'),
    # Input('yaxis-column', 'value'),
    # Input('xaxis-type', 'value'),
    # Input('yaxis-type', 'value')
    # Input('year--slider', 'value')
    )
def update_graph(xaxis_column_name):
    client = Client(secret.server, secret.port, secret.token, secret.org).client()
    dp = DeviceProfile('LHT65', config.LHT65_FIELDS)
        
    device = Device('L1', dp, client, 'Arvores')
    df = device.query_field(xaxis_column_name, START)

    # dff = df[df['Year'] == year_value]
    # dff = back_up(ORG, 'Arvores', START, LHT65_MEAS_FIELDS, SIGNAL_FIELDS, ['time', 'bat', 'hum', 'tmp', 'ill'], MAX_LHT65_DEVICES, 'L')
    # print(type(dff['time'][0]), dff['time'][0])

    fig = px.line(df, x='time', y=xaxis_column_name)

    # fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    # fig.update_xaxes(title=xaxis_column_name,
    #                  type='linear' if xaxis_type == 'Linear' else 'log')

    # fig.update_yaxes(title=yaxis_column_name,
    #                  type='linear' if yaxis_type == 'Linear' else 'log')

    return fig






##################################################################
# client = InfluxDBClient(host='23.88.101.43', port=8486)
from influxdb_client import InfluxDBClient
import pandas as pd
from datetime import datetime
import os
import csv
import urllib3
import certifi


MAX_LHT65_DEVICES = 25
MAX_LSE01_DEVICES = 6
ORG = 'ceot'


INFLUX_FIELDS = ['FIELD', 'MEASUREMENT', 'START', 'STOP', 'TIME', 'VALUE']

START = int(datetime(2022,3,12,7,30,0, tzinfo=None).timestamp())


http = urllib3.PoolManager(
    cert_reqs="CERT_REQUIRED",
    ca_certs=certifi.where()
)
resp = http.request('GET', 'https://us-west-2-1.aws.cloud2.influxdata.com/ping')


client = InfluxDBClient(url='https://23.88.101.43:8086', token='HQuhjRudPv_fmY-tEvCvaPapbKL4paqydZUdxgTELMjWok3NHpDlpGDPzNgisAUz1nonYbg96ClO5CDgLS9HcQ==', org='ceot',
    ssl_ca_cert=certifi.where(), 
    verify_ssl=False
)

# script='''from(bucket: "Arvores")
#   |> range(start:-100d)
#   |> filter(fn: (r) => r["device_name"] == "L1")
#   |> filter(fn: (r) => r["_measurement"] == "device_frmpayload_data_BatV" or r["_measurement"] == "device_frmpayload_data_Ext_sensor" or r["_measurement"] == "device_frmpayload_data_Hum_SHT" or r["_measurement"] == "device_frmpayload_data_ILL_lux" or r["_measurement"] == "device_frmpayload_data_TempC_SHT")
#   |> aggregateWindow(every: 1s, fn: last, createEmpty: false)
#   |> yield(name: "last")
# '''


def lht65_query_all_data(bucket, device, start):
    return f'''from(bucket: "{bucket}")
  |> range(start:{start})
  |> filter(fn: (r) => r["device_name"] == "{device}")
  |> filter(fn: (r) => r["_measurement"] == "device_frmpayload_data_BatV" or r["_measurement"] == "device_frmpayload_data_Hum_SHT" or r["_measurement"] == "device_frmpayload_data_ILL_lux" or r["_measurement"] == "device_frmpayload_data_TempC_SHT")
    '''
def lse01_query_all_data(bucket, device, start):
    return f'''from(bucket: "{bucket}")
  |> range(start:{start})
  |> filter(fn: (r) => r["device_name"] == "{device}")
  |> filter(fn: (r) =>  r["_measurement"] == "device_frmpayload_data_Bat" or r["_measurement"] == "device_frmpayload_data_water_SOIL" or r["_measurement"] == "device_frmpayload_data_conduct_SOIL" or r["_measurement"] == "device_frmpayload_data_temp_SOIL")
    '''
def ws_query_all_data(bucket, device, start):
    return f'''from(bucket: "{bucket}")
    |> range(start:{start})
    |> filter(fn: (r) => r["device_name"] == "{device}")
    |> filter(fn: (r) => r["_measurement"] == "device_frmpayload_data_BARTREND" or r["_measurement"] == "device_frmpayload_data_DAYET" or r["_measurement"] == "device_frmpayload_data_DAYRAIN" or r["_measurement"] == "device_frmpayload_data_FORECASTICONS" or r["_measurement"] == "device_frmpayload_data_OUTSIDETEMPERATURE" or r["_measurement"] == "device_frmpayload_data_OUTSIDEHUMIDITY" or r["_measurement"] == "device_frmpayload_data_PRESSURE" or r["_measurement"] == "device_frmpayload_data_SOLARADIATION" or r["_measurement"] == "device_frmpayload_data_RAINRATE" or r["_measurement"] == "device_frmpayload_data_TENMINUTESAVGWINDSPEED" or r["_measurement"] == "device_frmpayload_data_UV" or r["_measurement"] == "device_frmpayload_data_WINDDIRECTION" or r["_measurement"] == "device_frmpayload_data_WINDSPEED")
    '''



def query_signal(bucket, device, start):
    return f'''from(bucket: "{bucket}")
  |> range(start:{start})
  |> filter(fn: (r) => r["device_name"] == "{device}")
  |> filter(fn: (r) => r["_field"] == "rssi" or r["_field"] == "snr")
    '''




def write_to_csv(device_name, data):
    time = datetime.date(datetime.now()).__str__()
    path = f'backup_{time}'
    
    isPath = os.path.exists(path)

    if not isPath:
        os.makedirs(path)
    data.to_csv(f'{path}/{device_name}_{time}.csv')




LHT65_MEAS_FIELDS = ['device_frmpayload_data_BatV', 'device_frmpayload_data_Hum_SHT', 'device_frmpayload_data_TempC_SHT', 'device_frmpayload_data_ILL_lux']
LSE01_MEAS_FIELDS = ['device_frmpayload_data_Bat',  'device_frmpayload_data_conduct_SOIL', 'device_frmpayload_data_temp_SOIL', 'device_frmpayload_data_water_SOIL']
WS_MEAS_FIELDS = ['device_frmpayload_data_BARTREND',  'device_frmpayload_data_DAYET', 'device_frmpayload_data_DAYRAIN', 'device_frmpayload_data_FORECASTICONS', 
                'device_frmpayload_data_OUTSIDEHUMIDITY',
                'device_frmpayload_data_OUTSIDETEMPERATURE',
                'device_frmpayload_data_PRESSURE',
                'device_frmpayload_data_RAINRATE',
                'device_frmpayload_data_SOLARADIATION',
                'device_frmpayload_data_TENMINUTESAVGWINDSPEED',
                'device_frmpayload_data_UV',
                'device_frmpayload_data_WINDDIRECTION',
                'device_frmpayload_data_WINDSPEED',]

SIGNAL_FIELDS = ['snr', 'rssi']




def collect_measurements(query, fields, cols, type_collect='measurement'):

    tmp  = []
    for i in query:
        for j in i:
            # print(j.get_measurement(), j.get_time(), j.get_value())
            tmp.append([j.get_measurement() if type_collect == 'measurement' else j.get_field(), j.get_time(), j.get_value()])
    df = pd.DataFrame(tmp, columns=[type_collect, 'time', 'value'])
    df = df.sort_values(by=['time'])
    
    tmp = []
    # print(df)

    for i in range(0, len(df), len(fields)):
        sliced = df.iloc[i:i+len(fields)].sort_values(by = [type_collect])
        tinkge = [sliced[sliced[type_collect] == f]['value'].values[0] for f in fields]
        tinkge.insert(0, str(sliced['time'].head(1).values[0]))
        tmp.append(tinkge)
    # print(tmp[0])

    return pd.DataFrame(tmp, columns=cols)



def back_up(org, bucket, start, meas_fields, signal_fields, save_fields, max_devices, prefix):
    query_api = client.query_api()
    for i in range(1, max_devices + 1):
        device = f'{prefix}{i}'
        # device = 'L1'
        if prefix == 'L':
            r = query_api.query(org=org, query=lht65_query_all_data(bucket, device, start))
        elif prefix == 'SM':
            r = query_api.query(org=org, query=lse01_query_all_data(bucket, device, start))
        elif prefix == 'WS':
            device = 'Weather-Station' #lazy programming
            r = query_api.query(org=org, query=ws_query_all_data(bucket, device, start))
        measure = collect_measurements(r, meas_fields, save_fields, type_collect='measurement')
        # dataset = collect_uplink_data()

        r = query_api.query(org=org, query=query_signal(bucket, device, start))
        signal = collect_measurements(r, signal_fields, ['time', 'snr', 'rssi'], type_collect='field')
        # print(signal)
        dataset = pd.merge(measure, signal, on=['time'])
        # print(dataset)
        return dataset



# back_up(ORG, 'Arvores', START, LHT65_MEAS_FIELDS, SIGNAL_FIELDS, ['time', 'bat', 'hum', 'tmp', 'ill'], MAX_LHT65_DEVICES, 'L')
# back_up(ORG, 'Solo', START, LSE01_MEAS_FIELDS, SIGNAL_FIELDS, ['time', 'bat', 'soil_conduct', 'soil_tmp', 'soil_water' ], MAX_LSE01_DEVICES, 'SM')
# back_up(ORG, 'Weather-Station', START, WS_MEAS_FIELDS, SIGNAL_FIELDS,  ['time', 'bartrend','dayet','dayrain', 'forecasticons', 'hum', 'tmp','pressure','rainrate','solarrad', '10minavgwindspeed', 'uv', 'winddirection','windspeed' ], 1, 'WS')
