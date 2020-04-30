import pathlib
import dash
import pandas as pd
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
# from functions import load_data
# from functions import functions
# import os
# from datetime import datetime
# import dash_table
# import plotly.graph_objects as go
# import plotly.express as px
# import base64

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

########### Initiate the app
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server
app.title = 'Covid-19 Canada'

########### Set up the layout
app.layout = html.Div(
    [
        dcc.Store(id="storage", data='a'),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("logo2.png"),
                            id="plotly-image",
                            style={
                                "height": "120px",
                                "width": "auto",
                                "margin-bottom": "25px",
                                "align-items": "center",
                            },
                        )
                    ],
                    className="one-third column",
                    style={'textAlign': 'center'}
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H2(
                                    "Canada Coronavirus Tracker",
                                    style={'font-weight': 'bold', 'fontSize': '4vh', "margin-bottom": "0px"}
                                ),
                                html.H5(
                                    "Last Updated today "
                                    # .format(str(time)[:-10])
                                    ,
                                    style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("Data Source", id="learn-more-button"),
                            href="https://docs.google.com/spreadsheets/d/1D6okqtBS3S2NRC7GFVHzaZ67DuTw7LX49-fqSLwJyeo",
                            target='_blank'
                        )
                    ],
                    className="one-third column",
                    id="button",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Loading(html.H6(id="well_text",
                                         style={'color': 'white', 'font-weight': 'bold', 'fontSize': '4vh'}
                                         )),
                     html.P("CONFIRMED",
                            style={'color': 'white', 'fontSize': '2vh'}
                            )],
                    className="pretty_container one-fourth column",
                    style={'backgroundColor': '#0099e5'}
                ),

                html.Div(
                    [dcc.Loading(html.H6(id="gasText",
                                         style={'color': 'white', 'font-weight': 'bold', 'fontSize': '4vh'}
                                         )),
                     html.P("RECOVERED",
                            style={'color': 'white', 'fontSize': '2vh'}
                            )],
                    className="pretty_container one-fourth column",
                    style={'backgroundColor': '#6cc644'}
                ),
                html.Div(
                    [dcc.Loading(html.H6(id="waterText",
                                         style={'color': 'white', 'font-weight': 'bold', 'fontSize': '4vh'}
                                         )),
                     html.P("DECEASED",
                            style={'color': 'white', 'fontSize': '2vh'}
                            )],
                    className="pretty_container one-fourth column",
                    style={'backgroundColor': 'rgb(255,27,14)'}
                ),
                html.Div(
                    [dcc.Loading(html.H6(id="oilText",
                                         style={'color': 'white', 'font-weight': 'bold', 'fontSize': '4vh'}
                                         )),
                     html.P("TESTED",
                            style={'color': 'white', 'fontSize': '2vh'}
                            )],
                    className="pretty_container one-fourth column",
                    style={'backgroundColor': '#fbbc05'}
                ),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)

if __name__ == '__main__':
    app.run_server()
