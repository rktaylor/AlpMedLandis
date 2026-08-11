from grass_session import Session
import json
import re
from collections import defaultdict

# these are the default paths for a conda installation
DEFAULT_GISDB = "/opt/conda/lib/grass85"
DEFAULT_LOCATION = "cascadia"


class GrassController:
    """
    This is a lightweight wrapper around Grass GIS Python.
    The purpose is to expose core functionality that's oft-repeated
    in an easily re-usable, testable way.
    """
    def __init__(self, db: str, loc: str, maps: str = None):
        """
        db (str): Grass Database location (usually /opt/conda/grass)
        loc (str): The name of the location data-set for Grass
        maps (str): The mapset Grass will load from `loc`. 
            If `None`, defaults to `PERMANENT` (Grass behavior)
        """
        self.__GISDB = db
        self.__LOCATION = loc
        self.__MAPSET = maps
        self.sesh = Session()
        self.sesh.open(gisdb=db, location=loc, mapset=maps)
        # As of Grass 8.x, the scripting library/client cannot be
        # imported without first configuring environment variables
        # that Grass uses in the backend for execution. These are
        # set in the line above and managed in the Session object.
        import grass.script as grass
        self.grass_client = grass

    @classmethod
    def default(cls):
        return cls(db=DEFAULT_GISDB, loc=DEFAULT_LOCATION)

    def __del__(self):
        """
        Kills the helper, cleans up retained resources, closes Grass.
        """
        self.sesh.close()

    def test(self):
        """
        Creates a GrassController and uses it to run a command
        that should always resolve. Asserts the output is not empty.
        If Grass throws an error, this test will fail (that's a good thing).
        """
        # arrange
        grass = self.grass_client

        # act and assert
        try:
            result = grass.parse_command('g.region', flags='p')
            print("Succeeded: {}".format(result))
        except e:
            print("Errored: {}".format(e))