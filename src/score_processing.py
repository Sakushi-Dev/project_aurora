import os
import json
from emotion_tracker import emotion_tracker

debug = False

if debug:
    print("DebugMode: score_processing.py")

def feelings_over_time():

     # Read emotion_score.json
    if os.path.exists("./data/emotion_score.json"):
        with open("./data/emotion_score.json", "r", encoding="utf-8") as f:
            score = json.load(f)

    angry_value = score["Angry_Level"]
    sad_value = score["Sad_Level"]
    affection_value = score["Affection_Level"]
    arousal_value = score["Arousal_Level"]
    trust_value = score["Trust_Level"]

    if angry_value > 20:
        angry_value -= 10
    if sad_value > 20:
        sad_value -= 5
    if affection_value < 1000:
        affection_value += 2
    if arousal_value > 20:
        arousal_value -= 2
    if trust_value < 1000:
        trust_value += 5

    # Create emotion_score.json
    if os.path.exists("./data/emotion_score.json"):
        with open("./data/emotion_score.json", "w", encoding="utf-8") as f:
            score = {
                "Angry_Level": angry_value,
                "Sad_Level": sad_value,
                "Affection_Level": affection_value,
                "Arousal_Level": arousal_value,
                "Trust_Level": trust_value
            }
            json.dump(score, f, indent=4)
        


    

def score_processing(dialogue_len:int):

    global debug

    angry, sad, affection, arousal, trust = emotion_tracker(dialogue_len)

    # Read emotion_trigger.json
    if os.path.exists("./data/emotion_trigger.json"):
        with open("./data/emotion_trigger.json", "r", encoding="utf-8") as f:
            data = json.load(f)


    angry_trigger = data["angry_trigger"]
    sad_trigger = data["sad_trigger"]
    affection_trigger = data["affection_trigger"]
    arousal_trigger = data["arousal_trigger"]
    trust_trigger = data["trust_trigger"]


    # Read emotion_score.json
    if os.path.exists("./data/emotion_score.json"):
        with open("./data/emotion_score.json", "r", encoding="utf-8") as f:
            score = json.load(f)
    else:
        # Create emotion_score.json
        if not os.path.exists("./data"):
            os.makedirs("./data")
        with open("./data/emotion_score.json", "w", encoding="utf-8") as f:
            score = {
                "Angry_Level": 0,
                "Sad_Level": 0,
                "Affection_Level": 0,
                "Arousal_Level": 0,
                "Trust_Level": 0
            }
            json.dump(score, f, indent=4)

    # Debugging
    if debug:
        print(f"""
        Old Emotion Score:

        Angry_Level: {score["Angry_Level"]}
        Sad_Level: {score["Sad_Level"]}
        Affection_Level: {score["Affection_Level"]}
        Arousal_Level: {score["Arousal_Level"]}
        Trust_Level: {score["Trust_Level"]}
        """)


    triggers = [
        ("Angry_Level", angry_trigger),
        ("Sad_Level", sad_trigger),
        ("Affection_Level", affection_trigger),
        ("Arousal_Level", arousal_trigger),
        ("Trust_Level", trust_trigger),
    ]

    
    score["Angry_Level"] += triggers[0][1].get(angry, 0)
    if score["Angry_Level"] < 0:
            score["Angry_Level"] = 0
    elif score["Angry_Level"] > 100:
            score["Angry_Level"] = 100
    score["Sad_Level"] += triggers[1][1].get(sad, 0)
    if score["Sad_Level"] < 0:
            score["Sad_Level"] = 0
    elif score["Sad_Level"] > 100:
            score["Sad_Level"] = 100
    score["Affection_Level"] += triggers[2][1].get(affection, 0)
    if score["Affection_Level"] < 0:
            score["Affection_Level"] = 0
    score["Arousal_Level"] += triggers[3][1].get(arousal, 0)
    if score["Arousal_Level"] < 0:
            score["Arousal_Level"] = 0
    elif score["Arousal_Level"] > 9000:
            score["Arousal_Level"] = 0   
    score["Trust_Level"] += triggers[4][1].get(trust, 0)
    if score["Trust_Level"] < -50:
            score["Trust_Level"] = -50

        

    # Debugging
    if debug:
        print(f"""
        New Emotion Score:

        Angry_Level: {score["Angry_Level"]}
        Sad_Level: {score["Sad_Level"]}
        Affection_Level: {score["Affection_Level"]}
        Arousal_Level: {score["Arousal_Level"]}
        Trust_Level: {score["Trust_Level"]}
        """)

    # Write new emotion_score.json
    with open("./data/emotion_score.json", "w", encoding="utf-8") as f:
        json.dump(score, f, indent=4)


if debug:  
    score_processing()