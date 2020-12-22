#! python3
# coding: utf-8
from LTspice.Circuit import CircuitRAW
import matplotlib.pyplot as plt

#set the simulation directory
simulation_dir = './Examples/'

#define the Values
L1 = 33E-6
Lin = 33E-6
Cin = 33E-6
Cout = 4.7E-6
Uin = 48
f = 1.0E+6
T = 1/f
Uout = 24
Iout = 5
Rload = Uout / Iout

#define which variables in the schematic has to replaced with which value
value_dict = {'{L1}':L1,'{Cout}':Cout,'{Uin}':Uin,'{Rload}':Rload,'{Tperiode}':T,'{Ton}':(T*Uout/Uin),'{Tstop}':1E-3}

#create a CricuitRaw object with the directory reference to the schematic file and read the content of the file
Buck = CircuitRAW(simulation_dir,'BuckSimple.asc')

#replace the place holder with the defined values in the dictionary
Buck.set_values(value_dict)

#save the schematic with the right values to a new asc-File
Buck.save_simulation()

#run LTspice and simulate the new schematic file (asc-File) and wait until simulation is finish
Buck.run()

#pars the ASCII raw-File
Buck.pars()

#remove all automatic generated files and folder
Buck.remove_output()

#shows the variable names which are read from the raw file
print(Buck.namesOfVariables)


time = Buck.values['time']
uout = Buck.values['V(out)']
uin = Buck.values['V(in)']

#plot the output and input voltage
plt.plot(time,uout,time,uin)
plt.ylabel('Ausgangsspannung [V]')
plt.xlabel('Zeit in [s]')
plt.grid(True)
plt.show()

