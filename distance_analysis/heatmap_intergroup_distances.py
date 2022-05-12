import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

ruolo = 'Sen' # Utile per specificare la cartella (Sen/Dep)
path = 'Networks/TimeIntervals/'+ruolo+'/' # Path in cui si trova il csv e dove verrà salvato il png dei plot

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

fig = make_subplots(rows=1, cols=3, 
                    horizontal_spacing=0.1,
                    subplot_titles=('Conte I cabinet', 
                                    'Conte II cabinet',
                                    'Draghi cabinet'))

id_votazione = 'Jun_2018' # Specifichiamo il/gli id della/e votazione/i considerate
df_intergroup_distance = pd.read_csv(path+'IntergroupsDistanceReadyToPlot_'+id_votazione+'_'+ruolo+'.csv')
df_intergroup_distance = df_intergroup_distance.replace(sigle)
df = pd.pivot_table(data=df_intergroup_distance, index=['Gr1'], columns=['Gr2'], values='Distance')
df = df.fillna(0)
df = round(df, 2)
fig1 = px.imshow(df, text_auto=True,
                labels=dict(x='Group 1', y='Group 2', color='Distance'),
                aspect='auto')
fig1.update_layout(title={
                          'y':0.9,
                          'x':0.5,
                          'xanchor': 'center',
                          'yanchor': 'top'})

id_votazione = '6Sep_25Oct_2019' # Specifichiamo il/gli id della/e votazione/i considerate
df_intergroup_distance = pd.read_csv(path+'IntergroupsDistanceReadyToPlot_'+id_votazione+'_'+ruolo+'.csv')
df_intergroup_distance = df_intergroup_distance.replace(sigle)
df = pd.pivot_table(data=df_intergroup_distance, index=['Gr1'], columns=['Gr2'], values='Distance')
df = df.fillna(0)
df = round(df, 2)
fig2 = px.imshow(df, text_auto=True,
                labels=dict(x='Group 1', y='Group 2', color='Distance'),
                aspect='auto')
fig2.update_layout(title={
                          'y':0.9,
                          'x':0.5,
                          'xanchor': 'center',
                          'yanchor': 'top'})

id_votazione = '13Feb_10May_2021' # Specifichiamo il/gli id della/e votazione/i considerate
df_intergroup_distance = pd.read_csv(path+'IntergroupsDistanceReadyToPlot_'+id_votazione+'_'+ruolo+'.csv')
df_intergroup_distance = df_intergroup_distance.replace(sigle)
df = pd.pivot_table(data=df_intergroup_distance, index=['Gr1'], columns=['Gr2'], values='Distance')
df = df.fillna(0)
df = round(df, 2)
fig3 = px.imshow(df, text_auto=True,
                labels=dict(x='Group 1', y='Group 2', color='Distance'),
                aspect='auto')
fig3.update_layout(title={
                          'y':0.9,
                          'x':0.5,
                          'xanchor': 'center',
                          'yanchor': 'top'})

fig.add_trace(fig1.data[0], row=1, col=1)
fig.add_trace(fig2.data[0], row=1, col=2)
fig.add_trace(fig3.data[0], row=1, col=3)
fig.update_layout(title_text='Intergroup Distances in Senato',
                  title={
                          'y':0.93,
                          'x':0.5,
                          'xanchor': 'center',
                          'yanchor': 'top'},
                  coloraxis=dict(colorscale='blues', colorbar_title_text='Distance'))
fig.show()
fig.write_image(path+'heatmap_interdistance_'+ruolo+'.png')