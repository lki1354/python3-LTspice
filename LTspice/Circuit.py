import os
import logging
import shutil

from .LTspiceAutomation import run_simulation, LTSPICE_FLAG_BATCH_RUN, LTSPICE_FLAG_BATCH_RUN_ASCII_OUT
from .Parser import pars_log_file

from quantiphy import Quantity

param_file_internal = 'values.param'

class Parameter:
    def __init__(self,dir,filename):
        self.dir = dir
        self.filename = filename
        self.names = list()
        self.__read_content()
        
    def __read_content(self):
        with open(os.path.normpath(self.dir + self.filename), "r", encoding="ansi") as file:
            for line in file:
                if '*' not in  line[0][0] and '.param' in line:  
                    line = line.replace('.param','').split('=')
                    name =  line[0].replace(' ','')
                    self.names.append(name)
                    try:
                        value =  Quantity(line[1])
                        logging.info( name+'='+str(value) )
                    except:
                        value = line[1]
                    self.__dict__[name] = value
    def save_param_file(self):
        with open(os.path.normpath(self.dir + param_file_internal), "w", encoding="ansi") as file:
            for name in self.names:
                file.write('.param '+name+' = '+str(self.__dict__[name]).replace(' ', '')+' \n')
    def __str__(self):
        strOut = '**Values of the Parameters** : \n'
        for name in self.names:
            strOut += '* '+ name + '='+str(self.__dict__[name]) +'\n'
        return strOut
        

class Circuit:
    def __init__(self, directory, file_name, run_original=False, param_filename = None):
        self.dir = directory
        self.file = file_name
        self.simulation_file = file_name
        self.simulation_dir = directory
        self.run_original = run_original
        if not self.run_original:
            self.simulation = open(os.path.normpath(self.dir + self.file), "r", encoding="ansi").read()
            if param_filename is not None:
                self.param = Parameter(self.dir,param_filename)
                self.simulation = self.simulation.replace(param_filename,param_file_internal)

                
    def set_value(self, identifier, value):
        self.simulation = self.simulation.replace(identifier, str(value))
    def set_values(self,value_dict):
        for identifier, value in value_dict.items():
            self.set_value(identifier,value)
    def save_simulation(self, directory=None,name=None ):
        if (name is not None):
            self.simulation_file = name
        else:
            self.simulation_file = r'new_' + self.file
        if (directory is not None):
            os.makedirs(directory)
            self.simulation_dir = directory
        if hasattr(self,'param'):
            self.param.save_param_file() 
        file_sim = open(os.path.normpath(self.simulation_dir + self.simulation_file), "w", encoding="ansi")
        file_sim.write(self.simulation)
        file_sim.close()
        return (self.simulation_dir, self.simulation_file)
        
    def reload_simulation(self):
        self.simulation = open(os.path.normpath(self.dir + self.file), "r", encoding="ansi").read()
        if hasattr(self,'param'):
            self.simulation = self.simulation.replace(self.param.filename,param_file_internal)

    def pars_log(self, file_name=None):
        if file_name == None:
            file_name = self.simulation_dir +self.simulation_file.replace('asc','log')
        self.data = pars_log_file( file_name )
        self.__dict__.update( self.data )

    def run(self, flags = LTSPICE_FLAG_BATCH_RUN ):
        run_simulation(self.simulation_dir,self.simulation_file,flags)

    def remove_output(self):
        if hasattr(self,'param'):
            os.remove(self.dir+param_file_internal)
        if self.simulation_dir == self.dir:
            if not self.run_original:
                os.remove(self.simulation_dir+self.simulation_file)
            os.remove(self.simulation_dir+self.simulation_file.replace('asc', 'log'))
            os.remove(self.simulation_dir+self.simulation_file.replace('asc', 'raw'))
            #os.remove(self.simulation_dir+self.simulation_file.replace('asc', 'op.raw'))
        else:
            shutil.rmtree(self.simulation_dir, ignore_errors=False, onerror=None)


class LTspiceRAWdata():
    variableNumber = None
    pointsNumber = None
    values = dict()

class CircuitRAW(Circuit):

    def __init__(self,directory, file_name,run_original=False,param_filename = None):
        super().__init__(directory,file_name,run_original,param_filename)
        self.__initialize_variables()
        
    def __initialize_variables(self):
        self.numberOfVariables = None
        self.numberOfPoints = None
        self.namesOfVariables = []
        if hasattr(self,'values'):
            for name in self.values.keys():
                self.__dict__[name] = None
        self.values = dict()
    
    def run(self, flags = LTSPICE_FLAG_BATCH_RUN_ASCII_OUT):
        run_simulation(self.simulation_dir,self.simulation_file,flags)

    def pars_raw(self, file_name=None):
        self.__initialize_variables()
        if file_name == None:
            file_name = os.path.normpath(self.simulation_dir +self.simulation_file.split('.')[0] + r'.raw')
        with open(file_name, encoding="ansi") as f:
            for line in f:
                if 'No. Variables:' in line:
                    self.numberOfVariables = int(line.split(':')[1])
                    break
            for line in f:
                logging.info('Line Parsing: '+line)
                if 'No. Points:' in line:
                    self.numberOfPoints = int(line.split(':')[1])
                    break
            for line in f:
                if 'Variables:' in line:
                    break
            i = 0
            for line in f:
                if 'Values:' in line:
                    break
                variables = line.split('\t')
                if int(variables[1]) == i:
                    logging.info('Variable:'+variables[2]+' unit:'+variables[3])
                self.namesOfVariables.append(variables[2].replace('V','v').replace('I','i'))
                self.values.update({self.namesOfVariables[i]:[]})
                i = i+1
            i = 0
            logging.info('Number of Points in RAW-File: %i'%self.numberOfPoints)
            while i < self.numberOfPoints:
                line = f.readline()
                position, empty, value = line.split('\t')
                if i != int(position):
                    logging.warning('Position i=5i is not the same, position=%i'%(i,int(position)) )
                countVariables = 1
                for variableName in self.namesOfVariables:
                    self.values[variableName].append(float(value))
                    if countVariables < self.numberOfVariables:
                        value = f.readline().replace('\t','')
                    countVariables = countVariables + 1
                i = i+1
        f.closed
        for name, value in self.values.items():
            self.__dict__.update( { name.replace('(','_').replace(')','').replace(':','_') :value } )
        logging.info('pars finished!')