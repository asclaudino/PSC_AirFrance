from tasksCreator import generate_tasks_lists
from rosterCreator import generate_rosters_list
from allPairings import all_pairings


#all tasks that should been atributed (or not) 
pairings_tasks, ground_activity_tasks, standby_tasks = generate_tasks_lists()
print(len(ground_activity_tasks), ground_activity_tasks[0], ground_activity_tasks[1])
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

# print(len(rosters))
# print(rosters[0])
# print(all_pairings_dict['20240623MCR3T203D'].blockPeriod)



#DONE ######TODO CREATE THE SORTED ALL BLOCK PERIODS IN THE ROSTER CLASS.

def test_if_task_fits(first_task, second_task, new_task) -> bool:
    #print(first_task, second_task, new_task)
    return first_task['end'] < new_task['start'] and new_task['end'] < second_task['start']
    
#start of the real optmization algorithm



for pairing in pairings_tasks:
    #print('entrei na pairing ', pairing.pairing_number, 'type: ', pairing.type_place, ' place number: ', pairing.place_number, ' out of: ', pairing.total_places)
    flag = False
    if not pairing.filled:
        for roster in rosters: 
            for (pos,block_period) in enumerate(roster.block_periods):
                new_task = {
                    'start': pairing.start,
                    'end': pairing.end
                }
                if  pos < len(roster.block_periods)-1 \
                    and test_if_task_fits(block_period,roster.block_periods[pos+1], new_task) \
                    and roster.crew_type == pairing.type_place:
                    #print(pos)
                    #print('added pairing ', pairing.pairing_number, 'type: ', pairing.type_place, ' place number: ', pairing.place_number, ' out of: ', pairing.total_places)
                    roster.block_periods.append(block_period)
                    roster.block_periods.sort(key=lambda block_period: block_period['start'])
                    roster.pairings_tasks.append(pairing) #check the format of pairing and the pairings_tasks in roster
                    pairing.filled = True
                    pairing.was_assigned_by_algo = True
                    flag = True
                    break
            if flag: 
                break

pairings_assigned_by_algo = 0

for pairing in pairings_tasks:
    if pairing.was_assigned_by_algo: pairings_assigned_by_algo+=1
print(len(pairings_tasks), ' = ', pairings_assigned_by_algo, ' + ', len(pairings_tasks) - pairings_assigned_by_algo)



for ga_task in ground_activity_tasks:
    #print('entrei na ground_activity_task ', ga_task.ground_activity_number, 'type: ', ga_task.type_place, ' place number: ', ga_task.place_number, ' out of: ', ga_task.total_places)
    flag = False
    if not ga_task.filled:
        for roster in rosters: 
            for (pos,block_period) in enumerate(roster.block_periods):
                print(ga_task)
                new_task = {
                    'start': ga_task.start,
                    'end': ga_task.end
                }
                if  pos < len(roster.block_periods)-1 \
                    and test_if_task_fits(block_period,roster.block_periods[pos+1], new_task) \
                    and roster.crew_type == ga_task.type_place:
                    #print(pos)
                    #print('added pairing ', pairing.pairing_number, 'type: ', pairing.type_place, ' place number: ', pairing.place_number, ' out of: ', pairing.total_places)
                    roster.block_periods.append(block_period)
                    roster.block_periods.sort(key=lambda block_period: block_period['start'])
                    roster.ground_activities_tasks.append(ga_task) #check the format of pairing and the pairings_tasks in roster
                    ga_task.filled = True
                    ga_task.was_assigned_by_algo = True
                    flag = True
                    break
            if flag: 
                break
            
ga_assigned_by_algo = 0
for ga_task in ground_activity_tasks:
    if ga_task.was_assigned_by_algo: ga_assigned_by_algo+=1
print(len(ground_activity_tasks), ' = ', ga_assigned_by_algo, ' + ', len(pairings_tasks) - ga_assigned_by_algo)
#and so on for ground_activity_tasks and stand_by_tasks

            

