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


lht65_location = pd.read_csv("lht65_device_loc.csv")


START = int(datetime(2022,3,12,7,30,0, tzinfo=None).timestamp())

layout = html.Div([
      dcc.Dropdown(
                    list(config.LHT65_FIELDS.keys())[1:],
                    list(config.LHT65_FIELDS.keys())[1],
                    id='mapbox-fields'
                ),
        dcc.Graph(id='mapbox', style={
            'width':'90vw',
            'height':'100vh'
        }),
]),

@app.callback(
    Output('mapbox', 'figure'),
    Input('mapbox-fields', 'value'))
def mapbox(field):


    client = Client(secret.server, secret.port, secret.token, secret.org).client()
    dp = DeviceProfile('LHT65', config.LHT65_FIELDS)
    
    tmp = []
    for index, row in lht65_location.iterrows():
        device = Device(row['Device'], dp, client, 'Arvores')
        df = device.get_last_value(field)
        tmp.append(df)
        
    clone = lht65_location.__deepcopy__()

    clone[field] = tmp

    fig = px.density_mapbox(clone, lat='Lat', lon='Lon', z=field, radius=40,
                        center=dict(lat=0, lon=180), zoom=8,
                        # mapbox_style="stamen-terrain", 
                        color_continuous_scale= [
                                [0.1, "#0d0887"],
                                [0.2, "#46039f"],
                                [0.3, "#7201a8"],
                                [0.4, "#bd3786"],
                                [0.5, "#d8576b"],
                                [0.6, "#ed7953"],
                                [0.7, "#fb9f3a"],
                                [0.8, "#fdca26"],
                                [0.9, "#f0f921"],
                                ],
                                # range_color=[min(tmp), max(tmp)],
                        opacity=1,
                        )

    fig.update_layout(
        mapbox_accesstoken=secret.MAPBOX_TOKEN, 
        mapbox_style='satellite-streets',
        mapbox=dict(
            center=dict(
                lat=37.1,
                lon=-8.07
            )),)
    fig.update_geos(projection_type="orthographic")

    return fig