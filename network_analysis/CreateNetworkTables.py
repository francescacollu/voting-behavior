# IMPORTANTE: bisogna specificare, se necessario: 
# 1) il ruolo dei parlamentari (se Sen o Dep) 
# 2) il nome da assegnare alla votazione per salvare il nome delle tabelle nel DB (id_votazione)
# 3) l'id del ddl relativo alle date votazioni (id_ddl) o l'intervallo temporale di interesse (specificando start_date ed end_date)

import pandas as pd
from sqlalchemy import create_engine
import networkx as nx
import datetime

ruolo = 'Sen'
# id_ddl = 'ac18_491'
start_date = '2019-09-06'
end_date = '2019-10-25'
id_table =  'ForzeArmateEDellOrdine' # Specifichiamo il/gli id della/e votazione/i considerate (con il fine di salvare i nomi delle tabelle sul DB)


engine = create_engine('mysql+mysqlconnector://root:Fiorentino68*@127.0.0.1:3306/VotingBehavior')

def GetIdParlamentari(DB_engine, ruolo):
    df = pd.read_sql('''
    SELECT DISTINCT P.IdParlamentare
    FROM Parlamentare P INNER JOIN Mandato M ON P.IdParlamentare=M.IdParlamentare
	INNER JOIN VariazioneGruppo VG ON P.IdParlamentare=VG.IdParlamentare
	INNER JOIN Votazione V ON V.IdParlamentare=P.IdParlamentare
    WHERE M.Ruolo=%s AND V.IdDdl IN
    ('50700',
'49170',
'48739',
'50278',
'50386',
'50447',
'52256',
'ac18_1346',
'ac18_2242',
'ac18_1012',
'ac18_875');
    ''', con=DB_engine, params=[ruolo])
    print('Just got IdParlamentari list!')
    return df.IdParlamentare
#AND V.IdDdl="'''+id_ddl+'''";
#AND V.DataVotazione BETWEEN "'''+start_date+'''" AND "'''+end_date+'''";

def GetIdDdl(DB_engine):
    df = pd.read_sql('''
    SELECT IdDdl
    FROM Atto;
    ''', con=DB_engine)
    return df.IdDdl

# GetIdVotazione con la lista degli atti
def GetIdVotazione(DB_engine, id_ddl):
    df = pd.read_sql('''
    SELECT DISTINCT V.IdVotazione 
    FROM Votazione V 
    WHERE V.IdDdl IN
    ('50700',
'49170',
'48739',
'50278',
'50386',
'50447',
'52256',
'ac18_1346',
'ac18_2242',
'ac18_1012',
'ac18_875');
    ''', con=DB_engine)
    return df.IdVotazione

def GetVotazione(DB_engine, id_ddl):
    df = pd.read_sql(f'''
    SELECT V.* 
    FROM Votazione V 
    WHERE V.IdDdl IN
    ('50700',
'49170',
'48739',
'50278',
'50386',
'50447',
'52256',
'ac18_1346',
'ac18_2242',
'ac18_1012',
'ac18_875');
    ''', con=DB_engine)
    print('Just got Votazione dataframe!')
    return df

#GetIdVotazione con un limite temporale    
# def GetIdVotazione(DB_engine, startDate, endDate, ruolo):
#     df = pd.read_sql('''
#     SELECT DISTINCT V.IdVotazione 
#     FROM Votazione V INNER JOIN Mandato M ON V.IdParlamentare = M.IdParlamentare
#     WHERE DataVotazione BETWEEN %s AND %s
#     AND M.Ruolo = %s;
#     ''', con=DB_engine, params=[startDate, endDate, ruolo])
#     return df.IdVotazione

# def GetVotazione(DB_engine, startDate, endDate, ruolo):
#     df = pd.read_sql('''
#     SELECT V.* 
#     FROM Votazione V INNER JOIN Mandato M ON V.IdParlamentare = M.IdParlamentare
#     WHERE DataVotazione BETWEEN %s AND %s
#     AND M.Ruolo = %s;
#     ''', con=DB_engine, params=[startDate, endDate, ruolo])
#     print('Just got Votazione dataframe!')
#     return df

def CreateEmptyTable(parlamentari, votazioni):
    df = pd.DataFrame(columns = votazioni, index=parlamentari)
    df.index.name = 'IdParlamentare'
    print('Just created table!')
    return df

def CreateFavorevoliTable(empty_df, votazioni, parlamentari):
    idVotazioni_list = list(id_votazioni)
    for i, parlamentare in enumerate(parlamentari):
        print(str(i)+' over '+str(len(parlamentari)))
        for idvotazione in idVotazioni_list:
            if len(votazioni[(votazioni['IdVotazione']==idvotazione) & (votazioni['IdParlamentare']==parlamentare) & (votazioni['Voto']=='Favorevole')])>0:
                empty_df.loc[parlamentare, idvotazione] = 1 
            else:
                empty_df.loc[parlamentare, idvotazione] = 0 
        fav_df = empty_df.copy()
    return fav_df

def CreateContrariTable(empty_df, votazioni, parlamentari):
    idVotazioni_list = list(id_votazioni)
    for i, parlamentare in enumerate(parlamentari):
        print(str(i)+' over '+str(len(parlamentari)))
        for idvotazione in idVotazioni_list:
            if len(votazioni[(votazioni['IdVotazione']==idvotazione) & (votazioni['IdParlamentare']==parlamentare) & (votazioni['Voto']=='Contrario')])>0:
                empty_df.loc[parlamentare, idvotazione] = 1 
            else:
                empty_df.loc[parlamentare, idvotazione] = 0 
        con_df = empty_df.copy()
    return con_df

def CreateAstenutiTable(empty_df, votazioni, parlamentari):
    idVotazioni_list = list(id_votazioni)
    for i, parlamentare in enumerate(parlamentari):
        print(str(i)+' over '+str(len(parlamentari)))
        for idvotazione in idVotazioni_list:
            if len(votazioni[(votazioni['IdVotazione']==idvotazione) & (votazioni['IdParlamentare']==parlamentare) & (votazioni['Voto']=='Astenuto')])>0:
                empty_df.loc[parlamentare, idvotazione] = 1 
            else:
                empty_df.loc[parlamentare, idvotazione] = 0 
        fav_df = empty_df.copy()
    return fav_df


parlamentari = list(GetIdParlamentari(engine, ruolo))
# votazioni = GetVotazione(engine, start_date, end_date, ruolo)
# id_votazioni = GetIdVotazione(engine, start_date, end_date, ruolo)
votazioni = GetVotazione(engine, ruolo)
id_votazioni = GetIdVotazione(engine, ruolo)
empty_table = CreateEmptyTable(parlamentari, id_votazioni)
fav_df = CreateFavorevoliTable(empty_table, votazioni, parlamentari)
print('=============================')
empty_table = CreateEmptyTable(parlamentari, id_votazioni)
con_df = CreateContrariTable(empty_table, votazioni, parlamentari)
print('=============================')
empty_table = CreateEmptyTable(parlamentari, id_votazioni)
ast_df = CreateAstenutiTable(empty_table, votazioni, parlamentari)
fav_df.reset_index(inplace=True)
con_df.reset_index(inplace=True)
ast_df.reset_index(inplace=True)

fav_df.to_sql(name='V_Fav_'+id_table+'_'+ruolo, con=engine, if_exists='replace', index=False)
con_df.to_sql(name='V_Con_'+id_table+'_'+ruolo, con=engine, if_exists='replace', index=False)
ast_df.to_sql(name='V_Ast_'+id_table+'_'+ruolo, con=engine, if_exists='replace', index=False)