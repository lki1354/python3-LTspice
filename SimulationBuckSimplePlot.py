#! python3
# coding: utf-8
from LTspice.Circuit import CircuitRAW
from LTspice.LTspiceAutomation import LTSPICE_FLAG_RUN_ASCII_OUT,LTSPICE_FLAG_BATCH_RUN_ASCII_OUT

import matplotlib.pyplot as plt

#set the simulation directory
simulation_dir = './Examples/'
simulation_file = 'BuckVariable.asc'
parameter_file = 'default_values.param'


#define the values

f = 1.0E+6
N_cycles = 1000
Uout = 24
Iout = 5
Rload = Uout / Iout

#create a Converter object which create a copy of the stimulation file 'BuckVariable.asc' but with the set values from above
Buck =  CircuitRAW(simulation_dir,simulation_file,run_original=False,param_filename = parameter_file)
Buck.param.Rload = Rload
Buck.param.Tsim = N_cycles/f
Buck.param.Tperiode = 1/f
Buck.param.Tstart = Buck.param.Tsim-2.0/f
Buck.param.Ton = (1/f*Uout/Buck.param.Uin) 
print(Buck.param)

Buck.save_simulation(name='Example_Run.asc')

Buck.run(LTSPICE_FLAG_BATCH_RUN_ASCII_OUT)
#Buck.run(LTSPICE_FLAG_RUN_ASCII_OUT)
Buck.pars_raw()
Buck.pars_log()
Buck.remove_output()

#shows the variable names which are read from the raw file
print(Buck.namesOfVariables)

time = Buck.values['time']
uout = Buck.values['v(out)']
uin = Buck.values['v(in)']

#plot the output and input voltage
plt.plot(time,uout,label='output')
plt.plot(time,uin,label='input')
plt.ylabel('voltage [V]')
plt.xlabel('time in [s]')
plt.legend()
plt.grid(True)
plt.show()

