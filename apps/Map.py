from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly
import plotly.express as px
import plotly.figure_factory as ff

import pandas as pd
import pathlib
from app import app
import datetime
import numpy as np

from .modules.device import DeviceProfile, Device
from datetime import datetime
from .modules.client import Client
import config as config
import secret
import plotly.graph_objects as go

import pandas as pd


lht65_location = pd.read_csv("lht65_device_loc.csv")
lse01_location = pd.read_csv("lse01_device_loc.csv")

START = '-1d' #int(datetime(2022,3,12,7,30,0, tzinfo=None).timestamp())
layout = html.Div([
    html.Div([
      dcc.Dropdown(
                    list(config.LHT65_FIELDS.keys()),
                    list(config.LHT65_FIELDS.keys())[2],
                    id='mapbox-fields',
                ),
      ], 
        
        style={'width': '25%', 'display': 'inline-block'}),
        dcc.Graph(id='mapbox1', style={
            'text-align':'center',
            'width':'90vw',
            'height':'100vh'
        }),
    html.Div([
          dcc.Dropdown(
                        list(config.LSE01_FIELDS.keys()),
                        list(config.LSE01_FIELDS.keys())[1],
                        id='mapbox-fields-soil',
                    ),
          ], 
            
            style={'width': '25%', 'display': 'inline-block'}),
            dcc.Graph(id='mapbox1-soil', style={
                'text-align':'center',
                'width':'90vw',
                'height':'100vh'
            })   
]),

@app.callback(
    Output('mapbox1', 'figure'),
    Output('mapbox1-soil', 'figure'),
    Input('mapbox-fields', 'value'),
    Input('mapbox-fields-soil', 'value'))

def mapbox(field,field_soil):
   
    ## Color scales: 
    #        bat -> 'RdYlGn'
    #        tmp ->'Portland'
    #        ilx -> 'blackbody'
    #        hum -> 'YlGnBu'
    
    client = Client(secret.server, secret.port, secret.token, secret.org).client()
    dp = DeviceProfile('LHT65', config.LHT65_FIELDS)
    dp_soil = DeviceProfile('LSE01', config.LSE01_FIELDS)
    
    tmp = []
    tmp_soil = []
    
    for index, row in lht65_location.iterrows():
        device = Device(row['Device'], dp, client, 'Arvores')
        df,time = device.get_last_value(field)
        ## If the device is offline at the time of query (-1h) the df will
        ## contain None types. To avoid errors of this kind we check for None
        ## and substitute them with a small value e.g. 1e-3
        if df is None: df = 1e-3
        tmp.append(df)
        
    for index, row in lse01_location.iterrows():
        device2 = Device(row['Device'], dp_soil, client, 'Solo')
        df2,time2 = device2.get_last_value(field_soil)
        tmp_soil.append(df2)
        
    clone = lht65_location.__deepcopy__()
    clone_soil = lse01_location.__deepcopy__()

    clone[field] = tmp
    clone_soil[field_soil] = tmp_soil
    field_label = str(field)
    field_color = {'battery (V)':'RdYlGn', 'temperature (ºC)':'Portland', 
                   'illumination (lux)':'blackbody', 'humidity (%)':'YlGnBu'}
    
    field_color2 = {'battery (V)':'RdYlGn', 'soil temperature (ºC)':'Portland', 
                   'soil water content (%)':'YlGnBu', 'soil conductivity (uS/cm)':'Cividis_r'}
    field_label2 = str(field_soil)
    
    ## Generate a list of values without 1e-3 values. This will be used for 
    ## plotting purposes (for getting the correct color scale)
    tmp_good=[i for i in tmp if i!=1e-3]
    
    ## Option 1 -> Scatter plot
    # fig = px.scatter_mapbox(clone, lat='Lat', lon='Lon', color=tmp, size=tmp,
    #                     center=dict(lat=37.192723, lon=-8.182952), zoom=18,
    #                     mapbox_style="stamen-terrain", 
    #                     color_continuous_scale = field_color[field],
    #                     labels = {'color': field_label, 'size':''},
    #                     color_continuous_midpoint = (max(tmp)-min(tmp))/2.,
    #                     range_color=[min(tmp), max(tmp)],
    #                     opacity=0.75,
    #                     )
    ## Option 2 -> Density plot 
    # fig = px.density_mapbox(clone, lat='Lat', lon='Lon', z=tmp, radius=75,
    #                     center=dict(lat=37.192723, lon=-8.182952), zoom=18,
    #                     mapbox_style="stamen-terrain", 
    #                     color_continuous_scale = field_color[field],
    #                     labels = {'z': field_label},
    #                     color_continuous_midpoint = (max(tmp)-min(tmp))/2.,
    #                     range_color=[min(tmp), max(tmp)],
    #                     opacity=0.75,
    #                     )
    fig = px.scatter_mapbox(clone, lat='Lat', lon='Lon', color=tmp, size=tmp,
                            hover_name='Device',
                        center=dict(lat=37.192723, lon=-8.182952), zoom=18,
                        mapbox_style="stamen-terrain", 
                        color_continuous_scale = field_color[field],
                        labels = {'color': field_label},
                        color_continuous_midpoint = (max(x for x in tmp_good if x is not None)-min(x for x in tmp_good if x is not None))/2.,
                        range_color=[min(x for x in tmp_good if x is not None), max(x for x in tmp_good if x is not None)],
                        opacity=0.75,
                        )
    # Option 3 -> Hexagonal mesh plot
    fig_soil = ff.create_hexbin_mapbox(data_frame=clone_soil, lat='Lat', lon='Lon', 
                                  nx_hexagon=5,
                                  center=dict(lat=37.192723, lon=-8.182952), zoom=18,
                                  color = tmp_soil,
                                  color_continuous_scale = field_color2[field_soil],
                                  labels = {'color': field_label2},
                                  mapbox_style="stamen-terrain", 
                                  range_color=[min(x for x in tmp_soil if x is not None), max(x for x in tmp_soil if x is not None)],
                                  show_original_data=True,
                                  opacity=0.5, min_count=1
                        )
    
    fig.layout.update({'title': 'Sensores de copa (25)'})
    fig.update_layout(
        hovermode="y unified",
        mapbox_accesstoken=secret.MAPBOX_TOKEN, 
        # mapbox_bearing = -21,
        mapbox_style='satellite-streets',
        mapbox=dict(
            center=dict(
                lat=37.192723,
                lon=-8.182952
            )),)
    fig.update_geos(projection_type="orthographic" )
    
    fig_soil.layout.update({'title': 'Sensores de solo (6)'})
    fig_soil.update_layout(
        hovermode="y unified",
        mapbox_accesstoken=secret.MAPBOX_TOKEN, 
        # mapbox_bearing = -21,
        mapbox_style='satellite-streets',
        mapbox=dict(
            center=dict(
                lat=37.192723,
                lon=-8.182952
            )),)
    fig_soil.update_geos(projection_type="orthographic" )

    return fig, fig_soil