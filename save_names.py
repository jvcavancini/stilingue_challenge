from operator import mod
import requests
import json
import pandas as pd
import time

def get_names(dict):
    return dict['nome']

def get_locations_ids():
    return list(pd.read_csv('locations.csv')['id'])

def get_names_frequency_by_location(names, location_id):
    names_location = ''
    while names_location == '':
        try:
            names_location = requests.get("https://servicodados.ibge.gov.br/api/v2/censos/nomes/" + '|'.join(names) + '?localidade=' + str(location_id)).content.decode('utf-8')
            break
        except:
            print("Connection refused by the server")
            print("Waiting for 5 seconds")
            time.sleep(5)
            print("Continuing")
            continue
    return json.loads(names_location)

def get_attributes(local_id, res):
    attributes = []
    for n in res:
        for r in n['res']:
            attributes.append({
                'nome': n['nome'],
                'local_id': local_id,
                'periodo': r['periodo'],
                'frequencia': r['frequencia']
            })
    return attributes

names = requests.get("https://servicodados.ibge.gov.br/api/v2/censos/nomes/").content.decode('utf-8')
names_data = list(map(get_names, json.loads(names)[:10]))

locals = get_locations_ids()

mapped_names = []
for i in locals:
    res = get_names_frequency_by_location(names_data, i)
    if res:
        mapped_names+=get_attributes(i, res)
    if mod(locals.index(i), 100) == 0:
        print(locals.index(i))

df = pd.DataFrame(mapped_names)
df.to_csv('names.csv', index=False)
