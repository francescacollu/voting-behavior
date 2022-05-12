from networkx.algorithms.centrality.eigenvector import eigenvector_centrality
from networkx.algorithms.shortest_paths import weighted
from networkx.classes.function import nodes
import pandas as pd
from sqlalchemy import create_engine
import networkx as nx
from itertools import combinations
from collections import Counter
import matplotlib.pyplot as plt
from random import gauss, seed
import csv
from networkx.algorithms import community
import os
import datetime
from datetime import date
import networkx.algorithms.community as nx_comm

engine = create_engine('mysql+mysqlconnector://root:Fiorentino68*@127.0.0.1:3306/VotingBehavior')
id_table = 'ForzeArmateEDellOrdine'
ruolo = 'Sen'
path = 'Networks/Topics/'+ruolo+'/'#SpecificGroups/'+id_table+'/'+str(id_gruppo)+'/'
if not os.path.exists(path):
    os.makedirs(path)
data_votazione = '2020-12-15'

# WHERE VG.IdGruppo = '''+id_gruppo+''' # condizione da aggiungere alle tre query seguenti se si vuole fare l'analisi dei singoli gruppi
fav_df = pd.read_sql('''
SELECT Fav.*
FROM VotingBehavior.V_Fav_'''+id_table+'''_'''+ruolo+''' Fav
	INNER JOIN Mandato M ON Fav.IdParlamentare = M.IdParlamentare;
''', con=engine)

con_df = pd.read_sql('''
SELECT Con.*
FROM VotingBehavior.V_Con_'''+id_table+'''_'''+ruolo+''' Con
	INNER JOIN Mandato M ON Con.IdParlamentare = M.IdParlamentare;
''', con=engine)

ast_df = pd.read_sql('''
SELECT Ast.*
FROM VotingBehavior.V_Ast_'''+id_table+'''_'''+ruolo+''' Ast
	INNER JOIN Mandato M ON Ast.IdParlamentare = M.IdParlamentare;
''', con=engine)

G = nx.Graph()

# Selezioniamo il corretto gruppo parlamentare sulla base della data di votazione
def GetVotingParty(data_votazione, df_appartenenza_input):
    df_appartenenza_output = pd.DataFrame()
    lista_parlamentari = df_appartenenza_input.IdParlamentare.unique()
    df_appartenenza_output['IdParlamentare'] = pd.Series(lista_parlamentari)
    for parlamentare in lista_parlamentari:
        lista_date_ingresso = list(df_appartenenza_input[(df_appartenenza_input.IdParlamentare == parlamentare)]['DataIngresso'])
        lista_date_ingresso.append(str(date.today()))
        lista_date_ingresso = sorted(lista_date_ingresso, key=lambda date: datetime.datetime.strptime(date, "%Y-%m-%d"))
        for i in range(len(lista_date_ingresso)):
            if (lista_date_ingresso[i]) <= data_votazione < (lista_date_ingresso[i+1]):
                df_appartenenza_output.loc[df_appartenenza_output.IdParlamentare == parlamentare, ['DataIngresso']] = lista_date_ingresso[i]
    return df_appartenenza_output

df_appartenenza = pd.read_sql('''
SELECT IdParlamentare,
	   DataIngresso,
       IdGruppo
FROM VariazioneGruppo;
''', con=engine)
df_appartenenza2 = GetVotingParty(data_votazione, df_appartenenza)
df_appartenenza2 = df_appartenenza.merge(df_appartenenza2, how='inner', on=['DataIngresso', 'IdParlamentare'])
fav_df = fav_df.merge(df_appartenenza2, how='inner', on=['IdParlamentare'])
con_df = con_df.merge(df_appartenenza2, how='inner', on=['IdParlamentare'])
ast_df = ast_df.merge(df_appartenenza2, how='inner', on=['IdParlamentare'])

# Specifichiamo il gruppo considerato 
# fav_df = fav_df[fav_df.IdGruppo == id_gruppo]
# con_df = con_df[con_df.IdGruppo == id_gruppo]
# ast_df = ast_df[ast_df.IdGruppo == id_gruppo]

default_weight = 1/len(fav_df.columns[1:-2])#0.0001
fav_members = list()
for col in fav_df.columns[1:-2]:
    fav_members = list(fav_df[fav_df[str(col)]==1]['IdParlamentare'])
    combinazioni = list(combinations(fav_members, 2))
    for c in combinazioni:
        if G.has_edge(c[0], c[1]):
            G[c[0]][c[1]]['weight'] += default_weight
        else:
            G.add_edge(c[0], c[1], weight=default_weight)
nx.set_node_attributes(G, pd.Series(list(fav_df['IdGruppo']), index=list(fav_df.IdParlamentare)).to_dict(), 'gruppo_appartenenza')

con_members = list()
for col in con_df.columns[1:-2]:
    con_members = list(con_df[con_df[str(col)]==1]['IdParlamentare'])
    combinazioni = list(combinations(con_members, 2))
    for c in combinazioni:
        if G.has_edge(c[0], c[1]):
            G[c[0]][c[1]]['weight'] += default_weight
        else:
            G.add_edge(c[0], c[1], weight=default_weight)
nx.set_node_attributes(G, pd.Series(list(con_df['IdGruppo']), index=list(con_df.IdParlamentare)).to_dict(), 'gruppo_appartenenza')

ast_members = list()
for col in ast_df.columns[1:-2]:
    ast_members = list(ast_df[ast_df[str(col)]==1]['IdParlamentare'])
    combinazioni = list(combinations(ast_members, 2))
    for c in combinazioni:
        if G.has_edge(c[0], c[1]):
            G[c[0]][c[1]]['weight'] += default_weight
        else:
            G.add_edge(c[0], c[1], weight=default_weight)

nx.set_node_attributes(G, pd.Series(list(ast_df['IdGruppo']), index=list(ast_df.IdParlamentare)).to_dict(), 'gruppo_appartenenza')

color_map = nx.get_node_attributes(G, 'gruppo_appartenenza')
for key in color_map:
    if color_map[key] == 4:
        color_map[key] = 'red'
    if color_map[key] == 1:
        color_map[key] = 'green'
    if color_map[key] == 0:
        color_map[key] = 'yellow'
    if color_map[key] == 10:
        color_map[key] = 'deeppink'
    if color_map[key] == 5:
        color_map[key] = 'deeppink'
    if color_map[key] == 12:
        color_map[key] = 'grey'
    if color_map[key] == 2:
        color_map[key] = 'blue'
    if color_map[key] == 6:
        color_map[key] = 'black'
    if color_map[key] == 9:
        color_map[key] = 'lightsalmon'
    if color_map[key] == 3:
        color_map[key] = 'royalblue'
    if color_map[key] == 7:
        color_map[key] = 'darkred'
    if color_map[key] == 8:
        color_map[key] = 'green'
    if color_map[key] == 11:
        color_map[key] = 'aquamarine'

gruppo_appartenenza_color_map = [color_map.get(node) for node in G.nodes()]

pos_layout=nx.spring_layout(G)
nx.draw_networkx(G, pos=pos_layout, width=[d['weight'] for u, v, d in G.edges(data=True)], with_labels=False, node_size=4, node_color = gruppo_appartenenza_color_map, alpha=1.)
G.remove_edges_from(nx.selfloop_edges(G))
deg_centrality_dict = nx.degree_centrality(G)
bet_centrality_dict = nx.betweenness_centrality(G, weight='weight')
eig_centrality_dict = nx.eigenvector_centrality(G, weight='weight')
communities = community.greedy_modularity_communities(G, weight='weight', resolution=1)

with open(path+'DegreeCentrality_'+id_table+'_'+ruolo+'.csv', 'w') as f:
    f.write('IdParlamentare,DegreeCentrality\n')
    for key in deg_centrality_dict.keys():
        f.write('%s,%s\n'%(key, deg_centrality_dict[key]))
with open(path+'BetweennessCentrality_'+id_table+'_'+ruolo+'.csv', 'w') as f:
    f.write('IdParlamentare,BetweennessCentrality\n')
    for key in bet_centrality_dict.keys():
        f.write('%s,%s\n'%(key, bet_centrality_dict[key]))
with open(path+'Density_'+id_table+'_'+ruolo+'.txt', 'w') as f:
    f.write(str(nx.density(G)))
with open(path+'EigenvectorCentrality_'+id_table+'_'+ruolo+'.csv', 'w') as f:
    f.write('IdParlamentare,EigenvectorCentrality\n')
    for key in eig_centrality_dict.keys():
        f.write('%s,%s\n'%(key, eig_centrality_dict[key]))
with open(path+'Communities_'+id_table+'_'+ruolo+'.csv', 'w') as f:
    for i, c in enumerate(communities):
        f.write('%s,%s\n'%(i, list(c)))
with open(path+'Modularity_'+id_table+'_'+ruolo+'.csv', 'w') as f:
    f.write(str(nx_comm.modularity(G, communities, weight='weight', resolution=1)))
# with open(path+'Coverage_Performance'+id_table+'_'+ruolo+'.csv', 'w') as f:
#     for i, c in enumerate(communities):
#         f.write('%s,%s\n'%(i, nx_comm.partition_quality(G, c)))
plt.title('Votes Network in '+id_table+' ['+ruolo+']')
plt.tight_layout()
nx.write_gexf(G, path+'VotesNetwork_'+id_table+'_'+ruolo+'.gexf')
#plt.savefig(path+'VotesNetwork_'+id_table+'_'+ruolo+'.png', dpi=1000)