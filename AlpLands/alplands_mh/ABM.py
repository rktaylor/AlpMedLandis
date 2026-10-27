# Where the ABMs go
import sys
import os
import subprocess
import shutil
from grass_controller import GrassController

startcmd = ["grass", "--config", "path"]
p = subprocess.Popen(startcmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()
if p.returncode != 0:
    raise Exception("GRASS not found. Ensure 'grass' is in your PATH.")
gisbase = out.decode().strip()
os.environ['GISBASE'] = gisbase
gpydir = os.path.join(gisbase, "etc", "python")
sys.path.append(gpydir)

import grass.script as gscript

def null_strategy(timestamp):
    pass
    # grass_scripts_dir = "/opt/conda/lib/grass85/scripts"
    # cfact_rules = "cfactor_recode_rules.txt"
    # if grass_scripts_dir not in os.environ.get('PATH', ''): os.environ['PATH'] = grass_scripts_dir + os.pathsep + os.environ['PATH']
    # # TODO make this happen in R
    # try:
    #     output = gscript.parse_command('r.recode', quiet = True, input = r"biomass-anpp-5.tif", output = "outcfact-{}".format(timestamp), rules = cfact_rules)
    #     return output
    # except Exception as e:
    #     print("🏁🏁🏁: {}".format(e))
    

# TODO - biomass-succession\biomass-anpp uses windows backslash, find that and replace with proper route.