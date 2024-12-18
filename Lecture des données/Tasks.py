
class PairingTask:
    
    def __init__(self, pairing_number: str, id: str, type_place: str, filled: bool, block_period: str):
        
        self.pairing_number = pairing_number
        self.id = id
        self.type_place = type_place
        self.filled = filled
        self.block_period = block_period    

    def __str__(self):
        return (
            f"PairingTask(\n"
            f"  Pairing Number: {self.pairing_number}\n"
            f"  ID: {self.id}\n"
            f"  Type Place: {self.type_place}\n"
            f"  Filled: {self.filled}\n"
            f"  Block Period: {self.block_period}\n"
            f")"
        )

class StandByTask:
    
    def __init__(self, standby_number: str, id: str, type_place: str, filled: bool, block_period: str):
        
        self.standby_number = standby_number
        self.id = id
        self.type_place = type_place
        self.filled = filled
        self.block_period = block_period    
        
    def __str__(self):
        return (
            f"StandByTask(\n"
            f"  Standby Number: {self.standby_number}\n"
            f"  ID: {self.id}\n"
            f"  Type Place: {self.type_place}\n"
            f"  Filled: {self.filled}\n"
            f"  Block Period: {self.block_period}\n"
            f")"
        )
        
class GroundActivityTask:
    
    def __init__(self, ground_activity_number: str, id: str, type_place: str, filled: bool, block_period: str):
        
        self.ground_activity_number = ground_activity_number
        self.id = id
        self.type_place = type_place
        self.filled = filled
        self.block_period = block_period    
    
    def __str__(self):
        return (
            f"GroundActivityTask(\n"
            f"  GroundActivity Number: {self.ground_activity_number}\n"
            f"  ID: {self.id}\n"
            f"  Type Place: {self.type_place}\n"
            f"  Filled: {self.filled}\n"
            f"  Block Period: {self.block_period}\n"
            f")"
        )