import pandas as pd
from datetime import datetime

from DF_GruppiParlamentari import *

path_to_data = 'data/'
df_variazione_gruppo_deputati = pd.read_csv(path_to_data+'camera/variazioni_gruppi_deputati.csv')
df_variazione_gruppo_senatori = pd.read_csv(path_to_data+'senato/variazioni_gruppi_senatori.csv')

df_variazione_gruppo_deputati['persona'] = df_variazione_gruppo_deputati['persona'].apply(lambda x:x.split('/')[5])
df_variazione_gruppo_deputati = df_variazione_gruppo_deputati.rename(columns = {'persona': 'IdParlamentare', 'GruppoStartDate':'DataIngresso', 'nomeGruppo':'NomeGruppo'})

for i in df_variazione_gruppo_deputati.index:
    if df_variazione_gruppo_deputati.loc[i, 'NomeGruppo'].startswith('MISTO'):
        df_variazione_gruppo_deputati.loc[i, 'NomeGruppo'] = 'Misto'
    elif df_variazione_gruppo_deputati.loc[i, 'NomeGruppo'].startswith('PARTITO'):
        df_variazione_gruppo_deputati.loc[i, 'NomeGruppo'] = 'Partito Democratico'
    elif df_variazione_gruppo_deputati.loc[i, 'NomeGruppo'].startswith('FORZA'):
        df_variazione_gruppo_deputati.loc[i, 'NomeGruppo'] = 'Forza Italia-Berlusconi Presidente'
    elif df_variazione_gruppo_deputati.loc[i, 'NomeGruppo'].startswith('FRATELLI'):
        df_variazione_gruppo_deputati.loc[i, 'NomeGruppo'] = 'Fratelli d\'Italia'
    elif df_variazione_gruppo_deputati.loc[i, 'NomeGruppo'].startswith('LEGA'):
        df_variazione_gruppo_deputati.loc[i, 'NomeGruppo'] = 'Lega-Salvini Premier'
    elif df_variazione_gruppo_deputati.loc[i, 'NomeGruppo'].startswith('CORAGGIO'):
        df_variazione_gruppo_deputati.loc[i, 'NomeGruppo'] = 'Coraggio Italia'
    elif df_variazione_gruppo_deputati.loc[i, 'NomeGruppo'].startswith('LIBERI'):
        df_variazione_gruppo_deputati.loc[i, 'NomeGruppo'] = 'Liberi e Uguali'
    elif df_variazione_gruppo_deputati.loc[i, 'NomeGruppo'].startswith('MOVIMENTO'):
        df_variazione_gruppo_deputati.loc[i, 'NomeGruppo'] = 'MoVimento 5 Stelle'
    elif df_variazione_gruppo_deputati.loc[i, 'NomeGruppo'].startswith('ITALIA'):
        df_variazione_gruppo_deputati.loc[i, 'NomeGruppo'] = 'Italia Viva'
    else:
        df_variazione_gruppo_deputati.loc[i, 'NomeGruppo'] = ''

df_variazione_gruppo_deputati = df_variazione_gruppo_deputati[['IdParlamentare', 'NomeGruppo', 'DataIngresso']].drop_duplicates()
for row in df_variazione_gruppo_deputati.index:
    df_variazione_gruppo_deputati['DataIngresso'][row] = datetime.strptime(str(df_variazione_gruppo_deputati['DataIngresso'][row]), '%Y%m%d').strftime('%Y-%m-%d')

df_variazione_gruppo_senatori['senatore'] = df_variazione_gruppo_senatori['senatore'].apply(lambda x:x.split('/')[4])
df_variazione_gruppo_senatori = df_variazione_gruppo_senatori.rename(columns = {'senatore': 'IdParlamentare', 'inizio':'DataIngresso', 'nomeGruppo':'NomeGruppo'})
df_variazione_gruppo_senatori = df_variazione_gruppo_senatori[['IdParlamentare', 'NomeGruppo', 'DataIngresso']].drop_duplicates()

lista_variazione_camera_senato = [df_variazione_gruppo_deputati, df_variazione_gruppo_senatori]

df_variazione_gruppi_parlamento = pd.concat(lista_variazione_camera_senato)

df_variazione_gruppi_parlamento = pd.merge(df_variazione_gruppi_parlamento, df_gruppi_parlamentari, on=['NomeGruppo'])
df_variazione_gruppi_parlamento = df_variazione_gruppi_parlamento[['IdParlamentare', 'IdGruppo', 'DataIngresso']]