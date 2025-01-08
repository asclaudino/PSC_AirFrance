import json
import ast
#import pandas as pd
import tkinter as tk
from tkinter import ttk
from datetime import timedelta


from GroundActivity import GroundActivity
from Pairing import Pairing
from Standby import Standby
from IndividualAssignment import IndividualAssignment
from Pilot import Pilot
from readerClass import readerClass
from Tasks import StandByTask, PairingTask
from Tasks import GroundActivityTask
from Roster import Roster

def generate_rosters_list():
    
    with open('Ressources/Export20PN.xml.json', 'r') as file:
         data = json.load(file)


    rosters_data = data.get('EasyData').get('Roster')
    rosters_list = []

    for roster in rosters_data: 
        crew_type = roster.get("CockpitCrew").get("COTypeRateQualification").get("@specialityCode")
        assignments = roster.get("Assignments")
        ground_activity_assignment = roster.get("Assignments").get("GroundActivityAssignment", None)
        standby_assignment = roster.get("Assignments").get("StandbyAssignment", None)
        individual_assignment = roster.get("Assignments").get("IndividualAssignment", None)
        pairings_assignment = roster.get("Assignments").get("PairingAssignment", None)
        fcNumber = roster.get("CockpitCrew").get("@fcNumber")
        fcSpouseNumber = roster.get("CockpitCrew").get("@fcSpouseNumber")
        new_roster = Roster(crew_type, assignments,ground_activity_assignment, standby_assignment,individual_assignment, pairings_assignment, fcSpouseNumber,fcNumber)
        rosters_list.append(new_roster)

    #print(rosters_list[0])
    #print(len(rosters_list))
    #print(rosters_list[0].individual_tasks[0])
    
    return rosters_list