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

data_votazione = '2018-06-01' # Specifichiamo la data delle votazioni considerate
id_votazione = 'Jun_2018' # Specifichiamo il/gli id della/e votazione/i considerate
ruolo = 'Sen' # Utile per specificare la cartella
path = 'Networks/TimeIntervals/'+ruolo+'/'
sns.set_style('whitegrid') # Impostiamo il tema di Seaborn
sns.despine() # Removing top and right axes spines
sns.set_context("paper")
#groups = ['M5S', 'LSP', 'FI', 'PD', 'FDI', 'LEU', 'MISTO']
#cabinets = ['Conte I', 'Conte II', 'Draghi']
groups = ['M5S', 'FI', 'PD', 'FDI', 'LSP-PSDAZ', 'AUT', 'MISTO']
#groups = ['M5S', 'LSP', 'FI', 'PD', 'IV', 'FDI', 'LEU', 'MISTO']
#groups = ['M5S', 'FI', 'PD', 'FDI', 'LSP-PSDAZ', 'AUT', 'IV-PSI', 'MISTO']


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

df_single_distance = pd.read_csv(path+'SingleDistanceFromGroup_'+data_votazione+'_'+id_votazione+'.csv')
group_list = list(df_single_distance.IdGruppo.unique())
# plt.figure(figsize=(10,10))
# sns.violinplot(data=df_single_distance, x='IdGruppo', y='Distance', hue='IdGruppo', palette=color_mapping_by_id)
# plt.legend([],[], frameon=False)
# plt.xticks(np.arange(len(group_list)), groups, rotation=45, fontsize=10)
# plt.ylabel('Distance from the Group')
# plt.xlabel('')
# plt.ylim(0, 1.1)
# plt.tight_layout
# plt.savefig(path+'LoyaltyViolinPlot_'+data_votazione+'_'+id_votazione+'_'+ruolo+'.png')#, dpi=1000)

plt.figure(figsize=(10,10))
sns.boxplot(data=df_single_distance, x='IdGruppo', y='Distance', palette=color_mapping_by_id)
plt.legend([],[], frameon=False)
plt.xticks(np.arange(len(group_list)), groups, rotation=45, fontsize=25, fontweight='bold')
plt.yticks(fontsize=25, fontweight='bold')
plt.ylabel('Distance from the Group', fontsize=30, fontweight='bold')
plt.xlabel('')
plt.ylim(0.5, 1)
plt.tight_layout()
plt.savefig(path+'LoyaltyBoxPlot_'+data_votazione+'_'+id_votazione+'_'+ruolo+'.png', dpi=200)