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
    dcc.Checklist(
        id="checklist",
        options=['L'+ str(i) for i in range(1, config.MAX_LHT65_DEVICES + 1)],
        value=['L1'],
        inline=True
    ),

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

import plotly.graph_objects as go

@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('xaxis-column', 'value'),
    Input("checklist", "value"),
    Input('indicator-graphic', 'figure'),)
def update_graph(xaxis_column_name, checklist, graph):
    existing_fields = []
    new_data = []




    fig = go.Figure() 
    fig.update_layout(title_text=f'LHT65 {xaxis_column_name} measurement', 
                        title_x=0.5,                    
                        xaxis_title='Date',
                        yaxis_title=f'{xaxis_column_name}')


    if graph != None and graph['layout']['yaxis']['title']['text'] == xaxis_column_name:

        existing_fields = [g['name'] for g in graph['data']]
        for g in graph['data']:
            if g['name'] in checklist:
                new_data.append(g)
        graph['data'] = new_data
        fig = go.Figure(graph)
    
    

    client = Client(secret.server, secret.port, secret.token, secret.org).client()
    dp = DeviceProfile('LHT65', config.LHT65_FIELDS)
        
    
    for k in checklist:
        if not k in existing_fields:
            device = Device(k, dp, client, 'Arvores')
            df = device.query_field(xaxis_column_name, START)
            fig.add_trace(go.Scatter(
                x=df['time'],
                y=df[xaxis_column_name],
                name=k
            ))
    return fig

