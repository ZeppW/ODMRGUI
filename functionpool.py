from modules import SE5082functionpool_python as AWG
from modules import GEM_500_COM3 as GEM
from modules import NI_DAQconfig as DAQ


class savedPara:
    def __init__(self, MW_pw, MW_trig, MW_smode, Laser_pw, DAQ_Nsample, DAQ_timeout):
        self.MW_pw = MW_pw
        self.MW_trig = MW_trig
        self.MW_smode = MW_smode
        self.Laser_pw = Laser_pw
        self.DAQ_Nsample = DAQ_Nsample
        self.DAQ_timeout = DAQ_timeout
        self.DAQ_isExternalclock = True
        self.readytogo = False

    def export(self):
        print("Current setting:")
        awg_ampl = AWG.amplitudeQ()
        print("MW power: {} Vpp".format(awg_ampl))
        awg_trig = AWG.trigQ()
        print("AWG trigger mode: {}".format(awg_trig))
        awg_sampling = AWG.samplingQ()
        print("AWG sampling mode: {}".format(awg_sampling))
        laser_pw = GEM.PowerQ()
        print("Laser power: {}".format(laser_pw))
        DAQ_Nsample = DAQ.sampleQ()
        print("DAQ N sample: {}".format(DAQ_Nsample))


    def loadParameters(self):
    ## preload settings for AWG and DAQ
        try:
            V_pp = 2*10**((self.MW_pw - 10)/20)
            AWG.setAmplitude(V_pp)
            AWG.setTriggermode(self.MW_trig)
            AWG.setSamplingmode(self.MW_smode)
            self.DAQ_task = DAQ.configureDAQ(self.DAQ_Nsample, self.DAQ_isExternalclock)
        except Exception as excpt:
            print('Error configuring setup. Exception details:', \
                  type(excpt).__name__,'.',excpt)
            self.DAQ_task.close()
        print("system is all set")

    def execute(self):
        if readytogo:
            try:
                GEM.Turn_on()
                GEM.SetPower(self.Laser_pw)
                AWG.setOutput(1)
            except Exception as excpt:
                print('Error configuring setup. Exception details:', \
                      type(excpt).__name__,'.',excpt)
                self.DAQ_task.close()
                AWG.setOutput(0)
            print("system operating!")
        else:
            print("system is not ready yet!")

        
                
