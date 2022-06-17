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


START = int(datetime(2022,3,18,0,0,0, tzinfo=None).timestamp())

layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                dcc.Dropdown(
                    list(config.WS_FIELDS.keys()),
                    list(config.WS_FIELDS.keys())[0],
                    id='xaxis-column-meteo'
                ),
            ], style={'width': '25%', 'display': 'inline-block'}),

        ]),
    dcc.Graph(id='indicator-graphic-meteo',
                style={
                  'height':'70vh'
              }),
    ]),
    
    # dcc.Checklist(
    #     id="checklist",
    #     options=['L'+ str(i) for i in range(1, config.MAX_LHT65_DEVICES + 1)],
    #     value=['L1'],
    #     inline=True,
    #     inputStyle={
    #         "margin-left": "20px",
    #         "margin-right": "2px",
    #     }
    # ),


], className='container-fluid inline-block')

##############################################################
@app.callback(
    Output('indicator-graphic-meteo', 'figure'),
    Input('xaxis-column-meteo', 'value'),
    Input('indicator-graphic-meteo', 'figure'))

def update_graph(xaxis_column_name, graph):

    # vars
    existing_fields = []
    new_data = []

    # new figure
    fig = go.Figure() 
    fig.update_layout(title_text=f'Weather station data', 
                        title_x=0.5,                    
                        xaxis_title='Date',
                        yaxis_title=f'{xaxis_column_name}',)



    # inicia o cliente IDB
    client = Client(secret.server, secret.port, secret.token, secret.org).client()
    dp = DeviceProfile('WS', config.WS_FIELDS)

    # se o valor o dispositivo estiver na checklist e ainda nao exisitr no grafico é adiconado
    # for k in checklist:
    #     if not k in existing_fields:
    device = Device('Weather-Station', dp, client, 'Weather-Station')
    df = device.query_field(xaxis_column_name, START)

    fig.add_trace(go.Scatter(
           x=df['time'],
           y=df[xaxis_column_name],
           name='Weather-Station',
           mode='lines'
         )
    )
    return fig




