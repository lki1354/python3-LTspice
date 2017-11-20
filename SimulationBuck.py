# coding: utf-8

from LTspice.Converter import Converter

#simulation_dir = 'C:\\Users\\Lukas Kiechle\\Documents\\GitHub\\python3-LTspice\\Examples'
simulation_dir = '\\Examples'


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
Rload

Buck = Converter(simulation_dir,'BuckVariable.asc',{'L1':L1,'Cout':Cout,'Uin':Uin,'Rload':Rload,'Tperiode':T,'Ton':(T*Uout/Uin)})
Buck.run(delete_simulation=True)
print(Buck)


