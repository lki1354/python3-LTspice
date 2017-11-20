import os

from .LTspiceAutomation import run_simulation,delete_simulation, LTSPICE_FLAG_RUN_ASCII_OUT

class Circuit:
    def __init__(self, directory, file_name):
        self.dir = directory
        self.file = file_name
        self.simulation = open(os.path.normpath(self.dir + self.file), "r", encoding="utf-8").read()
    def set_value(self, identifier, value):
        self.simulation = self.simulation.replace(identifier, str(value))
    def set_values(self,value_dict):
        for identifier, value in value_dict.items():
            self.set_value(identifier,value)
    def save_simulation(self, name=None, directory=None):
        if (name is not None):
            self.simulation_file = name
        else:
            self.simulation_file = r'new_' + self.file
        if (directory is not None):
            self.simulation_dir = directory
        else:
            self.simulation_dir = self.dir
        file_sim = open(os.path.normpath(self.simulation_dir + self.simulation_file), "w", encoding="utf-8")
        file_sim.write(self.simulation)
        file_sim.close()
        self.new_simulation = ( self.simulation_dir, self.simulation_file)
        return self.new_simulation

    def pars_log(self):
        raise NotImplementedError

    def run(self):
        run_simulation(self.simulation_dir,self.simulation_file)

    def remove_output(self):
        delete_simulation(self.simulation_dir,self.simulation_file)
class LTspiceRAWdata():
    variableNumber = None
    pointsNumber = None
    values = dict()

class CircuitRAW(Circuit):
    numberOfVariables = None
    numberOfPoints = None
    namesOfVariables = []
    values = dict()

    def __init__(self,directory, file_name):
        super().__init__(directory,file_name)
    def run(self):
        run_simulation(self.simulation_dir,self.simulation_file,ltspice_flags=LTSPICE_FLAG_RUN_ASCII_OUT)

    def pars(self):
        with open(os.path.normpath(self.simulation_dir + self.simulation_file.split('.')[0] + '/' +self.simulation_file.split('.')[0] + r'.raw'), encoding="utf-8") as f:
            for line in f:
                if 'No. Variables:' in line:
                    self.numberOfVariables = int(line.split(':')[1])
                    break
            for line in f:
                print(line)
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
                    print(variables[2]+variables[3])
                self.namesOfVariables.append(variables[2])
                self.values.update({self.namesOfVariables[i]:[]})
                i = i+1
            i = 0
            print(self.numberOfPoints)
            while i < self.numberOfPoints:
                line = f.readline()
                position, empty, value = line.split('\t')
                #if i == int(position):
                #print(int(position))
                countVariables = 1
                for variableName in self.namesOfVariables:
                    self.values[variableName].append(float(value))
                    if countVariables < self.numberOfVariables:
                        value = f.readline().replace('\t','')
                    countVariables = countVariables + 1
                i = i+1
        f.closed
        print('pars finished!')