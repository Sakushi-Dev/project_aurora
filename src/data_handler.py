import json
import yaml
from pathlib import Path
from globals import FOLDER, FILE


# Einstellungen
set_path                = "./data/set"
set_char_path           = "./data/set/set_char.json"
set_color_path          = "./data/set/set_color.json"
set_freq_path           = "./data/set/set_freq.json"
set_imp_path            = "./data/set/set_imp.json"
set_max_t_path          = "./data/set/set_max_t.json"
set_time_sense_path     = "./data/set/set_time_sense.json"
set_slot                = "./data/set/set_slot.json"

# Daten zur emotionsbasierten Textgenerierung
emo_score_path          = "./data/mood/emotion_score.json"
emo_trigger_path        = "./data/mood/emotion_trigger.json"
score_trigger_path      = "./data/mood/score_trigger.json"
imp_prompt_path         = "./data/mood/impatience_prompt.json"
mood_sys_p              = "./data/mood/mood_sys_p.json"

# Dialog Slots
slot_path               = "./data/history"
char_memory_path        = "./data/memory"
cost_path               = "./data/costs/slot_costs.json"
last_msg_time_path      = "./data/last_msg_time/time.json"

# Prompt Pfade für User-Namen und Char-Namen
user_name_path          = "./prompts/user_spec/user_name.json"
user_gender_path        = "./prompts/user_spec/user_gender.json"
user_language_path      = "./prompts/user_spec/user_language.json"
mia_name_path           = "./prompts/char_spec/mia_desc/char_name.json"
yujun_name_path         = "./prompts/char_spec/yujun_desc/char_name.json"

# Prompt Pfade
user_path               = "./prompts/user_spec"
mia_desc_path           = "./prompts/char_spec/mia_desc"
yujun_desc_path         = "./prompts/char_spec/yujun_desc"
utility_path            = "./prompts/utility"
memory_path             = "./prompts/memory"


#Lesen aller relevanten Dateien
def read_file(path, debug=True):
    """
    Reads various file formats (json, jsonl, txt, yaml) and returns their contents.
    
    Args:
        path: Path to the file (string or Path object)
        debug: Whether to print error messages (default: True)
    
    Returns:
        The content of the file, or None/False on error
    """
    # Convert string paths to Path objects if necessary
    path = Path(path) if isinstance(path, str) else path
    
    if not path.exists():
        if debug:
            print(f"Error: File {path} not found.")
        return None
    
    try:
        suffix = path.suffix.lower()
        with open(path, "r", encoding="utf-8") as file:
            if suffix == ".json":
                data = json.load(file)
            elif suffix == ".jsonl":
                data = [json.loads(line.strip()) for line in file if line.strip()]
            elif suffix == ".txt":
                data = file.read()
            elif suffix == ".yaml" or suffix == ".yml":
                data = yaml.safe_load(file)
            else:
                if debug:
                    print(f"Error: Unsupported file format {suffix}")
                return None
                
        return False if data is None or data == {} or data == [] or data == "" else data
                
    except json.JSONDecodeError:
        if debug:
            print(f"Error: File {path} is not valid JSON/JSONL.")
    except yaml.YAMLError:
        if debug:
            print(f"Error: File {path} is not valid YAML.")
    except Exception as e:
        if debug:
            print(f"Error reading file {path}: {e}")
            
    return None

#=================================  Refactoring  ============================================

#NOTE Refactoring: read_json -> read_file (dont use the function read_json)
def read_json(path:str, debug:bool=True) -> any:
    try:
        if not Path(path).is_file():
            print(f"Error: Datei {path} nicht gefunden.")
            return None
        
        with open(path, "r", encoding="utf-8") as file:
            data=json.load(file)
            if not data:
                return False
            return data
        
        
    except FileNotFoundError:
        if debug:
            print(f"Error: Datei {path} existiert nicht.")
    except json.JSONDecodeError:
        if debug:
            print(f"Error: Datei {path} ist leer.")
    except Exception as e:
        if debug:
            print(f"Error beim Lesen der Datei {path}: {e}")

    return None

#NOTE Refactoring: read_jsonl -> read_file (dont use the function read_jsonl)
def read_jsonl(file_path):
    '''
    Reads a jsonl file and returns the data as a list
    '''
    data = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            data.append(json.loads(line.strip()))
    return data
            

#NOTE Refactoring: read_txt -> read_file (dont use the function read_txt)
def read_txt(path:str):
    try:
        if not Path(path).is_file():
            print(f"Error: Datei {path} nicht gefunden.")
            return None
        
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
        
    except FileNotFoundError:
        print(f"Error: Datei {path} existiert nicht.")
    except Exception as e:
        print(f"Error beim Lesen der Datei {path}: {e}")

    return None

#============================================================================================

# Schreiben von JSON-Dateien
def write_json(path:str, data=None) -> bool:
    try:
        path = Path(path)

        # Sicherstellen, dass das Verzeichnis existiert
        path.parent.mkdir(parents=True, exist_ok=True)

        if data:
            with open(path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        else:
            with open(path, "w", encoding="utf-8") as file:
                file.write("")
        return True
    
    except FileNotFoundError:
        print(f"Error: Datei {path} konnte nicht gefunden werden.")
    except IsADirectoryError:
        print(f"Error: {path} ist ein Verzeichnis, keine Datei.")
    except PermissionError:
        print(f"Error: Keine Berechtigung zum Schreiben in {path}.")
    except Exception as e:
        print(f"Error writing JSON to {path}: {e}")

    return False


def load_set(
        char:bool=False,
        color:bool=False,
        freq:bool=False,
        imp:bool=False,
        max_t:bool=False,
        time_sense:bool=False
        ) -> any:
    '''
    Lädt die Einstellungen für die KI
    '''
    global set_color_path, set_freq_path, set_imp_path, set_max_t_path, set_time_sense_path, set_char_path
    
    flags = [
        (char, set_char_path, "set_char"),
        (color, set_color_path, "color_choice"),
        (freq, set_freq_path, "set_freq"),
        (imp, set_imp_path, "set_imp"),
        (max_t, set_max_t_path, "max_token"),
        (time_sense, set_time_sense_path, "time_sense"),
    ]
    for flag, path, key in flags:
        if flag:
            data = read_json(path)
            return data[key]
    return None
    
def save_set(
        char:bool=False,
        color:bool=False,
        freq:bool=False,
        imp:bool=False,
        max_t:bool=False,
        time_sense:bool=False,
        slot:bool=False,
        data:any=None
        ):
    '''
    Speichert die Einstellungen für die KI
    '''
    global set_color_path, set_freq_path, set_imp_path, set_max_t_path, set_time_sense_path, set_char_path
    
    flags = [
        (char, set_char_path, "set_char"),
        (color, set_color_path, "color_choice"),
        (freq, set_freq_path, "set_freq"),
        (imp, set_imp_path, "set_imp"),
        (max_t, set_max_t_path, "max_token"),
        (time_sense, set_time_sense_path, "time_sense"),
        (slot, set_slot, "set_slot")
    ]
    for flag, path, key in flags:
        if flag:
            write_json(path, {key: data})
            return
    return None

def get_user_name() -> str:
    '''
    read user_name.json
    return: key["user_name"]
    '''
    return read_file(FILE['user_name'])["user_name"]
    
def load_user_char_name(user:bool=False, char:str=None) -> str:
    '''
    Lädt den Benutzer- und Charakternamen
    return: user_name, char_name
    '''
    global user_name_path, mia_name_path, yujun_name_path

    char_name_path = None

    if char == "mia":
        char_name_path = mia_name_path
    elif char == "yu-jun":
        char_name_path = yujun_name_path

    if user and char_name_path:
        data_0 = read_json(user_name_path)
        data_1 = read_json(char_name_path)
        return data_0["user_name"], data_1["char_name"]
    elif user and not char_name_path:
        data = read_json(user_name_path, debug=False)
        if not data:
            return None
        return data["user_name"]
    elif char_name_path and not user:
        data = read_json(char_name_path)
        return data["char_name"]
    else:
        return None
    
def save_user_name(user:str):
    '''
    Speichert den Benutzernamen
    '''
    global user_name_path
    
    file = {"user_name": user}
    write_json(user_name_path, file)

def load_prompts(char:str=None, utility:bool=False, memory:bool=False) -> dict:
    '''
    Lädt die Prompts für die KI
    '''
    global mia_desc_path, yujun_desc_path, utility_path, memory_path

    path = None

    # Everything to lower case
    if char:
        char=char.lower()

    if char == "mia":
        path = mia_desc_path
    elif char == "yu-jun":
        path = yujun_desc_path
    else:
        pass
    if utility:
        path = utility_path
    elif memory:
        path = memory_path
    
    data = {}
    for file_name in Path(path).iterdir():
        if file_name.is_file() and file_name.suffix == ".txt":
            with open(file_name, "r", encoding="utf-8") as f:
                data[file_name.stem] = f.read()
    return data

def get_slot() -> int:
    '''
    Gibt den aktiven Slot zurück
    '''
    global set_slot
    slot = read_json(set_slot)
    return slot["set_slot"]

def slot_content() -> list:
    '''
    Gibt den Inhalt des Slots zurück
    return: list[dict]
    '''
    global slot_path

    slots = ["slot_0", "slot_1", "slot_2", "slot_3", "slot_4"]
    slot_content_list = []

    for slot in slots:
        data = read_json(slot_path + f"/{slot}.json", debug=False)
        if data:
            chat_len = len(data[slot][1]["chat_history"])
            slot_content_list.append({f"{slot}":[data[slot][0]["char"], data[slot][0]["time"], chat_len]})
        else:
            slot_content_list.append({f"{slot}":[None, None, None]})
    return slot_content_list

#test
#print(slot_content())

def load_slot(slot:int=None) -> any:
    '''
    return: [char:str, time:str, chat:[list[dict]]
    or None
        
    '''
    global slot_path

    path = slot_path + f"/slot_{slot-1}.json"
    key = f"slot_{slot-1}"
    
    data = read_json(path, debug=False)
    
    if not data:
        return None

    char = data[key][0]["char"]
    time = data[key][0]["time"]
    chat = data[key][1]["chat_history"]
            
    return [char, time, chat]
    
    
def select_slot(char:str, time:str, f_msg:list, slot:int=None):
    '''
    Speichert die Dialog-Slots
    '''
    global slot_path

    path = slot_path + f"/slot_{slot-1}.json"
    key = f"slot_{slot-1}"

    data = {key: [{"char": char, "time": time}, {"chat_history": f_msg}]}

    write_json(path, data)

def save_dialog(message:list=None):
    '''
    Speichert den Dialogverlauf
    '''
    global slot_path

    slot = get_slot()

    path = slot_path + f"/slot_{slot-1}.json"
    key = f"slot_{slot-1}"

    data = read_json(path)
    for msg in message:
        data[key][1]["chat_history"].append(msg)

    write_json(path, data)

#test select_slot
#select_slot("mia", "2022-03-02T15:00:00.000Z", [{"role": "assistant","content": "hallo","history": True}], 2)
#test save_dialog
#save_dialog([{"role": "user","content": "hallo","history": True},{"role": "assistant","content": "hallo","history": True}], 2)

def load_history(slot:int=None) -> list:
    '''
    Lädt den Dialogverlauf
    -> list
    history: [{"role":str, "content":str, "analysis":dict, "history":bool}, ...]
    list_msg: [[str(Name), str(Text), dict(Analyse), bool], ...]
    Analyse User: {"input_t":int, "msg":int}
    Analyse KI: {"output_t":int, "msg":int, "imp":bool}
    '''
    data = load_slot(slot)

    if data:
        history = data[2]
    else:
        return None, None

    list_msg = []
    
    for message in history:
        single_msg = [value for key, value in message.items() if key in {"role", "content", "analysis", "history"}]
        list_msg.append(single_msg)

    return history, list_msg

#test load_history
#print(load_history(1))

def load_format_history(value:int=None) -> str:
    '''
    Lädt den Dialogverlauf
    -> str
    '''
    global slot_path

    slot = get_slot()

    data = load_slot(slot)

    user = read_json(user_name_path)["user_name"]
    char = load_set(char=True)
    history = data[2]
    list_msg = []

    for message in history:
        single_msg = [value for key, value in message.items() if key in {"role", "content"}]
        list_msg.append(single_msg)

    if value != None:
        # Begrenzung der Nachrichten, lädt nur die letzten value Nachrichten
        list_msg = list_msg[-value:]
        
    string = ""

    for msg in list_msg:
        if msg[0] == "user":
            string += f"{user}: {msg[1]}\n\n"
        elif msg[0] == "assistant":
            string += f"{char}: {msg[1].strip()}\n\n"

    return string

#print(load_format_history())

def load_api_messages(history_data:dict=None) -> list:
    '''
    Läd die API-Nachrichten
    '''

    api_messages = [
        {"role": msg["role"], "content": msg["content"]}
        for msg in history_data if "role" in msg and "content" in msg
    ]

    return api_messages

def load_current_emo_score() -> dict:
    '''
    Lädt die Emotionswerte
    '''
    global emo_score_path

    slot = get_slot()

    data = read_json(emo_score_path)

    data = data[f"slot_{slot-1}"]

    return data

def save_current_emo_score(score:dict):
    '''
    Speichert die Emotionswerte
    '''
    global emo_score_path

    slot = get_slot()

    data = read_json(emo_score_path)

    data[f"slot_{slot-1}"] = score

    write_json(emo_score_path, data)

def get_slot_cost() -> float:
    '''
    Gibt die Kosten für die Slots zurück
    '''
    global cost_path

    slot = get_slot()

    data = read_json(cost_path)

    data = data[f"slot_{slot-1}"]

    c_input = data["total_input_cost"]
    c_output = data["total_output_cost"]

    return c_input, c_output

def save_slot_cost(c_input:float, c_output:float):
    '''
    Speichert die Kosten für die Slots
    '''
    global cost_path

    slot = get_slot()

    data = read_json(cost_path)

    data[f"slot_{slot-1}"] = {"total_input_cost": c_input, "total_output_cost": c_output}

    write_json(cost_path, data)

def get_last_msg_time() -> str:
    '''
    Gibt die letzte Nachrichtenzeit zurück
    '''
    global last_msg_time_path
    
    slot = get_slot()

    time = read_json(last_msg_time_path)

    time = time[f"slot_{slot-1}"]

    time = time["last_msg_time"]

    if time == "":
        return None

    return time

def save_msg_time(time:str):
    '''
    Speichert die letzte Nachrichtenzeit
    '''
    global last_msg_time_path

    slot = get_slot()

    data = read_json(last_msg_time_path)

    data[f"slot_{slot-1}"] = {"last_msg_time": time}

    write_json(last_msg_time_path, data)

def get_score_trigger(
        angry:bool=False,
        sad:bool=False,
        affection:bool=False,
        arousal:bool=False,
        trust:bool=False,
        low_trust:bool=False,
        high_trust:bool=False,
        value:int=None
        ) -> str:
    '''
    Gibt die Score-Trigger zurück
    '''
    global score_trigger_path

    flags = [
        (angry, f"angry_{value}"),
        (sad, f"sad_{value}"),
        (affection, f"affection_{value}"),
        (arousal, f"arousal_{value}"),
        (trust, f"trust_{value}"),
        (low_trust, "low_trust"),
        (high_trust, "high_trust")
        
    ]

    char = load_set(char=True)

    data = read_json(score_trigger_path)

    data = data[char]

    for flag, key in flags:
        if flag:
            return data[key]["behave"], data[key]["tag_desc"]

    return None