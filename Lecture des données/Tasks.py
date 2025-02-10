
from datetime import datetime


def parse_block_period(block_period):
        if block_period:
            start_str, end_str = block_period.split(';')
            start = datetime.strptime(start_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            end = datetime.strptime(end_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            return start, end
        return None, None
def parse_racDuration(racDuration):
    origin = datetime(0,0,0)
    if racDuration:
        DurDate = datetime.strptime(racDuration,"P%YY%mM%dDT%HH%MM%S.%fS")
        Duration = DurDate-origin


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
        self.racDuration = parse_racDuration(racDuration)
        self.rpcDuration = parse_racDuration(rpcDuration)

        
    
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
    
    def __init__(self, id: str,block_period: str):
        
        self.id = id
        self.block_period = block_period  
        self.start, self.end = parse_block_period(block_period)   
    
    def __str__(self):
        return (
            f"IndividualAssignmentTask(\n"
            f"  ID: {self.id}\n"
            f"  Block Period: {self.block_period}\n"
            f"  Start: {self.start}\n"
            f"  End: {self.end}\n"
            f")"
        )