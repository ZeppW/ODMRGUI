import nidaqmx
from  nidaqmx.constants import *
import sys
import matplotlib.pyplot as plt
import numpy as np

DAQ_APDInput = "DAQ/ai0"
minVoltage = -10
maxVoltage = 10
DAQ_MaxSamplingRate = 2e6
NsampsPerDAQread = 1000
DAQ_StartTrig = "PFI0" 

def configureDAQ(Nsamples, isExternalclock = True):
    global NsampsPerDAQread
    try:
    #Create and configure an analog input voltage task
        NsampsPerDAQread = Nsamples
        readTask = nidaqmx.Task()
        channel = readTask.ai_channels.add_ai_voltage_chan(DAQ_APDInput,"",TerminalConfiguration.RSE,minVoltage,maxVoltage,VoltageUnits.VOLTS)
    #Configure sample clock
        if isExternalclock is True:
            print("external clock")
            DAQ_SampleClk = "PFI1"
            readTask.timing.cfg_samp_clk_timing(DAQ_MaxSamplingRate, DAQ_SampleClk, Edge.RISING, AcquisitionType.FINITE, NsampsPerDAQread)
##            readTask.timing.ai_conv_src = DAQ_SampleClk
##            readTask.timing.ai_conv_active_edge = Edge.RISING
        else:
            print("internal clock")
            DAQ_SampleClk = None
            readTask.timing.cfg_samp_clk_timing(DAQ_MaxSamplingRate,DAQ_SampleClk)
        #Configure start trigger
        readStartTrig = readTask.triggers.start_trigger
        readStartTrig.dig_edge_src = DAQ_StartTrig
        readStartTrig.cfg_dig_edge_start_trig(DAQ_StartTrig,Edge.FALLING)
        print("DAQ configuration completed!!")
    except Exception as excpt:
        print('Error configuring DAQ. Please check your DAQ is connected and powered. Exception details:', type(excpt).__name__,'.',excpt)
        closeDAQTask(readTask)
        sys.exit()
    return readTask
def readDAQ(task,Nsamples = NsampsPerDAQread, timeout = 60):
    try:
        counts = task.read(Nsamples,timeout)
    except Exception as excpt:
        print('Error: could not read DAQ. Please check your DAQ\'s connections. Exception details:', type(excpt).__name__,'.',excpt)
        sys.exit()
    return counts
def plot_read(counts):
    t_min = 1/DAQ_MaxSamplingRate
    x_time = np.arange(0, len(counts), 1)*t_min
    fig = plt.figure()
    plt.plot(x_time, counts, 'bo-')
    plt.xlabel('Time')
    plt.ylabel('Voltage')
    plt.show()

def closeDAQTask(task):
    task.close()

def sampleQ():
    return NsampsPerDAQread
