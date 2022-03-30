from tabnanny import check
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

import plotly.express as px

START = int(datetime(2022,3,12,7,30,0, tzinfo=None).timestamp())
token = 'pk.eyJ1IjoiYmVtZW5kZXMiLCJhIjoiY2wxZG03aWo0MGl1NjNqbzBocDN5empjaCJ9.fqgJSctKC4dKZFiNhsjpZQ'

layout = html.Div([
      dcc.Dropdown(
                    list(config.LHT65_FIELDS.keys()),
                    list(config.LHT65_FIELDS.keys())[0],
                    id='xaxis-column'
                ),
        dcc.Graph(id='mapbox'),
]),

@app.callback(
    Output('mapbox', 'figure'),
    Input('xaxis-column', 'value'))
def mapbox(heatmap):
    # print()
    # fig = px.scatter_mapbox(lht65_location, lat="Lat", lon="Lon", hover_name="Device",
    #                         color_discrete_sequence=["fuchsia"], zoom=3, height=300)
    # fig.update_layout(mapbox_style="stamen-terrain", mapbox_accesstoken=token)
    # fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


    client = Client(secret.server, secret.port, secret.token, secret.org).client()
    dp = DeviceProfile('LHT65', config.LHT65_FIELDS)
    
    tmp = []
    for index, row in lht65_location.iterrows():
        device = Device(row['Device'], dp, client, 'Arvores')
        df = device.get_last_value('tmp')
        tmp.append(df)
        
    clone = lht65_location.__deepcopy__()

    clone['tmp'] = tmp

    fig = px.density_mapbox(clone, lat='Lat', lon='Lon', z='tmp', radius=10,
                        center=dict(lat=0, lon=180), zoom=0,
                        # mapbox_style="stamen-terrain", 
                        # color_continuous_scale= [
                        #         [0.0, "green"],
                        #         [0.5, "green"],
                        #         [0.51111111, "yellow"],
                        #         [0.71111111, "yellow"],
                        #         [0.71111112, "red"],
                        #         [1, "red"]],
                        #         opacity = 1,
                        #         # range_color=[min(tmp), max(tmp)],
                        opacity=1,
                        )

    fig.update_layout(mapbox_accesstoken=token, mapbox_style='satellite-streets')

    return fig