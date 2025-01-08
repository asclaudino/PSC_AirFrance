from tasksCreator import generate_tasks_lists
from rosterCreator import generate_rosters_list
from allPairings import all_pairings


#all tasks that should been atributed (or not) 
pairings_tasks, ground_activity_tasks, standby_tasks = generate_tasks_lists()

#all pilots with its respectives assignments with its respectives block period (except for the pairings)
rosters = generate_rosters_list()

#all pairings dictionary that should be used to find the corresponding block period wheen needed 
# just use it like all_pairings['20240623MCR3T203D'].blockPeriod , where 20240623MCR3T203D is the @activitIid of the pairing
# of the @id after the # symbol, example "@id": "8290515#20240426ZTC5F0116"

all_pairings = all_pairings()

#print(all_pairings.keys())
print(len(rosters))
print(all_pairings['20240623MCR3T203D'].blockPeriod)
