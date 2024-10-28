#from bs4 import BeautifulSoup
#import xmltodict
import json
from GroundActivity import GroundActivity
from Pairing import Pairing
from Standby import Standby
from IndividualAssignment import IndividualAssignment
from Pilot import Pilot

with open('Ressources/insolo.json', 'r') as file:
    data = json.load(file)


## Création des classes d'activités
#Creating ground activities
ground_activity = data.get('EasyData').get('Activities').get('GroundActivity')

dict_ground = {}
for x in ground_activity:
    id = x.get('@id')
    block = x.get('@blockPeriod')
    dict_ground[id] = GroundActivity(id,block)


#Creating pairings
pairing = data.get('EasyData').get('Activities').get('Pairing')
dict_pairing = {}

for x in pairing:
    id = x.get('@id')
    block = x.get('PairingValues').get('COPairingElements').get('@blockPeriod')
    dict_pairing[id] = Pairing(id,block)

#Creating Standby (in the present case it seems there is only one Standby assignement ; hence the absence of a loop)
standby_data = data.get('EasyData').get('Activities').get('Standby')
dict_standby = {}

id = standby_data.get('@id') 
block = standby_data.get('StandbyElements').get('@blockPeriod')
dict_standby[id] = Standby(id, block)

#------------------

##Creating a pilot : pilot1 
pilot1 = Pilot(data.get('EasyData').get('Roster').get('CockpitCrew').get('@fcNumber'),{})

assignments = data.get('EasyData').get('Roster').get('Assignments')

#Adding all the assignments to a dictionnary
for x in assignments.get('GroundActivityAssignment'):
    assignmentcourant = x.get('@activityId')
    if assignmentcourant in dict_ground: pilot1.assignments[assignmentcourant] = dict_ground[assignmentcourant]
    else : print('Base de données de GroundActivity incomplète')


for x in assignments.get('PairingAssignment'):
    assignmentcourant = x.get('@activityId')
    if assignmentcourant in dict_pairing : pilot1.assignments[assignmentcourant] = dict_pairing[assignmentcourant]
    else : print('Base de données des Pairings incomplète')

#Only one Standby, hence no loop
assignmentcourant= assignments.get('StandbyAssignment').get('@activityId')
if assignmentcourant in dict_standby : pilot1.assignments[assignmentcourant] = dict_standby[assignmentcourant]
else : print('Base de données des Standby incomplète') 
        

for x in assignments.get('IndividualAssignment'):
    id = x.get('@id')
    block = x.get('Elements').get('@blockPeriod')
    pilot1.assignments[f"{id}"] = IndividualAssignment(id,block)

#pilot1 est désormais initialisé, avec son id et un dictionnaire qui contient toutes ses activités

#------------

blocks = [] #initializing a list that contains all the block periods
   
for x in pilot1.assignments:
    if pilot1.assignments[x].blockPeriod == None :
        print("L'activité :"+pilot1.assignments[x].id+" n'a pas de blockperiod")
        continue
    start, end = pilot1.assignments[x].parse_block_period(pilot1.assignments[x].blockPeriod)
    blocks.append(start)
    blocks.append(end)

blocks.sort()
#blocks contient maintenant la liste des blocks occupés par les assignments du pilote, dans l'ordre



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
