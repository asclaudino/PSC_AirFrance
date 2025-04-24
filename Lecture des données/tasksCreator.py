import json
#import pandas as pd
import re
import tkinter as tk
from tkinter import ttk
from datetime import timedelta


from GroundActivity import GroundActivity
from Pairing import Pairing
from Standby import Standby
from IndividualAssignment import IndividualAssignment
from Pilot import Pilot
from readerClass import readerClass
from Tasks import StandByTask, PairingTask
from Tasks import GroundActivityTask
from dateutil.relativedelta import relativedelta



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



def generate_tasks_lists(): 
    with open('Ressources/Export100PN.xml.json', 'r') as file:
         data = json.load(file)




    pairing_data = data.get('EasyData').get('Activities').get('Pairing')
    pairings_tasks = []

    for pairing_task in pairing_data:
        pairing_number = pairing_task.get('@pairingNumber')
        id = pairing_task.get('@id')
        block_period = pairing_task.get('PairingValues').get('COPairingElements').get('@blockPeriod')
        aircraft_type = pairing_task.get('@listAircraftType')
        racDuration = pairing_task.get('PairingValues').get('COPairingElements').get('@racDuration')
        rpcDuration = pairing_task.get('PairingValues').get('COPairingElements').get('@rpcDuration')

        
        if(pairing_task.get('Booking')):
            total_flight_time = timedelta(0)

            flight_duties = pairing_task.get('FlightDuty')
            if flight_duties:
                if isinstance(flight_duties, list):
                    duties = flight_duties
                else:
                    duties = [flight_duties]

                for duty in duties:
                    if not isinstance(duty, dict): continue
                    co_values = duty.get('COFlightDutyValues')

                    if co_values:
                        if isinstance(co_values, list):
                            for value in co_values:
                                flight_time = value.get('@flightTime')
                                if flight_time:
                                    #print(f"Extracted @flightTime: {flight_time}")
                                    total_flight_time += parse_duration(flight_time)
                        elif isinstance(co_values, dict):
                            flight_time = co_values.get('@flightTime')
                            if flight_time:
                                #print(f"Extracted @flightTime: {flight_time}")
                                total_flight_time += parse_duration(flight_time)

            for booking in pairing_task.get('Booking'):
                if not booking: continue
                type = booking.get('@requiredCode')
                nb_min = int(booking.get('@nbMin'))
                if nb_min > 0 : 
                    for i in range(int(booking.get('@nbMin'))):
                        task = PairingTask(pairing_number,id,type,False,block_period,aircraft_type, i+1, nb_min, racDuration, rpcDuration, total_flight_time)
                        duration = task.end - task.start
                        ##keeping just the rotations with at least 24hours of duration
                        if duration and duration >= timedelta(hours=24):
                            pairings_tasks.append(task)
        
        

                        
                        
        ## sorting by the longest block periods to the smallest
        sorted(pairings_tasks, key=lambda task: task.end - task.start, reverse=True)

    standby_data = data.get('EasyData').get('Activities').get('Standby')

    standby_tasks = []

    for standby_task in standby_data:
        standby_number = standby_task.get('@id')
        id = standby_task.get('@id')
        block_period = standby_task.get('StandbyElements').get('@blockPeriod')
        rpc_duration = standby_task.get('StandbyElements').get('@rpcDuration')
        aircraft_type = standby_task.get('@listAircraftType')

        for booking in standby_task.get('Booking'):
            type = booking.get('@requiredCode')
            nb_min = int(booking.get('@nbMin'))
            if nb_min > 0 :
                for i in range(int(booking.get('@nbMin'))):
                    task = StandByTask(standby_number,id,type,False,block_period,aircraft_type,i+1, nb_min, rpc_duration)
                    standby_tasks.append(task)



    ground_activity_data = data.get('EasyData').get('Activities').get('GroundActivity')
    ground_activity_tasks = []

    for ground_activity_task in ground_activity_data :
        ground_activity_number = ground_activity_task.get('@activityNumber')
        id = ground_activity_task.get('@id')
        block_period = ground_activity_task.get('@blockPeriod')
        bookings = ground_activity_task.get('Booking')
        
        if bookings:  
            if isinstance(bookings,list):
                for booking in bookings:
                    type = booking.get('@requiredCode')
                    nb_min = int(booking.get('@nbMin'))
                    if nb_min > 0 :
                        for i in range(int(booking.get('@nbMin'))):
                            task = GroundActivityTask(ground_activity_number,id,type,False,block_period,i+1, nb_min)
                            ground_activity_tasks.append(task)
            else:
                type = bookings['@requiredCode']
                nb_min = int(bookings['@nbMin'])
                if nb_min > 0 :
                    for i in range(int(bookings['@nbMin'])):
                        task = GroundActivityTask(ground_activity_number,id,type,False,block_period,i+1, nb_min)
                        ground_activity_tasks.append(task)
        else:
            task = GroundActivityTask(ground_activity_number,id,'',False,block_period)
            ground_activity_tasks.append(task)
        
            
   
    return pairings_tasks, ground_activity_tasks, standby_tasks


