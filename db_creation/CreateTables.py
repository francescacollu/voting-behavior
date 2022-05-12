# The db is made up by the following tables:
# 1. Parlamentare (from DF_Parlamentari import *)
# 2. GruppoParlamentare
# 3. VariazioneGruppo
# 4. Mandato
# 5. Atto
# 6. Votazione
# In order to create (or re-create) the entire database, you must create all these tables.
# You are going to need the dataframe (DF) that you can create with the corrensponding scripts.


from sqlalchemy import create_engine
import numpy as np
import math
from credentials_file import *
from DF_Votazioni import *

###########################################
# Set:
table_name = 'Votazione'
df_to_convert = df_votazioni_parlamento
###########################################

engine = create_engine('mysql+mysqlconnector://root:'+db_password+'@127.0.0.1:3306/'+db_name)
# df_to_convert.to_sql(name=table_name, con=engine, if_exists='replace', index=False)

# Uncomment for the creation of votations table only:

rows_per_packet = 100000
splitted_df = np.array_split(df_votazioni_parlamento, math.ceil(len(df_votazioni_parlamento.index)/rows_per_packet))

for i, chunk in enumerate(splitted_df):
    print('Appending chunk number '+ str(i+1) + '/' + str(len(splitted_df)))
    chunk.to_sql(name='Votazione', con=engine, if_exists='append', index=False)