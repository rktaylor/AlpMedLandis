import os
import sys
import subprocess

# 1. Get the GRASS installation path dynamically
startcmd = ["grass", "--config", "path"]
p = subprocess.Popen(startcmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()

if p.returncode != 0:
    raise Exception("GRASS not found. Ensure 'grass' is in your PATH.")

gisbase = out.decode().strip()

# 2. Set GISBASE environment variable
os.environ['GISBASE'] = gisbase

# 3. Add GRASS Python library to sys.path
gpydir = os.path.join(gisbase, "etc", "python")
sys.path.append(gpydir)

# 4. Now you can import
import grass.script as gscript
print(gscript.__version__)    