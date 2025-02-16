import os

from data_handler import (
    write_json,
    cost_path,
    slot_path,
    last_msg_time_path,
    emo_score_path,
    set_path,
    user_name_path
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
                "total_input_cost": 0.0,
                "total_output_cost": 0.0
            }
        })
    os.makedirs(dir_path, exist_ok=True)
    write_json(full_path, costs)


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

def init_emo_scores():
    dir_path, full_path = spit_path(emo_score_path)
    os.makedirs(dir_path, exist_ok=True)
    data = {}
    for i in range(0, 5):
        data.update({
            f"slot_{i}": {
                "Angry_Level": 0,
                "Sad_Level": 0,
                "Affection_Level": 0,
                "Arousal_Level": 0,
                "Trust_Level": 0
            }
        })
    write_json(full_path, data)

def init_set():
    # Create set with standard values
    route = {
        "set_char": {"set_char": "Mia"},
        "set_color": {"color_choice": ""},
        "set_freq": {"set_freq": 2},
        "set_imp": {"set_imp": "off"},
        "set_max_t": {"max_token": 4096},
        "set_slot": {"set_slot": 1},
        "set_time_sense": {"time_sense": False}
    }

    os.makedirs(set_path, exist_ok=True)

    for key in route:
        write_json(set_path + f"/{key}.json", route[key])

def init_user_spec():
    dir_path, full_path = spit_path(user_name_path)
    os.makedirs(dir_path, exist_ok=True)
    write_json(full_path)

def init_data():
    init_costs()
    init_history_slots()
    init_last_msg_time()
    init_emo_scores()
    init_set()
    init_user_spec()