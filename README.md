# python3-LTspice
a tool to use LTspice from python

To run the example you have to move the "SimulationBuck.py" from the Example folder to the top. (where the LTspice folder with the python files located)

The actual version is for Windows and tested on Windows 10 with LTspiceXVII. To change the LTspice version or the executable directory you have to do this in the "LTspice\run_LTspice.cmd" file.

# Introduction
This document is meant to guide the user on how to work with the Python module python3-LTspice which provide set variables in the schematic and run LTspice from Python. After simulation is finished, it is possible to extract data from the log file or raw file.

## Deeded Tools
The programs used are Python and LTspice.
For the latest version of LTspice
*	http://www.linear.com/designtools/software/#LTspice 
Python 3.6.2 Version or higher is needed:
*	https://www.python.org/downloads/
*	For plotting data two libraries are needed:
*	Matplotlib
*	Run following command in the command windnow (cmd):
python -m pip install matplotlib

## Tools Versionw
The scripts were tested by usage and worked in the following versions: 
*	Python 3.6.2 
*	LTspice XVII(x64) Sep 14 2017

# Workflow For Given Example

## Steady-state analysis of one Converter

### LTspice Part
First you have to build a schematic (for this example see Figure 2.1) in LTspice with a transient analysis of the desired stop time or a representing variable name with curly braces (such as {stop_time}). For a steady state analyse you have to now when the simulation reach the steady state point and how long the simulation has to be.You have to set up measurements in LTspice, for example .meas TRAN IoutRMS RMS I(Rload) FROM 2ms TO 10ms. The Converter class pars automatically the log-File after the simulation is finish and expect following variables:
*	UinRMS
*	IinRMS
*	UoutRMS
*	IoutRMS
*	IoutRippel 
*	UoutRippel 
*	IinRippel 
*	UinRippel
*	PoutRMS
*	PinAVG
These variable names are defined in the function __search_position which is defined in the class ConverterSimulation. In the LTspice schematic (*.asc) all these variables has to be define in a measurement (.meas) otherwise an error will occur. The example schematic file BuckVariable.asc in the example folder can be used as a template.

### Python Part:
SimulationBuck.py has to be in the same directory where the LTspice module with the python files.

### directory path to run:

* SimualtionBuck.py
* LTspice
  * BuckVariable.asc
* Example
  * __init__.py
  * Circuits.py
  * DisplayData.py
  * LTspiceAutomation.py
  * run_LTspice.cmd


### notes
* http://cds.linear.com/docs/en/software-and-simulation/LTspice_ShortcutFlyerC.pdf
