# -*- coding: utf-8 -*-

# TODO imports require container rebuild
import sys
import os
#import subprocess
#import shutil
from grass_controller import GrassController
#import pandas as pd
#import rpy2.robjects as robjects
#from rpy2.robjects import pandas2ri

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
LOCATION = "cascadia" # TODO - make container build have this, it's just patched in rn

# os.chdir(r"D:\OneDrive -UQAM\OneDrive - UQAM\1 - Projets\Thèse - Chapitre 3\2_Projet_extension_REHARVEST\Examples")

pp("Python script : Running MagicHarvest::AlpineLakesOrchestrator !")
pp("HELLO FROM CLE ELUM! The time is {}".format(timestep))

if int(timestep) == 10:
    pp("Conditional logic check. Now attempting to invoke GRASS")
    gis = GrassController(GISDB, LOCATION)
    gis.test()


