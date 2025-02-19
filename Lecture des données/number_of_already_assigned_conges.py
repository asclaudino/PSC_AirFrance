from ast import List
from datetime import datetime, timedelta
from Tasks import IndividualAssignmentTask

def number_of_already_assigned_conges(tasks: List, month: int = 6) -> int:
    tasks.sort(key=lambda task: task.start if task.start is not None else datetime.max)
    total_conges_time = timedelta(0)

    for task in tasks:
        if task.start and task.end and task.end < datetime.max and task.start < datetime.max:
            if task.fast_activit_code in ['MCA', 'MCE', 'MDV', 'MAS']:
                
                # For each year that the task spans, calculate the overlap with the specified month.
                for year in range(task.start.year, task.end.year + 1):
                    
                    # try:
                    #     # Define the start and end of the month for this year.
                    #     
                    # except ValueError:
                    #     # Skip invalid dates (if month is out of range, though it shouldn't be)
                    #     continue
                    
                    month_start = datetime(year, month, 1)
                    # Calculate the start of the next month.
                    if month == 12:
                        month_end = datetime(year + 1, 1, 1)
                    else:
                        month_end = datetime(year, month + 1, 1)

                    # Determine the overlapping period between the task and the month.
                    overlap_start = max(task.start, month_start)
                    overlap_end = min(task.end, month_end)
                    if overlap_end > overlap_start:
                        total_conges_time += (overlap_end - overlap_start)

    return total_conges_time.days
