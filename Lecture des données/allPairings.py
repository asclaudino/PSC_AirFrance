


import json
from readerClass import readerClass


def all_pairings():
    with open('../Ressources/Export20PN.json', 'r') as file:
        data = json.load(file)

    reader = readerClass()

    pairing = data.get('EasyData').get('Activities').get('Pairing')
    dict_pairing = reader.PairingsReader(pairing)
    
    return dict_pairing