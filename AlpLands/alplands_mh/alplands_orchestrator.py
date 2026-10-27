# -*- coding: utf-8 -*-

# TODO imports require container rebuild
import sys
import os
#import subprocess
#import shutil
from grass_controller import GrassController
import ABM
#import pandas as pd
import rpy2.robjects as robjects
#from rpy2.robjects import pandas2ri

from rpy2.robjects import r



# Set R's working directory
r('setwd("/Medlands/Landis-Docker/AlpLands/alplands_mh/")')

timestep = sys.argv[1]

## Grass Notes:
"""
Grass will invoke landscape.evol.
That means Grass needs to begin with a correct location. 

initial communities is the map he was looking at.
eco_regions_fake is the template file we use for creating a grass location.

We don't NEED to delete the old maps, but each time the Orchestrator calls .
Might could be safe to do it. 

Landis -> Orchestrator: Run with current maps
Orchestrator -> ABMs: Run agent models
ABMs -> Orchestrator: Updated maps
Orchestrator -> Orchestrator: Check if it's time to run landscape evol
Orchestrator -> Grass Controller: Update map set with current timestamps
Orchestrator -> Grass Controller: invoke landscape.evol
Grass Controller -> Orchestrator: Synchronous blocker, return success/fail
Orchestrator -> Landis: Return control to Landis

"""
def pp(text):
    print("🏞️🔥🫐: {}".format(text))


# TODO - change these to the new one
GISDB = "/opt/conda/lib/grass85" # run "grass --config path" from container
LOCATION = "cascadia" # TODO - make container build have this, it's just patched in rn [line 534, verify it]

# os.chdir(r"D:\OneDrive -UQAM\OneDrive - UQAM\1 - Projets\Thèse - Chapitre 3\2_Projet_extension_REHARVEST\Examples")

pp("Python script : Running MagicHarvest::AlpineLakesOrchestrator !")
pp("HELLO FROM CLE ELUM! The time is {}".format(timestep))

if int(timestep) == 10:
    pp("Conditional logic check. Now attempting to invoke GRASS")
    gis = GrassController(GISDB, LOCATION)
    gis.test()

if int(timestep) == 10:
    pp("Calling landscape evol...")
    import find_grass as F
    # TODO - See note at end
    status_code = 0# F.run_landscape_evol(str(timestep))
    sc = ""
    if status_code == 0:
        sc += "---✅️"
    else:
        sc += "---❌️"
    pp("{}: {}".format(sc, status_code))

if int(timestep) == 10:
    #ABM.null_strategy(timestep)
    # Get R's current working directory
    current_r_dir = r("getwd()")[0]
    print("🏁🏁🏁🏁🏁🏁🏁🏁🏁")
    print("R's current working directory:", current_r_dir)
    print("🏁🏁🏁🏁🏁🏁🏁🏁🏁")

if int(timestep) == 20:
    files = os.listdir('.')
    print("🏁🏁🏁: {}",files)
    robjects.r.source("NEW_AND_IMPROVED.R")
    r_function = robjects.globalenv["converter"]
    result = r_function(
        "/Medlands/Landis-Docker/AlpLands/alplands_mh/ecoregions_fake_UTM_100.tif",
        "/Medlands/Landis-Docker/AlpLands/alplands_mh/biomass.anpp-5.tif",
        "/Medlands/Landis-Docker/AlpLands/alplands_mh/landis-out-20.tif",
        "/Medlands/Landis-Docker/AlpLands/alplands_mh/medlands-out-20.tif",
        "/Medlands/Landis-Docker/AlpLands/alplands_mh/cfact-20.tif"
    )

"""
(base) root@eea810d5b2d2:/Medlands/Landis-Docker/AlpLands/alplands_mh# history | grep land
    1  cd /Medlands/
    6  cd alplands_mh/
   33  grass -t "/opt/conda/lib/grass85/cascadia" -c "g.extension extension=r.landscape.evol operation=add"
   34  grass "/opt/conda/lib/grass85/cascadia" -c "g.extension extension=r.landscape.evol operation=add"
   35  grass /opt/conda/lib/grass85/cascadia -c "g.extension extension=r.landscape.evol operation=add"
   36  grass /opt/conda/lib/grass85/cascadia/PERMANENT -c "g.extension extension=r.landscape.evol operation=add"
   37  grass /opt/conda/lib/grass85/cascadia/PERMANENT "g.extension extension=r.landscape.evol operation=add"
   38  grass /opt/conda/lib/grass85/cascadia/PERMANENT --exec "g.extension extension=r.landscape.evol operation=add"
   39  grass /opt/conda/lib/grass85/cascadia/PERMANENT --exec g.extension extension=r.landscape.evol operation=add
   44  chmod +x r.landscape.evol
   64  history | grep land

"""

# TODO - change initial communities file

