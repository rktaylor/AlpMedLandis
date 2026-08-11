import os
import sys
import subprocess

# Robot code -- tested working -- for configuring grass.script before import.
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

from datetime import datetime

# Get current time as integer seconds
nownow = str(int(datetime.now().timestamp()))


# TODO - how do we feedback Landscape Evol's changing landscape to the ecosystem communities?
# TODO - and what map is mutating on the way in? Vegetation, surely? But what parameter is that?
# TODO - the second tab in landscape.evol has "c-factor" for vegetation
# TODO - Manning's N needs tuning.
def run_landscape_evol(input_stem):
    print("⏰️⏰️⏰️: {}".format(input_stem))
    # Have a folder that's based on nownow, that's how we get distinct. 
    # We'll have to handle the upstream knowing what nownow is...
    op = "grassout{}".format(nownow)
    print(op)
    #setup_landscape_evol(None)
    status_code = gscript.run_command(
        '/Medlands/Landis-Docker/AlpLands/alplands_mh/r.landscape.evol',
        elev="elevation@PERMANENT",
        initbdrk="bedrock@PERMANENT",
        outdem=op+"_dem",
        outsoil=op+"_soil",
        prefx=op,
    )
    return status_code

# def setup_landscape_evol(script_path):
#     # TODO replace this with logic to find and import local file
#     gscript.run_command(
#         "g.extension",
#         extension="r.landscape.evol",
#         operation="add"
#         )

def setup_landscape_evol():
    grass_scripts_dir = "/opt/conda/lib/grass85/scripts"
    if grass_scripts_dir not in os.environ.get('PATH', ''): os.environ['PATH'] = grass_scripts_dir + os.pathsep + os.environ['PATH']
    gscript.run_command('g.extension', extension='r.landscape.evol', operation='add')
    
