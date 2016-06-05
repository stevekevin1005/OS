#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading
import time
import random
import copy

exitFlag = 0

class checkup (threading.Thread):  #繼承thred 檢查流程
  def __init__(self, threadID, patientList, patientStatus):
    threading.Thread.__init__(self)
    self.threadID = threadID
    self.patientList = patientList
    self.patientStatus = patientStatus
  def run(self):                   #檢查中
    while True:
      if(check(self.patientList)):
        break
      for i in range( 0, 2, 1):
        for status in self.patientStatus:
          if status['name'] == self.patientList[i]['name'] and status['status'] == False and self.patientList[i]['status'] == False:
            status['status'] = True
            checkTime = random.randint(1,3)
            print "%s: %s check time(%d)" % (self.patientList[i]['name'], self.threadID, checkTime)
            time.sleep(checkTime)
            self.patientList[i]['status'] = True
            status['status'] = False
            time.sleep(1)

#check all patients have to be ckecked
def check(patientList):
  checkFlag = False
  for patient in patientList:
    if patient['status'] == True:
      checkFlag = True
    else:
      checkFlag = False
  if checkFlag:
    return True
  else:
    return False

# patients init
patients = [{
  'name': 'Kevin',
  'status': False
},{
  'name': 'Tom',
  'status': False
}]

# Outpatient init
random.shuffle(patients)
Cardiology = {
  'name': 'Cardiology',
  'patientList':  copy.deepcopy(patients),
  'patientStatus': patients
}
CardiologyCheckup = checkup('Cardiology', Cardiology['patientList'], Cardiology['patientStatus'])

random.shuffle(patients)
Chest = {
  'name': 'Chest',
  'patientList':  copy.deepcopy(patients),
  'patientStatus': patients
}
ChestCheckup = checkup('Chest', Chest['patientList'], Chest['patientStatus'])

ChestCheckup.start()
CardiologyCheckup.start()
