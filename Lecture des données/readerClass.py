from datetime import datetime
from GroundActivity import GroundActivity
from Pairing import Pairing
from Standby import Standby
from IndividualAssignment import IndividualAssignment
from Pilot import Pilot

class readerClass:
    
    def __init__(self):
        self.ground_activity_dict = None
        self.pairings_dict = None
        self.standby_dict = None
    
    
    def GroundActivityReader(self,ground_activity):
        
        if not ground_activity:
            print("Ground Activity hasn't been initialised")
            return None

        dict_ground = {}
        for x in ground_activity:
            id = x.get('@id')
            block = x.get('@blockPeriod')
            dict_ground[id] = GroundActivity(id,block)
            
        self.ground_activity_dict = dict_ground    
        
        return dict_ground

    def PairingsReader(self,pairings):
        if not pairings:
            print("Pairings hasn't been initialised")
            return None
        dict_pairing = {}
        for pairing in pairings:
            id = pairing.get('@id')
            block = pairing.get('PairingValues').get('COPairingElements').get('@blockPeriod')
            dict_pairing[id] = Pairing(id,block)
            
        self.pairings_dict = dict_pairing
        
        return dict_pairing


    def StandByReader(self,stand_by):
        if not stand_by:
            print("Standby hasn't been initialised")
            return None
    # Creating Standby (in the present case it seems there is only one 
    # Standby assignement ; hence the absence of a loop)
        dict_standby = {}
        id = stand_by.get('@id') 
        block = stand_by.get('StandbyElements').get('@blockPeriod')
        dict_standby[id] = Standby(id, block)
        self.standby_dict = dict_standby
        return dict_standby

    def PilotReader(self,pilot):
        # We expect here pilot to be an instance of <Roster> 

        if not pilot:
            print("Pilot hasn't been initialised")
            return None

        ##Creating a pilot : pilot1 
        pilot1 = Pilot(pilot.get('CockpitCrew').get('@fcNumber'),{})

        assignments = pilot.get('Assignments')

        dict_ground = self.ground_activity_dict
        dict_pairing = self.pairings_dict
        dict_standby = self.standby_dict
        
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
        return pilot1
        #------------
