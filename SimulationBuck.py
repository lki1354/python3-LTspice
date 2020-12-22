#! python3
# coding: utf-8
from LTspice.Converter import Converter

#set the simulation directory
simulation_dir = './Examples/'

#define the values
L1 = 33E-6
L2 = 33E-6
CC = 4.7E-6
Lin = 33E-6
Cin = 33E-6
Cout = 4.7E-6
Uin = 48

f = 1.0E+6
T = 1/f
Uout = 24
Iout = 5
Rload = Uout / Iout

#create a Converter object which create a copy of the stimulation file 'BuckVariable.asc' but with the set values from above
Buck = Converter(simulation_dir,'BuckVariable.asc',{'L1_v':L1,'Cout_v':Cout,'Uin_v':Uin,'Rload_v':Rload,'Tperiode_v':T,'Ton_v':(T*Uout/Uin)})

#starts LTspice in background and run the simulation, after finish parsing the log-File all automatically created files will be deleted
Buck.run(delete_simulation=True)

#shows the result form the simulation
print(Buck)

