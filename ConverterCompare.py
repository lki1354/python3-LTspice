#! python3
# coding: utf-8

from LTspice.Converter import Converter
from LTspice.DisplayData import displayResults

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
Rload = Uout / Iout

Buck = Converter(simulation_dir,'BuckVariable.asc',{'L1_v':L1,'Cout_v':Cout,'Uin_v':Uin,'Rload_v':Rload,'Tperiode_v':T,'Ton_v':(T*Uout/Uin)})
BuckLowFET = Converter(simulation_dir,'BuckLowFetVariable.asc',{'L1_v':L1,'Cout_v':Cout,'Uin_v':Uin,'Rload_v':Rload,'Tperiode_v':T,'Ton_v':(T*Uout/Uin)})
Sepic = Converter(simulation_dir,'SepicVariable.asc',{'L1_v':L1,'L2_v':L2,'CC_v':CC,'Cout_v':Cout,'Uin_v':Uin,'Rload_v':Rload,'Tperiode_v':T,'Ton_v':(T*Uout/(Uout+Uin))})
BuckBoost = Converter(simulation_dir,'BuckBoostVariable.asc',{'L1_v':L1,'Cout_v':Cout,'Uin_v':Uin,'Rload_v':Rload,'Tperiode_v':T,'Ton_v':(T*Uout/(Uout+Uin))})
Cuk = Converter(simulation_dir,'CukVariable.asc',{'L1_v':L1,'L2_v':L2,'CC_v':CC,'Cout_v':Cout,'Uin_v':Uin,'Rload_v':Rload,'Tperiode_v':T,'Ton_v':(T*Uout/(Uout+Uin)) })
Buck.run()
BuckLowFET.run()
Sepic.run()
BuckBoost.run()
Cuk.run()

displayResults([Buck,BuckLowFET,Sepic,BuckBoost,Cuk])