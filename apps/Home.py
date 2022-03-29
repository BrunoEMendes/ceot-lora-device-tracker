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


START = int(datetime(2022,3,12,7,30,0, tzinfo=None).timestamp())

layout = html.Div([

]),