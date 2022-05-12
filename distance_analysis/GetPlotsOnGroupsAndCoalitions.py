from itertools import groupby
from random import randint
from matplotlib import colors
import pandas as pd
from sqlalchemy import create_engine
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from datetime import date
import numpy as np
import plotly.express as px
from matplotlib.patches import Patch
import csv
import math
from scipy.optimize import fmin

engine = create_engine('mysql+mysqlconnector://root:Fiorentino68*@127.0.0.1:3306/VotingBehavior')
ruolo = 'Sen' # Utile per specificare la cartella
data_votazione = '2021-03-01' # Specifichiamo la data delle votazioni considerate
id_votazione = '13Feb_23Mar_2021' # Specifichiamo il/gli id della/e votazione/i considerate
path = 'Networks/TimeIntervals/'+ruolo+'/'
sns.set_theme() # Impostiamo il tema di default di Seaborn
groups = ['M5S', 'LSP', 'FI', 'PD', 'IV', 'FDI', 'LEU', 'MISTO']
sns.set_style('whitegrid') # Impostiamo il tema di Seaborn
#sns.despine() # Removing top and right axes spines
sns.set_context("paper")

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

#Histogram of distances
# distances = pd.read_excel(path+'NormalizedDistanceMatrix_'+data_votazione+'_'+id_votazione+'.xlsx')
# distances_array = np.triu(distances.iloc[:, 1:].to_numpy(), 1)
# distances_array = np.concatenate(distances_array)
# ax = sns.histplot(data=distances_array, legend=False, binwidth=0.05)
# ax.set(xlim=(0,1))
# plt.savefig(path+'HistNormalizedDistances_'+data_votazione+'_'+id_votazione+'_'+ruolo+'.png')

# Plots of group cohesion
# df_group_cohesion = pd.read_csv(path+'GroupCohesion_'+data_votazione+'_'+id_votazione+'.csv')
# group_list = list(df_group_cohesion.IdGruppo.unique())
# plt.figure(figsize=(10,10))
# sns.catplot(data=df_group_cohesion, x='IdGruppo', y='GroupCohesion', hue='IdGruppo', palette=color_mapping_by_id, legend=False, s=10)
# patches = [Patch(color=v, label=k) for k, v in color_mapping_by_id.items()]
# plt.xticks(np.arange(len(group_list)), groups, rotation=45, fontsize=10)
# plt.xlabel('')
# plt.tight_layout
# plt.savefig(path+'GroupCohesion_'+data_votazione+'_'+id_votazione+'_'+ruolo+'.png')



# Run only after the previous block
# df_intergroup_distance = pd.read_csv(path+'IntergroupsDistanceReadyToPlot_'+id_votazione+'_'+ruolo+'.csv')
# group_list = list(df_intergroup_distance['Gr1'].unique())
# group_list = group_list+list(df_intergroup_distance['Gr2'].unique())
# group_list = list(set(group_list))
# plt.figure(figsize=(10,10))
# patches = [Patch(color=v, label=k) for k, v in color_mapping_by_id.items()]
# sns.barplot(x='Gr1', y='Distance', hue='Gr2', data=df_intergroup_distance, palette=color_mapping_by_id)
# plt.legend(title='Groups', labels=sigle.values(), handles=patches)
# plt.xticks(np.arange(len(group_list)), groups, rotation=45, fontsize=10)
# plt.xlabel(' ')
# plt.tight_layout
# plt.savefig(path+'IntergroupDistance_'+id_votazione+'_'+ruolo+'.png', dpi=1000)


# Plots of distance of a single member from group
###### Per realizzare i plot di lealtà di più gruppi parlamentari:
# df_single_distance = pd.read_csv(path+'SingleDistanceFromGroup_'+data_votazione+'_'+id_votazione+'.csv')
# group_list = list(df_single_distance.IdGruppo.unique())
# plt.figure(figsize=(10,10))
# sns.catplot(data=df_single_distance, x='IdGruppo', y='Distance', hue='IdGruppo', palette=color_mapping_by_id)
# patches = [Patch(color=v, label=k) for k, v in color_mapping_by_id.items()]
# #plt.legend(title='Groups', labels=sigle.values(), handles=patches, loc='lower right')
# plt.xticks(np.arange(len(group_list)), groups, rotation=45, fontsize=10)
# plt.ylabel('Distance from the Group')
# plt.xlabel('')
# plt.tight_layout
# plt.savefig(path+'Loyalty_'+data_votazione+'_'+id_votazione+'_'+ruolo+'.png', dpi=1000)

###### Per realizzare i plot di lealtà di un singolo gruppo parlamentare:
# df_single_distance = pd.read_csv(path+'SingleDistance_IVFormation_TimePeriod_IdGruppoIV.csv')
# df_single_distance = df_single_distance[df_single_distance['IdGruppo']==4]
# group_list = list(df_single_distance.IdGruppo.unique())
# plt.figure(figsize=(10,10))
# sns.lineplot(data=df_single_distance, x='DataVotazione', y='Distance', hue='IdGruppo', palette=color_mapping_by_id, linewidth=0.5, style='IdParlamentare', size=3, markers=True)
# patches = [Patch(color=v, label=k) for k, v in color_mapping_by_id.items()]
# plt.xticks(np.arange(5), ['Jun', 'Jul', 'Aug', 'Sept', 'Oct'], fontsize=20, fontweight='bold')
# plt.ylim(0, 1)
# plt.legend(title='Groups', labels=sigle.values(), handles=patches, fontsize=20)
# plt.tight_layout
# plt.yticks(fontsize=25, fontweight='bold')
# plt.xlabel('')
# plt.ylabel('Loyalty to PD party', fontsize=25, fontweight='bold')
# plt.savefig(path+'Loyalty_IVFormation_TimePeriod_PD_members.png', dpi=200)


###### Per realizzare i plot di distanza tra i PG:
# xy è un vettore di lunghezza 2N contiene le coordinate dei nodi:
# x=xy(1:N) , y=xy(N+1,2N)
# passo un solo vettore a causa di come funzionano le routine di minimizzazione di matlab
# N è il numero di nodi
# l(i,j) è la distanza a riposo fra due nodi (quella che tu hai calcolato)
#function [EKK dxE dyE]=KKenergy(xy, l, N)  
# def KKenergy(xy, l, N):
#     EKK=0 
#     dxE=np.zeros(N,1) 
#     dyE=np.zeros(N,1)
#     for i in range(2,N):
#         for j in range(1,i-1):
#             DX=xy[i]-xy[j]
#             DY=xy[i+N]-xy[j+N]
#             D=math.sqrt(DX^2 + DY^2) # distanza fra i e j
#             EKK=EKK+(DX*DX+DY*DY+l(i,j)^2-2*l(i,j)*D) # distanza fra i e j meno la distanza a riposo l(,j)
#             C=1-l(i,j)/D
#             dxE[i]=dxE[i]+DX*C 
#             dyE[i]=dyE[i]+DY*C
#             dxE[j]=dxE[j]-DX*C
#             dyE[j]=dyE[j]-DY*C
#     return dxE, dyE

# # dist è la matrice delle distanze (letta dai tuoi csv)
# dist = pd.read_csv(path+'IntergroupsDistanceReadyToPlot_Jun_2018_Sen.csv')
# group_list = list(dist['Gr1'].unique())
# N = len(group_list)
# l = dist['Distance']
# x0=2*np.mean(dist)*randint(1, N) # prendo posizioni a caso per le x
# y0=2*np.mean(dist)*randint(1, N) # prendo posizioni a caso per le y
# # il minimizzatore di matlab ha bisogno di una funzione di un solo argomento
# fnc=KKenergy(xy,l,N) # definisco la funzione di xy da minimizzare (quindi l,N sono fissate)
# xy0=[x0,y0] # valore iniziale per la funzione fnc da minimizzare
# xy1 = fmin(fnc, xy0) # calcolo le coorninate xy1 che minimizzano l'energia
# x1=xy1[1:N]
# y1=xy1[N+1,2*N]# coordinate dei nodi

data_sen_conte1 = pd.read_csv(path+'GGxySenConte1.csv')
plt.figure(figsize=(10,10))
sns.scatterplot(data=data_sen_conte1, x='x', y='y', hue='group', palette=color_mapping_by_id, marker='o', s=1000, markers=True, legend=False)
#patches = [Patch(color=v, label=k) for k, v in color_mapping_by_id.items()]
plt.xticks(fontsize=25, fontweight='bold')
plt.yticks(fontsize=25, fontweight='bold')
plt.xlabel('')
plt.ylabel('')
plt.ylim(0., 0.8)
plt.xlim(0., 0.8)
plt.savefig(path+'GGxyConte1'+ruolo+'.png', dpi=200)

data_sen_conte2 = pd.read_csv(path+'GGxySenConte2.csv')
plt.figure(figsize=(10,10))
sns.scatterplot(data=data_sen_conte2, x='x', y='y', hue='group', palette=color_mapping_by_id, marker='o', s=1000, markers=True, legend=False)
#patches = [Patch(color=v, label=k) for k, v in color_mapping_by_id.items()]
plt.xticks(fontsize=25, fontweight='bold')
plt.yticks(fontsize=25, fontweight='bold')
plt.xlabel('')
plt.ylabel('')
plt.ylim(0., 0.8)
plt.xlim(0., 0.8)
plt.savefig(path+'GGxyConte2'+ruolo+'.png', dpi=200)

data_sen_draghi = pd.read_csv(path+'GGxySenDraghi.csv')
plt.figure(figsize=(10,10))
sns.scatterplot(data=data_sen_draghi, x='x', y='y', hue='group', palette=color_mapping_by_id, marker='o', s=1000, markers=True, legend=False)
#patches = [Patch(color=v, label=k) for k, v in color_mapping_by_id.items()]
plt.xticks(fontsize=25, fontweight='bold')
plt.yticks(fontsize=25, fontweight='bold')
plt.xlabel('')
plt.ylabel('')
plt.ylim(0., 0.8)
plt.xlim(0., 0.8)
plt.savefig(path+'GGxyDraghi'+ruolo+'.png', dpi=200)