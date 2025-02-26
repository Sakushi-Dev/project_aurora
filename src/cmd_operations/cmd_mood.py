from globals import console

def execute_mood():
    from rich.table import Table
    from data_handler import load_current_emo_score

    score = load_current_emo_score()

    # Threshold definitions for less-comparator emotions (Angry, Sad)
    less_thresholds = {
        "Angry_Level": {"yellow": 20, "red": 60},
        "Sad_Level": {"yellow": 20, "red": 60},
    }

    # Threshold definitions for greater-comparator emotions (Affection, Arousal, Trust)
    greater_thresholds = {
        "Affection_Level": {"green": 600, "orange1": 400, "red": 10},
        "Arousal_Level": {"green": 70, "orange1": 40, "red": 5},
        "Trust_Level": {"green": 600, "orange1": 400, "red": 10},
    }

    def get_color_less(value, thresholds):
        if value < thresholds["yellow"]:
            return "green"
        elif value < thresholds["red"]:
            return "yellow"
        else:
            return "red"

    def get_color_greater(value, thresholds):
        if value > thresholds["green"]:
            return "pink"
        elif value > thresholds["orange1"]:
            return "green"
        elif value > thresholds["red"]:
            return "orange1"
        else:
            return "red"

    # Calculate colors for each emotion based on value and appropriate thresholds
    angry_color = get_color_less(score["Angry_Level"], less_thresholds["Angry_Level"])
    sad_color = get_color_less(score["Sad_Level"], less_thresholds["Sad_Level"])
    affection_color = get_color_greater(score["Affection_Level"], greater_thresholds["Affection_Level"])
    arousal_color = get_color_greater(score["Arousal_Level"], greater_thresholds["Arousal_Level"])
    trust_color = get_color_greater(score["Trust_Level"], greater_thresholds["Trust_Level"])

    # Create a Rich table for displaying emotion scores
    table = Table(title="Emotions Score")
    table.add_column("Emotions", justify="center", style="bold")
    table.add_column("Score", justify="right")

    table.add_row(f"[{angry_color}]Anger[/{angry_color}]", str(score["Angry_Level"]))
    table.add_row(f"[{sad_color}]Sadness[/{sad_color}]", str(score["Sad_Level"]))
    table.add_row(f"[{affection_color}]Affection[/{affection_color}]", str(score["Affection_Level"]))
    table.add_row(f"[{arousal_color}]Arousal[/{arousal_color}]", str(score["Arousal_Level"]))
    table.add_row(f"[{trust_color}]Trust[/{trust_color}]", str(score["Trust_Level"]))

    console.print(table)