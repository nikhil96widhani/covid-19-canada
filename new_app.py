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
import pandas as pd
import requests
import time
now = time.strftime('%d%m%Y%H%M%S')
url_ctv = 'https://www.ctvnews.ca/health/coronavirus/tracking-every-case-of-covid-19-in-canada-1.4852102'
html_ctv = requests.get(url_ctv).content
df_list_ca = pd.read_html(html_ctv)
df_ca = df_list_ca[0:2]
df_bc = df_list_ca[2:5]
df_ab = df_list_ca[5:8]
df_sk = df_list_ca[8:11]
df_mb = df_list_ca[11:14]
df_on = df_list_ca[14:17]
df_qc = df_list_ca[17:20]
df_nb = df_list_ca[20:23]
df_ns = df_list_ca[23:26]
df_pe = df_list_ca[26:29]
df_nf = df_list_ca[29:32]


# isolate test number from each table - there has got to be a better way
ca_t = df_ca[1]
ca_t.to_csv('bc_t.csv')
ca_t1 = pd.read_csv('bc_t.csv')
ca_tests = ca_t1['Administered'].values
