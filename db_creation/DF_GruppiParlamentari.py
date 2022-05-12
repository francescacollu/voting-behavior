import pandas as pd

lista_gruppi_parlamentari = ['MoVimento 5 Stelle', 'Lega-Salvini Premier', 'Forza Italia-Berlusconi Presidente', 'Coraggio Italia', 'Partito Democratico', 'Italia Viva', "Fratelli d'Italia", 'Liberi e Uguali', "Lega-Salvini Premier-Partito Sardo d'Azione", 'Per le Autonomie (SVP-PATT, UV)', 'Italia Viva - P.S.I.', 'Europeisti-MAIE-Centro Democratico', 'Misto']
d = {'IdGruppo': list(range(13)), 'NomeGruppo': lista_gruppi_parlamentari}
df_gruppi_parlamentari = pd.DataFrame(data = d)