from rich.console import Console
console = Console(width=120)

#==================================================================================================

from jinja2 import Environment

jinja_env = Environment(
            variable_start_string='{',
            variable_end_string='}'
        )

#==================================================================================================

from pathlib import Path

class PathManager:
    def path(self):
        return self.base_dir

    def __init__(self, base_dir):
        self.base_dir = base_dir

    def __getattr__(self, name):
        return PathManager(self.base_dir / name).path()

    def __getitem__(self, name):
        return (self.base_dir / name)
    
    

manager         = PathManager(Path("."))
manage_data     = PathManager(Path(manager.data))
manage_prompts  = PathManager(Path(manager.prompts))
manage_char_spec= PathManager(Path(manage_prompts.char_spec))

DATA_DIR        = manager.data
PROMPTS_DIR     = manager.prompts
SET_DIR         = manage_data.set
HIST_DIR        = manage_data.history
MEM_DIR         = manage_data.memory
COST_DIR        = manage_data.costs
MOOD_DIR        = manage_data.mood
L_MSG_DIR       = manage_data.last_msg_time
UTILITY_DIR     = manage_prompts.utility
MEM_P_DIR       = manage_prompts.memory
USER_SPEC_DIR   = manage_prompts.user_spec
CHAR_SPEC_DIR   = manage_prompts.char_spec
MIA_SPEC_DIR    = manage_char_spec.mia_desc
YU_JUN_SPEC_DIR  = manage_char_spec.yujun_desc

CACHE_L_DIR     = [
    PathManager(Path("./src"))["__pycache__"],
    PathManager(Path("./src/cmd_operations"))["__pycache__"]
    ]

# Set paths
char_file          = SET_DIR/"set_char.json"
color_file         = SET_DIR/"set_color.json"
freq_file          = SET_DIR/"set_freq.json"
imp_file           = SET_DIR/"set_imp.json"
max_t_file         = SET_DIR/"set_max_t.json"
time_sense_file    = SET_DIR/"set_time_sense.json"
slot_file          = SET_DIR/"set_slot.json"

# Mood data paths
emo_score_file     = MOOD_DIR/"emotion_score.json"
emo_trigger_file   = MOOD_DIR/"emotion_trigger.json"
score_trigger_file = MOOD_DIR/"score_trigger.json"
imp_prompt_file    = MOOD_DIR/"impatience_prompt.json"
mood_sys_file      = MOOD_DIR/"mood_sys_p.json"

# Cost and last message time paths
costs_file         = COST_DIR/"slot_costs.json"
last_msg_time_file = L_MSG_DIR/"last_msg_time.json"

# Prompt paths
user_name_file     = USER_SPEC_DIR/"user_name.json"
user_gender_file   = USER_SPEC_DIR/"user_gender.json"
user_language_file = USER_SPEC_DIR/"user_language.json"

# Character name paths
mia_name_file      = CHAR_SPEC_DIR/"char_name.json"
yujun_name_file    = CHAR_SPEC_DIR/"char_name.json"


FOLDER = {
	key.replace("_DIR", "").lower(): value
	for key, value in locals().items()
	if key.endswith("_DIR")
}
FILE = {
    key.replace("_file", ""): value
	for key, value in locals().items()
	if key.endswith("_file")
}

def get_path(path:str):
    return FOLDER[path]
def get_file(file:str):
    return FILE[file]

# NOTE: Significant attributes of the Path object
'''
print(FOLDER["data"])                   # Output: './data' 
print(FILE["char"])                     # Output: './data/set/set_char.json'
print(FILE["char"].name)                # Output: 'slot_costs.json'
print(FILE["char"].parent)              # Output: './data/costs'
print(FILE["char"].parent.name)         # Output: 'costs'
print(FILE["char"].parent.parent)       # Output: './data'
print(FILE["char"].parent.parent.name)  # Output: 'data'
print(FILE["char"].exists())            # Output: True or False
print(FILE["char"].is_dir())            # Output: False
print(FILE["char"].is_file())           # Output: True
print(FILE["char"].resolve())           # Output: '/workspaces/project_aurora/data/set/set_char.json'
print(FILE["char"].stem)                # Output: 'slot_costs'
print(FILE["char"].suffix)              # Output: '.json'`

# file in folder
for file in FOLDER["mood"].iterdir():   # Iterates over all files in the mood folder
    print(file)

'''
#==================================================================================================