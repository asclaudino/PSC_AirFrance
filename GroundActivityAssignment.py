from datetime import datetime


class GroundActivityAssignment:
  
   def __init__(self, id, block_period):
       self.id = id
       self.block_period = block_period


   def parse_block_period(self, block_period):
       start_str, end_str = block_period.split()
       start = datetime.strptime(start_str, "%Y-%m-%dT%H:%M:%S.%fZ")
       end = datetime.strptime(end_str, "%Y-%m-%dT%H:%M:%S.%fZ")
       return start, end

