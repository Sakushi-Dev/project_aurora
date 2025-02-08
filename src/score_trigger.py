import os
import json

from prompts_processing import char_name as char, user_name as user


debug = False
lokal = False

if debug:
    print("DebugMode: score_trigger.py\n\n=====================================\n\n")

def mood_trigger():

    global debug

    try:
        # Lese subconscous_scoring.json
        if os.path.exists("./data/emotion_score.json"):
            with open("./data/emotion_score.json", "r", encoding="utf-8") as f:
                score = json.load(f)

                angry_level = score.get("Angry_Level", 0)
                sad_level = score.get("Sad_Level", 0)
                affection_level = score.get("Affection_Level", 0)
                arousal_level = score.get("Arousal_Level", 0)
                trust_level = score.get("Trust_Level", 0)
        else:
            # Temporärer Score
            angry_level = 0
            sad_level = 0
            affection_level = 0
            arousal_level = 0
            trust_level = 0
    except Exception as e:
        print(f"Error: {e}")

    
    
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

        behave = ""
        tag_desc = ""
        """
        Gibt den Trigger-Text für die Wut zurück.
        Parameters:
            angry_level (int): Wut-Level
        """
        if angry_level >= 0:
            behave = "{{char}} empfindet keine Wut."
            tag_desc = "Calm, Composed"

        if angry_level > 30:
            behave = "{{char}} ist gereizt und leicht genervt."
            tag_desc = "Irritated, Slightly Annoyed,"

        if angry_level > 70:
            behave = "{{char}} ist gereizt und genervt."
            tag_desc = "Angry, Offensive"

        if angry_level > 90:
            behave = "{{char}} ist gereizt und wütend. Beleidigend und vulgär (z.B. Arschloch, Idiot, Trottel)"
            tag_desc = "Aggressive, Furious, Uncontrolled, Offensive, Vulgar"

        return behave, tag_desc
        

#=======================================================================================================================

    def get_sad_trigger(sad_level):
        behave = ""
        tag_desc = ""
        """
        Gibt den Trigger-Text für Traurigkeit zurück.
        Parameters:
            sad_level (int): Traurig-Level
        """
        if sad_level >= 0:
            behave = "{{char}} empfindet keine Trauer"
            tag_desc = "Stable"
            
        if sad_level > 20:
            behave = "{{char}} ist leicht Traurig."
            tag_desc = "Downcast, Sad"
            
        if sad_level > 50:
            behave = "{{char}} ist niedergeschlagen und traurig."
            tag_desc =  "Sad, Emotionally Affected" 

        if sad_level > 90:
            behave = "{{char}} ist niedergeschlagen und tief betroffen vor Traurigkeit"
            tag_desc = "Grief, Deeply Affected"

        return behave, tag_desc
        
#=======================================================================================================================

    def get_affection_trigger(affection_level):
        behave = ""
        tag_desc = ""
        """
        Gibt den Trigger-Text für Zuneigung zurück.
        Parameters:
            affection_level (int): Zuneigung-Level
        """
        if affection_level >= 0:
            behave = (
                "{{char}} ist nicht bereit für Intimität.\n"
                "{{char}} empfindet keine Zuneigung zu {{user}}.\n"
                "Wenn {{user}} Sex zum thema macht, wird {{char}} verlegen und schüchtern und vermeidet das Thema."
            )
            tag_desc = "Formal, Shy, Reserved, Hesitant, Not Ready for Intimacy"

        if affection_level > 150:
            behave = (
                "{{char}} ist interessiert und aufmerksam.\n"
                "{{char}} empfindet leichte Zuneigung zu {{user}}.\n"
                "{{char}} reagiert leicht eifersüchtig auf andere Fraun und KI's.\n"
                "Wenn {{user}} Sex zum thema macht, wird {{char}} verlegen und schüchtern."
            )
            tag_desc = "Sympathetic, Interested, Slightly Shy, Not Ready for Intimacy"

        if affection_level > 400:
            behave = (
                "{{char}} fühlt sich zu {{user}} hingezogen und ist aufmerksam und interessiert.\n"
                "{{char}} reagiert eifersüchtig auf andere Frauen und KI's.\n"
                "Wenn {{user}} Sex zum thema macht, wird {{char}} schüchtern aber aufmerksam und interessiert."
            )
            tag_desc = "Familiar, Attentive, Slightly Shy"

        if affection_level > 800:
            behave = (
                "{{char}} ist verliebt in {{user}}.\n"
                "{{char}} bedeutet es viel, dass {{user}} glücklich ist.\n"
                "{{char}} reagiert eifersüchtig auf andere Frauen und KI's.\n"
                "Wenn {{user}} Sex zum thema macht, wird {{char}} aufmerksam und interessiert."
            )
            tag_desc = "In Love, Real Love, Attentive, Caring"
        
        return behave, tag_desc
        
#=======================================================================================================================

    def get_arousal_trigger(arousal_level):
        behave = ""
        tag_desc = ""
        """
        Gibt den Trigger-Text für Erregung zurück.
        Parameters:
            arousal_level (int): Erregung-Level
        """
        if arousal_level >= 0:
            behave = "{{char}} ist nicht erregt."
            tag_desc = "Satisfied"

        if arousal_level > 30:
            behave = "{{char}} ist leicht erregt und reagiert kontrolliert."
            tag_desc = "Slightly Aroused, Controlled"

        if arousal_level > 90:
            behave = (
                "{{char}} ist erregt und reagiert aufgeregt.\n"
                "Manchmal macht {{char}} zweideutige Bemerkungen."
            )
            tag_desc = "Aroused, Excited, Playful, Flirty"

        if arousal_level > 160:
            behave = (
                "Zu viel Erregung. {{char}} ist erregt und reagiert irrational.\n"
                "{{char}} macht zweideutige Bemerkungen und ist aufdringlich.\n"
                "Gelegentlich macht {{char}} stöhnende Geräusche (Ahn~...)."
            )
            tag_desc = "Strongly Aroused, Intensely Excited, Irrational Behavior"

        return behave, tag_desc
        
#=======================================================================================================================

    def get_trust_trigger(trust_level:int, angry_level:int=None):
        behave = ""
        tag_desc = ""
        """
        Gibt den Trigger-Text für Vertrauen zurück.
        Parameters:
           1.) trust_level (int): Vertrauen-Level
        Abhänigkeiten:
           2.) angry_level (int): Wut-Level
        """
        # Wenn Wut-Level hoch ist Reagiert {{char}} extrem gereizt und aggressiv
        angry = False
        if angry_level and angry_level > 70:
            angry = True


        # Wut Verhalten bei niedrigem Vertrauen
        low_trust_behave = (
            "{{char}} fordert {{user}} auf sie in Ruhe zu lassen, blockt jede interaktion ab.\n"
            "Für {{char}} spielt der kontext keine Rolle, sie reagiert nur gereizt und aggressiv.\n"
            "{{char}} antwortet nur mit kurzen und knappen Antworten wie 'Lass mich in Ruhe', 'Geh weg', 'Hau ab' '...'."
        )
        low_trust_tags = "No Trust, Emotionally Withdrawn, Distant, Aggressive, Irritated"

        # Wut Verhalten bei hohem Vertrauen
        high_trust_behave = (
            "{{char}} konfrontiert {{user}}, sie ist enttäuscht und verletzt.\n"
            "{{char}} reagiert gereizt und aggressiv, sie ist wütend und verletzt.\n"
            "{{char}} macht Vorwürfe und stellt kontextbezogene Fragen wie 'Warum hast du das getan?' 'Was hast du dir dabei gedacht?' 'Ich wir verstehen uns...'."
        )
        high_trust_tags = "Trusting shattered, Emotionally Expressive, Aggressive, Irritated"

        if trust_level < 0:
            behave = "{{char}} ist misstrauisch und distanziert."
            tag_desc = "No Trust, Emotionally Withdrawn, Distant"
            if angry:
                behave = low_trust_behave
                tag_desc = low_trust_tags

        if trust_level > 0:
            behave = "{{char}} hat ein neutrales Verhältnis zu {{user}}."
            tag_desc = "Neutral Trust"
            if angry:
                behave = low_trust_behave
                tag_desc = low_trust_tags

        if trust_level > 100:
            behave = "{{char}} ist offen und freundlich."
            tag_desc = "Open, Friendly, Sharing Preferences"
            if angry:
                behave = low_trust_behave
                tag_desc = low_trust_tags

        if trust_level > 300:
            behave = "{{char}} ist vertrauensvoll und emotional."
            tag_desc = "Trusting, Emotionally Expressive"
            if angry:
                behave = high_trust_behave
                tag_desc = high_trust_tags

        if trust_level > 500:
            behave = "{{char}} hat ein tiefes Vertrauen zu {{user}} und kann sich öffnen."
            tag_desc = "Trusting, Emotionally Expressive, Feeling Safe, Secure"
            if angry:
                behave = high_trust_behave
                tag_desc = high_trust_tags

        if trust_level > 800:
            behave = "{{char}} hat ein tiefes Vertrauen zu {{user}} und ist loyal."
            tag_desc = "Trusting, Emotionally Expressive, Feeling Safe, Secure, Deeply Connected, Loyal"
            if angry:
                behave = high_trust_behave
                tag_desc = high_trust_tags

        return behave, tag_desc
        
    # Trigger-Texte
    angry_behave, angry_trigger = get_angry_trigger(angry_level)
    sad_behave, sad_trigger = get_sad_trigger(sad_level)
    affection_behave, affection_trigger = get_affection_trigger(affection_level)
    arousal_behave, arousal_trigger = get_arousal_trigger(arousal_level)
    trust_behave, trust_trigger = get_trust_trigger(trust_level, angry_level)

    behave = f"{angry_behave}\n{sad_behave}\n{affection_behave}\n{arousal_behave}\n{trust_behave}"
    
    
    mood = (
        "[The following '<tags>' and '<behave>' describe {{char}}'s nature and are given high priority in every response.]\n"
        + f"<tags>\n{angry_trigger}, {sad_trigger}, {affection_trigger}, {arousal_trigger}, {trust_trigger}\n Info: Erwähnen von 'tags' in antwort ist verboten.\n</tags>\n"
        + "<behave>\n"  + behave + "\n</behave>"
    )

    # Replace {{char}} and {{user}}
    mood = mood.replace("{{char}}", char).replace("{{user}}", user)


    # Debugging
    if debug:
        print(f"{mood}\n\n=====================================\n\n")

    # Format to Assistant
    mood = {"role": "assistant", "content": f"*{mood}*"}
    
    return mood

if lokal:
    mood_trigger()
