#from bs4 import BeautifulSoup
#import xmltodict
import json
import pandas as pd
import tkinter as tk
from tkinter import ttk
from datetime import timedelta


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

#### Affichage des blockperiods



# Création d'une liste de tuples de périodes (début, fin) à partir de la liste "blocks"
def create_periods(blocks):
    return [(blocks[i], blocks[i+1]) for i in range(0, len(blocks), 2)]

# Conversion des périodes en DataFrame pour faciliter l'affichage
periods = create_periods(blocks)
df_blocks = pd.DataFrame(periods, columns=['Début', 'Fin'])

# Création de la fenêtre principale
root = tk.Tk()
root.title("Périodes de Temps")
root.geometry("400x200")

# Création d'un Treeview pour afficher le DataFrame sous forme de tableau
tree = ttk.Treeview(root, columns=list(df_blocks.columns), show="headings", height=10)
for col in df_blocks.columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=150)

# Ajout des données au Treeview
for index, row in df_blocks.iterrows():
    tree.insert("", "end", values=list(row))

# Placement du tableau dans la fenêtre
tree.pack(expand=True, fill="both")

# Démarrage de l'interface graphique
root.mainloop()
# Initialisation de l'interface graphique
root = tk.Tk()
root.title("Calendrier des Périodes d'Indisponibilité")
canvas = tk.Canvas(root, width=1000, height=400, bg="white")
canvas.pack()

# Définir les limites de temps pour l'affichage
start_time = min(period[0] for period in periods)  # Heure de début la plus tôt
end_time = max(period[1] for period in periods) + timedelta(days=1)  # Heure de fin la plus tard +1 jour pour couverture



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
