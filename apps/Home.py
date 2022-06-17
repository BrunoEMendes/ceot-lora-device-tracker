from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd
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
        # html.Div(children=[
        #             html.Img(src=app.get_asset_url('ceot-logo2.png'),
        #                      style={'margin-left':'15px','width':'445', 'height':'62'}),
        #             html.H2(children='Experimental Tree Orange Sensor Network (Paderne)',
        #                     style={'margin-left':'15px'})
        #             ],style={'text-align':'center'}),
        dcc.Interval(
            id='update-ws',
            interval=30*10000, # in milliseconds
            n_intervals=0
        ),
        dcc.Interval(
            id='update-clock',
            interval=1000, #1sec
        ),
        
html.Div(className='center',
                         children=[
                             html.Div(className='main',
                                      children=[
                                          html.H2(children='Valores médios agora'),
                                          html.P(id='texto_temp',children=[]),
                                          html.P(id='texto_hum',children=[]),
                                          html.P(id='texto_lum',children=[]),
                                          html.P(id='texto_soil_water',children=[]),
                                          html.P(id='texto_soil_temp',children=[]),
                                          html.P(id='texto_soil_cond',children=[])
                                       ],
                                      style={
                                      'margin-left':'10px',
                                      'width':'40%',
                                      'vertical-align':'text-top',
                                      'text-align':'left',
                                      'font-family': 'sans-serif',
                                      'display':'inline-block',
                                      }),
                             html.Div(className='main',
                                      children=[
                                          html.H2(children='Condições meteorológicas agora'),
                                          html.P(id='texto_meteo_time',children=[]),
                                          html.P(id='texto_meteo_temp',children=[]),
                                          html.P(id='texto_meteo_hum',children=[]),
                                          html.P(id='texto_meteo_lum',children=[]),  
                                          html.P(id='texto_meteo_press',children=[]),
                                          html.P(id='texto_meteo_rain',children=[]),
                                          html.P(id='texto_meteo_wind',children=[]),
                                          html.P(id='texto_meteo_wind_dir',children=[]),
                                          html.P(id='texto_meteo_wind_10min',children=[]),
                                          ],style={
                                          'margin-left':'30px',
                                          'width':'40%',
                                          'vertical-align':'text-top',
                                          'font-family': 'sans-serif',
                                          'text-align':'left',
                                          'display':'inline-block',
                                          }),
                                html.Br(),
                             ]),
        html.Br(),
        html.Br(),                                      
        html.Div(className='navbar navbar-default',
                 children=[
                     html.P(children='Visualização de dados de uma rede de sensores LoRaWAN distribuidos num pomar de laranjeiras. \
                            São 25 sensores de luminosidade/humidade/temperatura na copa de 25 árvores, \
                             6 sensores de humidade de solo, e uma estação meteorológica. A cadencia dos sensores é 30 min\
                            e da estação meteorológica é 15 min.\
                            Este é um projeto desenvolvido pelo CEOT- Ualg (www.ceot.ualg.pt) que tem como objectivos a\
                            implementação e estudo operacional deste tipo de redes de sensores para agricultura de precisão \
                            e, neste caso, o estudo das condições de maturação de citrinos. Para mais informação contactar:\
                            ceot@ualg.pt .\
                            Este projecto tem da apoio da Altice Labs')], 
                     style={
                     'margin-left':'10px',
                     'width':'90%',
                     'vertical-align':'text-top',
                     'text-align':'left',
                     'font-family': 'sans-serif',
                     'display':'inline-block',
                     })        
        ])

# @app.callback(
#     Output(component_id = 'texto_meteo_time', component_property='children'),
#     Input('update-clock', 'n_intervals')
# )
# def update_clock(n):
#     return f'current time: {datetime.now()}'









@app.callback(
    [Output(component_id = 'texto_temp', component_property='children'),
     Output(component_id = 'texto_hum', component_property='children'),
     Output(component_id = 'texto_lum', component_property='children'),
    [Input('update-ws', 'n_intervals')]]
)
def update_mean_data_lht65(n):
    client = Client(secret.server, secret.port, secret.token, secret.org).client()
    dp = DeviceProfile('LHT65', config.LHT65_FIELDS)
    df = pd.DataFrame(columns=list(config.LHT65_FIELDS.keys()))
    for d in range(0, config.MAX_LHT65_DEVICES+1):
        d = Device(f'L{d}', dp, client, 'Arvores')
        tmp = []
        for k, v in config.LHT65_FIELDS.items():
            r,_ = d.get_last_value(k)
            if r != None:
                tmp.append(r)
        # df = pd.concat([df, tmp], ignore_index=True, axis=0)
        # print(tmp)
        if len(tmp) > 0:
            df.loc[len(df)] = tmp
       
    texto_temp = f'Temperatura media: {df["temperature (ºC)"].mean():.2f} ºC'
    texto_hum = f'Humidade media: {df["humidity (%)"].mean():.2f}% RH '
    texto_lum = f'Luminosidade media: {df["illumination (lux)"].mean()} lux'
    return  texto_temp, texto_hum, texto_lum


@app.callback(
    [Output(component_id = 'texto_soil_water', component_property='children'),
     Output(component_id = 'texto_soil_temp', component_property='children'), 
     Output(component_id = 'texto_soil_cond', component_property='children'), 
    [Input('update-ws', 'n_intervals')]]
)

def update_mean_data_lse01(n):
    client = Client(secret.server, secret.port, secret.token, secret.org).client()

    dp = DeviceProfile('LS01', config.LSE01_FIELDS)
    df = pd.DataFrame(columns=list(config.LSE01_FIELDS.keys()))
    for d in range(0, config.MAX_LSE01_DEVICES+1):
        d = Device(f'SM{d}', dp, client, 'Solo')
        tmp = []
        for k, v in config.LSE01_FIELDS.items():
            r,_ = d.get_last_value(k)
            if r != None:
                tmp.append(r)
        if len(tmp) > 0:
            df.loc[len(df)] = tmp

    texto_soil_water = f'Humidade media do solo (20 cm prof.): {df["soil water content (%)"].mean():.2f} %'
    texto_soil_temp = f'Temperatura media do solo (20 cm prof.): {df["soil temperature (ºC)"].mean():.2f} ºC'
    texto_soil_cond = f'Condutividade media do solo (20 cm prof.): {df["soil conductivity (uS/cm)"].mean():.2f}'
    return texto_soil_water, texto_soil_temp, texto_soil_cond


@app.callback(
    [Output(component_id = 'texto_meteo_time', component_property='children'),
     Output(component_id = 'texto_meteo_temp', component_property='children'),
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
        df,time = device.get_last_value(key)
        tmp.append(df)  

    meteo_time = f'Última Medição: {time.strftime("%d/%m/%Y %H:%M:%S")}'
    meteo_temp = f'Temperatura: {tmp[0]} ºC'
    meteo_hum = f'Humidade: {tmp[1]:.2f} % '
    meteo_lum = f'Radiação solar: {tmp[2]:.2f} W/m^2'
    meteo_press = f'Pressão atmosférica: {tmp[3]:.2f} hPa'
    meteo_rain = f'Precipitação: {tmp[4]:.2f} mm/h'
    meteo_wind = f'Velocidade do vento: {tmp[5]:.2f} m/s'
    meteo_wind_dir = f'Direção do vento: {tmp[6]:.2f} º (360=N, 270=W, 180=S, 90=E)'
    meteo_wind_10min = f'Velocidade média do vento (10 min): {tmp[7]:.2f} m/s'
    
    return meteo_time, meteo_temp, meteo_hum, meteo_lum, meteo_press, meteo_rain, meteo_wind, meteo_wind_dir, meteo_wind_10min