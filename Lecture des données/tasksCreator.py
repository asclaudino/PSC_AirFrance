import json
#import pandas as pd
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


with open('Ressources/Export20PN.xml.json', 'r') as file:
     data = json.load(file)
     



pairing_data = data.get('EasyData').get('Activities').get('Pairing')
pairings_tasks = []

for pairing_task in pairing_data:
    pairing_number = pairing_task.get('@pairingNumber')
    id = pairing_task.get('@id')
    block_period = pairing_task.get('PairingValues').get('COPairingElements').get('@blockPeriod')
    if(pairing_task.get('Booking')):
        for booking in pairing_task.get('Booking'):
            if not booking: continue
            type = booking.get('@requiredCode')
            nb_min = int(booking.get('@nbMin'))
            if nb_min > 0 :
                for i in range(int(booking.get('@nbMin'))):
                    task = PairingTask(pairing_number,id,type,False,block_period)
                    pairings_tasks.append(task)

print(len(pairings_tasks))

standby_data = data.get('EasyData').get('Activities').get('Standby')

standby_tasks = []

for standby_task in standby_data:
    standby_number = standby_task.get('@standbyNumber')
    id = standby_task.get('@id')
    block_period = standby_task.get('StandbyElements').get('@blockPeriod')
    for booking in standby_task.get('Booking'):
        type = booking.get('@requiredCode')
        nb_min = int(booking.get('@nbMin'))
        if nb_min > 0 :
            for i in range(int(booking.get('@nbMin'))):
                task = StandByTask(standby_number,id,type,False,block_period)
                standby_tasks.append(task)

print(len(standby_tasks))

GroundActivity_data = data.get('EasyData').get('Activities').get('GroundActivity')
GroundActivity_tasks = []
for GroundActivity_task in GroundActivity_data :
    ground_activity_number = GroundActivity_task.get('activityNumber')
    id = GroundActivity_task.get('id')
    block_period = GroundActivity_task.get('@blockPeriod')
    if GroundActivity_task.get('Booking'):  
        for booking in GroundActivity_task.get('Booking'):
            type = booking.get('@requiredCode')
            nb_min = int(booking.get('@nbMin'))
            if nb_min > 0 :
                for i in range(int(booking.get('@nbMin'))):
                    task = GroundActivityTask(ground_activity_number,id,type,False,block_period)
                    GroundActivity_tasks.append(task)

print(len(GroundActivity_tasks))
   



