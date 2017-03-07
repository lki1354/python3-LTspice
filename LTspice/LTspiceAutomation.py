#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

def Simulate(path):
    sim = LTSpice(sim_file=path[0], sim_dir=path[1] )
    sim.run_simulation()
    sim.pars_log()
    return sim.get_data()


class ConverterData:
    PinAVG = None
    PoutRMS = None
    UinRMS = None
    IinRMS = None
    UoutRMS = None
    IoutRMS = None
    UinRippel = None
    IinRippel = None
    UoutRippel = None
    IoutRippel = None
    
    def __init__(self,name):
        self.name = name
    def getValues(self):
        return (self.efficiency_percent,self.IoutRippel*1E+3, self.UoutRippel*1E+3,
                self.IoutRMS,self.UoutRMS,self.IinRippel)
    @property
    def output_power(self):
        return self.PoutRMS
    @property
    def input_power(self):
        return self.PinAVG
    @property
    def efficiency(self):
        return self.output_power / self.input_power
    @property
    def efficiency_percent(self):
        return self.efficiency*100.0
    def __str__(self):
        self.toPrint = 'Data printed from converter %s\n'%self.name
        self.toPrint += 'Efficiency = %3.2f%% \n'%self.efficiency_percent
        self.toPrint += 'Input Power = %3.2fW \n'%self.input_power
        self.toPrint += 'Output Power = %3.2fW \n'%self.output_power
        self.toPrint += '#############################\n'
        self.toPrint += 'Input Voltage RMS = %3.4fV \n'%self.UinRMS
        self.toPrint += 'Input Current RMS = %3.4fA \n'%self.IinRMS
        self.toPrint += 'Output Voltage RMS = %3.4fV \n'%self.UoutRMS
        self.toPrint += 'Output Current RMS = %3.4fA \n'%self.IoutRMS
        self.toPrint += 'Input Voltage Rippel = %.4fV \n'%self.UinRippel
        self.toPrint += 'Input Current Rippel = %.4fA \n'%self.IinRippel
        self.toPrint += 'Output Voltage Rippel = %.4fmV \n'%(self.UoutRippel*1.0E+3)
        self.toPrint += 'Output Current Rippel = %.4fmA \n'%(self.IoutRippel*1.0E+3)
        return self.toPrint


class ConverterSimulation:
    def __init__(self,converter_file,converter_dir):
        self.converter_file = converter_file
        self.converter_dir = converter_dir
        self.simulation = open(converter_dir+converter_file,"r",encoding="utf-8").read()
    def set_value(self,identifier,value):
        self.simulation = self.simulation.replace(identifier,str(value))
    def remove_new_simulation(self):
        os.system('rm "'+self.new_simulation[1]+self.new_simulation[0]+'"')
    def save_simulation(self,name=None,directory=None):
        if(name is not None):
            self.converter_file = name
        else :
            self.converter_file = 'new_'+self.converter_file
        if(directory is not None):
            self.converter_dir = directory
        file_sim = open(self.converter_dir+self.converter_file,"w",encoding="utf-8")
        file_sim.write(self.simulation)
        file_sim.close()
        self.new_simulation = (self.converter_file, self.converter_dir)
        return self.new_simulation
        
    
    
class LTSpice:
    _LTSpice_dir = '~/.wine/drive_c/Program Files/LTC/LTspiceXVII/'
    
    def __init__(self,sim_file,sim_dir,log_name='logPythonLTSpice.txt',sim_script='run_LTSpice_from_cmd.sh',data = None):
        self.sim_file = sim_file
        self.sim_dir = sim_dir
        self.log_name = log_name
        self._sim_script = sim_script
        if data is None:
            self.data = ConverterData(sim_file.split('.')[0])
        else:
            self.data = data
    
    def run_simulation(self):
        cp_sim = '"'+self.sim_dir+self.sim_file+'" "'+self._LTSpice_dir+'"'
        #print( cp_sim )
        os.system('cp '+cp_sim)
        run_sim = '"'+self._LTSpice_dir+self._sim_script+'" "'+self.sim_file+'" "'+self.log_name+'"'
        #print( run_sim )
        run_sim = os.system(run_sim)
        os.system('rm "'+self._LTSpice_dir+self.sim_file+'"')
        print('Simulation finished!')
        
    def pars_log(self):
        self._log = open(self._LTSpice_dir+self.log_name,encoding="utf-16-le").read()
        self.read_values()
        os.system('rm "'+self._LTSpice_dir+self.log_name+'"')
        print('pars finished!')
        
    def search_position(self):
        self.pos_uinrms = self._log.find('uinrms')
        self.pos_iinrms = self._log.find('iinrms')
        self.pos_uoutrms = self._log.find('uoutrms')
        self.pos_ioutrms = self._log.find('ioutrms')

        self.pos_ioutrippel = self._log.find('ioutrippel')
        self.pos_uoutrippel = self._log.find('uoutrippel')
        self.pos_iinrippel = self._log.find('iinrippel')
        self.pos_uinrippel = self._log.find('uinrippel')
        
        self.pos_pinavg= self._log.find('pinavg')
        self.pos_poutrms= self._log.find('poutrms')
        
        
    def read_values(self):
        self.search_position()
        self.data.UinRMS = float(self._log[self.pos_uinrms:self._log.find('FROM',self.pos_uinrms)].split('=')[1])
        self.data.IinRMS = float(self._log[self.pos_iinrms:self._log.find('FROM',self.pos_iinrms)].split('=')[1])
        self.data.UoutRMS = float(self._log[self.pos_uoutrms:self._log.find('FROM',self.pos_uoutrms)].split('=')[1])
        self.data.IoutRMS = float(self._log[self.pos_ioutrms:self._log.find('FROM',self.pos_ioutrms)].split('=')[1])

        self.data.UinRippel = float(self._log[self.pos_uinrippel:self._log.find('FROM',self.pos_uinrippel)].split('=')[1])
        self.data.IinRippel = float(self._log[self.pos_iinrippel:self._log.find('FROM',self.pos_iinrippel)].split('=')[1])
        self.data.UoutRippel = float(self._log[self.pos_uoutrippel:self._log.find('FROM',self.pos_uoutrippel)].split('=')[1])
        self.data.IoutRippel = float(self._log[self.pos_ioutrippel:self._log.find('FROM',self.pos_ioutrippel)].split('=')[1])
        
        self.data.PoutRMS = float(self._log[self.pos_poutrms:self._log.find('FROM',self.pos_poutrms)].split('=')[1])
        self.data.PinAVG = float(self._log[self.pos_pinavg:self._log.find('FROM',self.pos_pinavg)].split('=')[1])

    def get_data(self):
        return self.data
