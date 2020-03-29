import pandas as pd

dffff = pd.read_excel('./data/data.xlsx', sheet_name='Cases')
dffff = dffff.dropna(axis=1, how='all')
dffff.columns = dffff.iloc[2]
dffff = dffff.iloc[3:]

# dffff['date_recovered'] = pd.to_datetime(dffff['date_recovered'])
# dffff = dffff.sort_values(by='date_recovered', ascending=False)
# dffff = dffff.drop_duplicates(subset=['province'], keep='first')
#
#
# dffff = dffff[dffff['cumulative_recovered'].notna()]
# Total = dffff['cumulative_recovered'].sum()
print(dffff.head(10))

a = str(pd.to_datetime('today'))

#%%
# df = dffff[['province']].copy().reset_index()
#
# df2 = df.groupby(['province']).province.agg('count').to_frame('total_cases').reset_index()
#
# province = [{'province': 'Alberta', 'lat': 55.000000, 'lon': -115.000000},
#          {'province': 'BC', 'lat': 53.726669, 'lon': -127.647621},
#          {'province': 'Manitoba', 'lat': 53.760860, 'lon': -98.813873},
#          {'province': 'NL', 'lat': 53.135509, 'lon': -57.660435},
#          {'province': 'NWT', 'lat': 64.8255, 'lon': -124.8457},
#          {'province': 'New Brunswick', 'lat': 46.498390, 'lon': -66.159668},
#          {'province': 'Nova Scotia', 'lat': 45.000000, 'lon': -63.000000},
#          {'province': 'Ontario', 'lat': 50.000000, 'lon': -85.000000},
#          {'province': 'PEI', 'lat': 46.250000, 'lon': -63.000000},
#          {'province': 'Ouebec', 'lat': 53.000000, 'lon': -70.000000},
#          {'province': 'Repatriated', 'lat': 0, 'lon': 0},
#          {'province': 'Saskatchewan', 'lat': 55.000000, 'lon': -106.000000},
#          {'province': 'Yukon', 'lat': 64.2823, 'lon': -135.0000},]
#
# df3 = pd.DataFrame(province)
#
# df = pd.merge(df2, df3, on='province')
#


#%%
# import plotly.express as px
# px.set_mapbox_access_token('pk.eyJ1IjoibmlraGlsOTZ3aWRoYW5pIiwiYSI6ImNrM3p4aW5nMjBhdGMzZXMxdjhndWYyczMifQ.zOzJZkhUYpyZQRfb1XNlmQ')
# df= df.dropna()
# df = df[~df.province.str.contains("Repatriated")]
# fig = px.scatter_mapbox(df, lat="lat", lon="lon",color="total_cases", size=df.index,
#                   color_continuous_scale=px.colors.sequential.matter, size_max=50, zoom=4)
# fig.show()

#%%
# import plotly.graph_objects as go
# import numpy as np
# import pandas as pd
#
# mapbox_access_token = 'pk.eyJ1IjoibmlraGlsOTZ3aWRoYW5pIiwiYSI6ImNrM3p4aW5nMjBhdGMzZXMxdjhndWYyczMifQ.zOzJZkhUYpyZQRfb1XNlmQ'
#
# site_lat = df.lat
# site_lon = df.lon
#
# df['total_cases_str'] = df['total_cases'].astype(str)
# df['text'] = df['province'] + '<br>' + \
#     'Total Cases: ' + df['total_cases_str']
#
# locations_name = df.text
#
# colour_scale = ['rgb(255,213,210)', 'rgb(255,194,191)', 'rgb(255,176,171)', 'rgb(255,157,151)', 'rgb(255,139,132)',
#                 'rgb(255,120,112)', 'rgb(255,102,93)', 'rgb(255,83,73)', 'rgb(255,64,53)', 'rgb(255,46,34)',
#                 'rgb(255,27,14)']
#
# df = df.sort_values('total_cases', ascending=True)
# df.index = np.arange(1,len(df)+1)
# df['bubble_size'] = 16 * df.index.values
# site_size = df.bubble_size
#
# df['colour_scale'] = colour_scale
# site_colour = df.colour_scale
#
# fig = go.Figure()
#
# fig.add_trace(go.Scattermapbox(
#         lat=site_lat,
#         lon=site_lon,
#         mode='markers',
#         marker=go.scattermapbox.Marker(
#             size=site_size,
#             color=site_colour,
#             opacity=0.7
#         ),
#         text=locations_name,
#         hoverinfo='text'
#     ))
#
# fig.add_trace(go.Scattermapbox(
#         lat=site_lat,
#         lon=site_lon,
#         mode='markers',
#         marker=go.scattermapbox.Marker(
#             size=8,
#             color='rgb(242, 177, 172)',
#             opacity=0.7
#         ),
#         hoverinfo='none'
#     ))
#
# fig.update_layout(
#     autosize=True,
#     hovermode='closest',
#     showlegend=False,
#     mapbox=dict(
#         accesstoken=mapbox_access_token,
#         bearing=0,
#         center=dict(
#             lat=58.995311,
#             lon=-99.969179
#         ),
#         pitch=0,
#         zoom=3,
#         style='light'
#     ),
# )
#
# fig.show()


#%%
# import plotly.graph_objects as go
#
# df = dffff
# df= df[['date_report']].copy()
# df['sum'] = 1
# df = df.groupby('date_report').date_report.agg('count').to_frame('total_mortality').reset_index()
#
#
# fig = go.Figure()
# fig.add_trace(go.Scatter(x=df.date_report, y=df['total_mortality'], name="mortality",
#                          line_color='deepskyblue'))
#
# fig.add_trace(go.Scatter(x=df.date_report, y=df['total_mortality'], name="mortality",
#                          line_color='deepskyblue'))
# fig.update_layout(title_text='Time Series with Rangeslider',
#                   xaxis_rangeslider_visible=True)
# fig.update_layout(width=450, height=450, plot_bgcolor='rgb(255, 255, 255)')
# fig.show()


#%%
# import plotly.express as px
# df = pd.DataFrame(columns=['reason'])
# df['reason'] = dffff['travel_history_country'].combine_first(dffff['locally_acquired'])
# df = df['reason'].str.split(',', expand=True).stack().reset_index(level=1,drop=True).to_frame()
# df = df.rename(columns={0: 'reason'})
# df = df.groupby('reason').reason.agg('count').to_frame('total').reset_index()
#
# fig = px.pie(df, values='total', names='reason')
# fig.update_traces(textposition='inside')
# fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
# fig.show()