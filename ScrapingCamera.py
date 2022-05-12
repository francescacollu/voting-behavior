import urllib3
import os

def get_url(congressman_last_name, date, legislature):
    url = "http://dati.camera.it/sparql?query=select+distinct+%3Fcognome+%3Fnome+%3Fvotazione+%3Fdata+%3Fdescrizione+%3FnumeroVotazione+%0D%0A%3Fespressione+%3FesitoVotazione+%3FAtto%0D%0A%3FinfoAssenza+where+%7B%0D%0A%0D%0A%3Fdeputato+foaf%3Asurname+%3Fcognome%3B+foaf%3AfirstName+%3Fnome%3B+ocd%3Arif_leg+%0D%0A%3Chttp%3A%2F%2Fdati.camera.it%2Focd%2Flegislatura.rdf%2Frepubblica_"+legislature+"%3E%0D%0AFILTER%28REGEX%28%3Fcognome%2C%27"+congressman_last_name+"%27%2C%27i%27%29%29%0D%0A%0D%0A%3Fvoto+a+ocd%3Avoto%3B%0D%0A+++ocd%3Arif_votazione+%3Fvotazione%3B%0D%0A+++dc%3Atype+%3Fespressione%3B%0D%0A+++ocd%3Arif_deputato+%3Fdeputato.%0D%0AOPTIONAL%7B%3Fvoto+dc%3Adescription+%3FinfoAssenza%7D%0D%0A%0D%0A%3Fvotazione+a+ocd%3Avotazione%3B%0D%0A+++ocd%3Aapprovato+%3FesitoVotazione%3B%0D%0A+++dc%3Adescription+%3Fdescrizione%3B%0D%0A+++dc%3Aidentifier+%3FnumeroVotazione%3B%0D%0A+++ocd%3Arif_attoCamera+%3FAtto%3B%0D%0A+++dc%3Adate+%3Fdata.+FILTER%28REGEX%28%3Fdata%2C%27%5E"+date+"%27%2C%27i%27%29%29+%0D%0A%0D%0A%7D&debug=on&default-graph-uri=&format=text%2Fcsv"
    return url

def create_doc(folder, congressman_name, data):
    f = open(os.path.relpath(folder+'/'+congressman_name+'.csv'), 'wb')
    f.write(data)
    f.close()
    
def retrieve_congressman_data(congressman_surname, date, legislature):
    http = urllib3.PoolManager()
    url = get_url(congressman_surname, date, legislature)
    response = http.request('GET', url)
    return response.data

def run_scraping(congressmen_list, path, year, legislature, min_index, max_index):
    for i in range(min_index, max_index):
        print('Downloading '+str(i+1-min_index)+' of '+str(max_index-min_index))  
        output_data = retrieve_congressman_data(congressmen_list[i], year, legislature)
        create_doc(path, congressmen_list[i], output_data)