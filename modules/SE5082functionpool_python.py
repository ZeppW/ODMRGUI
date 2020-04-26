import pyvisa
import time
from datetime import datetime
import serial
import os
import numpy as np
import matplotlib.pyplot as plt
import struct

#pyvisa.log_to_screen()
rm = pyvisa.ResourceManager() # check what devices are connected
rm.list_resources() # tell you names of connected devices
SE5082 = rm.open_resource('GPIB0::10::INSTR') # connect to AWG

def idn(inputs = 0):
    out = SE5082.query('*RST;*STB?;*IDN?')
    return out

    
def reset(inputs = 0):
##Reset to factory settings
##*CLS;*RST;*OPC?
    out = SE5082.query('*CLS;*RST;*OPC?')
    return out

    
def checkErr(inputs):
    out = SE5082.query('SYST:ERR?')

    return out

def setChn(inputs):
## inputs = 1 or 2
    SE5082.write('INST:SEL ' + str(inputs))

def setOutput(inputs):
## inputs = 1(on) or 0(off)
    if inputs:
        SE5082.write('OUTP ON')
    else:
        SE5082.write('OUTP OFF')

def eraseSeg(inputs):
## inputs = 0(for all) or arbitrary number
    if inputs == 0:
        SE5082.write('TRAC:DEL:ALL')
        SE5082.write('SEQ:DEL:ALL')
    else:
        SE5082.write('TRAC:DEL ' + str(inputs))

def setMode(inputs):
## inputs = FIXed | USER | SEQuence | ASEQuence | MODulation | PULSe | PATTern
    SE5082.write('FUNC:MODE' + inputs)

def setSamplingmode(inputs):
## inputs = NRZ | NRTZ | RTZ | RF
    SE5082.write('OUTP:SAMP:FORM ' + inputs)

def samplingQ():
    return SE5082.query('OUTP:SAMP:FORM?').split()[0]

def getMode(inputs = 0):
    out = E5082.query('FUNC:MODE?')
    return out


def setAmplitude(inputs):
    if inputs > 2:
        print('Amplitude too high, aborting...')

    else:

        SE5082.write('VOLT:AMPL ' + str(inputs))

def amplitudeQ():
    return float(SE5082.query('VOLT?'))
    

                

def setTriggermode(inputs):
    global trig_stat
##inputs = cont, gate or trig
    ## set input impedence to 50
    SE5082.write('TRIG:INP:IMP 10k')
    print(SE5082.query('TRIG:INP:IMP?'))
    if inputs == 'cont':
        SE5082.write('INIT:CONT 1')
        trig_stat = 'cont'
    elif inputs == 'gate':
        SE5082.write('INIT:CONT 0')
        SE5082.write('INIT:GATE 1')
        SE5082.write('TRIG:SOUR:ADV EXT')
        SE5082.write('TRIG:SLOP POS')
        SE5082.write('TRIG:SEQ:LEV 1.200e+00')
        trig_stat = 'gate'
    elif inputs == 'trig':
        SE5082.write('INIT:CONT 0')
        SE5082.write('INIT:TRIG 1')
        SE5082.write('TRIG:SOUR:ADV EXT')
        SE5082.write('TRIG:SLOP POS')
        SE5082.write('TRIG:SEQ:LEV 1.200e+00')
        trig_stat = 'trig'
        
def trigQ():
    return trig_stat
    
    

    
def setSinewave(inputs):
    SE5082.write('FUNC:MODE FIX')
    SE5082.write('FUNC:SHAP SIN')
    SE5082.write('FREQ ' + str(inputs))
    
    
    
def transferAWF(inputs):
    SE5082.write('FUNC:MODE USER')
    awf=inputs.AWF

    npoints=len(awf)
    nbytes=2
    
    buffer=npoints*nbytes            
    ## get the amplitude
    amp = float(SE5082.query('VOLT?'))        
    if inputs.renormed:
        awgsig = (awf - min(awf))*4/(max(awf) - min(awf)) - 2 ## rescaled  between -2 and 2                
    else:
        awgsig = awf
    if ((max(awf) - min(awf)) > 2*amp): 
        print('Waveform out of bounds, please reupload.')
    awgsig = np.uint16((awgsig - min(awgsig))*4095/(max(awgsig) - min(awgsig)))
##    ## Create a block of data in IEEE 488.2 format(menu P 4-67)
    SE5082.write('TRAC:DEF {}, '.format(inputs.segNum) + str(npoints))
    SE5082.write('TRAC:SEL {}'.format(inputs.segNum))
    SE5082.write_binary_values('TRAC:DATA', awgsig, datatype = 'H')
##    SE5082.write('TRAC:DATA' + header)
##    SE5082.write_raw(datablock)
##    SE5082.write('TRAC:SEL:TIM COH')
            

    path_name = os.getcwd()
    path_name_out = path_name + "\\AWG_test\\"
    if not os.path.exists(path_name_out):
        os.makedirs(path_name_out)
    np.savetxt('%s.txt' % 'target_wave', awf)
## set arb waveform frequency        

    print("set to frequency: {}Hz".format(1/inputs.dt))
    SE5082.write('FREQ:RAST ' + str(1/inputs.dt))
    print(SE5082.query('FREQ:RAST?'))
    print(SE5082.query('TRAC:POIN?'))

def createSeq(inputs):
##    minimum length: 3
##    inputs = [[<segment>, <loops>, <jump_flag>],...]
    tbl_len = len(inputs)
    SE5082.write('SEQ:DEL 1')
    if tbl_len < 3:
        raise ValueError("Table length err: minimum length is 3!")
        return
    else:
        SE5082.write('FUNC:MODE SEQ')
        s = struct.Struct('<LHBx')
        s_size = s.size
        print(s_size)
        m = np.empty(s_size * tbl_len, dtype='uint8')
        for n in range(tbl_len):
            repeats, seg_nb, jump_flag = inputs[n]
            s.pack_into(m, n * s_size, int(repeats), int(seg_nb), int(jump_flag))
        SE5082.write_binary_values('SEQ:DATA', m, datatype = 'B')
        SE5082.write('ASEQ:ADV:ONCE')
        print('sequence has been set!')
    
