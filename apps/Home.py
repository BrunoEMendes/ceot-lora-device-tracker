from tabnanny import check
from turtle import width
from click import style
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
import plotly.graph_objects as go

import pandas as pd



layout = html.Div([
        html.Div(children=[
                    html.Img(src=app.get_asset_url('ceot-logo2.png'),
                             style={'width':'445', 'height':'62'}),
                    html.H2(children='Experimental Tree Orange Sensor Network (Paderne)')
                    ]),
        dcc.Interval(
            id='update-ws',
            interval=30*10000, # in milliseconds
            n_intervals=0
        ),
        dcc.Interval(
            id='update-clock',
            interval=1000, #1sec
        ),
        
        html.Div(className='6 columns div meteo',
            children=[
                html.H3(children='Condições meteorológicas agora'),
                html.P(id='texto_meteo_time',children=[]),
                html.P(id='texto_meteo_temp',children=[]),
                html.P(id='texto_meteo_hum',children=[]),
                html.P(id='texto_meteo_lum',children=[]),  
                html.P(id='texto_meteo_press',children=[]),
                html.P(id='texto_meteo_rain',children=[]),
                html.P(id='texto_meteo_wind',children=[]),
                html.P(id='texto_meteo_wind_dir',children=[]),
                html.P(id='texto_meteo_wind_10min',children=[])
                ],style={
                'margin-left':'30px',
                'width':'60%',
                'vertical-align':'text-top',
                'font-family': 'sans-serif',
                'text-align':'left',
                'display':'inline-block',
                'border-width':'0px',
                'border-style':'solid',
                'border-color':'black'
            }),
        ])

@app.callback(
    Output(component_id = 'texto_meteo_time', component_property='children'),
    Input('update-clock', 'n_intervals')
)
def update_clock(n):
    return f'current time: {datetime.now()}'





@app.callback(
    [Output(component_id = 'texto_meteo_temp', component_property='children'),
     Output(component_id = 'texto_meteo_hum', component_property='children'),
     Output(component_id = 'texto_meteo_lum', component_property='children'),
     Output(component_id = 'texto_meteo_press', component_property='children'),
     Output(component_id = 'texto_meteo_rain', component_property='children'),
     Output(component_id = 'texto_meteo_wind', component_property='children'),
     Output(component_id = 'texto_meteo_wind_dir', component_property='children'),
     Output(component_id = 'texto_meteo_wind_10min', component_property='children'),    
    [Input('update-ws', 'n_intervals')]
    ]
)
def update_ws_data(n):
    client = Client(secret.server, secret.port, secret.token, secret.org).client()
    dp = DeviceProfile('WS', config.WS_FIELDS)
    tmp = []
    for key, val in config.WS_FIELDS.items():
        device = Device('Weather-Station', dp, client, 'Weather-Station')
        df = device.get_last_value(key)
        tmp.append(df)  

    meteo_temp = f'Temperatura: {tmp[0]:.2} ºC'
    meteo_hum = f'Humidade: {tmp[1]:.2f} % '
    meteo_lum = f'Radiação solar: {tmp[2]:.2f} W/m^2'
    meteo_press = f'Pressão atmosférica: {tmp[3]:.2f} hPa'
    meteo_rain = f'Precipitação: {tmp[4]:.2f} mm/h'
    meteo_wind = f'Velocidade do vento: {tmp[5]:.2f} m/s'
    meteo_wind_dir = f'Direção do vento: {tmp[6]:.2f} º (360=N, 270=W, 180=S, 90=E)'
    meteo_wind_10min = f'Velocidade média do vento (10 min): {tmp[7]:.2f} m/s'
    
    return meteo_temp, meteo_hum, meteo_lum, meteo_press, meteo_rain, meteo_wind, meteo_wind_dir, meteo_wind_10min