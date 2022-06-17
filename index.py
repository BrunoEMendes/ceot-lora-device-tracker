from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from app import app
from app import server
from apps import LHT65, LSE01, Map, Home, METEO

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(children=[
                html.Img(src=app.get_asset_url('ceot-logo2.png'),
                         style={'margin-left':'15px','width':'445', 'height':'62'}),
                html.H2(className='navbar navbar-default',
                        children='Rede experimental de sensores (Pomar de laranjeiras @ Paderne)',
                        style={'margin-left':'15px'})
                ],style={'text-align':'center'}),
    html.Div([
        dcc.Link('Home ', href='/', style={'font-size':'16px'}, className='button-8'),
        dcc.Link('Sensores de Copa', href='/apps/LHT65', style={'font-size':'16px'}, className='button-8'),
        dcc.Link('Sensores de Solo', href='/apps/LSE01', style={'font-size':'16px'}, className='button-8'),
        dcc.Link('Estação meteorológica', href='/apps/METEO', style={'font-size':'16px'}, className='button-8'),
        dcc.Link('Mapas ', href='/apps/Map', style={'font-size':'16px'}, className='button-8'),
    ], className="inline-block", style={'text-align':'center'}),
    html.Br(),
    html.Br(),
    html.Div(id='page-content', children=[], style={'text-align':'center'})
 ],  
    className='container-fluid inline-block',
    style={
#        'padding-left':"5%",
#       'padding-right':"5%",
        'text-align':'center'
    })


# app._favicon = f'{os.getcwd()}\ceot-logo.png'

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])



def display_page(pathname):
    if pathname == '/':
        return Home.layout
    if pathname == '/apps/Map':
        return Map.layout
    if pathname == '/apps/LHT65':
        return LHT65.layout
    if pathname == '/apps/LSE01':
        return LSE01.layout
    if pathname == '/apps/METEO':
        return METEO.layout
    else:
        return Home.layout

if __name__ == '__main__':
    app.run_server(debug=False)