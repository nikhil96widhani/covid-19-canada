import pandas as pd
import plotly.graph_objects as go
import numpy as np


def gendf(sheet):
    dff = pd.read_excel('./data/data (1).xlsx', sheet_name=sheet)
    dff = dff.dropna(axis=1, how='all')
    dff.columns = dff.iloc[2]
    dff = dff.iloc[3:]
    return dff


def sumdf(dff, dt_col, sum_col):
    dff[dt_col] = pd.to_datetime(dff[dt_col])
    dff = dff.sort_values(by=dt_col, ascending=False)
    dff = dff.drop_duplicates(subset=['province'], keep='first')

    dff = dff[dff[sum_col].notna()]
    total = dff[sum_col].sum()
    return total


def gen_plot(dffff):
    df = dffff[['province']].copy().reset_index()

    df2 = df.groupby(['province']).province.agg('count').to_frame('total_cases').reset_index()

    province = [{'province': 'Alberta', 'lat': 55.000000, 'lon': -115.000000},
                {'province': 'BC', 'lat': 53.726669, 'lon': -127.647621},
                {'province': 'Manitoba', 'lat': 53.760860, 'lon': -98.813873},
                {'province': 'NL', 'lat': 53.135509, 'lon': -57.660435},
                {'province': 'NWT', 'lat': 64.8255, 'lon': -124.8457},
                {'province': 'New Brunswick', 'lat': 46.498390, 'lon': -66.159668},
                {'province': 'Nova Scotia', 'lat': 45.000000, 'lon': -63.000000},
                {'province': 'Ontario', 'lat': 50.000000, 'lon': -85.000000},
                {'province': 'PEI', 'lat': 46.250000, 'lon': -63.000000},
                {'province': 'Ouebec', 'lat': 53.000000, 'lon': -70.000000},
                {'province': 'Repatriated', 'lat': 0, 'lon': 0},
                {'province': 'Saskatchewan', 'lat': 55.000000, 'lon': -106.000000},
                {'province': 'Yukon', 'lat': 64.2823, 'lon': -135.0000}, ]

    df3 = pd.DataFrame(province)

    df = pd.merge(df2, df3, on='province')
    df = df.dropna()
    df = df[~df.province.str.contains("Repatriated")]

    mapbox_access_token = 'pk.eyJ1IjoibmlraGlsOTZ3aWRoYW5pIiwiYSI6ImNrM3p4aW5nMjBhdGMzZXMxdjhndWYyczMifQ.zOzJZkhUYpyZQRfb1XNlmQ'

    df['total_cases_str'] = df['total_cases'].astype(str)
    df['text'] = df['province'] + '<br>' + \
                 'Total Cases: ' + df['total_cases_str']

    colour_scale = ['rgb(255,213,210)', 'rgb(255,194,191)', 'rgb(255,176,171)', 'rgb(255,157,151)', 'rgb(255,139,132)',
                    'rgb(255,120,112)', 'rgb(255,102,93)', 'rgb(255,83,73)', 'rgb(255,64,53)', 'rgb(255,46,34)',
                    'rgb(255,27,14)']

    df = df.sort_values('total_cases', ascending=True)
    df.index = np.arange(1, len(df) + 1)
    df['bubble_size'] = 8 * df.index.values
    site_size = df.bubble_size
    site_lat = df.lat
    site_lon = df.lon
    locations_name = df.text

    df['colour_scale'] = colour_scale
    site_colour = df.colour_scale

    fig = go.Figure()

    fig.add_trace(go.Scattermapbox(
        lat=site_lat,
        lon=site_lon,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=site_size,
            color=site_colour,
            opacity=0.9
        ),
        text=locations_name,
        hoverinfo='text'
    ))

    fig.add_trace(go.Scattermapbox(
        lat=site_lat,
        lon=site_lon,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=8,
            color='rgb(242, 177, 172)',
            # opacity=0.7
        ),
        hoverinfo='none'
    ))

    fig.update_layout(
        # title="Total Covid-19 Cases by Province",
        autosize=True,
        hovermode='closest',
        showlegend=False,

        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=55.875311,
                lon=-97.471701
            ),
            pitch=0,
            zoom=3,
            style='light'
        ),
    )
    fig.update_layout(
        title={
            'text': "Total Cases by Province",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


def comma(num):
    '''Add comma to every 3rd digit. Takes int or float and
    returns string.'''
    if type(num) == int:
        return '{:,}'.format(num)
    elif type(num) == float:
        return '{:,.2f}'.format(num)  # Rounds to 2 decimal places
    else:
        return num
