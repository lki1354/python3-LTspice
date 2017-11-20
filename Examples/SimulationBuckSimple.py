# coding: utf-8
from LTspice.Circuit import CircuitRAW
#from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
#init_notebook_mode(connected=True)

simulation_dir = './Examples/'

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
#Rload = 0.001
Rload = Uout / Iout
value_dict = {'{L1}':L1,'{Cout}':Cout,'{Uin}':Uin,'{Rload}':Rload,'{Tperiode}':T,'{Ton}':(T*Uout/Uin),'{Tstop}':1E-3}

Buck = CircuitRAW(simulation_dir,'BuckSimple.asc')
Buck.set_values(value_dict)
Buck.save_simulation()
Buck.run()
Buck.pars()
print(Buck.namesOfVariables)
print(Buck.values)
Buck.remove_output()


