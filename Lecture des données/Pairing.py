from datetime import datetime

class Pairing:
    

    def __init__(self, id, blockPeriod):
        self.id = id
        self.blockPeriod = blockPeriod
        self.rpcDuration = None
        self.racDuration = None
        ## add already start and end as class properties. 
        ## methods for verifiying if a date is inside of a block period. 
        ## find already the corresponding legs of a pairing.
         

    def parse_block_period(self, block_period):
       start_str, end_str = block_period.split(';')
       start = datetime.strptime(start_str, "%Y-%m-%dT%H:%M:%S.%fZ")
       end = datetime.strptime(end_str, "%Y-%m-%dT%H:%M:%S.%fZ")
       return start, end