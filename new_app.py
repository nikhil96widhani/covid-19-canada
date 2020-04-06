# %%
import pandas as pd
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# %%
url_confirmed = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
url_recovered = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'
url_deaths = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
fips = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/UID_ISO_FIPS_LookUp_Table.csv'

dfConfirmed = pd.read_csv(url_confirmed)
dfConfirmed = dfConfirmed[dfConfirmed['Country/Region'] == 'Canada'].reset_index(drop=True)

dfRecovered = pd.read_csv(url_recovered)
dfRecovered = dfRecovered[dfRecovered['Country/Region'] == 'Canada'].reset_index(drop=True)

dfDeaths = pd.read_csv(url_deaths)
dfDeaths = dfDeaths[dfDeaths['Country/Region'] == 'Canada'].reset_index(drop=True)

dfFips = pd.read_csv(fips)
dfFips = dfFips[dfFips['Country_Region'] == 'Canada'].reset_index(drop=True)
dfFips['test'] = 'MN'

url_updates = 'https://opendata.arcgis.com/datasets/bbb2e4f589ba40d692fab712ae37b9ac_2.geojson'
import geopandas as gpd
import requests
data = requests.get('https://opendata.arcgis.com/datasets/bbb2e4f589ba40d692fab712ae37b9ac_2.geojson')
gdf = gpd.GeoDataFrame(url_updates)
gdf.head()
# %%
