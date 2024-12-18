
class PairingTask:
    
    def __init__(self, pairing_number: str, id: str, type_place: str, filled: bool, block_period: str):
        
        self.pairing_number = pairing_number
        self.id = id
        self.type_place = type_place
        self.filled = filled
        self.block_period = block_period    


class StandByTask:
    
    def __init__(self, standby_number: str, id: str, type_place: str, filled: bool, block_period: str):
        
        self.standby_number = standby_number
        self.id = id
        self.type_place = type_place
        self.filled = filled
        self.block_period = block_period    
        
class GroundActivityTask:
    
    def __init__(self, ground_activity_number: str, id: str, type_place: str, filled: bool, block_period: str):
        
        self.ground_activity_number = ground_activity_number
        self.id = id
        self.type_place = type_place
        self.filled = filled
        self.block_period = block_period    