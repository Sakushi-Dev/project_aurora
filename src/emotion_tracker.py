
import os
import json

# Import the functions from the anthropic_api.py file
from anthropic_api import init_anthropic_client, load_api_key
from prompts_processing import user_name as user, char_name as char


debug = False

if debug:
        print("DebugMode: emotion_tracker.py")


def detect_emotion(dialog_len:int, text, sub_text = None):

    global debug

    client = init_anthropic_client(load_api_key())

    #read mood_tracking.json
    if os.path.exists("./src/Prompts/emotion/mood_tracking.json"):
        with open("./src/Prompts/emotion/mood_tracking.json", "r", encoding="utf-8") as f:
            mood_system_prompt = json.load(f)
    else:
        print("mood_tracking.json not found")

    #read emotion_trigger.json
    if os.path.exists("./data/emotion_trigger.json"):
        with open("./data/emotion_trigger.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        # Liste zum Speichern aller Kategorien
        triggers_in_cat = []
        
        # Trigger in Category aufteilen und in Liste speichern
        for category, trigger_list in data.items():
                triggers_in_cat.append({category: list(trigger_list.keys())})

        if debug:
            print(triggers_in_cat, "\n\n=====================================\n\n")    
        
        triggers_map = {}

        for cat_dict in triggers_in_cat:
            for category, trigger_list in cat_dict.items():
                triggers_map[category] = "".join(f"\n- {emotion}" for emotion in trigger_list)

        angry_trigger = triggers_map.get("angry_trigger", "")
        sad_trigger = triggers_map.get("sad_trigger", "")
        affection_trigger = triggers_map.get("affection_trigger", "")
        arousal_trigger = triggers_map.get("arousal_trigger", "")
        trust_trigger = triggers_map.get("trust_trigger", "")
    else:
        print("emotion_trigger.json not found")

    if debug:
        print(f"Angry: {angry_trigger}\nSad: {sad_trigger}\nAffection: {affection_trigger}\nArousal: {arousal_trigger}\nTrust: {trust_trigger}\n\n=====================================\n\n")
    

    prompt_list = []
    triggers = [angry_trigger, sad_trigger, affection_trigger, arousal_trigger, trust_trigger]
    # Replace the {{trigger}} placeholder in the mood system prompt with the actual triggers

    for trigger in triggers:
        temp_list = []
        for prompt in mood_system_prompt:
            batch = ({key: str(value).replace("{{trigger}}", trigger).replace("{{char}}", char).replace("{{user}}", user) for key, value in prompt.items()})
            temp_list.append(batch)
        prompt_list.append(temp_list)

    if debug:
        print(f"Prompt List:\n\n{prompt_list}\n\n=====================================\n\n")

    requests_data = {
        "angry_prompts": prompt_list[0],
        "sad_prompts": prompt_list[1],
        "affection_prompts": prompt_list[2],
        "arousal_prompts": prompt_list[3],
        "trust_prompts": prompt_list[4]
        }
    
    if dialog_len == 2:
        user_message_1 = text[0]["content"]
        char_response_1 = text[1]["content"]
        dialog = (
        "Dialog:\n"
        f"{user}: {user_message_1}\n"
        f"{char}: {char_response_1}\n"
    )
    if dialog_len == 4:
        user_message_1 = text[0]["content"]
        char_response_1 = text[1]["content"]
        user_message_2 = text[2]["content"]
        char_response_2 = text[3]["content"]
        dialog = (
        "Dialog:\n"
        f"{user}: {user_message_1}\n"
        f"{char}: {char_response_1}\n"
        f"{user}: {user_message_2}\n"
        f"{char}: {char_response_2}\n"
    )
    if dialog_len == 6:
        user_message_1 = text[0]["content"]
        char_response_1 = text[1]["content"]
        user_message_2 = text[2]["content"]
        char_response_2 = text[3]["content"]
        user_message_3 = text[4]["content"]
        char_response_3 = text[5]["content"]
        dialog = (
        "Dialog:\n"
        f"{user}: {user_message_1}\n"
        f"{char}: {char_response_1}\n"
        f"{user}: {user_message_2}\n"
        f"{char}: {char_response_2}\n"
        f"{user}: {user_message_3}\n"
        f"{char}: {char_response_3}\n"
    )
    if dialog_len == 8:
        user_message_1 = text[0]["content"]
        char_response_1 = text[1]["content"]
        user_message_2 = text[2]["content"]
        char_response_2 = text[3]["content"]
        user_message_3 = text[4]["content"]
        char_response_3 = text[5]["content"]
        user_message_4 = text[6]["content"]
        char_response_4 = text[7]["content"]
        dialog = (
        "Dialog:\n"
        f"{user}: {user_message_1}\n"
        f"{char}: {char_response_1}\n"
        f"{user}: {user_message_2}\n"
        f"{char}: {char_response_2}\n"
        f"{user}: {user_message_3}\n"
        f"{char}: {char_response_3}\n"
        f"{user}: {user_message_4}\n"
        f"{char}: {char_response_4}\n"
        )


    # Batch request
    if debug:

        for key, value in requests_data.items():

            print(f"{key}: {value}\n\n")
        

    # Create the messages list
    messages = []

    if sub_text:
        messages.append(
            {
            "role": "assistant",
            "content": sub_text
            },
        )

    messages.append(
        {
        "role": "user",
        "content": dialog
        },
    )



    
    if debug:
        print(f"Dialog:\n{messages}\n\n=====================================\n\n")
        


    response_list = []
    for key, prompt in requests_data.items():
        response_list.append({key: (client.messages.create(
                    model="claude-3-5-haiku-20241022",
                    max_tokens=20,
                    temperature=0.7,
                    system=prompt,
                    messages=messages,
                ),
            )
        }
    )
        
    if debug:
        print(f"Raw:\n\n{response_list}\n\n=====================================\n\n")

    # Extract the response from the response_list
    mood = {}
    for response in response_list:
        for key, value in response.items():
            mood[key] = [text_block.text for text_block in value[0].content]

    if debug:
        print(f"Extracted:\n\n{mood}\n\n=====================================\n\n")

    return mood



import sys
def load_history_replay():
    """
    Load the last 4 messages from history
    """
    file_path = "./src/history/history_backup.py"
    if not os.path.exists(file_path):
        return None

    if "history.history_backup" in sys.modules:
        del sys.modules["history.history_backup"]
    from history.history_backup import history_backup  # type: ignore

    replay = history_backup[-8:]

    return replay

def emotion_tracker(dialogue_len:int):

    global debug

    """
    Track the emotions of the last 4 messages
    """
    if os.path.exists("./data/emotion_trigger.json"):
        with open("./data/emotion_trigger.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    # Liste zum Speichern aller Kategorien
    all_triggers = []
    
    for _, trigger_list in data.items():
                all_triggers.append(list(trigger_list.keys()))

    text = load_history_replay()

    emotion_response = detect_emotion(dialogue_len, text, "Understood. I will respond with only the trigger word or phrase exactly as it is written in the '**Guidelines:**' section. No additional text, explanations, or descriptions will be included.")

    # ================================================================================================

    # Debugging
    if debug:
        for key, value in emotion_response.items():
            print(f"{key}: {value}\n")

    mapping = {
        "angry_prompts": "angry",
        "sad_prompts": "sad",
        "affection_prompts": "affection",
        "arousal_prompts": "arousal",
        "trust_prompts": "trust",
    }

   
    for key, value in emotion_response.items():
        label = mapping.get(key)
        if label and any(trigger in sublist for sublist in all_triggers for trigger in value):
            if debug:
                print(f"Detected {label}")


    angry = emotion_response["angry_prompts"][0]
    sad = emotion_response["sad_prompts"][0]
    affection = emotion_response["affection_prompts"][0]
    arousal = emotion_response["arousal_prompts"][0]
    trust = emotion_response["trust_prompts"][0]


    return angry, sad, affection, arousal, trust



if debug:
    emotion_tracker()