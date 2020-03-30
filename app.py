import pathlib
import dash
import pandas as pd
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from functions import load_data
from functions import functions
import os
from datetime import datetime
import dash_table
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()
# load_data.run_check()
########### Initiate the app
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server
app.title = 'Covid-19 Canada'
#


dfcases = functions.gendf('Cases')
dfmortality = functions.gendf('Mortality')
dfrecovered = functions.gendf('Recovered')
dftesting = functions.gendf('Testing')

dropdown_cities_confirmed = dfcases['health_region'].unique()
dropdown_cities_recovered = dfrecovered['province'].unique()
dropdown_cities_mortality = dfmortality['health_region'].unique()

file = "./data/data (1).xlsx"
time = datetime.fromtimestamp(os.path.getctime(file))

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
                                    "Last Updated at {} ".format(str(time)[:-10]),
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
                    id="wells",
                    className="mini_container",
                    style={'backgroundColor': '#0099e5'}
                ),
                html.Div(
                    [dcc.Loading(html.H6(id="gasText",
                                         style={'color': 'white', 'font-weight': 'bold', 'fontSize': '4vh'}
                                         )),
                     html.P("RECOVERED",
                            style={'color': 'white', 'fontSize': '2vh'}
                            )],
                    id="gas",
                    className="mini_container",
                    style={'backgroundColor': '#6cc644'}
                ),
                html.Div(
                    [dcc.Loading(html.H6(id="waterText",
                                         style={'color': 'white', 'font-weight': 'bold', 'fontSize': '4vh'}
                                         )),
                     html.P("DECEASED",
                            style={'color': 'white', 'fontSize': '2vh'}
                            )],
                    id="water",
                    className="mini_container",
                    style={'backgroundColor': 'rgb(255,27,14)'}
                ),
                html.Div(
                    [dcc.Loading(html.H6(id="oilText",
                                         style={'color': 'white', 'font-weight': 'bold', 'fontSize': '4vh'}
                                         )),
                     html.P("TESTED",
                            style={'color': 'white', 'fontSize': '2vh'}
                            )],
                    id="oil",
                    className="mini_container",
                    style={'backgroundColor': '#fbbc05'}
                ),
            ],
            className="row flex-display",
        ),
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
                                                             'fontSize': 16,
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
                            "Filtered by most Confirmed cases first",
                            className="control_label",
                        ),
                    ],
                    className="pretty_container four columns",
                    id="cross-filter-options",
                ),
                html.Div(
                    [
                        html.Div(
                            [dcc.Loading(dcc.Graph(id="count_graph"))],
                            id="countGraphContainer",
                            className="pretty_container",
                            # style={'width': '100%'}
                        ),
                    ],
                    id="right-column",
                    className="eight columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [html.P("New cases by time",
                            className="control_label",
                            style={'textAlign': 'center', 'fontSize': '1.8vh'}, ),
                     dcc.Loading(dcc.Graph(id="main_graph"))],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [html.P("Top 15 Reason of Transmission (Travel to/Reason)",
                            className="control_label",
                            style={'textAlign': 'center', 'fontSize': '1.8vh'}),
                     dcc.Loading(dcc.Graph(id="individual_graph"))],
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
                                                             'fontSize': 16,
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
                html.Div(
                    [
                        html.P("Case Count by City (type/select a city)",
                               className="control_label",
                               style={'textAlign': 'center', 'fontSize': '1.8vh'}),
                        html.Div(
                            [dcc.Dropdown(
                                id='city_dropdown_confirmed',
                                options=[{'label': i, 'value': i} for i in dropdown_cities_confirmed],
                                value='Ottawa',
                                className="dcc_controls",
                                placeholder='All Departments'
                            ),
                                dcc.Loading(html.P(id='confirmed_city_text',
                                                   style={'color': 'white', 'fontSize': '2vh', 'padding-top': '15px'}
                                                   ))],
                            id="welldss",
                            className="mini_container",
                            style={'backgroundColor': '#0099e5'}
                        ),
                        html.Div(
                            [dcc.Dropdown(
                                id='city_dropdown_recovered',
                                options=[{'label': i, 'value': i} for i in dropdown_cities_recovered],
                                value='Ontario',
                                className="dcc_controls",
                                placeholder='All Departments'
                            ),
                                dcc.Loading(html.P(id='recovered_city_text',
                                                   style={'color': 'white', 'fontSize': '2vh', 'padding-top': '15px'}
                                                   ))],
                            id="gadss",
                            className="mini_container",
                            style={'backgroundColor': '#6cc644'}
                        ),
                        html.Div(
                            [dcc.Dropdown(
                                id='city_dropdown_mortality',
                                options=[{'label': i, 'value': i} for i in dropdown_cities_mortality],
                                value='Ottawa',
                                className="dcc_controls",
                                placeholder='All Departments'
                            ),
                                dcc.Loading(html.P(id='mortality_city_text',
                                                   style={'color': 'white', 'fontSize': '2vh', 'padding-top': '15px'}
                                                   ))],
                            id="welldsds",
                            className="mini_container",
                            style={'backgroundColor': 'rgb(255,27,14)'}
                        ),
                    ],
                    className="pretty_container six columns",
                ),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)


# Selectors -> well text
@app.callback(
    Output("well_text", "children"),
    [Input("storage", "data")],
)
def update_well_text(data):
    total_cases = functions.comma(len(dfcases))
    return total_cases


@app.callback(
    [
        Output("gasText", "children"),
        Output("oilText", "children"),
        Output("waterText", "children"),
    ],
    [Input("storage", "data")],
)
def update_text(data):
    total_recovered = functions.sumdf(dfrecovered, 'date_recovered', 'cumulative_recovered')
    total_recovered = functions.comma(total_recovered)
    total_testing = functions.sumdf(dftesting, 'date_testing', 'cumulative_testing')
    total_testing = functions.comma(total_testing)

    return total_recovered, total_testing, len(dfmortality)


# Selectors -> count graph
@app.callback(
    Output("count_graph", "figure"),
    [Input("storage", "data")],
)
def make_count_figure(val):
    return functions.gen_plot(dfcases)


# Selectors -> count graph
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
    Output("main_graph", "figure"),
    [Input("storage", "data")],
)
def make_line_chart(val):
    dff1 = dfcases[['date_report']].copy()
    dff1 = dff1.groupby('date_report').date_report.agg('count').to_frame('total_cases').reset_index()

    dff2 = dfmortality[['date_death_report']].copy()
    dff2 = dff2.groupby('date_death_report').date_death_report.agg('count').to_frame('total_mortality').reset_index()

    dff3 = dfrecovered[['date_recovered', 'cumulative_recovered']].copy()
    dff3 = dff3.groupby('date_recovered', as_index=False).agg({'cumulative_recovered': 'sum'})

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dff1.date_report, y=dff1['total_cases'], name="Confirmed",
                             line_color='deepskyblue'))

    fig.add_trace(go.Scatter(x=dff2.date_death_report, y=dff2['total_mortality'], name="mortality",
                             line_color='tomato'))

    fig.add_trace(go.Scatter(x=dff3.date_recovered, y=dff3['cumulative_recovered'], name="Recovered",
                             line_color='green'))

    # fig.update_layout(xaxis_rangeslider_visible=True)
    fig.update_layout(margin={"r": 10, "t": 80, "l": 10, "b": 10})
    fig.update_layout(
        # width=450,
        # height=450,
        plot_bgcolor='rgb(255, 255, 255)')
    return fig


@app.callback(
    Output("individual_graph", "figure"),
    [Input("storage", "data")],
)
def make_pie_chart(val):
    dff = pd.DataFrame(columns=['reason'])
    dff['reason'] = dfcases['travel_history_country'].combine_first(dfcases['locally_acquired'])
    dff = dff['reason'].str.split(',', expand=True).stack().reset_index(level=1, drop=True).to_frame()
    dff = dff.rename(columns={0: 'reason'})
    dff['reason'] = dff['reason'].replace({'Close contact': 'Close Contact'})
    dff = dff.groupby('reason').reason.agg('count').to_frame('total').reset_index()
    dff = dff.sort_values(by='total', ascending=False)
    dff = dff.head(15)

    fig = px.pie(dff, values='total', names='reason',
                 hover_data=['total'], labels={'total': 'total cases'})
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(margin={"r": 10, "t": 35, "l": 10, "b": 10},
                      showlegend=False  # bring leadgend side
                      )
    return fig


@app.callback(
    Output("news_table", "data"),
    [Input("storage", "data")],
)
def make_count_figure(val):
    dff = dfcases[
        ['case_id', 'age', 'sex', 'health_region', 'date_report', 'travel_history_country', 'locally_acquired']]
    dff = dff.sort_values(by=['case_id'], ascending=False)
    dff = dff.dropna(subset=['age', 'sex', 'health_region'], how='all')
    dff['reason'] = dff['travel_history_country'].combine_first(dff['locally_acquired'])
    dff['reason'] = dff['reason'].fillna("Unknown")
    dff['text'] = 'A person of ' + dff['sex'].astype(str) + ' gender' + ' who was in their ' \
                  + dff['age'].astype(str) + ' age group ' + ' from ' + dff['health_region'].astype(str) + \
                  ' acquired virus from travel to/reason of : ' + dff['reason'].astype(str)
    dff2 = dff.head(100)
    data = dff2.to_dict('rows')

    return data


@app.callback(
    Output("confirmed_city_text", "children"),
    [Input("city_dropdown_confirmed", "value")],
)
def confirmed_city(value):
    dff = dfcases[['health_region']]
    dff = dff.groupby('health_region').health_region.agg('count').to_frame('total_cases').reset_index()
    dff = dff[dff['health_region'].str.contains(value)].reset_index()
    if len(dff) > 0:
        count = dff.iloc[0]['total_cases']
    else:
        count = 'No Data for'

    return '{} CONFIRMED cases in {}'.format(count, value)


@app.callback(
    Output("recovered_city_text", "children"),
    [Input("city_dropdown_recovered", "value")],
)
def recovered_city(value):
    dff = dfrecovered[['date_recovered', 'province', 'cumulative_recovered']]
    dff = dff.fillna(0)
    dff = dff.sort_values(by='date_recovered', ascending=False)
    dff = dff.drop_duplicates(subset='province', keep='first', inplace=False)
    dff = dff[dff['province'].str.contains(value)].reset_index()
    if len(dff) > 0:
        count = dff.iloc[0]['cumulative_recovered']
    else:
        count = 'No Data for'

    return '{} RECOVERED cases in {}'.format(count, value)


@app.callback(
    Output("mortality_city_text", "children"),
    [Input("city_dropdown_mortality", "value")],
)
def mortality_city(value):
    dff = dfmortality[['health_region']]
    dff = dff.groupby('health_region').health_region.agg('count').to_frame('total_cases').reset_index()
    dff = dff[dff['health_region'].str.contains(value)].reset_index()
    if len(dff) > 0:
        count = dff.iloc[0]['total_cases']
    else:
        count = 'No Data for'

    return '{} DEATHS in {}'.format(count, value)


if __name__ == '__main__':
    app.run_server()
