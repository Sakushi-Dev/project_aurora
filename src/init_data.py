import os

from data_handler import (
    write_json,
    cost_path,
    slot_path,
    last_msg_time_path
)

def spit_path(path):
    split_path = path.split("/")
    relative_path = split_path.pop(0)
    dir_path = relative_path
    # Dir path is the path without the file name
    for i in range(0, len(split_path)-1):
        dir_path += "/" + split_path[i]
    full_path = path


    return dir_path, full_path

def init_costs():
    dir_path, full_path = spit_path(cost_path)

    costs = {}
    for i in range(0, 5):
        costs.update({
            f"slot_{i}": {
                "total_input_costs": 0.0,
                "total_output_cost": 0.0
            }
        })
    os.makedirs(dir_path, exist_ok=True)
    write_json(full_path, costs)

init_costs()

def init_history_slots():
    
    os.makedirs(slot_path, exist_ok=True)
    # Create empty history slots
    for i in range(0, 5):
        write_json(f"{slot_path}/slot_{i}.json")

def init_last_msg_time():
    dir_path, full_path = spit_path(last_msg_time_path)
    os.makedirs(dir_path, exist_ok=True)
    data = {}
    for i in range(0, 5):
        data.update({
            f"slot_{i}": {
                "last_msg_time": ""
            }
        })
    write_json(full_path, data)

init_last_msg_time()
