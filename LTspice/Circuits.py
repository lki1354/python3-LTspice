#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from LTspiceAutomation import ConverterSimulation,LTSpice, ConverterData

from IPython.display import Markdown,Latex, display
def printmd(string):
    display(Markdown(string))


def displayEfficiencies(toShow):
    table = '| Konverter Type | Effizienz [%] |\n'
    table += '| --- | --- | \n'
    for name , converter in toShow.items():
        table += '|'+name+'| %3.2f | \n'%converter.efficiency_percent
    printmd(table)

def displayResults(toShow):
    table = '| Konverter Type | Effizienz [%] |dIout [mA] |dUout [mV]|Iout [A] |Uout [V]|dIin [A] |\n'
    table += '| --- | --- | --- | --- | --- | --- | \n'
    for converter in toShow:
        table += '|'+converter.name+'|%3.0f | %3.2f | %3.2f| %.3f |%.3f| %.3f |  \n'%converter.getValues()
    printmd(table)
    
def displayResultsTEX(toShow):
    table = 'Konverter Type & Eff. [\%] & dIout [mA] &dUout [mV]&Iout [A] &Uout [V]&dIin [A] \\\\ \hline \n'
    for converter in toShow:
        table += ''+converter.name+'& %3.2f & %3.2f & %3.2f & %.3f & %.3f & %.3f \\\\ \n'%converter.getValues()
    #display(Latex(table.replace('.',',')))
    print(table.replace('.',','))
    
    
class Converter(ConverterData):
    data = None
    __circuit = None
    control = None
    #eff
    components = None
    amount_L = 0
    amount_C = 0
    amount_Cp = 0
    amount_FET = 0
    amount_Diode = 0
    cost = 0
    modularisation = 0

    def __init__(self,sim_file,sim_dir, value_list = None):
        super().__init__(sim_file.split('.')[0] ) 
        self.__circuit = ConverterSimulation(sim_file,sim_dir)
        if value_list is not None:
            self.set_values(value_list)
    def calculate_cost(self,component_costs):
        self.cost += component_costs['L']*self.amount_L
        self.cost += component_costs['C']*self.amount_C
        self.cost += component_costs['Cp']*self.amount_Cp
        self.cost += component_costs['FET']*self.amount_FET
        self.cost += component_costs['Diode']*self.amount_Diode
      
      
    
    def set_values(self,value_list):
        for name , value in value_list.items():
            self.__circuit.set_value(name+'_v',value)
    def run(self):
        self.__circuit.save_simulation()
        sim = LTSpice(sim_file=self.__circuit.new_simulation[0], sim_dir=self.__circuit.new_simulation[1],data = self)
        sim.run_simulation()
        sim.pars_log()
        #self.__circuit.remove_new_simulation()
        return sim
        

