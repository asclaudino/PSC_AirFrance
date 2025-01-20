from tasksCreator import generate_tasks_lists
from rosterCreator import generate_rosters_list
from allPairings import all_pairings


#all tasks that should been atributed (or not) 
pairings_tasks, ground_activity_tasks, standby_tasks = generate_tasks_lists()

ground_tasks_dict   = {task.ground_activity_number: task for task in ground_activity_tasks}
pairings_tasks_dict = {task.id : task for task in pairings_tasks}
standby_tasks_dict  = {task.standby_number : task for task in standby_tasks}

#all pilots with its respectives assignments with its respectives block period (except for the pairings)
rosters = generate_rosters_list()


#DONE # TODO GO THROUGH ALL ROSTERS AND MARK THE RESPECTIVE TASK IN pairings_tasks, etc... WITH FILLED = TRUE 

# print(rosters[0])
# print(standby_tasks[1])

for roster in rosters:
    
    if roster.ground_activities_tasks and len(roster.ground_activities_tasks) > 0:
        for ground_activity in roster.ground_activities_tasks:
            id = ground_activity.ground_activity_number
            if id in ground_tasks_dict:
                ground_task = ground_tasks_dict.get(id)
                ground_task.filled = True
        
    if roster.standby_tasks and len(roster.standby_tasks) > 0:
        for standby_activity in roster.standby_tasks:
            id = standby_activity.standby_number
            if id in standby_tasks_dict:
                standby_task = standby_tasks_dict.get(id)
                standby_task.filled = True
                
    if roster.pairings_tasks and len(roster.pairings_tasks) > 0:
        for pairing_activity in roster.pairings_tasks:
            id = pairing_activity.pairing_number
            if id in pairings_tasks_dict:
                pairing_task = pairings_tasks_dict.get(id)
                pairing_task.filled = True
                        
        


#all pairings dictionary that should be used to find the corresponding block period wheen needed 
# just use it like all_pairings['20240623MCR3T203D'].blockPeriod , where 20240623MCR3T203D is the @activitIid of the pairing
# of the @id after the # symbol, example "@id": "8290515#20240426ZTC5F0116"

all_pairings_dict = all_pairings()

print(len(rosters))
print(rosters[0])
print(all_pairings_dict['20240623MCR3T203D'].blockPeriod)



#DONE ######TODO CREATE THE SORTED ALL BLOCK PERIODS IN THE ROSTER CLASS.


#start of the real optmization algorithm

# for pairing in pairings_tasks:
#     if not pairing.filled:
#         for roster in rosters: 
#             for (pos,block_period) in enumerate(roster.block_periods):
#                 #if this pairing enters/fits between pos and pos+1:
#                     roster.block_periods.append(block_period)
#                     roster.block_periods.sort()
#                     roster.pairings_tasks.append(pairing) #check the format of pairing and the pairings_tasks in roster

#and so on for ground_activity_tasks and stand_by_tasks

            

