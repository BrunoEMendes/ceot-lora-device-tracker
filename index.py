from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from app import app
from app import server
from apps import chart, chart1
import dash


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('FIRST TAB |', href='/apps/chart'),
        dcc.Link('Other TAB', href='/apps/chart1'),
    ], className="row"),
    html.Div(id='page-content', children=[],)
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/chart':
        return chart.layout
    else:
        return chart1.layout


if __name__ == '__main__':
    app.run_server(debug=True)