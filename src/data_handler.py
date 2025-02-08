import json
from pathlib import Path


# Einstellungen
set_char_path           = "./data/set/set_char.json"
set_color_path          = "./data/set/set_color.json"
set_freq_path           = "./data/set/set_freq.json"
set_imp_path            = "./data/set/set_imp.json"
set_max_t_path          = "./data/set/set_max_t.json"
set_time_sense_path     = "./data/set/set_time_sense.json"

# Letzte Zeit der Interaktion
current_time_path       = "./data/current_time.txt"

# Daten zur emotionsbasierten Textgenerierung
emo_score_path          = "./data/emotion_score.json"
emo_trigger_path        = "./data/emotion_trigger.json"
imp_prompt_path         = "./data/impatience_prompt.json"

# Dialog Speicher
history_path            = "./src/history/history_backup.py"
cost_path               = "./src/history/costs_backup.py"
analytics_path          = "./src/history/analytics_backup.py"

# Prompt Pfade für User-Namen und Char-Namen
user_name_path          = "./prompts/user_spec/user_name.json"
mia_name_path           = "./prompts/char_spec/mia_desc/char_name.json"
jae_name_path           = "./prompts/char_spec/jae_desc/char_name.json"

# Prompt Pfade
user_path               = "./Prompts/user_spec"
mia_desc_path           = "./Prompts/char_spec/mia_desc"
jae_desc_path           = "./Prompts/char_spec/jae_desc"
utility_path            = "./Prompts/utility"


# Lesen von JSON-Dateien
def read_json(path:str):
    try:
        if not Path(path).is_file():
            print(f"Error: Datei {path} nicht gefunden.")
            return None
        
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
        
    except FileNotFoundError:
        print(f"Error: Datei {path} existiert nicht.")
    except json.JSONDecodeError:
        print(f"Error: Datei {path} ist kein gültiges JSON.")
    except Exception as e:
        print(f"Error beim Lesen der Datei {path}: {e}")

    return None
            
# Schreiben von JSON-Dateien
def write_json(path:str, data) -> bool:
    try:
        path = Path(path)

        # Sicherstellen, dass das Verzeichnis existiert
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

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

# Lesen von TXT-Dateien
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
        (time_sense, set_time_sense_path, "time_sense")
    ]
    for flag, path, key in flags:
        if flag:
            write_json(path, {key: data})
            return
    return None
    
def load_user_char_name(user:bool=False, char:str=None) -> str:
    '''
    Lädt den Benutzer- und Charakternamen
    return: user_name, char_name
    '''
    global user_name_path, mia_name_path, jae_name_path

    char_name_path = None

    if char == "mia":
        char_name_path = mia_name_path
    elif char == "jae":
        char_name_path = jae_name_path

    if user and char_name_path:
        data_0 = read_json(user_name_path)
        data_1 = read_json(char_name_path)
        return data_0["user_name"], data_1["char_name"]
    elif user and not char_name_path:
        data = read_json(user_name_path)
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

def load_prompts(char:str=None, utility:bool=False) -> dict:
    '''
    Lädt die Prompts für die KI
    '''
    global mia_desc_path, jae_desc_path, utility_path

    path = None

    if char == "mia":
        path = mia_desc_path
    elif char == "jae":
        path = jae_desc_path
    else:
        pass
    if utility:
        path = utility_path
    
    data = {}
    for file_name in Path(path).iterdir():
        if file_name.is_file() and file_name.suffix == ".txt":
            with open(file_name, "r", encoding="utf-8") as f:
                data[file_name.stem] = f.read()
    return data
    
    


