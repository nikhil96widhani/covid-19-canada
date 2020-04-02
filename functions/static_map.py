#%%
import matplotlib.pyplot as plt
import geopandas
import pandas as pd
from functions import load_data
from functions import functions

can = geopandas.read_file('maps/lpr_000b16a_e.shp')

df = functions.gendf('Cases')[['province']]
df = df.groupby(['province']).province.agg('count').to_frame('total_cases').reset_index()
df = df.sort_values('total_cases', ascending=False)

province = [{'province': 'Alberta', 'PRNAME': 'Alberta'},
            {'province': 'BC', 'PRNAME': 'British Columbia / Colombie-Britannique'},
            {'province': 'Manitoba', 'PRNAME': 'Manitoba'},
            {'province': 'NL', 'PRNAME': 'Newfoundland and Labrador / Terre-Neuve-et-Labrador'},
            {'province': 'NWT', 'PRNAME': 'Northwest Territories / Territoires du Nord-Ouest'},
            {'province': 'New Brunswick', 'PRNAME': 'New Brunswick / Nouveau-Brunswick'},
            {'province': 'Nova Scotia', 'PRNAME': 'Nova Scotia / Nouvelle-Écosse'},
            {'province': 'Ontario', 'PRNAME': 'Ontario'},
            {'province': 'PEI', 'PRNAME': 'Prince Edward Island / Île-du-Prince-Édouard'},
            {'province': 'Quebec', 'PRNAME': 'Quebec / Québec'},
            {'province': 'Saskatchewan', 'PRNAME': 'Saskatchewan'},
            {'province': 'Yukon', 'PRNAME': 'Yukon'}, ]

df = pd.merge(df, pd.DataFrame(province), on='province')
df = df[['PRNAME', 'total_cases']]

merged = can.set_index('PRNAME').join(df.set_index('PRNAME'))
# merged = can.set_index('total_cases')

# -----------------
# set a variable that will call whatever column we want to visualise on the map
variable = 'total_cases'

# set the range for the choropleth
vmin, vmax = 0, df['total_cases'].max()

# create figure and axes for Matplotlib
fig, ax = plt.subplots(1, figsize=(12, 8))

# create map
merged.plot(column=variable, cmap='YlOrRd', linewidth=0.8, ax=ax, edgecolor='0.8')

# Now we can customise and add annotations

# remove the axis
ax.axis('off')

# add a title
# ax.set_title('Preventable death rate in London', \
#              fontdict={'fontsize': '25',
#                        'fontweight': '3'})
bbox_props = dict(boxstyle="round4,pad=0.3", fc="dodgerblue",
                  # ec="r",
                  lw=1
                  )
e = 0
for i, geo in merged.centroid.iteritems():
    ax.annotate(s=int(merged.iloc[e]['total_cases']), xy=[geo.x, geo.y],
                xytext=(float(geo.x) - 100000, geo.y),
                color="white", size=16, bbox=bbox_props)
    e = e + 1
    if len(df) == e:
        break

# ax.annotate('Source: London Datastore, 2014',
#             xy=(0.1, .08), xycoords='figure fraction',
#             horizontalalignment='left', verticalalignment='top',
#             fontsize=10, color='#555555')

# Create colorbar as a legend
# sm = plt.cm.ScalarMappable(cmap='YlOrRd', norm=plt.Normalize(vmin=vmin, vmax=vmax))
# sm._A = []
# cbar = fig.colorbar(sm)

# this will save the figure as a high-res png. you can also save as svg
fig.show()
fig.savefig('testmap.png',
            bbox_inches="tight", pad_inches=0,
            dpi=120)
