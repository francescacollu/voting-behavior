import pandas as pd
from datetime import datetime

path_to_data = 'data/'
df_deputati = pd.read_csv(path_to_data+'camera/elenco_deputati_18_con_mandato.csv')
df_senatori1 = pd.read_csv(path_to_data+'senato/senatori_legislatura_18.csv')

df_collegi_senatori = pd.read_csv(path_to_data+'senato/collegio_elenco_senatori_18.csv')
df_collegi_senatori['senatore'] = df_collegi_senatori['senatore'].apply(lambda x: x.split('/')[4])

df_deputati['persona'] = df_deputati['persona'].apply(lambda x: x.split('/')[5])
df_deputati = df_deputati.rename(columns = {'persona': 'IdParlamentare', 'cognome': 'Cognome', 'nome':'Nome', 'dataNascita': 'DataNascita', 'luogoNascita':'CittaNascita', 'nato':'ProvinciaNascita', 'genere':'Sesso', 'collegio':'Collegio'})
df_deputati['ProvinciaNascita'] = df_deputati['ProvinciaNascita'].apply(lambda x:x.split(',')[1])
df_senatori1['senatore'] = df_senatori1['senatore'].apply(lambda x: x.split('/')[4])

df_senatori = pd.merge(df_collegi_senatori, df_senatori1, on=['senatore'], how='outer')
df_senatori = df_senatori.rename(columns = {'senatore': 'IdParlamentare', 'cognome': 'Cognome', 'nome':'Nome', 'dataNascita': 'DataNascita', 'cittaNascita':'CittaNascita', 'provinciaNascita':'ProvinciaNascita', 'regioneElezione':'Collegio', 'sesso':'Sesso'})

df_deputati = df_deputati[['IdParlamentare', 'Cognome', 'Nome', 'DataNascita', 'CittaNascita', 'ProvinciaNascita', 'Sesso']]

for row in df_deputati.index:
    df_deputati['DataNascita'][row] = datetime.strptime(str(df_deputati['DataNascita'][row]), '%Y%m%d').strftime('%Y-%m-%d')

df_deputati['Sesso'] = df_deputati['Sesso'].apply(lambda x : 'M' if x=='male' else 'F')

df_senatori = df_senatori[['IdParlamentare', 'Cognome', 'Nome', 'DataNascita', 'CittaNascita', 'ProvinciaNascita', 'Sesso']]

lista_camera_senato = [df_deputati, df_senatori]
df_parlamentari = pd.concat(lista_camera_senato, ignore_index=True)
df_parlamentari = df_parlamentari.drop_duplicates()

df_parlamentari['Cognome'] = df_parlamentari['Cognome'].apply(lambda x : x.title())
df_parlamentari['Nome'] = df_parlamentari['Nome'].apply(lambda x : x.title())
df_parlamentari['CittaNascita'] = df_parlamentari['CittaNascita'].apply(lambda x : x.title())

df_parlamentari['ProvinciaNascita'] = df_parlamentari['ProvinciaNascita'].apply(lambda x : str(x).title() if len(str(x))>0 else '')

df_parlamentari['ProvinciaNascita'] = df_parlamentari['ProvinciaNascita'].str.strip()