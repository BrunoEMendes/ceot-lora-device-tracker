from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from app import app
from app import server
from apps import LHT65
import dash


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('LHT65 |', href='/apps/LHT65'),
        dcc.Link('LSE01(NOT WORKING)', href='/apps/LSE01'),
    ], className="inline-block"),
    html.Div(id='page-content', children=[],)
],  className='container-fluid inline-block',
    style={
        'padding-left':"5%",
        'padding-right':"5%",
    })


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/LHT65':
        return LHT65.layout
    else:
        return LHT65.layout


if __name__ == '__main__':
    app.run_server(debug=True)