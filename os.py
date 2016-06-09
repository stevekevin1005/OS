#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""Explain here what this module has to offer."""
from __future__ import print_function
import copy
import random
import sys
import threading
import time

class CheckUp2(threading.Thread):
  """Explain here what this class represents and some usage hints."""
  def __init__(self, **kwargs):
    threading.Thread.__init__(self)
    self.threadID = kwargs['area_name']
    self.patient_list = kwargs['patient_list']

  def run(self):
    """Describe logic of processing here."""
    global mutex,patients,checkUP1Num,mutex2
    s_k, n_k , c_c= 'status', 'name', 'checkCount'
    busy_sleep_secs = 1
    while True:
      if check(self.patient_list):
        break
      for i in range(0, len(self.patient_list), 1):
        for status in patients:
          if status[n_k] == self.patient_list[i][n_k]:
            mutex.acquire()
            if status[c_c] >= checkUP1Num:
              if not (status[s_k] or self.patient_list[i][s_k]):
                status[c_c] = status[c_c] + 1;
                status[s_k] = True
                check_time = random.randint(1, 3)
                mutex2.acquire()
                print("%s: %s check time(%d)"
                   "" % (self.patient_list[i][n_k],
                      self.threadID, check_time))
                time.sleep(check_time)
                self.patient_list[i][s_k] = True
                mutex2.release()
                status[s_k] = False
                # time.sleep(busy_sleep_secs)
            mutex.release()


class CheckUp(threading.Thread):
  """Explain here what this class represents and some usage hints."""
  def __init__(self, **kwargs):
    threading.Thread.__init__(self)
    self.threadID = kwargs['area_name']
    self.patient_list = kwargs['patient_list']

  def run(self):
    """Describe logic of processing here."""
    global mutex,patients,mutex2
    s_k, n_k , c_c= 'status', 'name', 'checkCount'
    busy_sleep_secs = 1
    while True:
      if check(self.patient_list):
        break
      for i in range(0, len(self.patient_list), 1):
        for status in patients:
          if status[n_k] == self.patient_list[i][n_k]:
            mutex.acquire()
            
            if not (status[s_k] or self.patient_list[i][s_k]):
              status[c_c] = status[c_c] + 1;
              status[s_k] = True
              check_time = random.randint(1, 3)
              mutex2.acquire()
              print("%s: %s check time(%d)"
                 "" % (self.patient_list[i][n_k],
                    self.threadID, check_time))
              time.sleep(check_time)
              self.patient_list[i][s_k] = True
              mutex2.release()
              status[s_k] = False
              time.sleep(busy_sleep_secs)
            mutex.release()


def check(patient_list):
  """Check all patients have to be checked."""
  global mutex2
  check_flag = True
  mutex2.acquire()
  for patient in patient_list:
    if(patient['status'] == False):
      check_flag = False
  mutex2.release()
  return check_flag


def main():
  """Drive the endeavour."""
  

  # Outpatient init
  random.shuffle(patients)
  cardiology = {
    'area_name': 'Cardiology',
    'patient_list': copy.deepcopy(patients)
  }
  cardiologyCheckup = CheckUp(**cardiology)

  random.shuffle(patients)
  chest = {
    'area_name': 'Chest',
    'patient_list': copy.deepcopy(patients)
  }
  chestCheckup = CheckUp(**chest)

  random.shuffle(patients)
  ophthalmology = {
    'area_name': 'Ophthalmology',
    'patient_list': copy.deepcopy(patients)
  }
  ophthalmologyCheckup = CheckUp2(**ophthalmology)

  ophthalmologyCheckup.start()
  chestCheckup.start()
  cardiologyCheckup.start()
  


if __name__ == '__main__':
  # patients init
  patients = [{
    'name': 'Kevin',
    'status': False,
    'checkCount': 0
  }, {
    'name': 'Tom',
    'status': False,
    'checkCount': 0
  },{
    'name': 'Amy',
    'status': False,
    'checkCount': 0
  }]
  #checkUp step1 Num
  checkUP1Num = 2;

  mutex = threading.Lock()
  mutex2 = threading.Lock()
  sys.exit(main())