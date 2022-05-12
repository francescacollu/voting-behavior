import pandas as pd

path_to_data = 'data/'
df_gruppi_parlamentari = pd.read_csv(path_to_data+'senato/elenco_gruppi_senato.csv')
df_gruppi_parlamentari['Senatore'] = df_gruppi_parlamentari['cognome'] + ' ' + df_gruppi_parlamentari['nome']