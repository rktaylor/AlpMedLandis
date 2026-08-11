from grass_session import Session
import json
import re
from collections import defaultdict

# these are the default paths for a conda installation
DEFAULT_GISDB = "/opt/conda/grass84"
DEFAULT_LOCATION = "demolocation"

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


class ConfigParser:
    """
    This class provides methods for parsing GIS configurations.
    """

    def __init__(self):
        pass



class JsonConfig:
    def __init__(self):
        pass

    @classmethod
    def from_gis_python_header(cls, input_text):
        pass

def parse_text_to_nested_json(input_text, output_json_path):
    """
    Converts a configuration text (with sections and #%option blocks) into a nested JSON.
    
    :param input_text: String containing the full input text (or read from file)
    :param output_json_path: Path to save the resulting JSON file
    """
    # Split the text into lines
    lines = input_text.strip().splitlines()
    
    # Store final result
    result = {}
    current_section = None
    current_option = None
    option_stack = []  # Stack to handle multi-line values if needed (not used here)

    for line in lines:
        line = line.strip()
        
        # Detect section header: lines between ####... containing text
        if line.startswith("###################"):
            continue  # Skip the delimiter lines
        if line.startswith("#") and not line.startswith("#%"):
            # This is a candidate for a section header
            header_match = re.match(r"#\s*(.+)", line)
            if header_match:
                current_section = header_match.group(1).strip()
                result[current_section] = []
            continue
        
        # Handle #%option blocks
        if line == "#%option":
            current_option = {}
            continue
        
        if line == "#%END" and current_option is not None and current_section:
            result[current_section].append(current_option)
            current_option = None
            continue
        
        # Parse key-value pairs like: #% key: value
        if line.startswith("#% ") and current_option is not None:
            # Split only on the first colon
            part = line[3:]  # Remove '#% '
            if ':' in part:
                key, value = part.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                # Type conversion where possible
                if value.lower() == 'yes':
                    value = True
                elif value.lower() == 'no':
                    value = False
                elif re.fullmatch(r'-?\d+\.?\d*', value):  # Simple number detection
                    value = float(value) if '.' in value else int(value)
                elif ',' in value and all(v.strip().lstrip('-').replace('.','').isdigit() for v in value.split(',')):
                    # Handle comma-separated numbers (e.g., "3,2")
                    try:
                        value = [float(v.strip()) if '.' in v else int(v.strip()) for v in value.split(',')]
                    except:
                        pass  # fallback to string

                current_option[key] = value

    # Write to JSON file
    # with open(output_json_path, 'w', encoding='utf-8') as f:
    #     json.dump(result, f, indent=4, ensure_ascii=False)
    
    # print(f"Nested JSON saved to {output_json_path}")

def from_file(path):
    with open("agropastsemi_raw.conf", "r") as file:
        input_data = file.read()
    #parse_text_to_nested_json(input_data, "brave2.json")