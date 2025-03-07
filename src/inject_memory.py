
from data_handler import read_jsonl, load_set, get_slot

PATH = "data/memory/memory_analysis_slot_"
data_format = ".jsonl"

def read_memory(path):
    '''
    Read the memory_analysis.jsonl file and return the data.

    Returns:
        list: A list of dictionaries.
    '''
    data = read_jsonl(path)
    return data

def filtering_jsonl(data):
    '''
    Filter the data from memory_analysis.jsonl file.

    Args:
        data (list): A list of dictionaries.

    Returns:
        list: A list of dictionaries.
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


def memory_prompt_forming() -> dict:
    global PATH, data_format
    '''
    Form the memory prompt.
    '''
    slot = get_slot()
    path = PATH + str(slot-1) + data_format
    memory_str = filtering_jsonl(read_memory(path))

    char = load_set(char=True)
    
    prompt_discripton = (
        f"The following text in '<memory>' is a collection of memories from {char}."
        "Is composed of the following categories: System Core, Dynamic High, Dynamic Low, and Temporary."
        "The System Core category contains the most important memories."
        "The Dynamic High and Dynamic Low categories contain memories that are important but not as important as the System Core category."
        "The Temporary category contains memories that are not important but are still worth remembering."
        "The memories are as follows:\n"
        f"<memory>\n{memory_str}\n</memory>\n"
        "The memory is coposed as follows in each line: title | description | dialogue\n"
    )

    format_promt = [{"role": "assistant", "content": prompt_discripton}]

    return memory_str