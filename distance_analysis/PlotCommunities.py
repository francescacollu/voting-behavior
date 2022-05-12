# Modificare data_votazione, ruolo, id_table, path e inserire le liste delle comunità ricavate con Networkx

import pandas as pd
from matplotlib import colors
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from datetime import date
from sqlalchemy import create_engine

engine = create_engine('mysql+mysqlconnector://root:Fiorentino68*@127.0.0.1:3306/VotingBehavior')

data_votazione = '2020-12-15'
ruolo = 'Sen'
id_table = 'Immigrazione_Dec2020'
path = 'Networks/Topics/'+ruolo+'/'
sns.set_theme() # Impostiamo il tema di default di Seaborn
sns.despine() # Removing top and right axes spines
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

comm1 = ['32649', '32639', '30511', '29091', '29075', '29140', '32616', '29070', '32617', '32581', '21507', '32709', '29555', '25498', '31373', '17211', '32641', '29053', '32631', '29248', '29395', '32674', '32622', '29115', '32624', '32663', '32615', '17750', '32625', '32630', '32579', '32656', '29467', '23011', '32577', '32632', '32691', '29138', '29464', '29189', '32725', '32745', '32607', '32744', '32749', '32601', '32655', '29443', '1458', '32640', '32578', '29117', '18499', '321', '32629', '32600', '32651', '32692', '4522', '29072', '32689', '32648', '32612', '32580', '27476', '29040', '32606', '29599', '32619', '31143', '29161', '29604', '29107', '32718', '29288', '29110', '32594', '32662', '32660', '32704', '32684', '29174', '32698', '29398', '29157', '26041', '32703', '29143', '520', '32669', '29186', '32672', '17578', '29527', '32643', '32626', '32608', '29147', '29591', '32618', '32687', '32647', '32675', '32654', '29194', '32727', '29055', '32592', '32588', '29065', '32696', '34677', '29282', '32634', '29142', '25402', '23135', '32667', '32652', '32658', '29108', '29552', '32729', '28924', '29470', '32705', '20658', '32670', '32604', '32710', '32673', '32746', '29521', '29076', '29066', '14224', '1686', '29034', '29090', '32731', '32638', '35106', '32701', '4741', '32605', '4351', '32653', '31572', '29450', '32665']
comm2 = ['32599', '25295', '32613', '32628', '32741', '4584', '29292', '32682', '32748', '32728', '32697', '32635', '32666', '32590', '34675', '25199', '25412', '25446', '17841', '25218', '18740', '25207', '32706', '32751', '29039', '32597', '3939', '422', '32707', '32583', '32593', '25415', '24989', '29106', '32690', '29059', '32582', '32596', '29185', '32679', '29209', '22712', '32646', '33946', '25429', '32586', '32642', '31157', '32695', '17542', '32765', '32595', '34676', '29130', '32714', '32702', '26539', '32713', '32717', '30915', '32611', '2444', '18562', '32752', '1103', '23015', '2064', '32747', '32700', '32671', '29329', '1275', '32753', '25565', '18715', '32677', '22814', '32598', '19244', '29123', '32699', '32711', '32694', '22970', '29480', '25407', '32678', '25214', '32650', '27874', '30396', '32685', '32633', '34617', '35119', '4512', '32659', '32636', '32686', '32750', '18121', '32722', '32723', '32645', '32661', '32733', '32715', '32680', '32664', '32587', '32683', '32591', '1407']





#comm3 = ['32733', '22865', '34617', '32590', '29123', '32711', '32690', '34675', '32751', '32697', '32686', '32706', '32694', '29292', '19244', '35119', '25218', '18562', '32728', '23015', '25295', '29067', '32635', '32637', '32593', '32596', '32591', '32679', '29059', '32586', '32677', '32702', '32633', '29185', '32685', '32595', '25199', '32682', '32712', '25205', '32598', '25415', '32721', '32627', '32582', '32752', '32599', '32642', '32748', '32743', '32683']






df1 = pd.DataFrame({'IdParlamentare': comm1})
df1['Community'] = 1
df2 = pd.DataFrame({'IdParlamentare': comm2})
df2['Community'] = 2
#df3 = pd.DataFrame({'IdParlamentare': comm3})
#df3['Community'] = 3

df1 = pd.merge(df1, df_appartenenza2, on=['IdParlamentare'], how='inner')
df2 = pd.merge(df2, df_appartenenza2, on=['IdParlamentare'], how='inner')
#df3 = pd.merge(df3, df_appartenenza2, on=['IdParlamentare'], how='inner')

df1 = df1[['IdParlamentare', 'Community', 'IdGruppo']]
df2 = df2[['IdParlamentare', 'Community', 'IdGruppo']]
#df3 = df3[['IdParlamentare', 'Community', 'IdGruppo']]

df1['IdGruppo'] = df1['IdGruppo'].replace(sigle)
df2['IdGruppo'] = df2['IdGruppo'].replace(sigle)
#df3['IdGruppo'] = df3['IdGruppo'].replace(sigle)

df_pie1 = df1.groupby('IdGruppo').count().reset_index()
df_pie2 = df2.groupby('IdGruppo').count().reset_index()
#df_pie3 = df3.groupby('IdGruppo').count().reset_index()

labels1=list(df_pie1.IdGruppo)
labels2=list(df_pie2.IdGruppo)
#labels3=list(df_pie3.IdGruppo)
fig, ax = plt.subplots(1,2, figsize=(6,3))
ax[0].pie(list(df_pie1.IdParlamentare), labels=labels1, textprops={'fontsize': 15, 'weight':'bold'}, wedgeprops={"linewidth": 1, "edgecolor": "white"}, colors=[color_mapping_by_sigla[key] for key in labels1])#, radius=len(df1)/(max(len(df1), len(df2))))
ax[1].pie(list(df_pie2.IdParlamentare), labels=labels2, textprops={'fontsize': 15, 'weight':'bold'}, wedgeprops={"linewidth": 1, "edgecolor": "white"}, colors=[color_mapping_by_sigla[key] for key in labels2])#, radius=len(df2)/(max(len(df1), len(df2))))
#ax[2].pie(list(df_pie3.IdParlamentare), labels=labels3, textprops={'fontsize': 15, 'weight':'bold'}, wedgeprops={"linewidth": 1, "edgecolor": "white"}, colors=[color_mapping_by_sigla[key] for key in labels3])#, radius=len(df3)/(max(len(df1), len(df2), len(df3))))
ax[0].set_title('Community 1', fontsize=16, fontweight='bold')
ax[1].set_title('Community 2', fontsize=16, fontweight='bold')
#ax[2].set_title('Community 3', fontsize=16, fontweight='bold')
df_pie1.to_csv(path+'Community1Composition_'+id_table+'_'+ruolo+'.csv')
df_pie2.to_csv(path+'Community2Composition_'+id_table+'_'+ruolo+'.csv')
#df_pie3.to_csv(path+'Community3Composition_'+id_table+'_'+ruolo+'.csv')
plt.tight_layout()
plt.savefig(path+'CommunitiesComposition_'+id_table+'_'+ruolo+'.png', dpi=200)