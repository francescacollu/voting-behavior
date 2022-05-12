import pandas as pd

path_to_data = 'data/'
df_mandati_deputati = pd.read_csv(path_to_data+'camera/elenco_deputati_18_con_mandato.csv')
df_mandati_senatori = pd.read_csv(path_to_data+'senato/senatori_legislatura_18.csv')

df_mandati_deputati = df_mandati_deputati[['persona', 'inizioMandato', 'fineMandato']]
df_mandati_deputati['Legislatura'] = '18'
df_mandati_deputati['Ruolo'] = 'Dep'
df_mandati_senatori = df_mandati_senatori[['senatore', 'inizioMandato', 'fineMandato', 'legislatura']]
df_mandati_senatori['Ruolo'] = 'Sen'

df_mandati_deputati = df_mandati_deputati.rename(columns={'persona':'IdParlamentare', 'inizioMandato':'InizioMandato', 'fineMandato':'FineMandato'})
df_mandati_senatori = df_mandati_senatori.rename(columns={'senatore':'IdParlamentare', 'inizioMandato':'InizioMandato', 'fineMandato':'FineMandato', 'legislatura':'Legislatura'})

df_mandati_deputati['IdParlamentare'] = df_mandati_deputati['IdParlamentare'].apply(lambda x : x.split('/')[5])
df_mandati_senatori['IdParlamentare'] = df_mandati_senatori['IdParlamentare'].apply(lambda x : x.split('/')[4])

df_mandati_deputati['InizioMandato'] = pd.to_datetime(df_mandati_deputati['InizioMandato'], errors='coerce', format='%Y%m%d')
df_mandati_deputati['FineMandato'] = pd.to_datetime(df_mandati_deputati['FineMandato'], errors='coerce', format='%Y%m%d')
df_mandati_deputati['InizioMandato'] = df_mandati_deputati['InizioMandato'].apply(lambda x: x.strftime('%Y-%m-%d') if not pd.isnull(x) else '')
df_mandati_deputati['FineMandato'] = df_mandati_deputati['FineMandato'].apply(lambda x: x.strftime('%Y-%m-%d') if not pd.isnull(x) else '')

df_mandati_senatori['InizioMandato'] = pd.to_datetime(df_mandati_senatori['InizioMandato'], errors='coerce', format='%Y-%m-%d')
df_mandati_senatori['FineMandato'] = pd.to_datetime(df_mandati_senatori['FineMandato'], errors='coerce', format='%Y-%m-%d')
df_mandati_senatori['InizioMandato'] = df_mandati_senatori['InizioMandato'].apply(lambda x: x.strftime('%Y-%m-%d') if not pd.isnull(x) else '')
df_mandati_senatori['FineMandato'] = df_mandati_senatori['FineMandato'].apply(lambda x: x.strftime('%Y-%m-%d') if not pd.isnull(x) else '')

df_mandati_parlamento = pd.concat([df_mandati_deputati, df_mandati_senatori], ignore_index=True)


# for row in df_mandati_parlamento.index:
#     if df_mandati_parlamento['Ruolo'][row] == 'Dep':
#         df_mandati_parlamento['InizioMandato'][row] = datetime.strptime(str(df_mandati_parlamento['InizioMandato'][row]), '%Y%m%d').strftime('%Y-%m-%d')
#         df_mandati_parlamento['FineMandato'][row] = datetime.strptime(str(df_mandati_parlamento['FineMandato'][row]), '%Y%m%d').strftime('%Y-%m-%d')