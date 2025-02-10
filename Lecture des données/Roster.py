import ast
import json
from datetime import datetime
from GroundActivity import GroundActivity
from Pairing import Pairing
from Standby import Standby
from IndividualAssignment import IndividualAssignment
from Pilot import Pilot
from readerClass import readerClass
from Tasks import StandByTask, PairingTask
from Tasks import GroundActivityTask
from Tasks import IndividualAssignmentTask



class Roster:
    
    def __init__(self, crew_type: str, 
                 assignments: str, 
                 ground_activities_tasks: str,
                 standby_tasks: str,
                 individual_tasks: str,
                 pairings_tasks:  str,
                 fcSpouseNumber: str, 
                 fcNumber: str, 
                 all_pairings: dict,
                 all_standby: dict):
        self.crew_type = crew_type
        self.assignments = assignments
        self.fcSpouseNumber = fcSpouseNumber
        self.fcNumber = fcNumber
        self.ground_activities_tasks = []
        self.standby_tasks = []
        self.individual_tasks = []
        self.pairings_tasks = []
        self.all_pairings = all_pairings
        self.all_standby = all_standby
        self.block_periods = []
        self.tasksInitializer(ground_activities_tasks, standby_tasks, individual_tasks, pairings_tasks)
        self.blockPeriodsInitializer()
        
    def __str__(self):
        return (
            f"RosterObject(\n"
            f"  Crew Type: {self.crew_type}\n"
            f"  fcNumber: {self.fcNumber}\n"
            F"  fcSpouseNumber: {self.fcSpouseNumber}\n"
            f"  Ground Activity Tasks: {self.ground_activities_tasks}\n"
            f"  Pairings Tasks: {self.pairings_tasks}\n"
            f"  Standby Tasks: {self.standby_tasks}\n"
            f"  Individual Assignement Tasks: {self.individual_tasks}\n"
            f"  Block Periods: {self.block_periods}\n"
            f")"
        )
    
    
    def blockPeriodsInitializer(self):
        
        if len(self.ground_activities_tasks) > 0:
            for task in self.ground_activities_tasks: 
                self.block_periods.append({
                    'start': task.start,
                    'end': task.end
                })
        if len(self.pairings_tasks) > 0:
            for task in self.pairings_tasks:
                self.block_periods.append({
                    'start': task.start,
                    'end': task.end
                })
        if len(self.individual_tasks) > 0:
            for task in self.individual_tasks:
                self.block_periods.append({
                    'start': task.start,
                    'end': task.end
                })
        if len(self.standby_tasks) > 0:
            for task in self.standby_tasks:
                #print(task.standby_number)
                standby = self.all_standby.get(task.standby_number)
                start, end = standby.start, standby.end
                self.block_periods.append({
                    'start': start,
                    'end': end
                })

        self.block_periods.sort(key=lambda block_period: block_period['start'] if block_period['start'] is not None else datetime.max)

                
    
    def tasksInitializer(self, ground_activities_tasks, standby_tasks, individual_tasks, pairings_tasks):
        

        if individual_tasks:
             if isinstance(individual_tasks, list):
                for task in individual_tasks:
                    individual_assignment_id = task.get("@id")
                    block_period = task.get("Elements").get('@blockPeriod')
                    new_ia = IndividualAssignmentTask(individual_assignment_id,block_period)
                    self.individual_tasks.append(new_ia)
             else:
              
                individual_assignment_id = ground_activities_tasks.get('@id')
                block_period = ground_activities_tasks.get("Elements").get('@blockPeriod')
                new_ia = IndividualAssignmentTask(individual_assignment_id,block_period)
                self.individual_tasks.append(new_ia)
        
        if ground_activities_tasks:
            if isinstance(ground_activities_tasks, list):
                for task in ground_activities_tasks:
                    ground_activity_number = task.get("@activityId")
                    id = task.get('@id')
                    block_period = task.get("Elements").get('@blockPeriod')
                    new_ga = GroundActivityTask(ground_activity_number,id,'',True,block_period)
                    self.ground_activities_tasks.append(new_ga)
            else:
        
                    
                ground_activity_number = ground_activities_tasks.get("@activityId")
                id = ground_activities_tasks.get('@id')
                block_period = ground_activities_tasks.get("Elements").get('@blockPeriod')
                new_ga = GroundActivityTask(ground_activity_number,id,'',True,block_period)
                self.ground_activities_tasks.append(new_ga)
                
                
        if pairings_tasks:
            if isinstance(pairings_tasks, list):
                for task in pairings_tasks:
                    pairing_number = task.get("@activityId")
                    id = task.get('@id')
                    if self.all_pairings[pairing_number]:
                        block_period = self.all_pairings[pairing_number].blockPeriod
                    else:
                        block_period = "2024-01-01T06:30:00.000Z;2024-01-02T04:36:00.000Z"
                    new_pa = PairingTask(pairing_number,id,'',True,block_period, '')
                    self.pairings_tasks.append(new_pa)
            else:
  
                    
                ground_activity_number = ground_activities_tasks.get("@activityId")
                id = ground_activities_tasks.get('@id')
                new_pa = GroundActivityTask(ground_activity_number,id,'',True,'')
                self.pairings_tasks.append(new_pa)
                
        if standby_tasks:
            if isinstance(standby_tasks, list):
                for task in standby_tasks:
                    standby_number = task.get("@activityId")
                    id = task.get('@id')
                    #block_period = task.get("Elements").get('@blockPeriod')
                    new_stb = StandByTask(standby_number,id,'',True,'', '')
                    self.standby_tasks.append(new_stb)
            else:
                    
                standby_activity_number = standby_tasks.get("@activityId")
                id = standby_tasks.get('@id')
                #block_period = standby_tasks.get("Elements").get('@blockPeriod')
                new_stb = StandByTask(standby_activity_number,id,'',True,'','')
                self.standby_tasks.append(new_stb)
                

            