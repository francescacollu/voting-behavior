import pandas as pd
import glob
import os
from sqlalchemy import create_engine
from credentials_file import *
from DF_GruppiParlamentari import *

path_to_data = 'data/'
engine = create_engine('mysql+mysqlconnector://root:'+db_password+'@127.0.0.1:3306/'+db_name)
df_parlamentari = pd.read_sql("SELECT IdParlamentare, CONCAT(Cognome, ' ', Nome) AS Parlamentare FROM Parlamentare;", con=engine)

#Votazioni in Senato

globbed_files_senato = glob.glob(path_to_data+'senato/Senato_18/*.csv')
data_senato = []
votazioni_totale_senatori = pd.DataFrame()

for i, csv in enumerate(globbed_files_senato):
    print('Senate: '+str(i))
    votazioni_singolo_senatore = pd.read_csv(csv)
    file_name = os.path.basename(csv).split('_')[2]
    votazioni_singolo_senatore['Senatore'] = file_name.split('.')[0]
    data_senato.append(votazioni_singolo_senatore)

votazioni_totale_senatori = pd.concat(data_senato, ignore_index=True)
votazioni_totale_senatori['voto'] = votazioni_totale_senatori['voto'].apply(lambda x: x.split('/')[4])
votazioni_totale_senatori['atto'] = votazioni_totale_senatori['atto'].apply(lambda x: x.split('/')[4])
votazioni_totale_senatori['votazione'] = votazioni_totale_senatori['votazione'].apply(lambda x: x.split('/')[4])
votazioni_totale_senatori = votazioni_totale_senatori.rename(columns = {'votazione': 'IdVotazione', 'atto':'IdDdl', 'voto': 'Voto', 'dataSeduta':'DataVotazione'})
votazioni_totale_senatori = pd.merge(votazioni_totale_senatori, df_parlamentari, left_on=['Senatore'], right_on=['Parlamentare'])
votazioni_totale_senatori.to_csv(path_to_data+'votazioni_totale_senatori_18.csv')

df_votazioni_senato = pd.read_csv('votazioni_totale_senatori_18.csv', dtype={'Unnamed: 0':'string', 'DataVotazione':'string', 'numeroSeduta':'string', 'numeroVotazione':'string', 'IdVotazione':'string', 'oggetto':'string', 'IdDdl':'string', 'Voto':'string', 'Senatore':'string', 'IdParlamentare':'string', 'Parlamentare':'string'})
df_votazioni_senato = df_votazioni_senato.rename(columns = {'votazione': 'IdVotazione', 'atto':'IdDdl', 'voto': 'Voto', 'dataSeduta':'DataVotazione'})
df_votazioni_senato['Voto'] = df_votazioni_senato['Voto'].apply(lambda x: x.title() if not pd.isnull(x) else '')
df_votazioni_senato['Voto'] = df_votazioni_senato['Voto'].replace('Astensione', 'Astenuto')
df_votazioni_senato = df_votazioni_senato[df_votazioni_senato['Voto'] != 'Presente']
df_votazioni_senato = df_votazioni_senato[df_votazioni_senato['Voto'] != 'Ha Votato']
df_votazioni_senato = df_votazioni_senato[df_votazioni_senato['Voto'] != 'Non Ha Votato']
df_votazioni_senato = df_votazioni_senato[df_votazioni_senato['Voto'] != 'Votante']
df_votazioni_senato = df_votazioni_senato[df_votazioni_senato['Voto'] != 'Presentenonvotante']
df_votazioni_senato = df_votazioni_senato[df_votazioni_senato['Voto'] != 'Richiedentenonvotante']
df_votazioni_senato.drop_duplicates(inplace=True)
df_votazioni_senato = df_votazioni_senato[['IdVotazione', 'DataVotazione', 'IdDdl', 'IdParlamentare', 'Voto']]

print('Just made Senate df!')



#Votazioni alla Camera
n_rows = 0
data_camera = []
for year in range(2018, 2022):
    print('Year: '+str(year))
    globbed_files_camera = glob.glob(path_to_data+'camera/Camera_18/Camera_18_Y_'+str(year)+'/*.csv')

    for i, csv in enumerate(globbed_files_camera):
        votazioni_singolo_deputato = pd.read_csv(csv)
        n_rows += votazioni_singolo_deputato.shape[0]
        data_camera.append(votazioni_singolo_deputato)
    print(n_rows)
print(len(data_camera))
df_votazioni_camera = pd.concat(data_camera, ignore_index=True)
df_votazioni_camera.to_csv(path_to_data+'votazioni_totale_deputati_18.csv')

#df_votazioni_camera = pd.read_csv('votazioni_totale_deputati_18.csv', dtype={'Unnamed: 0':'string', 'Unnamed: 0.1':'string', 'cognome':'string', 'nome':'string', 'votazione':'string', 'data': np.float64, 'descrizione':'string', 'numeroVotazione':'string', 'espressione':'string', 'esitoVotazione':'string', 'Atto':'string', 'infoAssenza':'string'})

#df_votazioni_camera = df_votazioni_camera[['cognome', 'nome', 'votazione', 'data', 'numeroVotazione', 'espressione', 'esitoVotazione', 'Atto', 'infoAssenza']]

df_votazioni_camera['votazione'] = df_votazioni_camera['votazione'].apply(lambda x: str(x).split('/')[-1])
df_votazioni_camera['data'] = pd.to_datetime(df_votazioni_camera['data'], errors = 'coerce', format='%Y%m%d')
df_votazioni_camera['data'] = df_votazioni_camera['data'].apply(lambda x: x.strftime('%Y-%m-%d') if not pd.isnull(x) else '')
df_votazioni_camera['Atto'] = df_votazioni_camera['Atto'].apply(lambda x: x.split('/')[-1] if not pd.isnull(x) else '')
df_votazioni_camera['Parlamentare'] = df_votazioni_camera['cognome'] + ' ' + df_votazioni_camera['nome']
df_votazioni_camera['Parlamentare'] = df_votazioni_camera['Parlamentare'].apply(lambda x: x.title() if not pd.isnull(x) else '')
df_votazioni_camera = pd.merge(df_votazioni_camera, df_parlamentari, on=['Parlamentare'])
df_votazioni_camera = df_votazioni_camera.rename(columns = {'votazione': 'IdVotazione', 'Atto':'IdDdl', 'espressione': 'Voto', 'data':'DataVotazione'})
df_votazioni_camera['Voto'] = df_votazioni_camera['Voto'].apply(lambda x: x.title() if not pd.isnull(x) else '')
df_votazioni_camera['Voto'] = df_votazioni_camera['Voto'].replace('Astensione', 'Astenuto')
df_votazioni_camera = df_votazioni_camera[df_votazioni_camera['Voto'] != 'Presente']
df_votazioni_camera = df_votazioni_camera[df_votazioni_camera['Voto'] != 'Ha Votato']
df_votazioni_camera = df_votazioni_camera[df_votazioni_camera['Voto'] != 'Non Ha Votato']
df_votazioni_camera = df_votazioni_camera[df_votazioni_camera['Voto'] != 'Votante']
df_votazioni_camera = df_votazioni_camera[df_votazioni_camera['Voto'] != 'Presentenonvotante']
df_votazioni_camera = df_votazioni_camera[df_votazioni_camera['Voto'] != 'Richiedentenonvotante']
df_votazioni_camera.drop_duplicates(inplace=True)
df_votazioni_camera = df_votazioni_camera[['IdVotazione', 'DataVotazione', 'IdDdl', 'IdParlamentare', 'Voto']]

print('Just made Chamber of Deputies!')



# Le due Camere:

df_votazioni_parlamento = pd.concat([df_votazioni_camera, df_votazioni_senato], ignore_index=True)
df_votazioni_parlamento['Voto'] = df_votazioni_parlamento['Voto'].apply(lambda x: x.title() if not pd.isnull(x) else '')
df_votazioni_parlamento['Voto'] = df_votazioni_parlamento['Voto'].replace('Astensione', 'Astenuto')
df_votazioni_parlamento = df_votazioni_parlamento[df_votazioni_parlamento['Voto'] != 'Presente']
df_votazioni_parlamento = df_votazioni_parlamento[df_votazioni_parlamento['Voto'] != 'Ha Votato']
df_votazioni_parlamento = df_votazioni_parlamento[df_votazioni_parlamento['Voto'] != 'Non Ha Votato']
df_votazioni_parlamento = df_votazioni_parlamento[df_votazioni_parlamento['Voto'] != 'Votante']
df_votazioni_parlamento = df_votazioni_parlamento[df_votazioni_parlamento['Voto'] != 'Presentenonvotante']
df_votazioni_parlamento = df_votazioni_parlamento[df_votazioni_parlamento['Voto'] != 'Richiedentenonvotante']
df_votazioni_parlamento.drop_duplicates(inplace=True)
df_votazioni_parlamento.to_csv(path_to_data+'votazioni_totale_parlamento_18.csv')