from .LTspiceAutomation import ConverterSimulation,LTSpice, ConverterData
   
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

    def __init__(self,sim_dir,sim_file, value_list = None):
        super().__init__(sim_file.split('.')[0] ) 
        self.__circuit = ConverterSimulation(sim_dir,sim_file,data = self)
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
        sim = LTSpice(sim_dir=self.__circuit.new_simulation[1], sim_file=self.__circuit.new_simulation[0])
        sim.run_simulation()
        self.__circuit.pars_log()
        return sim
        

