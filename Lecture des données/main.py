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
from readerClass import readerClass

with open('Ressources/insolo.json', 'r') as file:
    data = json.load(file)


reader = readerClass()



ground_activity = data.get('EasyData').get('Activities').get('GroundActivity')
dict_ground = reader.GroundActivityReader(ground_activity)
print(dict_ground)




#Creating pairings


pairing = data.get('EasyData').get('Activities').get('Pairing')
dict_pairing = reader.PairingsReader(pairing)



#Creating Standby (in the present case it seems there is only one Standby assignement ; hence the absence of a loop)


standby_data = data.get('EasyData').get('Activities').get('Standby')

dict_standby = reader.StandByReader(standby_data)


##Creating a pilot : pilot1 
roster = data.get('EasyData').get('Roster')
pilot1 = reader.PilotReader(roster)
# pilot1 = Pilot(data.get('EasyData').get('Roster').get('CockpitCrew').get('@fcNumber'),{})


assignments = data.get('EasyData').get('Roster').get('Assignments')


# #pilot1 est désormais initialisé, avec son id et un dictionnaire qui contient toutes ses activités

#---------------
# Affichage

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

def create_periods(assignments):
    periods = []
    for key, activity in assignments.items():
        if activity.blockPeriod:
            start, end = activity.parse_block_period(activity.blockPeriod)
            periods.append((activity.id, activity.__class__.__name__, start, end))
    return periods

# Conversion des périodes en DataFrame pour faciliter l'affichage
periods = create_periods(pilot1.assignments)
df_blocks = pd.DataFrame(periods, columns=['ID', 'Activity','Début', 'Fin'])

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



