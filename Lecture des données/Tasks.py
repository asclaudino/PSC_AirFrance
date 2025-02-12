
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import re
from typing import Optional


def parse_block_period(block_period):
        if block_period:
            start_str, end_str = block_period.split(';')
            start = datetime.strptime(start_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            end = datetime.strptime(end_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            return start, end
        return None, None
    
# def parse_racDuration(racDuration):
#     origin = datetime(0,0,0)
#     if racDuration:
#         DurDate = datetime.strptime(racDuration,"P%YY%mM%dDT%HH%MM%S.%fS")
#         Duration = DurDate-origin
        
def parse_duration(duration: str):
    """
    Parses an ISO 8601 duration string of the form:
      "P{years}Y{months}M{days}DT{hours}H{minutes}M{seconds}S"
    e.g. "P0Y0M1DT20H35M0.000S" and returns either a timedelta (if years and months are zero)
    or a relativedelta (if years or months are nonzero).
    """
    pattern = (
        r'P(?P<years>\d+)Y(?P<months>\d+)M(?P<days>\d+)D'
        r'T(?P<hours>\d+)H(?P<minutes>\d+)M(?P<seconds>\d+(?:\.\d+)?)S'
    )
    if duration:
        match = re.match(pattern, duration)
    else: 
        match = False
        
    if not match:
        #raise ValueError("Invalid duration format: " + duration)
        #print("Invalid duration format: ", duration)
        return timedelta(0,0,0,0,0,0,0)
    
    years   = int(match.group('years'))
    months  = int(match.group('months'))
    days    = int(match.group('days'))
    hours   = int(match.group('hours'))
    minutes = int(match.group('minutes'))
    seconds = float(match.group('seconds'))
    
    # Use timedelta if years and months are zero, otherwise use relativedelta
    if years == 0 and months == 0:
        return timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    else:
        return relativedelta(years=years, months=months, days=days,
                             hours=hours, minutes=minutes, seconds=seconds)

def subtract_duration_from_datetime(start_datetime, duration: str):
    """
    Subtracts the duration specified by `duration` from the given datetime `start_datetime`
    and returns the resulting datetime.
    """
    #print(duration)
    duration = parse_duration(duration)
    if duration:
        return start_datetime - duration
    else: 
        return start_datetime
    
def add_duration_to_datetime(start_datetime, duration: str):
    """
    Adds the duration specified by `duration` to the given datetime `start_datetime`
    and returns the resulting datetime.
    """
    #print(duration)
    duration = parse_duration(duration)
    if duration:
        return start_datetime + duration
    else: 
        return start_datetime

class PairingTask:
    
    def __init__(self, pairing_number: str, id: str, type_place: str, filled: bool, block_period: str, aircraft_type: str, place_number=1, total_places=1, racDuration='', rpcDuration=''):
        
        self.pairing_number = pairing_number
        self.id = id
        self.type_place = type_place
        self.filled = filled
        self.block_period = block_period  
        self.place_number = place_number
        self.total_places = total_places
        self.was_assigned_by_algo = False
        self.aircraft_type = aircraft_type
        self.start, self.end = parse_block_period(block_period)
        self.rac_exact_date = subtract_duration_from_datetime(self.start, racDuration)
        self.rpc_exact_date = add_duration_to_datetime(self.end, rpcDuration)

        
    
    def __str__(self):
        return (
            f"PairingTask(\n"
            f"  Pairing Number: {self.pairing_number}\n"
            f"  ID: {self.id}\n"
            f"  Type Place: {self.type_place}\n"
            f"  Aircraft Type: {self.aircraft_type}\n"
            f"  Filled: {self.filled}\n"
            f"  Block Period: {self.block_period}\n"
            f"  Start: {self.start}\n"
            f"  End: {self.end}\n"
            f")"
        )
        


class StandByTask:
    
    def __init__(self, standby_number: str, id: str, type_place: str, filled: bool, block_period: str,aircraft_type: str,place_number=1, total_places=1):
        
        self.standby_number = standby_number
        self.id = id
        self.type_place = type_place
        self.filled = filled
        self.block_period = block_period   
        self.place_number = place_number
        self.total_places = total_places
        self.was_assigned_by_algo = False 
        self.aircraft_type = aircraft_type
        self.start, self.end = parse_block_period(block_period) 
        
    def __str__(self):
        return (
            f"StandByTask(\n"
            f"  Standby Number: {self.standby_number}\n"
            f"  ID: {self.id}\n"
            f"  Type Place: {self.type_place}\n"
            f"  Aircraft Type: {self.aircraft_type}\n"
            f"  Filled: {self.filled}\n"
            f"  Block Period: {self.block_period}\n"
            f"  Start: {self.start}\n"
            f"  End: {self.end}\n"
            f")"
        )

        
class GroundActivityTask:
    
    def __init__(self, ground_activity_number: str, id: str, type_place: str, filled: bool, block_period: str,place_number=1, total_places=1):
        
        self.ground_activity_number = ground_activity_number
        self.id = id
        self.type_place = type_place
        self.filled = filled
        self.block_period = block_period  
        self.place_number = place_number
        self.total_places = total_places
        self.was_assigned_by_algo = False
        self.start, self.end = parse_block_period(block_period)   
    
    def __str__(self):
        return (
            f"GroundActivityTask(\n"
            f"  GroundActivity Number: {self.ground_activity_number}\n"
            f"  ID: {self.id}\n"
            f"  Type Place: {self.type_place}\n"
            f"  Filled: {self.filled}\n"
            f"  Block Period: {self.block_period}\n"
            f"  Start: {self.start}\n"
            f"  End: {self.end}\n"
            f")"
        )
   
class IndividualAssignmentTask:
    
    def __init__(self, id: str,block_period: str, was_assigned_by_algo: Optional[bool] = False):
        
        self.id = id
        self.block_period = block_period  
        self.start, self.end = parse_block_period(block_period)   
        self.was_assigned_by_algo = was_assigned_by_algo 
    
    def __str__(self):
        return (
            f"IndividualAssignmentTask(\n"
            f"  ID: {self.id}\n"
            f"  Block Period: {self.block_period}\n"
            f"  Start: {self.start}\n"
            f"  End: {self.end}\n"
            f")"
        )