#from bs4 import BeautifulSoup
#import xmltodict
import json
from GroundActivity import GroundActivity
from Pairing import Pairing

with open('Ressources/insolo.json', 'r') as file:
    data = json.load(file)


#Creating ground activities
ground_activity = data.get('EasyData').get('Activities').get('GroundActivity')

dict_ground = {}
for x in ground_activity:
    id = x.get('@id')
    block = x.get('@blockPeriod')
    dict_ground[f"{id}"] = GroundActivity(id,block)


#Creating pairings
pairing = data.get('EasyData').get('Activities').get('Pairing')
dict_pairing = {}

for x in pairing:
    id = x.get('@id')
    block = x.get('PairingValues').get('COPairingElements').get('@blockPeriod')
    dict_pairing[f"{id}"] = Pairing(id,block)

#Creating Standby
standby_data = data.get('EasyData').get('Activities').get('Standby')
dict_standby = {}

for x in standby_data:
    id = x.get('@id')  
    block = x.get('StandbyElements').get('@blockPeriod')
    dict_standby[f"{id}"] = Standby(id, block)





#my_new_easydata = EasyData(var)



# Reading the data inside the xml
# file to a variable under the name 
# data
# with open('insolo.xml', 'r') as f:
#     data = f.read()

#print(data)

# Passing the stored data inside
# the beautifulsoup parser, storing
# the returned object 
# Bs_data = BeautifulSoup(data, "xml")

# print(Bs_data)
# legs = Bs_data.find('EasyData').text    
# print(legs)
# Parse XML into a dictionary
# xml_dict = xmltodict.parse(Bs_data)
    
# # Convert the dictionary to JSON
# json_data = json.dumps(xml_dict, indent=4)

# print(json_data)

# # Finding all instances of tag 
# # `unique`
# b_unique = Bs_data.find_all('unique')

# print(b_unique)

# # Using find() to extract attributes 
# # of the first instance of the tag
# b_name = Bs_data.find('child', {'name':'Frank'})

# print(b_name)

# # Extracting the data stored in a
# # specific attribute of the 
# # `child` tag
# value = b_name.get('test')

# print(value)
