import csv
from datetime import datetime, timedelta
from tasksCreator import generate_tasks_lists
from rosterCreator import generate_rosters_list
from allPairings import all_pairings
from does_planning_respect_repos import check_planning_conges


#all tasks that should been atributed (or not) 
pairings_tasks, ground_activity_tasks, standby_tasks = generate_tasks_lists()

#print(len(ground_activity_tasks), ground_activity_tasks[0], ground_activity_tasks[1])

ground_tasks_dict   = {task.ground_activity_number: task for task in ground_activity_tasks}
pairings_tasks_dict = {task.id : task for task in pairings_tasks}
standby_tasks_dict  = {task.standby_number : task for task in standby_tasks}

#all pilots with its respectives assignments with its respectives block period (except for the pairings)
rosters = generate_rosters_list()

#print(rosters[1].number_already_assigned_conges)



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



def test_if_task_fits(first_task, second_task, new_task) -> bool:
    
    if not new_task['start'] or not new_task['end']: return False
    return first_task['end'] < new_task['start'] \
           and new_task['end'] < second_task['start'] \
           and second_task['start'] >= new_task['rpcexactdate'] \
           and new_task['racexactdate'] >= first_task['end'] \
           and new_task['start'].month == 6 and new_task['end'].month == 6 \
           and new_task['start'].year == 2024 and new_task['end'].year == 2024

    
#start of the real optmization algorithm


count_rotations = 0
for pairing in pairings_tasks:
    flag = False
    if not pairing.filled and pairing.aircraft_type == '777':
        if pairing.start.month == 6  \
           and pairing.start.year == 2024 and pairing.end.year == 2024:
            count_rotations += 1

        for roster in rosters: 
            for (pos,block_period) in enumerate(roster.block_periods):
                new_task = {
                    'start': pairing.start,
                    'end': pairing.end,
                    'racexactdate': pairing.rac_exact_date,
                    'rpcexactdate': pairing.rpc_exact_date
                }
                
               
                if pos < len(roster.block_periods) - 1 \
                    and test_if_task_fits(block_period, roster.block_periods[pos + 1], new_task) \
                    and roster.crew_type == pairing.type_place:
                      
                        temp_block_periods = roster.block_periods.copy()
                        temp_block_periods.append(new_task)
                        
                        # New checking to verify the constraints of rest
                        if check_planning_conges(temp_block_periods, roster.number_already_assigned_conges):
                            roster.block_periods.append(new_task)
                            roster.block_periods.sort(key=lambda block_period: block_period['start'])
                            roster.pairings_tasks.append(pairing)  
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


 
# for ga_task in ground_activity_tasks:
#     #print('entrei na ground_activity_task ', ga_task.ground_activity_number, 'type: ', ga_task.type_place, ' place number: ', ga_task.place_number, ' out of: ', ga_task.total_places)
#     flag = False
#     if not ga_task.filled:
#         for roster in rosters: 
#             for (pos,block_period) in enumerate(roster.block_periods):
#                 #print(ga_task)
#                 new_task = {
#                     'start': ga_task.start,
#                     'end': ga_task.end
#                 }
#                 if  new_task['start'] and new_task['end'] \
#                     and pos < len(roster.block_periods)-1 \
#                     and test_if_task_fits(block_period,roster.block_periods[pos+1], new_task) \
#                     and roster.crew_type == ga_task.type_place:
#                     #print(pos)
#                     #print('added pairing ', pairing.pairing_number, 'type: ', pairing.type_place, ' place number: ', pairing.place_number, ' out of: ', pairing.total_places)
#                     roster.block_periods.append(block_period)
#                     roster.block_periods.sort(key=lambda block_period: block_period['start'])
#                     roster.ground_activities_tasks.append(ga_task) #check the format of pairing and the pairings_tasks in roster
#                     ga_task.filled = True
#                     ga_task.was_assigned_by_algo = True
#                     flag = True
#                     break
#             if flag: 
#                 break
            
# ga_assigned_by_algo = 0
# for ga_task in ground_activity_tasks:
#     if ga_task.was_assigned_by_algo: ga_assigned_by_algo+=1
# print(len(ground_activity_tasks), ' = ', ga_assigned_by_algo, ' + ', len(ground_activity_tasks) - ga_assigned_by_algo)


# count_standby = 0
# for standby_task in standby_tasks:
#     flag = False
#     if not standby_task.filled and standby_task.aircraft_type == '777':
#         if standby_task.start.month == 6  \
#            and standby_task.start.year == 2024 and standby_task.end.year == 2024:
#             count_standby += 1
#         for roster in rosters: 
#             for (pos,block_period) in enumerate(roster.block_periods):
#                 new_task = {
#                     'start': standby_task.start,
#                     'end': standby_task.end
                    
#                 }
#                 if  new_task['start'] and new_task['end'] \
#                     and pos < len(roster.block_periods)-1 \
#                     and test_if_task_fits(block_period,roster.block_periods[pos+1], new_task) \
#                     and roster.crew_type == standby_task.type_place:
#                     #print(pos)
#                     #print('added pairing ', pairing.pairing_number, 'type: ', pairing.type_place, ' place number: ', pairing.place_number, ' out of: ', pairing.total_places)
#                     roster.block_periods.append(new_task)
#                     roster.block_periods.sort(key=lambda block_period: block_period['start'])
#                     roster.standby_tasks.append(standby_task) #check the format of pairing and the pairings_tasks in roster
#                     standby_task.filled = True
#                     standby_task.was_assigned_by_algo = True
#                     flag = True
#                     break
#             if flag: 
#                 break
            
# standby_assigned_by_algo = 0
# for standby_task in standby_tasks:
#     if standby_task.was_assigned_by_algo: standby_assigned_by_algo+=1
# print(len(standby_tasks), ' = ', standby_assigned_by_algo, ' + ', len(standby_tasks) - standby_assigned_by_algo)

# print(count_rotations, count_standby)
# print('The glouton algo managed to place ' + f'{100*pairings_assigned_by_algo/count_rotations}% of the pairings!')
# print('The glouton algo managed to place ' + f'{100*standby_assigned_by_algo/count_standby}% of the standbys!')

for roster in rosters:
    roster.pairings_tasks = sorted(roster.pairings_tasks, key = lambda task: task.start)
    roster.standby_tasks = sorted(roster.standby_tasks, key = lambda task: task.start or datetime.max)
    roster.individual_tasks = sorted(roster.individual_tasks, key = lambda task: task.start or datetime.max)



       
            
                
# Initialize an empty list to collect all tasks from all rosters
all_planning = []

for roster in rosters:
    # Process pairing tasks
    for pairing in roster.pairings_tasks:
        task_pairing = {
            'roster_id': roster.fcNumber,
            'type': 'pairing_assignment',
            'id': pairing.id,
            'start': pairing.start,
            'end': pairing.end,
            'was_assigned_via_algo': pairing.was_assigned_by_algo,
            'rac_exact_date': pairing.rac_exact_date,
            'rpc_exact_date': pairing.rpc_exact_date
        }
        all_planning.append(task_pairing)
        
    # Process standby tasks
    for standby in roster.standby_tasks:
        task_standby = {
            'roster_id': roster.fcNumber,
            'type': 'standby_assignment',
            'id': standby.id,
            'start': standby.start,
            'end': standby.end,
            'was_assigned_via_algo': standby.was_assigned_by_algo
        }
        all_planning.append(task_standby)
        
    # Process individual tasks
    for individual in roster.individual_tasks:
        task_individual = {
            'roster_id': roster.fcNumber,
            'type': 'individual_assignment',
            'id': individual.id,
            'start': individual.start,
            'end': individual.end,
            'was_assigned_via_algo': individual.was_assigned_by_algo
        }
        all_planning.append(task_individual)

# Sort all tasks by the 'start' time, treating None as the maximum datetime
all_planning = sorted(all_planning, key=lambda task: task['roster_id'])

# Write the aggregated tasks to a single CSV file
filename = "all_rosters.csv"
fieldnames = ['roster_id', 'type', 'id', 'start', 'end', 'was_assigned_via_algo', 'rac_exact_date', 'rpc_exact_date']

with open(filename, mode="w", newline="") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()  # Write header row
    writer.writerows(all_planning)  # Write all task rows

print(f"CSV file '{filename}' has been created successfully.")
print(rosters[0].cost(6))
    




        