import pandas as pd
import numpy as np
import glob
import os
from DfGruppiParlamentari import *
from ProgressBar import *


globbed_files = glob.glob('data/senato/Senato_18/*.csv')
data = []

globbed_files = globbed_files
printProgressBar(0, len(globbed_files), prefix = 'Progress:', suffix = 'Complete', length = 50)

for csv in globbed_files:
    votazioni_singolo_senatore = pd.read_csv(csv)
    file_name = os.path.basename(csv).split('_')[2]
    votazioni_singolo_senatore['Senatore'] = file_name.split('.')[0]
    data.append(votazioni_singolo_senatore)
    printProgressBar(list(globbed_files).index(csv) + 1, len(globbed_files), prefix = 'Progress:', suffix = 'Complete', length = 50)


votazioni_totale_senatori = pd.concat(data, ignore_index=True)
votazioni_totale_senatori = votazioni_totale_senatori[['Senatore','votazione', 'atto', 'voto']]
votazioni_totale_senatori = votazioni_totale_senatori.rename(columns = {'votazione': 'Votazione', 'atto':'Ddl', 'voto': 'Voto'})
votazioni_totale_senatori['Voto'] = votazioni_totale_senatori['Voto'].apply(lambda x: x.split('/')[4])
votazioni_totale_senatori['Ddl'] = votazioni_totale_senatori['Ddl'].apply(lambda x: x.split('/')[4])
votazioni_totale_senatori['Votazione'] = votazioni_totale_senatori['Votazione'].apply(lambda x: x.split('/')[4])
votazioni_totale_senatori = votazioni_totale_senatori[(votazioni_totale_senatori['Voto'] == 'favorevole') | (votazioni_totale_senatori['Voto'] == 'contrario')]

votazioni_totale_senatori_con_gruppi = pd.merge(votazioni_totale_senatori, df_gruppi_parlamentari, on=['Senatore'])
votazioni_totale_senatori_con_gruppi = votazioni_totale_senatori_con_gruppi[['Senatore', 'Ddl', 'Voto', 'nomeGruppo']]
votazioni_totale_senatori_con_gruppi = votazioni_totale_senatori_con_gruppi.rename(columns = {'nomeGruppo': 'GruppoSenatoreVotante'})
votazioni_totale_senatori_con_gruppi = votazioni_totale_senatori_con_gruppi.drop_duplicates()
lista_ddl_con_presentatori = pd.read_csv('./SENATO/elenco_ddl_con_presentatori.csv')
lista_ddl_con_presentatori = lista_ddl_con_presentatori[['ddl', 'descrIniziativa']]
lista_ddl_con_presentatori['Ruolo'] = lista_ddl_con_presentatori['descrIniziativa'].apply(lambda x:x.split(' ')[0])
lista_ddl_con_presentatori['ParlamentareProponente'] = lista_ddl_con_presentatori['descrIniziativa'].apply(lambda x:x.split(' ')[1:])

for i in lista_ddl_con_presentatori.index:
    while 'ed' in lista_ddl_con_presentatori['ParlamentareProponente'][i] : lista_ddl_con_presentatori['ParlamentareProponente'][i].remove('ed')
    while 'altri' in lista_ddl_con_presentatori['ParlamentareProponente'][i]: lista_ddl_con_presentatori['ParlamentareProponente'][i].remove('altri')
    lista_ddl_con_presentatori['ParlamentareProponente'][i] = ' '.join(lista_ddl_con_presentatori['ParlamentareProponente'][i])

lista_ddl_con_presentatori['ddl'] = lista_ddl_con_presentatori['ddl'].apply(lambda x:x.split('/')[4])
lista_deputati_con_gruppo = pd.read_csv('./CAMERA/elenco_deputati_con_gruppo.csv')
lista_deputati_con_gruppo['Deputato'] = lista_deputati_con_gruppo['cognome'] + ' ' + lista_deputati_con_gruppo['nome']
lista_deputati_con_gruppo = lista_deputati_con_gruppo[['nomeGruppo', 'Deputato']]
lista_deputati_con_gruppo = lista_deputati_con_gruppo.rename(columns = {'nomeGruppo' : 'GruppoDeputato'})
lista_deputati_con_gruppo = lista_deputati_con_gruppo.drop_duplicates()

for i in lista_deputati_con_gruppo.index:
    lista_deputati_con_gruppo['Deputato'][i] = lista_deputati_con_gruppo['Deputato'][i].title()

    if lista_deputati_con_gruppo['GruppoDeputato'][i].startswith('MISTO'):
        lista_deputati_con_gruppo['GruppoDeputato'][i] = 'Misto'
    if lista_deputati_con_gruppo['GruppoDeputato'][i].startswith('PARTITO'):
        lista_deputati_con_gruppo['GruppoDeputato'][i] = 'Partito Democratico'
    if lista_deputati_con_gruppo['GruppoDeputato'][i].startswith('BERLUSCONI'):
        lista_deputati_con_gruppo['GruppoDeputato'][i] = 'Forza Italia - Berlusconi Presidente'
    if lista_deputati_con_gruppo['GruppoDeputato'][i].startswith('FRATELLI'):
        lista_deputati_con_gruppo['GruppoDeputato'][i] = 'Fratelli d\'Italia'
    if lista_deputati_con_gruppo['GruppoDeputato'][i].startswith('LEGA'):
        lista_deputati_con_gruppo['GruppoDeputato'][i] = 'Lega-Salvini Premier-Partito Sardo d\'Azione'
    if lista_deputati_con_gruppo['GruppoDeputato'][i].startswith('CORAGGIO'):
        lista_deputati_con_gruppo['GruppoDeputato'][i] = 'Coraggio Italia'
    if lista_deputati_con_gruppo['GruppoDeputato'][i].startswith('LIBERI'):
        lista_deputati_con_gruppo['GruppoDeputato'][i] = 'Liberi e Uguali'
    if lista_deputati_con_gruppo['GruppoDeputato'][i].startswith('MOVIMENTO'):
        lista_deputati_con_gruppo['GruppoDeputato'][i] = 'MoVimento 5 Stelle'
    if lista_deputati_con_gruppo['GruppoDeputato'][i].startswith('ITALIA'):
        lista_deputati_con_gruppo['GruppoDeputato'][i] = 'Italia Viva'

lista_senatori_con_gruppo = df_gruppi_parlamentari[['nomeGruppo', 'Senatore']]

votazioni_senatori_con_gruppi_proponenti_dep = pd.merge(lista_ddl_con_presentatori[lista_ddl_con_presentatori['Ruolo'] == 'Dep.'], lista_deputati_con_gruppo, left_on=['ParlamentareProponente'], right_on=['Deputato'])
votazioni_senatori_con_gruppi_proponenti_sen = pd.merge(lista_ddl_con_presentatori[lista_ddl_con_presentatori['Ruolo'] == 'Sen.'], lista_senatori_con_gruppo, left_on=['ParlamentareProponente'], right_on=['Senatore'])
frames = [votazioni_senatori_con_gruppi_proponenti_dep, votazioni_senatori_con_gruppi_proponenti_sen]
votazioni_senatori_con_gruppi_proponenti = pd.concat(frames)
votazioni_senatori_con_gruppi_proponenti = votazioni_senatori_con_gruppi_proponenti[['ddl', 'Ruolo', 'ParlamentareProponente', 'GruppoParlamentareProponente']]
votazioni_senatori_con_gruppi_proponenti = votazioni_senatori_con_gruppi_proponenti.rename(columns={'ddl':'Ddl'})
dataset_senato = pd.merge(votazioni_totale_senatori_con_gruppi, votazioni_senatori_con_gruppi_proponenti, on=['Ddl'])