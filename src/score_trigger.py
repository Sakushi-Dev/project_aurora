from data_handler import load_current_emo_score, get_score_trigger, load_set, read_json

from globals import FOLDER
char = load_set(char=True)
user = read_json(FOLDER["user_spec"] / "user_name.json")["user_name"]

debug = False
lokal = False

if debug:
    print("DebugMode: score_trigger.py\n\n=====================================\n\n")

def mood_trigger():

    global debug

    score = load_current_emo_score()

    angry_level = score.get("Angry_Level", 0)
    sad_level = score.get("Sad_Level", 0)
    affection_level = score.get("Affection_Level", 0)
    arousal_level = score.get("Arousal_Level", 0)
    trust_level = score.get("Trust_Level", 0)
         
    # Debugging
    if debug:
        print(
f"""
Angry_Level: {angry_level}
Sad_Level: {sad_level}
Affection_Level: {affection_level}
Arousal_Level: {arousal_level}
Trust_Level: {trust_level}
""")

#=======================================================================================================================   

    def get_angry_trigger(angry_level):
        """
        Gibt den Trigger-Text für die Wut zurück.
        Parameters:
            angry_level (int): Wut-Level
        """
        ranges = [(0, 30), (30, 70), (70, 90), (90, float('inf'))]
        for i, (low, high) in enumerate(ranges):
            if low <= angry_level < high:
                return get_score_trigger(angry=True, value=i)
        return "", ""
        

#=======================================================================================================================

    def get_sad_trigger(sad_level):
        """
        Gibt den Trigger-Text für Traurigkeit zurück.
        Parameters:
            sad_level (int): Traurig-Level
        """
        ranges = [(0, 20), (20, 50), (50, 90), (90, float('inf'))]
        for i, (low, high) in enumerate(ranges):
            if low <= sad_level < high:
                return get_score_trigger(sad=True, value=i)
        return "", ""
        
#=======================================================================================================================

    def get_affection_trigger(affection_level):
        """
        Gibt den Trigger-Text für Zuneigung zurück.
        Parameters:
            affection_level (int): Zuneigung-Level
        """
        ranges = [(0, 150), (150, 400), (400, 800), (800, float('inf'))]
        for i, (low, high) in enumerate(ranges):
            if low <= affection_level <high:
                return get_score_trigger(affection=True, value=i)
        return "", ""
        
#=======================================================================================================================

    def get_arousal_trigger(arousal_level):
        """
        Gibt den Trigger-Text für Erregung zurück.
        Parameters:
            arousal_level (int): Erregung-Level
        """
        ranges = [(0, 30), (30, 90), (90, 160), (160, float('inf'))]
        for i, (low, high) in enumerate(ranges):
            if low <= arousal_level < high:
                return get_score_trigger(arousal=True, value=i)
        return "", ""
        
#=======================================================================================================================

    def get_trust_trigger(trust_level: int, angry_level: int = None):
        """
        Gibt den Trigger-Text für Vertrauen zurück.
        Parameters:
           1.) trust_level (int): Vertrauen-Level
        Abhänigkeiten:
           2.) angry_level (int): Wut-Level
        """
        # Wenn Wut-Level hoch ist Reagiert {{char}} extrem gereizt und aggressiv
        angry = angry_level and angry_level > 70

        # Wut Verhalten bei niedrigem Vertrauen
        low_trust_behave, low_trust_tags = get_score_trigger(low_trust=True)

        # Wut Verhalten bei hohem Vertrauen
        high_trust_behave, high_trust_tags = get_score_trigger(high_trust=True)

        ranges = [
            (0, 0, 0),
            (0, 100, 1),
            (100, 300, 2),
            (300, 500, 3),
            (500, 800, 4),
            (800, float('inf'), 5)
        ]

        for low, high, value in ranges:
            if low <= trust_level < high:
                behave, tag_desc = get_score_trigger(trust=True, value=value)
                if angry:
                    behave = low_trust_behave if value <= 3 else high_trust_behave
                    tag_desc = low_trust_tags if value <= 3 else high_trust_tags
                return behave, tag_desc

        return "", ""
        
    # Trigger-Texte
    angry_behave, angry_trigger = get_angry_trigger(angry_level)
    sad_behave, sad_trigger = get_sad_trigger(sad_level)
    affection_behave, affection_trigger = get_affection_trigger(affection_level)
    arousal_behave, arousal_trigger = get_arousal_trigger(arousal_level)
    trust_behave, trust_trigger = get_trust_trigger(trust_level, angry_level)

    behave = f"{angry_behave}\n{sad_behave}\n{affection_behave}\n{arousal_behave}\n{trust_behave}"
    
    
    mood = (
        "[The following '<tags>' and '<behave>' describe {{char}}'s nature and are given high priority in every response.]\n"
        + f"[START HIGH PRIO]<tags>\n{angry_trigger}, {sad_trigger}, {affection_trigger}, {arousal_trigger}, {trust_trigger}\n Info: Erwähnen von 'tags' in antwort ist verboten.\n</tags>\n"
        + "<behave>\n"  + behave + "\n</behave>[END HIGH PRIO]"
    )

    # Replace {{char}} and {{user}}
    mood = mood.replace("{{char}}", char).replace("{{user}}", user)


    # Debugging
    if debug:
        print(f"{mood}\n\n=====================================\n\n")
    
    return mood

if lokal:
    mood_trigger()
