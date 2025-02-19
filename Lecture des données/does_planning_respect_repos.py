from datetime import datetime, timedelta
from typing import List
from number_of_already_assigned_conges import number_of_already_assigned_conges
from conges_after_prorata import number_of_conges_after_proata

def overlap_in_month(interval_start: datetime, interval_end: datetime, month: int) -> timedelta:
    """
    Returns the total overlap (as a timedelta) between the interval [interval_start, interval_end)
    and all occurrences of the given month in the interval's timespan.
    """
    total_overlap = timedelta(0)
    # Loop over each year the interval spans.
    for year in range(interval_start.year, interval_end.year + 1):
        try:
            month_start = datetime(year, month, 1)
        except ValueError:
            # Skip invalid month (should not happen if month is valid)
            continue
        
        # Determine the start of the next month.
        if month == 12:
            month_end = datetime(year + 1, 1, 1)
        else:
            month_end = datetime(year, month + 1, 1)
        
        # The overlapping portion for this year is:
        overlap_start = max(interval_start, month_start)
        overlap_end = min(interval_end, month_end)
        if overlap_end > overlap_start:
            total_overlap += (overlap_end - overlap_start)
    return total_overlap

def check_planning_conges(planning: List, prorata_days: int, month: int = 6) -> bool:
    """
    Given a planning (list of tasks with 'start' and 'end' datetimes), the number of already
    assigned congés days (prorata_days), and an optional month (default=6), this function verifies that:
    
      - There is at least one gap (the portion of the gap within the specified month) that is as long as the
        consecutive rest threshold, and
      - The sum (in whole days) of the portions of the remaining gaps within that month is at least as long as
        the non-consecutive rest threshold.
    
    The thresholds (in whole days) are determined by the function number_of_conges_after_proata.
    """
    # Get thresholds (expressed in whole days)
    consecutive_threshold, nonconsecutive_threshold = number_of_conges_after_proata(prorata_days)
    
    # Sort planning by start time (tasks with missing start are pushed to the end)
    planning.sort(key=lambda task: task['start'] if task.get('start') is not None else datetime.max)
    
    # Compute intervals (gaps) between consecutive tasks.
    intervals = []
    for i in range(len(planning) - 1):
        current_end = planning[i]['end']
        next_start = planning[i+1]['start']
        if current_end and next_start:
            intervals.append((current_end, next_start))
    
    consecutive_found = False
    nonconsec_sum = 0  # Sum in whole days from the remaining intervals (within the specified month)
    
    # Process each gap, computing its overlap with the given month.
    for start, end in intervals:
        gap_overlap = overlap_in_month(start, end, month)
        whole_days = gap_overlap.days
        # If we haven't yet found a gap that meets the consecutive threshold and this gap qualifies...
        if not consecutive_found and gap_overlap >= timedelta(days=consecutive_threshold):
            consecutive_found = True
        else:
            nonconsec_sum += whole_days

    return consecutive_found and (nonconsec_sum >= nonconsecutive_threshold)
