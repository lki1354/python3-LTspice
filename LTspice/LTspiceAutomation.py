import os
import shutil

LTSPICE_FLAG_RUN = '-Run -b'
LTSPICE_FLAG_RUN_ASCII_OUT = '-ascii -Run -b '
LTSPICE_PROGRAM = 'C:/Program Files/LTC/LTspiceXVII/XVIIx64.exe'

#,sim_script = '"'+os.path.dirname(os.path.realpath(__file__))+'\\run_LTspice.cmd"'
def run_simulation(sim_dir,sim_file,ltspice=LTSPICE_PROGRAM , ltspice_flags=LTSPICE_FLAG_RUN):
    print(os.path.dirname(os.path.realpath(__file__)))
    cp_sim = os.path.normpath(sim_dir+sim_file.split('.')[0])
    os.makedirs(cp_sim)
    shutil.move(os.path.normpath(sim_dir+sim_file),cp_sim)
    #run_cmd ='& "C:\Program Files\LTC\LTspiceXVII\XVIIx64.exe" -Run -b "'+os.path.normpath(cp_sim+'/'+self.sim_file)+'"'
    #run_cmd = sim_script+' "'+os.path.normpath(cp_sim+'\\'+sim_file)+'"'
    run_cmd = 'call "'+os.path.normpath(ltspice)+'" '+ltspice_flags+' "'+os.path.normpath(cp_sim+r'/'+sim_file)+'"'
    print(run_cmd)
    os.system(run_cmd)
    print('Simulation finished!')

def delete_simulation(sim_dir,sim_file):
    shutil.rmtree(sim_dir + sim_file.split('.')[0], ignore_errors=False, onerror=None)
