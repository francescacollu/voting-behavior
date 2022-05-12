# IMPORTANTE: specificare 
# 1) il nome delle tabelle su cui si vuole creare la matrice delle distanze (fav_df, con_df, ast_df) 
# 2) la data in cui è avvenuta la votazione
# 3) il path in cui salvare le matrici

from os import write
from matplotlib import colors
from networkx.algorithms.shortest_paths import weighted
import pandas as pd
from sqlalchemy import create_engine
import networkx as nx
from itertools import combinations
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.spatial.distance import pdist, squareform
import datetime
from datetime import date
import numpy as np
from functools import reduce
import os

engine = create_engine('mysql+mysqlconnector://root:Fiorentino68*@127.0.0.1:3306/VotingBehavior')
ruolo = 'Sen'
id_votazione = '13Feb_10May_2021'
data_votazione = '2021-05-02' # Specifichiamo la data delle votazioni considerate
path = 'Networks/TimeIntervals/'+ruolo+'/' # Specifichiamo il path in cui salvare le matrici calcolate
if not os.path.exists(path):
    os.makedirs(path)
fav_df = pd.read_sql('''
SELECT Fav.*
FROM VotingBehavior.V_Fav_'''+id_votazione+'''_'''+ruolo+''' Fav;
''', con=engine)

con_df = pd.read_sql('''
SELECT Con.*
FROM VotingBehavior.V_Con_'''+id_votazione+'''_'''+ruolo+''' Con;
''', con=engine)

ast_df = pd.read_sql('''
SELECT Ast.*
FROM VotingBehavior.V_Ast_'''+id_votazione+'''_'''+ruolo+''' Ast;
''', con=engine)

print('Tables retrieved from db!')

fav_df = fav_df.replace({1:1})
con_df = con_df.replace({1:-1})
ast_df = ast_df.replace({1:0})

df = fav_df+con_df+ast_df

df.insert(0, 'IdParlamentare2', fav_df['IdParlamentare'])
df = df.drop(columns=['IdParlamentare'])
df = df.rename(columns={'IdParlamentare2': 'IdParlamentare'})
df.drop_duplicates(inplace=True)

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
df = pd.merge(df, df_appartenenza2, how='inner', on=['IdParlamentare'])
df = df.sort_values(by=['IdGruppo'])
M = len(df.columns[1:-2]) # number of votations
distance_matrices_list = []
for c in range(M):
    distance_matrix = pd.DataFrame(squareform(pdist(df.iloc[:, c+1:c+2].values, 'cityblock')), index=df.IdParlamentare, columns=df.IdParlamentare)
    distance_matrices_list.append(distance_matrix)
distance_matrix = reduce(lambda x, y: x.add(y, fill_value=0), distance_matrices_list)
writer = pd.ExcelWriter(path+'DistanceMatrix_'+data_votazione+'_'+id_votazione+'.xlsx')
distance_matrix.to_excel(writer, sheet_name='distance_matrix')
writer.save()
f = pd.DataFrame() # votes fractions (fraction of y, n, a for each voter)
f.index = df['IdParlamentare']
f['Y_Fraction'] = pd.Series(dtype=np.float64)
f['N_Fraction'] = pd.Series(dtype=np.float64)
f['A_Fraction'] = pd.Series(dtype=np.float64)
voters_list = list(df.IdParlamentare)
favs_number = []
cons_number = []
absts_number = []
df_votations = df.iloc[:, 0:M+1]
df_votations = df_votations.set_index('IdParlamentare').transpose()
f['Y_Fraction'] = df_votations[df_votations==1].count()
f['N_Fraction'] = df_votations[df_votations==-1].count()
f['A_Fraction'] = df_votations[df_votations==0].count()

d0 = pd.DataFrame(index=df['IdParlamentare'], columns=df['IdParlamentare'])
d0_array = d0.to_numpy()
reduced_distance_matrix = pd.DataFrame(index=df['IdParlamentare'], columns=df['IdParlamentare'])
reduced_distance_matrix_array = reduced_distance_matrix.to_numpy()
distance_matrix_array = distance_matrix.to_numpy()
normalized_distance_matrix = distance_matrix/(2*M)
f_array = f.to_numpy()
for p in range(f_array.shape[0]):
    for q in range(f_array.shape[0]):
        d0_array[p, q] = f_array[p, 0]*f_array[q, 2] + 2*f_array[p, 0]*f_array[q, 1] + f_array[p, 2]*f_array[q, 0] + f_array[p, 2]*f_array[q, 1] + 2*f_array[p, 1]*f_array[q, 0] + f_array[p, 1]*f_array[q, 2]
        if d0_array[p,q] != 0:
            reduced_distance_matrix_array[p, q] = distance_matrix_array[p, q]/d0_array[p, q]
        else:
            reduced_distance_matrix_array[p, q] = distance_matrix_array[p, q]

reduced_distance_matrix.fillna(0, inplace=True)
writer = pd.ExcelWriter(path+'ReducedDistanceMatrix_'+data_votazione+'_'+id_votazione+'.xlsx')
reduced_distance_matrix.to_excel(writer, sheet_name='reduced_distance_matrix')
writer.save()
writer = pd.ExcelWriter(path+'NormalizedDistanceMatrix_'+data_votazione+'_'+id_votazione+'.xlsx')
normalized_distance_matrix.to_excel(writer, sheet_name='reduced_distance_matrix')
writer.save()

# Group cohesion
print('Group Cohesion')
normalized_distance_matrix2 = pd.merge(normalized_distance_matrix, df, on=['IdParlamentare'], how='inner')
groups_list = list(df.IdGruppo.unique())
cohesion_dict = dict.fromkeys(groups_list)
for id_gruppo in groups_list:
    cohesion_and_size_group_list = []
    df_temp = normalized_distance_matrix2[normalized_distance_matrix2['IdGruppo']==id_gruppo]
    member_temp = list(df_temp.IdParlamentare)
    df_temp = df_temp[member_temp]
    upper_values_list = np.triu(df_temp.to_numpy(), 1)
    upper_values_list = np.concatenate(upper_values_list)
    #upper_values_list = [df_temp_array[i][i+1:] for i in range(len(df_temp_array))]
    N_G = normalized_distance_matrix2[normalized_distance_matrix2['IdGruppo']==id_gruppo].shape[0]
    if N_G != 1:
        gr_cohesion = 1-(sum(upper_values_list)/(0.5*N_G*(N_G-1)))
    else:
        gr_cohesion = 1-(sum(upper_values_list))
    cohesion_and_size_group_list.append(gr_cohesion)
    cohesion_and_size_group_list.append(N_G)
    cohesion_and_size_group_list.append(data_votazione)
    cohesion_dict[id_gruppo] = cohesion_and_size_group_list
cohesion_df = pd.DataFrame.from_dict(cohesion_dict, orient='index', columns=['GroupCohesion','GroupSize','DataVotazione'])
cohesion_df.index.name = 'IdGruppo'
cohesion_df.to_csv(path+'GroupCohesion_'+data_votazione+'_'+id_votazione+'.csv')

# Different groups distance
print('Groups Interdistance')
comb_tuples = list(combinations(groups_list, 2))
interdistances_dict = dict.fromkeys(comb_tuples)
normalized_distance_matrix2 = normalized_distance_matrix2.set_index('IdParlamentare')
for t in comb_tuples:
    distancesAB_list = []
    id_grA = t[0]
    id_grB = t[1]
    voters_grA = normalized_distance_matrix2.index[(normalized_distance_matrix2['IdGruppo']==id_grA)]
    voters_grB = normalized_distance_matrix2.index[(normalized_distance_matrix2['IdGruppo']==id_grB)]
    for p in voters_grA:
        for q in voters_grB:
            distancesAB_list.append(normalized_distance_matrix2.loc[p,q])
    interdistances_dict[t] = sum(distancesAB_list)/((len(voters_grA))*(len(voters_grB)))
interdistances_df = pd.DataFrame.from_dict(interdistances_dict, orient='index', columns=['Distance'])
interdistances_df.index.name = 'GroupPair'
interdistances_df.to_csv(path+'IntergroupDistances_'+data_votazione+'_'+id_votazione+'.csv')

# Distance of a member from a group
print('Single distance from group')
lista_parlamentari = normalized_distance_matrix2.index.unique()
single_distance = dict.fromkeys(lista_parlamentari)
for id_gr in groups_list:
    voters_gr = normalized_distance_matrix2.index[(normalized_distance_matrix2['IdGruppo']==id_gr)]
    for p in voters_gr:
        distancesP_list = []
        for q in voters_gr:
            if q != p:
                distancesP_list.append(normalized_distance_matrix2.loc[p,q])
        if len(voters_gr) != 1:
            single_distance[p] = [1-(sum(distancesP_list)/(len(voters_gr)-1)), id_gr, data_votazione]
        else:
            single_distance[p] = [1-(sum(distancesP_list)), id_gr, data_votazione]
single_distance = pd.DataFrame.from_dict(single_distance, orient='index', columns=['Distance','IdGruppo','DataVotazione'])
single_distance.index.name = 'IdParlamentare'
single_distance.to_csv(path+'SingleDistanceFromGroup_'+data_votazione+'_'+id_votazione+'.csv')



##### Di seguito una versione non debuggata in cui utilizzo la distanza random come metodo per normalizzare la distanza
# print('Group Cohesion:')
# reduced_distance_matrix2 = pd.merge(reduced_distance_matrix, df, on=['IdParlamentare'], how='inner')
# groups_list = list(df.IdGruppo.unique())
# cohesion_dict = dict.fromkeys(groups_list)
# for id_gruppo in groups_list:
#     cohesion_and_size_group_list = []
#     df_temp = reduced_distance_matrix2[reduced_distance_matrix2['IdGruppo']==id_gruppo].iloc[:, 1:-3]
#     df_temp_array = df_temp.to_numpy()
#     upper_values_list = [df_temp_array[i][i+1:] for i in range(len(df_temp_array))]
#     N_G = reduced_distance_matrix2[reduced_distance_matrix2['IdGruppo']==id_gruppo].shape[0]
#     if N_G != 1:
#         gr_cohesion = 1-(sum([sum(i) for i in zip(*upper_values_list)])/(0.5*N_G*(N_G-1)))
#     else:
#         gr_cohesion = 1-(sum([sum(i) for i in zip(*upper_values_list)]))
#     cohesion_and_size_group_list.append(gr_cohesion)
#     cohesion_and_size_group_list.append(N_G)
#     cohesion_and_size_group_list.append(data_votazione)
#     cohesion_dict[id_gruppo] = cohesion_and_size_group_list
# cohesion_df = pd.DataFrame.from_dict(cohesion_dict, orient='index', columns=['GroupCohesion','GroupSize','DataVotazione'])
# cohesion_df.index.name = 'IdGruppo'
# cohesion_df.to_csv(path+'GroupCohesion_'+data_votazione+'_'+id_votazione+'.csv')

# Different groups distance
# print('Groups Interdistance:')
# comb_tuples = list(combinations(groups_list, 2))
# interdistances_dict = dict.fromkeys(comb_tuples)
# reduced_distance_matrix2 = reduced_distance_matrix2.set_index('IdParlamentare')
# distancesAB_list = []
# for t in comb_tuples:
#     id_grA = t[0]
#     id_grB = t[1]
#     voters_grA = reduced_distance_matrix2.index[(reduced_distance_matrix2['IdGruppo']==id_grA)]
#     voters_grB = reduced_distance_matrix2.index[(reduced_distance_matrix2['IdGruppo']==id_grB)]
#     for p in voters_grA:
#         for q in voters_grB:
#             distancesAB_list.append(reduced_distance_matrix2.loc[p,q])
#     interdistances_dict[t] = sum(distancesAB_list)/((voters_grA.shape[0])*(voters_grB.shape[0]))
# interdistances_df = pd.DataFrame.from_dict(interdistances_dict, orient='index', columns=['Distance'])
# interdistances_df.index.name = 'GroupPair'
# interdistances_df.to_csv(path+'IntergroupDistances_'+data_votazione+'_'+id_votazione+'.csv')


# # Distance of a member from a group
# print('Single distance from group')
# lista_parlamentari = reduced_distance_matrix2.index.unique()
# single_distance = dict.fromkeys(lista_parlamentari)
# for id_gr in groups_list:
#     print(str(id_gr))
#     distancesP_list = []
#     voters_gr = reduced_distance_matrix2.index[(reduced_distance_matrix2['IdGruppo']==id_gr)]
#     for i, p in enumerate(voters_gr):
#         for q in voters_gr:
#             distancesP_list.append(reduced_distance_matrix2.loc[p,q])
#             if voters_gr.shape[0] != 1:
#                 single_distance[p] = [1-sum(distancesP_list)/(voters_gr.shape[0]-1), id_gr, data_votazione]
#             else:
#                 single_distance[p] = [1-sum(distancesP_list), id_gr, data_votazione]
# single_distance = pd.DataFrame.from_dict(single_distance, orient='index', columns=['Distance','IdGruppo','DataVotazione'])
# single_distance.index.name = 'IdParlamentare'
# single_distance.to_csv(path+'SingleDistanceFromGroup_'+data_votazione+'_'+id_votazione+'.csv')


# Plots of intergroups distances
df_intergroup_distance = pd.read_csv(path+'IntergroupDistances_'+data_votazione+'_'+id_votazione+'.csv')
df_intergroup_distance[['Gr1', 'Gr2']] = df_intergroup_distance['GroupPair'].str.split(',', 1, expand=True)
df_intergroup_distance['Gr1'] = df_intergroup_distance['Gr1'].str[1:]
df_intergroup_distance['Gr2'] = df_intergroup_distance['Gr2'].str[:-1]
df_intergroup_distance['Gr2'] = df_intergroup_distance['Gr2'].apply(lambda x: x.strip(' '))
group_list = list(df_intergroup_distance['Gr1'].unique())
group_list = group_list+list(df_intergroup_distance['Gr2'].unique())
group_list = list(set(group_list))
with open(path+'IntergroupsDistanceReadyToPlot_'+id_votazione+'_'+ruolo+'.csv', 'w') as f:
    f.write('Gr1,Gr2,Distance\n')
    for i, g in enumerate(group_list):
        g = str(g)
        df_temp = df_intergroup_distance[(df_intergroup_distance['Gr1']==g) | (df_intergroup_distance['Gr2']==g)]
        for row in df_temp.index:
            if df_temp.at[row, 'Gr1']==g:
                x_value = int(df_temp.at[row, 'Gr2'])
                y_value = df_temp.at[row, 'Distance']
                f.write(g+','+str(x_value)+','+str(y_value)+'\n')
            elif df_temp.at[row, 'Gr2']==g:
                x_value = int(df_temp.at[row, 'Gr1'])
                y_value = df_temp.at[row, 'Distance']
                f.write(g+','+str(x_value)+','+str(y_value)+'\n')