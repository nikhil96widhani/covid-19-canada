import pathlib
import dash
import pandas as pd
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
# from functions import load_data
from functions import functions
import os
from datetime import datetime
import dash_table
import plotly.graph_objects as go
import plotly.express as px
import base64
import urllib.request
import json
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

########### Initiate the app
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server
app.title = 'Covid-19 Canada'

url_cases = 'https://raw.githubusercontent.com/ishaberry/Covid19Canada/master/cases.csv'
url_mortality = 'https://raw.githubusercontent.com/ishaberry/Covid19Canada/master/mortality.csv'
url_recovered = 'https://raw.githubusercontent.com/ishaberry/Covid19Canada/master/recovered_cumulative.csv'
url_testing = 'https://raw.githubusercontent.com/ishaberry/Covid19Canada/master/testing_cumulative.csv'

dfcases = pd.read_csv(url_cases)
dfmortality = pd.read_csv(url_mortality)
dfrecovered = pd.read_csv(url_recovered)
dftesting = pd.read_csv(url_testing)

image_filename = 'testmap.png'  # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# dfFips = pd.read_csv(fips)
# dfFips = dfFips[dfFips['Country_Region'] == 'Canada'].reset_index(drop=True)
# dfFips['test'] = 'MN'

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
                                         style={'color': 'white', 'font-weight': 'bold', 'fontSize': '3vh'}
                                         )),
                     html.P("CONFIRMED",
                            style={'color': 'white', 'fontSize': '2vh'}
                            )],
                    className="pretty_container one-fourth column",
                    style={'backgroundColor': '#0099e5'}
                ),

                html.Div(
                    [dcc.Loading(html.H6(id="gasText",
                                         style={'color': 'white', 'font-weight': 'bold', 'fontSize': '3vh'}
                                         )),
                     html.P("RECOVERED",
                            style={'color': 'white', 'fontSize': '2vh'}
                            )],
                    className="pretty_container one-fourth column",
                    style={'backgroundColor': '#6cc644'}
                ),
                html.Div(
                    [dcc.Loading(html.H6(id="waterText",
                                         style={'color': 'white', 'font-weight': 'bold', 'fontSize': '3vh'}
                                         )),
                     html.P("DECEASED",
                            style={'color': 'white', 'fontSize': '2vh'}
                            )],
                    className="pretty_container one-fourth column",
                    style={'backgroundColor': 'rgb(255,27,14)'}
                ),
                html.Div(
                    [dcc.Loading(html.H6(id="oilText",
                                         style={'color': 'white', 'font-weight': 'bold', 'fontSize': '3vh'}
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
        html.Marquee("Few days ago data source format was changed, accuracy after this line is compromised. "
                     "New update will be pushed on the weekend", dir='ltr',
                     style={'font-weight': 'bold', 'fontSize': '2vh', "margin-bottom": "10px"}),
        # html.Div(
        #     [
        #         html.Div(
        #             [dcc.Loading(html.H6(id="well_text",
        #                                  style={'color': 'white', 'font-weight': 'bold', 'fontSize': '4vh'}
        #                                  )),
        #              html.P("CONFIRMED",
        #                     style={'color': 'white', 'fontSize': '2vh'}
        #                     )],
        #             id="wells",
        #             className="mini_container",
        #             style={'backgroundColor': '#0099e5'}
        #         ),
        #         html.Div(
        #             [dcc.Loading(html.H6(id="gasText",
        #                                  style={'color': 'white', 'font-weight': 'bold', 'fontSize': '4vh'}
        #                                  )),
        #              html.P("RECOVERED",
        #                     style={'color': 'white', 'fontSize': '2vh'}
        #                     )],
        #             id="gas",
        #             className="mini_container",
        #             style={'backgroundColor': '#6cc644'}
        #         ),
        #         html.Div(
        #             [dcc.Loading(html.H6(id="waterText",
        #                                  style={'color': 'white', 'font-weight': 'bold', 'fontSize': '4vh'}
        #                                  )),
        #              html.P("DECEASED",
        #                     style={'color': 'white', 'fontSize': '2vh'}
        #                     )],
        #             id="water",
        #             className="mini_container",
        #             style={'backgroundColor': 'rgb(255,27,14)'}
        #         ),
        #         html.Div(
        #             [dcc.Loading(html.H6(id="oilText",
        #                                  style={'color': 'white', 'font-weight': 'bold', 'fontSize': '4vh'}
        #                                  )),
        #              html.P("TESTED",
        #                     style={'color': 'white', 'fontSize': '2vh'}
        #                     )],
        #             id="oil",
        #             className="mini_container",
        #             style={'backgroundColor': '#fbbc05'}
        #         ),
        #     ],
        #     className="row flex-display",
        # ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Loading(dash_table.DataTable(id='reg_table',
                                                         columns=[{'name': 'Province', 'id': 'province'},
                                                                  {'name': 'Confirmed', 'id': 'total_cases'},
                                                                  {'name': 'Recovered', 'id': 'total_recovered'},
                                                                  {'name': 'Deceased', 'id': 'total_mortality'}],
                                                         style_cell={
                                                             'textAlign': 'left',
                                                             'fontSize': '1.5vh',
                                                             'font-family': 'sans-serif',
                                                             'overflow': 'hidden',
                                                             'textOverflow': 'ellipsis',
                                                             'maxWidth': 0,
                                                         },
                                                         style_table={
                                                             'maxHeight': '700px',
                                                             'overflowY': 'scroll',
                                                             'border': 'thin lightgrey solid'
                                                         },
                                                         style_data={
                                                             'whiteSpace': 'normal',
                                                             'height': 'auto'
                                                         },
                                                         style_cell_conditional=[
                                                             {
                                                                 'if': {'column_id': 'province'},
                                                                 'padding-left': '10px'
                                                             },
                                                             {
                                                                 'if': {'column_id': 'total_cases'},
                                                                 'textAlign': 'center',
                                                                 'width': '20%'
                                                             },
                                                             {
                                                                 'if': {'column_id': 'total_recovered'},
                                                                 'textAlign': 'center',
                                                                 'width': '20%'
                                                             },
                                                             {
                                                                 'if': {'column_id': 'total_mortality'},
                                                                 'textAlign': 'center',
                                                                 'width': '20%'
                                                             }

                                                         ],
                                                         style_data_conditional=[
                                                             {
                                                                 'if': {'row_index': 'odd'},
                                                                 'backgroundColor': 'rgb(248, 248, 248)'
                                                             },
                                                             {
                                                                 'if': {'column_id': 'total_cases'},
                                                                 'backgroundColor': '#8ad8ff',
                                                                 'color': 'black',
                                                             },
                                                             {
                                                                 'if': {'column_id': 'total_recovered'},
                                                                 'backgroundColor': '#a6dc8e',
                                                                 'color': 'black',
                                                             },
                                                             {
                                                                 'if': {'column_id': 'total_mortality'},
                                                                 'backgroundColor': '#ff8680',
                                                                 'color': 'black',
                                                             },
                                                         ],
                                                         style_header={
                                                             'backgroundColor': 'rgb(230, 230, 230)',
                                                             'fontWeight': 'bold',
                                                         },
                                                         style_as_list_view=True,
                                                         )),
                        html.P(
                            "*Filtered by most Confirmed cases first",
                            className="control_label",
                        ),
                    ],
                    className="pretty_container four columns",
                    id="cross-filter-options",
                ),
                html.Div(
                    [
                        dcc.RadioItems(
                            id='radio_map',
                            options=[
                                {'label': 'Mapbox (Responsive)', 'value': 0},
                                {'label': 'Static Plot', 'value': 1}
                            ],
                            value=0,
                            inputStyle={"margin-right": "10px"},
                            labelStyle={'display': 'inline-block', "margin-right": "20px"},
                            style={'textAlign': 'center', 'padding-bottom': '5px'},
                            # className="pretty_container",
                        ),
                        html.Div(
                            html.Div(id='count_graph'),
                            id="countGraphContainer",
                            # className="pretty_container",
                            # style={'width': '100%'}
                        ),
                    ],
                    id="right-column",
                    className="pretty_container eight columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [html.P("Daily new cases by time",
                            className="control_label",
                            style={'textAlign': 'center', 'fontSize': '1.8vh'}, ),
                     dcc.Loading(dcc.Graph(id="main_graph", config=dict(displayModeBar=False)))],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [html.P("Top 15 Reason of Transmission (Travel to/Reason)",
                            className="control_label",
                            style={'textAlign': 'center', 'fontSize': '1.8vh'}),
                     dcc.Loading(dcc.Graph(id="individual_graph", config=dict(displayModeBar=False)))],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [
                        # html.P("Top 15 Reason of Transmission (Travel to/Reason)",
                        #        className="control_label",
                        #        style={'textAlign': 'center', 'fontSize': '1.8vh'}),
                        dcc.Loading(dash_table.DataTable(id='news_table',
                                                         columns=[{'name': 'NEWS: Latest Confirmed Case details',
                                                                   'id': 'text'}],
                                                         style_cell={
                                                             'textAlign': 'left',
                                                             'fontSize': '1.5vh',
                                                             'font-family': 'sans-serif',
                                                             'overflow': 'hidden',
                                                             'textOverflow': 'ellipsis',
                                                             'maxWidth': 0,
                                                         },
                                                         style_table={
                                                             'maxHeight': '500px',
                                                             'overflowY': 'scroll',
                                                             'border': 'thin lightgrey solid'
                                                         },
                                                         style_data={
                                                             'whiteSpace': 'normal',
                                                             'height': 'auto'
                                                         },
                                                         style_cell_conditional=[
                                                             {
                                                                 'if': {'column_id': 'text'},
                                                                 'padding-left': '10px'
                                                             },
                                                         ],
                                                         style_data_conditional=[
                                                             {
                                                                 'if': {'row_index': 'odd'},
                                                                 'backgroundColor': '#d7f2ff'
                                                             },
                                                             {
                                                                 'if': {'column_id': 'total_cases'},
                                                                 'backgroundColor': '#d7f2ff',
                                                                 'color': 'black',
                                                             },
                                                         ],
                                                         style_header={
                                                             'backgroundColor': '#d7f2ff',
                                                             'fontWeight': 'bold',
                                                             'textAlign': 'center',
                                                         },
                                                         # fixed_rows={'headers': True, 'data': 0},
                                                         style_as_list_view=True,
                                                         ))],
                    className="pretty_container six columns",
                ),
                # html.Div(
                #     [
                #         html.P("Case Count by City (type/select a city)",
                #                className="control_label",
                #                style={'textAlign': 'center', 'fontSize': '1.8vh'}),
                #         html.Div(
                #             [dcc.Dropdown(
                #                 id='city_dropdown_confirmed',
                #                 options=[{'label': i, 'value': i} for i in dropdown_cities_confirmed],
                #                 value='Ottawa',
                #                 className="dcc_controls",
                #                 placeholder='All Departments'
                #             ),
                #                 dcc.Loading(html.P(id='confirmed_city_text',
                #                                    style={'color': 'white', 'fontSize': '2vh', 'padding-top': '15px'}
                #                                    ))],
                #             id="welldss",
                #             className="mini_container",
                #             style={'backgroundColor': '#0099e5'}
                #         ),
                #         html.Div(
                #             [dcc.Dropdown(
                #                 id='city_dropdown_recovered',
                #                 options=[{'label': i, 'value': i} for i in dropdown_cities_recovered],
                #                 value='Ontario',
                #                 className="dcc_controls",
                #                 placeholder='All Departments'
                #             ),
                #                 dcc.Loading(html.P(id='recovered_city_text',
                #                                    style={'color': 'white', 'fontSize': '2vh', 'padding-top': '15px'}
                #                                    ))],
                #             id="gadss",
                #             className="mini_container",
                #             style={'backgroundColor': '#6cc644'}
                #         ),
                #         html.Div(
                #             [dcc.Dropdown(
                #                 id='city_dropdown_mortality',
                #                 options=[{'label': i, 'value': i} for i in dropdown_cities_mortality],
                #                 value='Ottawa',
                #                 className="dcc_controls",
                #                 placeholder='All Departments'
                #             ),
                #                 dcc.Loading(html.P(id='mortality_city_text',
                #                                    style={'color': 'white', 'fontSize': '2vh', 'padding-top': '15px'}
                #                                    ))],
                #             id="welldsds",
                #             className="mini_container",
                #             style={'backgroundColor': 'rgb(255,27,14)'}
                #         ),
                #     ],
                #     className="pretty_container six columns",
                # ),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)


@app.callback(
    [
        Output("well_text", "children"),
        Output("gasText", "children"),
        Output("oilText", "children"),
        Output("waterText", "children"),
    ],
    [Input("storage", "data")],
)
def update_text(data):
    try:
        dict_can = dict()
        url_updates = 'https://opendata.arcgis.com/datasets/bbb2e4f589ba40d692fab712ae37b9ac_2.geojson'
        with urllib.request.urlopen(url_updates) as url:
            data = json.loads(url.read().decode())

        for k, v in data.items():
            v = v
            for i in v:
                if 'Canada' in str(i):
                    dict_can = i
                    break
                else:
                    continue

        confirmed = dict_can.get('properties').get('Confirmed')
        deaths = dict_can.get('properties').get('Deaths')
        recovered = dict_can.get('properties').get('Recovered')
    except:
        confirmed = len(dfcases)
        recovered = functions.sumdf(dfrecovered, 'date_recovered', 'cumulative_recovered')
        deaths = len(dfmortality)
    # else:
    #     confirmed = 0
    #     recovered = 0
    #     deaths = 0

    total_testing = functions.sumdf(dftesting, 'date_testing', 'cumulative_testing')
    total_testing = functions.comma(int(total_testing))

    mortality_text = '{} ({})'.format(functions.comma(deaths), functions.get_percentage(deaths, recovered))
    recovered_text = '{} ({})'.format(functions.comma(int(recovered)), functions.get_percentage(recovered, deaths))
    return functions.comma(confirmed), recovered_text, total_testing, mortality_text


@app.callback(
    Output("reg_table", "data"),
    [Input("storage", "data")],
)
def make_count_figure(val):
    dff1 = dfcases[['province']]
    dff1 = dff1.groupby(['province']).province.agg('count').to_frame('total_cases').reset_index()
    dff1 = dff1.sort_values('total_cases', ascending=False)

    dff2 = dfrecovered[['province', 'date_recovered', 'cumulative_recovered']].copy()
    dff2['date_recovered'] = pd.to_datetime(dff2['date_recovered'])
    dff2 = dff2.sort_values(by='date_recovered', ascending=False)
    dff2 = dff2.drop_duplicates(subset=['province'], keep='first')
    dff2 = dff2.rename(columns={'cumulative_recovered': 'total_recovered'})
    dff2 = dff2[['province', 'total_recovered']]
    # dff2 = dff2.groupby(['province']).province.agg('count').to_frame('total_recovered').reset_index()

    dff3 = dfmortality[['province']]
    dff3 = dff3.groupby(['province']).province.agg('count').to_frame('total_mortality').reset_index()

    dff = pd.merge(dff1, dff2, how='left', on='province')
    dff = pd.merge(dff, dff3, how='left', on='province')
    dff = dff.fillna(0)

    data = dff.to_dict('rows')

    return data


# Selectors -> count graph
@app.callback(
    Output("count_graph", "children"),
    [Input("radio_map", "value")],
)
def make_count_figure(val):
    if val == 0:
        return dcc.Graph(figure=functions.gen_plot(dfcases), config=dict(displayModeBar=False))
    else:
        return html.Div([
            html.Img(
                src='data:image/png;base64,{}'.format(encoded_image.decode()),
                height=470,
                # style={
                #     'height': '60%',
                #     'width': '60%'
                # }
            )
        ], style={'textAlign': 'center'})


if __name__ == '__main__':
    app.run_server()
