from matplotlib import colors
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from datetime import date
import numpy as np
import plotly.express as px
from matplotlib.patches import Patch
from plotly.express.colors import qualitative
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from math import pi

ruolo = 'Sen' # Utile per specificare la cartella
path = 'Networks/TimeIntervals/'+ruolo+'/' # Path in cui si trova il csv e dove verrà salvato il png dei plot
id_votazione = 'Jun_2018' # Specifichiamo il/gli id della/e votazione/i considerate
sns.set_theme() # Impostiamo il tema di Seaborn
sns.despine() # Removing top and right axes spines
sns.set_context("paper")
#groups = ['M5S', 'LSP', 'FI', 'PD', 'IV', 'FDI', 'LEU', 'MISTO']
cabinets = ['Conte I', 'Conte II', 'Draghi']

color_mapping_by_id = {0: 'yellow',
1:'green',
2:'blue',
3:'royalblue',
4:'red',
5:'deeppink',
6:'black',
7:'darkred',
8:'green',
9:'lightsalmon',
10:'deeppink',
11:'aquamarine',
12:'grey'
}

color_mapping_by_sigla = {'M5S': 'yellow',
'LSP':'green',
'FI':'blue',
'CI':'royalblue',
'PD':'red',
'IV':'deeppink',
'FDI':'black',
'LEU':'darkred',
'LSP-PSDAZ':'green',
'AUT':'lightsalmon',
'IV-PSI':'deeppink',
'EURCD':'aquamarine',
'MISTO':'grey'
}

sigle = {0: 'M5S',
1:'LSP',
2:'FI',
3:'CI',
4:'PD',
5:'IV',
6:'FDI',
7:'LEU',
8:'LSP-PSDAZ',
9:'AUT',
10:'IV-PSI',
11:'EURCD',
12:'MISTO'
}

df_intergroup_distance = pd.read_csv(path+'IntergroupsDistanceReadyToPlot_'+id_votazione+'_'+ruolo+'.csv')
#df_intergroup_distance = pd.read_csv(path+'SinglePG_IntergroupDistance.csv')
df_intergroup_distance = df_intergroup_distance.replace(sigle)
df = pd.pivot_table(data=df_intergroup_distance, index=['Gr1'], columns=['Gr2'], values='Distance')
group_list = list(df_intergroup_distance['Gr1'].unique())
df = df.reset_index()


# ------- PART 1: Define a function that do a plot for one line of the dataset!
 
def make_spider( row, title, color):

    # number of variable
    categories=list(df)[1:]
    N = len(categories)

    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    # Initialise the spider plot
    ax = plt.subplot(3,3,row+1, polar=True, )

    # If you want the first axis to be on top:
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)

    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], categories, color='black', size=25, weight='bold')

    # Draw ylabels
    ax.set_rlabel_position(0)
    ax.set_rmin(0)
    plt.yticks([0.2, 0.4, 0.6, 0.8], ['0.2', '0.4', '0.6', '0.8'], color="black", size=25, weight='bold')
    plt.ylim(0,1)

    # Ind1
    values=df.loc[row].drop('Gr1').values.flatten().tolist()
    values += values[:1]
    ax.scatter(angles, values, color=color, s = 80)
    ax.vlines(angles, 0, values, color=color, linewidth=5, linestyle='solid')
    #ax.plot(angles, values, color=color, linewidth=3, linestyle='solid')
    

    # Add a title
    plt.title(title, size=30, color=color, y=1.1, weight='bold')

    
# ------- PART 2: Apply the function to all individuals
# initialize the figure
# my_dpi=96
# plt.figure(figsize=(1000/my_dpi, 1000/my_dpi/2.5), dpi=my_dpi)
# plt.figure(figsize=(20,20))
 
# # Create a color palette:
# my_palette = [color for color in color_mapping_by_sigla.values()]
 
# # Loop to plot
# for row in range(0, len(df.index)):
#     make_spider(row=row, title=str(df.at[row, 'Gr1']), color=color_mapping_by_sigla[df.at[row, 'Gr1']])

# plt.tight_layout()
# plt.savefig(path+'IntergroupsDistancePolarPlots_'+id_votazione+'_'+ruolo+'.png', dpi=200)