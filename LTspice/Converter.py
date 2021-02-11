import os
import logging

from .Circuit import Circuit

class ConverterData():
    PinAVG = None
    PoutRMS = None
    UinRMS = None
    IinRMS = None
    UoutRMS = None
    IoutRMS = None
    UinRippel = None
    IinRippel = None
    UoutRippel = None
    IoutRippel = None

    def __init__(self, name):
        self.name = name

    def getValues(self):
        return (self.efficiency_percent, self.IoutRippel * 1E+3, self.UoutRippel * 1E+3,
                self.IoutRMS, self.UoutRMS, self.IinRippel)

    @property
    def output_power(self):
        return self.PoutRMS

    @property
    def input_power(self):
        return self.PinAVG

    @property
    def efficiency(self):
        return self.output_power / self.input_power

    @property
    def efficiency_percent(self):
        return self.efficiency * 100.0

    def __str__(self):
        self.toPrint = 'Data printed from converter %s\n' % self.name
        self.toPrint += 'Efficiency = %3.2f%% \n' % self.efficiency_percent
        self.toPrint += 'Input Power = %3.2fW \n' % self.input_power
        self.toPrint += 'Output Power = %3.2fW \n' % self.output_power
        self.toPrint += '#############################\n'
        self.toPrint += 'Input Voltage RMS = %3.4fV \n' % self.UinRMS
        self.toPrint += 'Input Current RMS = %3.4fA \n' % self.IinRMS
        self.toPrint += 'Output Voltage RMS = %3.4fV \n' % self.UoutRMS
        self.toPrint += 'Output Current RMS = %3.4fA \n' % self.IoutRMS
        self.toPrint += 'Input Voltage Rippel = %.4fV \n' % self.UinRippel
        self.toPrint += 'Input Current Rippel = %.4fA \n' % self.IinRippel
        self.toPrint += 'Output Voltage Rippel = %.4fmV \n' % (self.UoutRippel * 1.0E+3)
        self.toPrint += 'Output Current Rippel = %.4fmA \n' % (self.IoutRippel * 1.0E+3)
        return self.toPrint


class ConverterSimulation(Circuit):
    def __init__(self, converter_dir, converter_file, data=None):
        super().__init__(directory=converter_dir, file_name=converter_file)
        if data is None:
            self.data = ConverterData(converter_file.split('.')[0])
        else:
            self.data = data

    def pars_log(self):
        self._log = open(os.path.normpath(
            self.simulation_dir + self.simulation_file.split('.')[0] + r'/' + self.simulation_file.split('.')[0] + r'.log'), encoding="ansi").read()
        self.__read_values()
        logging.info('pars finished!')

    def __read_values(self):
        self.__search_position()
        self.data.UinRMS = float(self._log[self.pos_uinrms:self._log.find('FROM', self.pos_uinrms)].split('=')[1])
        self.data.IinRMS = float(self._log[self.pos_iinrms:self._log.find('FROM', self.pos_iinrms)].split('=')[1])
        self.data.UoutRMS = float(self._log[self.pos_uoutrms:self._log.find('FROM', self.pos_uoutrms)].split('=')[1])
        self.data.IoutRMS = float(self._log[self.pos_ioutrms:self._log.find('FROM', self.pos_ioutrms)].split('=')[1])

        self.data.UinRippel = float(
            self._log[self.pos_uinrippel:self._log.find('FROM', self.pos_uinrippel)].split('=')[1])
        self.data.IinRippel = float(
            self._log[self.pos_iinrippel:self._log.find('FROM', self.pos_iinrippel)].split('=')[1])
        self.data.UoutRippel = float(
            self._log[self.pos_uoutrippel:self._log.find('FROM', self.pos_uoutrippel)].split('=')[1])
        self.data.IoutRippel = float(
            self._log[self.pos_ioutrippel:self._log.find('FROM', self.pos_ioutrippel)].split('=')[1])

        self.data.PoutRMS = float(self._log[self.pos_poutrms:self._log.find('FROM', self.pos_poutrms)].split('=')[1])
        self.data.PinAVG = float(self._log[self.pos_pinavg:self._log.find('FROM', self.pos_pinavg)].split('=')[1])

    def __search_position(self):
        self.pos_uinrms = self._log.find('uinrms')
        self.pos_iinrms = self._log.find('iinrms')
        self.pos_uoutrms = self._log.find('uoutrms')
        self.pos_ioutrms = self._log.find('ioutrms')

        self.pos_ioutrippel = self._log.find('ioutrippel')
        self.pos_uoutrippel = self._log.find('uoutrippel')
        self.pos_iinrippel = self._log.find('iinrippel')
        self.pos_uinrippel = self._log.find('uinrippel')

        self.pos_pinavg = self._log.find('pinavg')
        self.pos_poutrms = self._log.find('poutrms')

    def get_data(self):
        return self.data


class Converter(ConverterData):
    data = None
    _circuit = None

    def __init__(self, sim_dir, sim_file, value_list=None):
        super().__init__(sim_file.split('.')[0])
        self._circuit = ConverterSimulation(sim_dir, sim_file, data=self)
        if value_list is not None:
            self.set_values(value_list)

    def set_values(self, value_list):
        for name, value in value_list.items():
            self._circuit.set_value(name, value)

    def run(self,delete_simulation=True):
        self._circuit.save_simulation(directory = os.path.normpath(directory+self.simulation_file.split('.')[0]))
        try:
            self._circuit.run()
            self._circuit.pars_log()
            if delete_simulation:
                self._circuit.remove_output()
        except Exception as ex:
            if delete_simulation:
                self._circuit.remove_output()
            raise ex

    def delete_simulation(self):
        self._circuit.remove_output()
