import requests
import json
import pandas as pd

locals = requests.get("https://servicodados.ibge.gov.br/api/v1/localidades/distritos").content.decode('utf-8')
locals_data = json.loads(locals)

def get_attributes(dict):
    return {
        'id': dict['municipio']['id'], 
        'nome': dict['municipio']['nome'],
        'uf_id': dict['municipio']['regiao-imediata']['regiao-intermediaria']['UF']['id'],
        'uf_sigla': dict['municipio']['regiao-imediata']['regiao-intermediaria']['UF']['sigla'],
        'uf_nome': dict['municipio']['regiao-imediata']['regiao-intermediaria']['UF']['nome'],
        'regiao_id': dict['municipio']['regiao-imediata']['regiao-intermediaria']['UF']['regiao']['id'],
        'regiao_nome': dict['municipio']['regiao-imediata']['regiao-intermediaria']['UF']['regiao']['nome']
        }
  
mapped_locations = []
saved_ids = []
for l in locals_data:
    if l['municipio']['id'] not in saved_ids:
        mapped_locations.append(get_attributes(l))
        saved_ids.append(l['municipio']['id'])

df = pd.DataFrame(mapped_locations)
df.to_csv('locations.csv', index=False)
