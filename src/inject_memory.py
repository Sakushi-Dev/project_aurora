from globals import MEM_DIR
from data_handler import read_file, get_slot

PATH = MEM_DIR/"memory_analysis_slot_"
SUFFIX = ".jsonl"

def filtering_jsonl(data) -> str:
    '''
    Filter the data from memory_analysis_slot_(x).jsonl file.
    '''
    c_map = [
        "title",
        "description",
        "dialogue"
    ]

    memory_str = ""

    for entry in data:
        memory_str += f"{entry[c_map[0]]} | {entry[c_map[1]]} | {entry[c_map[2]]}\n"

    return memory_str


def memory_prompt_forming() -> str:
    global PATH, SUFFIX
    '''
    Merge the memory data into a string.
    '''

# NOTE: This function is called in 'response_manager.py' and permanently stores the data in the instance of 'PromptBuilder',
# where it is structured into an api_prompt. Subsequently, the class method 'get_reminder_api()' is called to generate the final prompt

    slot = get_slot()
    path = PATH / str(slot-1) + SUFFIX
    memory_str = filtering_jsonl(read_file(path))
    
    prompt_description = (
f"""
The System Core category contains the most important memories.
The Dynamic High and Dynamic Low categories contain memories that are important but not as important as the System Core category.
The Temporary category contains memories that are not important but are still worth remembering.
The memories are as follows:\n
<reminder>\n{memory_str}\n</reminder>\n
The (<reminder>) is composed as follows in each line: title | description | dialogue\n
"""
    )

    return prompt_description
