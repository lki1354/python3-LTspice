import os
import logging


LTSPICE_FLAG_RUN = '-Run '
LTSPICE_FLAG_BATCH_RUN = '-Run -b '
LTSPICE_FLAG_RUN_ASCII_OUT = '-ascii -Run '
LTSPICE_FLAG_BATCH_RUN_ASCII_OUT = '-ascii -Run -b '
LTSPICE_PROGRAM = 'C:/Program Files/LTC/LTspiceXVII/XVIIx64.exe'


def run_simulation(sim_dir,sim_file,ltspice_flags,ltspice=LTSPICE_PROGRAM):
    logging.info(os.path.dirname(os.path.realpath(__file__)))
    run_cmd = 'call "'+os.path.normpath(ltspice)+'" '+ltspice_flags+' "'+os.path.normpath(sim_dir+r'/'+sim_file)+'"'
    logging.info(run_cmd)
    os.system(run_cmd)
    logging.info('Simulation finished!')

