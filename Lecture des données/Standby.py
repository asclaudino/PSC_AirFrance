from datetime import datetime

class Standby:

    def __init__(self, id, blockPeriod):
        self.id = id
        self.blockPeriod = blockPeriod
    
    
    def parse_block_period(self, block_period):
       start_str, end_str = block_period.split(';')
       start = datetime.strptime(start_str, "%Y-%m-%dT%H:%M:%S.%fZ")
       end = datetime.strptime(end_str, "%Y-%m-%dT%H:%M:%S.%fZ")
       return start, end