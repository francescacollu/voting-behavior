import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from credentials_file import *
from DF_Parlamentari import *

path_to_data = 'data/'
engine = create_engine('mysql+mysqlconnector://root:'+db_password+'@127.0.0.1:3306/'+db_name)
df_parlamentari = pd.read_sql('''
SELECT P.IdParlamentare, CONCAT(P.Cognome, ' ', P.Nome) AS ParlamentareProponente
FROM Parlamentare P INNER JOIN Mandato M ON P.IdParlamentare=M.IdParlamentare
WHERE P.IdParlamentare NOT IN ('32898');
''', con=engine)

#Atti Senato
df_atti_senato_con_presentatori = pd.read_csv(path_to_data+'senato/atti_presentatori_leg18_2018_2021.csv')
df_atti_senato_con_presentatori['Ruolo'] = df_atti_senato_con_presentatori['descrIniziativa'].apply(lambda x:x.split(' ')[0])
df_atti_senato_con_presentatori['Iniziativa'] = df_atti_senato_con_presentatori['descrIniziativa'].apply(lambda x:x.split(' ')[1:] if x != 'POPOLARE' else x.title())

for i in df_atti_senato_con_presentatori.index:
    if df_atti_senato_con_presentatori['Iniziativa'][i] != 'Popolare':
        while 'ed' in df_atti_senato_con_presentatori['Iniziativa'][i] : df_atti_senato_con_presentatori['Iniziativa'][i].remove('ed')
        while 'altri' in df_atti_senato_con_presentatori['Iniziativa'][i]: df_atti_senato_con_presentatori['Iniziativa'][i].remove('altri')
        df_atti_senato_con_presentatori['Iniziativa'][i] = ' '.join(df_atti_senato_con_presentatori['Iniziativa'][i])
df_atti_senato_con_presentatori = df_atti_senato_con_presentatori.rename(columns={'ddl':'IdDdl','titolo':'Titolo', 'dataPresentazione':'DataPresentazione', 'stato':'FaseIter', 'dataStato':'DataIter'})
df_atti_senato_con_presentatori['IdDdl'] = df_atti_senato_con_presentatori['IdDdl'].apply(lambda x: x.split('/')[4])
df_atti_senato_con_presentatori = pd.merge(df_atti_senato_con_presentatori, df_parlamentari, left_on=['Iniziativa'], right_on=['ParlamentareProponente'], how='left')

df_atti_senato_con_presentatori = df_atti_senato_con_presentatori.rename(columns={'IdParlamentare':'IdParlamentareProponente'})
df_atti_senato_con_presentatori = df_atti_senato_con_presentatori[['IdDdl', 'IdParlamentareProponente', 'Iniziativa', 'Titolo', 'DataPresentazione', 'FaseIter', 'DataIter']]
df_atti_senato_con_presentatori.drop_duplicates(inplace=True)


#Atti Camera
df_atti_camera_con_presentatori_2018 = pd.read_csv(path_to_data+'camera/atti_optional_presentatori_leg18_2018.csv')
df_atti_camera_con_presentatori_2019 = pd.read_csv(path_to_data+'camera/atti_optional_presentatori_leg18_2019.csv')
df_atti_camera_con_presentatori_2020 = pd.read_csv(path_to_data+'camera/atti_optional_presentatori_leg18_2020.csv')
df_atti_camera_con_presentatori_2021 = pd.read_csv(path_to_data+'camera/atti_optional_presentatori_leg18_2021.csv')

df_atti_camera_con_presentatori = pd.concat([df_atti_camera_con_presentatori_2018, df_atti_camera_con_presentatori_2019], ignore_index=True)
df_atti_camera_con_presentatori = pd.concat([df_atti_camera_con_presentatori, df_atti_camera_con_presentatori_2020], ignore_index=True)
df_atti_camera_con_presentatori = pd.concat([df_atti_camera_con_presentatori, df_atti_camera_con_presentatori_2021], ignore_index=True)

df_atti_camera_con_presentatori['atto'] = df_atti_camera_con_presentatori['atto'].apply(lambda x: x.split('/')[5])

for row in df_atti_camera_con_presentatori.index:
    if df_atti_camera_con_presentatori.loc[row, 'iniziativa'] == 'Parlamentare' and df_atti_camera_con_presentatori.loc[row, 'proponente'] != '' and df_atti_camera_con_presentatori.loc[row, 'proponente'] is not np.nan:
        df_atti_camera_con_presentatori.loc[row, 'proponente'] = df_atti_camera_con_presentatori.loc[row, 'proponente'].split('/')[5].split('_')[-2][1:]
        df_atti_camera_con_presentatori.loc[row, 'proponente'] = 'p'+ df_atti_camera_con_presentatori.loc[row, 'proponente']

for row in df_atti_camera_con_presentatori.index:
    df_atti_camera_con_presentatori.loc[row, 'presentazione'] = datetime.strptime(str(df_atti_camera_con_presentatori.loc[row, 'presentazione']), '%Y%m%d').strftime('%Y-%m-%d')

for row in df_atti_camera_con_presentatori.index:
    df_atti_camera_con_presentatori.loc[row, 'dataIter'] = datetime.strptime(str(df_atti_camera_con_presentatori.loc[row, 'dataIter']), '%Y%m%d').strftime('%Y-%m-%d')

df_atti_camera_con_presentatori = df_atti_camera_con_presentatori[['atto', 'presentazione', 'titolo', 'proponente', 'fase', 'dataIter', 'iniziativa']]
df_atti_camera_con_presentatori = df_atti_camera_con_presentatori.rename(columns={'atto':'IdDdl','iniziativa':'Iniziativa', 'titolo':'Titolo', 'presentazione':'DataPresentazione', 'proponente':'ParlamentareProponente', 'fase':'FaseIter', 'dataIter':'DataIter'})

# df_atti_camera_con_presentatori = pd.merge(df_atti_camera_con_presentatori, df_parlamentari, on=['ParlamentareProponente'], how='left')
df_atti_camera_con_presentatori = df_atti_camera_con_presentatori.rename(columns={'ParlamentareProponente':'IdParlamentareProponente'})
df_atti_camera_con_presentatori = df_atti_camera_con_presentatori[['IdDdl', 'IdParlamentareProponente', 'Titolo', 'DataPresentazione', 'FaseIter', 'DataIter', 'Iniziativa']]

df_atti_camera_con_presentatori['Titolo'] = df_atti_camera_con_presentatori['Titolo'].apply(lambda x : x[x.find(' "')+1:].strip('"') if ': "' in x else x)
df_atti_camera_con_presentatori['Titolo'] = df_atti_camera_con_presentatori['Titolo'].apply(lambda x : x[:x.find(' (')])
df_atti_camera_con_presentatori['Titolo'] = df_atti_camera_con_presentatori['Titolo'].apply(lambda x : x.strip('"'))

df_atti_camera_con_presentatori.drop_duplicates(inplace=True)


#df_atti_con_presentatori = pd.concat([df_atti_senato_con_presentatori, df_atti_camera_con_presentatori], ignore_index=True)
#df_atti_con_presentatori = df_atti_con_presentatori.drop_duplicates()

#Puliamo due record che risultano avere qualche errore di formattazione:

df_atti_camera_con_presentatori['Titolo'] = df_atti_camera_con_presentatori['Titolo'].apply(lambda x : x[x.find('&quot;')+6:] if '&quot;' in x else x)
df_atti_camera_con_presentatori['Titolo'] = df_atti_camera_con_presentatori['Titolo'].apply(lambda x : x[:x.find('&quot;')] if '&quot;' in x else x)
df_atti_camera_con_presentatori['Titolo'] = df_atti_camera_con_presentatori['Titolo'].apply(lambda x : x.replace('&#39;', "'") if '&#39;' in x else x)
df_atti_camera_con_presentatori['Titolo'] = df_atti_camera_con_presentatori['Titolo'].apply(lambda x : x.replace('&eacute;', 'é') if '&eacute;' in x else x)
df_atti_camera_con_presentatori['Titolo'] = df_atti_camera_con_presentatori['Titolo'].apply(lambda x : x.replace('&rsquo;', "'") if '&rsquo;' in x else x)
df_atti_camera_con_presentatori['Titolo'] = df_atti_camera_con_presentatori['Titolo'].apply(lambda x : x.replace('&agrave;', 'à') if '&agrave' in x else x)

# Puliamo la colonna relativa alla fase dell'iter:

df_atti_camera_con_presentatori['FaseIter'] = df_atti_camera_con_presentatori['FaseIter'].apply(lambda x:x.title())
df_atti_senato_con_presentatori['FaseIter'] = df_atti_senato_con_presentatori['FaseIter'].apply(lambda x:x.title())


# Consideriamo solo l'ultima fase dell'iter al momento della raccolta dei dati:

df_atti_camera_con_presentatori = df_atti_camera_con_presentatori.sort_values('DataIter').groupby('IdDdl').tail(1)
df_atti_senato_con_presentatori = df_atti_senato_con_presentatori.sort_values('DataIter').groupby('IdDdl').tail(1)


# Concateniamo
df_atti_parlamento = pd.concat([df_atti_camera_con_presentatori, df_atti_senato_con_presentatori], ignore_index=True)