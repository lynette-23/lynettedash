import dash
from dash import Dash
from dash import html
from dash import dcc
import plotly.express as px
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import pandas as pd

df = pd.read_csv('dataset.csv')
print(df)

# app layout
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device=width, intial=scale1.0'}]
                )

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "blue",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("menu", className="display-5"),
        html.Hr(),
        html.P(
            "BAYJING FUN OLYMPICS 2022", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Page 1", href="/page-1", active="exact"),
                dbc.NavLink("Page 2", href="/page-2", active="exact"),
                dbc.NavLink("page 3", href="/page-3", active="exact"),
                dbc.NavLink("page4", href="/page-4", active="exact")
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return [
            html.H1('NUMBER OF VISITS PER SPORT',
                    style={'textAlign': 'center'}),
            dcc.Graph(id='bargraph',
                      figure=px.histogram(df, barmode='group', x='SPORTS',
                                    y=['NUMBER_OF_VISITS']))
        ]
    elif pathname == "/page-1":
        return [
            html.H1('VIEWS PER COUNTRY',
                    style={'textAlign': 'center'}),
            dcc.Graph(id='bargraph',
                      figure=px.bar(df, barmode='group', x='COUNTRY',
                                    y=['NUMBER_OF_VIEWS']))
        ]
    elif pathname == "/page-2":
        return [
            html.H1('SPORT PER COUNTRY',
                    style={'textAlign': 'center'}),
            dcc.Graph(id='linegraph',
                      figure=px.line(df, x='COUNTRY',
                                    y=['SPORTS']))
        ]
    elif pathname == "/page-3":
        return [
            html.H1('AVERAGE TIME VISITS',
                    style={'textAlign': 'center'}),
            dcc.Graph(id='scatter',
                      figure=px.scatter(df, x='COUNTRY',
                            y=['DATE', 'TIME']))
        ]
    elif pathname == "/page-4":
        return [
            html.H1('VIEWS PER SPORT',
                    style={'textAlign': 'center'}),
            dcc.Graph(id='pie',
                      figure=px.pie(df, values='NUMBER_OF_VIEWS', names='COUNTRY', color_discrete_sequence=px.colors.sequential.RdBu))
        ]

    # If the user tries to reach a different page, return a 304 message
    return dbc.Jumbotron(
        [
            html.H1("304: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == '__main__':
    app.run_server(debug=True, port=8050)




