import pyvisa
import time
import numpy as np
from struct import unpack
import matplotlib.pyplot as plt

rm = pyvisa.ResourceManager()
rm.list_resources()
GEM = rm.open_resource('ASRL3::INSTR')

def Turn_on():
    GEM.write('ON')
    GEM.write('POWER=001')
    print('Laser has initialized!!!')

def SetPower(pw_mw):
    GEM.write('POWER='+str(pw_mw))
    print('Power has changed to '+str(pw_mw)+' mW!!!Please wait...')
    time.sleep(10)

def Turn_off():
    GEM.write('POWER=001')
    print('Reset power!!!Please wait...')
    time.sleep(10)
    GEM.write('OFF')
    print('Laser has been disabled!!!')

def PowerQ():
    return GEM.query('POWER?').split()[0]

def tempQ():
    temp_list = []
    i = 0
    while i < 5:
        tt = GEM.query('LASTEMP?').split()
        if tt != []:
            tt = ''.join(list(tt[0])[:-1])
            temp_list.append(float(tt))
            i += 1

    print(temp_list)

