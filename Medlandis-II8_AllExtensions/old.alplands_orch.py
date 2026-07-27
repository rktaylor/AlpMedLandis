import sys
import os
import subprocess
import shutil
from grass_helpers import GrassController

grass_binary = "/opt/conda/bin/grass"
grass_database = "/Medlands/grass84"
location_name = "landis_mh"
mapset = "PERMANENT"
location_path = os.path.join(grass_database, location_name)
mapset_path = os.path.join(location_path, mapset)

def initialize_grass(initial_tiff_path):
    # clean prior runs
    if os.path.exists(location_path):
        shutil.rmtree(location_path)

    os.makedirs(grass_database)

    # grass -c /path/to/tiff -e 
    create_cmd = [
        "grass",
        "-c",
        initial_tiff_path,
        "-e",
        location_path
    ]
    subprocess.run(create_cmd, check=True)

    # grass /path/to/mapset --exec r.in.gdal -o input=path/to/tiff output=internal_name --overwrite
    import_cmd = [
        "grass",
        mapset_path,
        "--exec",
        "r.in.gdal",
        "-o",
        "input={}".format(initial_tiff_path),
        "output=test_0", # this needs to be dynamic
    ]
    subprocess.run(import_cmd, check=True)

    return

# -- Begin Script -- #

# Get the current timestep passed from Magic Harvest
current_timestep = sys.argv[1]

# TODO - this if cancels out the one above when initialization runs
if not os.path.exists(location_path):
    # TODO - get the most recent tif
    initial_tiff = "/Medlands/data/alpine_watersheds_cropped.tiff"
    #initial_tiff = r"/Medlands/data/MagicHarvest/biomass-succession\biomass-anpp-5.tif"
    initialize_grass(initial_tiff)
else:
    # TODO - add most recent map into the location
    C = 2.5
    # gs.mapcalc(
    #     "output_raster = input_raster * {}", 
    #     C, 
    #     input_raster="test_0", 
    #     output_raster="elev_scaled"
    # )   

grass_sesh = GrassController(
    db=grass_database,
    loc=location_name,
)
grass = grass_sesh.grass_client

def latest_name():
    data_name = "landis_t{}".format(current_timestep)
    return data_name

def import_latest():
    rawpath = r"/Medlands/data/MagicHarvest/biomass-succession\biomass-anpp-5.tif"
    tiff_path = rawpath[:60] + str(current_timestep) + ".tif"
    data_name = latest_name()
    import_cmd = [
        "grass",
        mapset_path,
        "--exec",
        "r.in.gdal",
        "-o",
        "input={}".format(tiff_path),
        "output={}".format(data_name), # this needs to be dynamic
    ]
    subprocess.run(import_cmd, check=True)

output = grass.parse_command('g.region', flags='p')

import_latest()
_ = grass.mapcalc("test = {}@PERMANENT + {}@PERMANENT".format(latest_name(), latest_name()))


# Example Logic: Modify a harvest parameter file based on the year
# You would typically read a .txt file, change values, and save it.
# For testing, we just verify the file write capability.
with open("medlands_log.txt", "a") as f:
    f.write(f"Parameters updated at year {current_timestep}\n")   
    f.write(str(output))
    f.write(str(_))