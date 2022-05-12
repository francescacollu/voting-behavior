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

ruolo = 'Dep' # Utile per specificare la cartella
path = 'Networks/TimeIntervals/'+ruolo+'/'
sns.set_style('whitegrid') # Impostiamo il tema di Seaborn
#sns.despine() # Removing top and right axes spines
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

df = pd.read_csv(path+'GroupCohesion_General.csv')
plt.figure(figsize=(10,10))
ax = plt.axes()
sns.scatterplot(data=df, x='DataVotazione', y='GroupCohesion', hue='IdGruppo', palette=color_mapping_by_id, legend=False, size='GroupSize', sizes=(100, 1000), ax=ax)
sns.lineplot(data=df, x='DataVotazione', y='GroupCohesion', hue='IdGruppo', palette=color_mapping_by_id, legend=False,linewidth=6, markers=False, style=True, dashes=[(2,2)], ax=ax)
patches = [Patch(color=v, label=k) for k, v in color_mapping_by_id.items()]
plt.xticks(np.arange(len(cabinets)), cabinets, fontsize=20, fontweight='bold')
plt.xticks(fontsize=25, fontweight='bold')
plt.yticks(fontsize=25, fontweight='bold')
plt.xlabel('')
plt.ylabel('Group Cohesion', fontsize=30, fontweight='bold')
plt.ylim(0.7, 1.01)
plt.savefig(path+'CoherenceGroupEvolution_'+ruolo+'.png', dpi=200)