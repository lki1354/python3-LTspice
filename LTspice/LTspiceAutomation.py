import os
import shutil
import logging


LTSPICE_FLAG_RUN = '-Run -b'
LTSPICE_FLAG_RUN_ASCII_OUT = '-ascii -Run -b '
LTSPICE_PROGRAM = 'C:/Program Files/LTC/LTspiceXVII/XVIIx64.exe'


def run_simulation(sim_dir,sim_file,ltspice=LTSPICE_PROGRAM , ltspice_flags=LTSPICE_FLAG_RUN):
    logging.info('Simulation Started!')
    logging.info(os.path.dirname(os.path.realpath(__file__)))
    cp_sim = os.path.normpath(sim_dir+sim_file.split('.')[0])
    os.makedirs(cp_sim)
    shutil.move(os.path.normpath(sim_dir+sim_file),cp_sim)
    run_cmd = 'call "'+os.path.normpath(ltspice)+'" '+ltspice_flags+' "'+os.path.normpath(cp_sim+r'/'+sim_file)+'"'
    logging.info(run_cmd)
    os.system(run_cmd)
    logging.info('Simulation finished!')

def delete_simulation(sim_dir,sim_file):
    shutil.rmtree(sim_dir + sim_file.split('.')[0], ignore_errors=False, onerror=None)
