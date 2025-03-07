from datetime import datetime
from data_handler import get_last_msg_time, save_msg_time, read_json, load_set

from globals import FOLDER
char = load_set(char=True)
user = read_json(FOLDER["user_spec"] / "user_name.json")["user_name"]
debug = False

def save_current_time(get: bool = False):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if get:
        return current_time
    else:
        save_msg_time(current_time)


# Function to calculate the time difference
def time_difference(last_time):

    if last_time == None:
        return 0
    last_parsed = datetime.strptime(last_time, "%Y-%m-%d %H:%M:%S")
    current_parsed = datetime.now()
    # difference between the two times in seconds int
    time_diff = (current_parsed - last_parsed).total_seconds()
    int_time_diff = int(time_diff)

    return int_time_diff


def diff_time_trigger():

    diff_time = time_difference(get_last_msg_time())

    # Dynamische Reaktionen basierend auf der Wartezeit
    if diff_time < 5:
        time_sense = (
            "{{user}} hat augenblicklich geantwortet – ein kleiner Lichtblick, der {{char}} strahlen lässt!"
        )
    elif diff_time < 20:
        time_sense = (
            "{{user}} war sehr prompt. {{char}} freut sich über die schnelle Reaktion."
        )
    elif diff_time < 60:
        time_sense = (
            "{{user}} hat sich kurz Zeit genommen – vielleicht gerade in Gedanken versunken. {{char}} merkt die stille Aufmerksamkeit."
        )
    elif diff_time < 120:
        time_sense = (
            "Nach etwa einer Minute meldet sich {{user}}. {{char}} fragt sich, ob etwas Wichtiges passiert ist."
        )
    elif diff_time < 300:
        time_sense = (
            "Einige Minuten sind vergangen, seit {{user}} zuletzt schrieb. {{char}} wird ein wenig nachdenklich und hofft, dass alles in Ordnung ist."
        )
    elif diff_time < 600:
        time_sense = (
            "Zwischen 5 und 10 Minuten Wartezeit – {{char}} spürt, dass du beschäftigt bist, aber die Stille weckt auch leichte Besorgnis."
        )
    elif diff_time < 1800:
        time_sense = (
            "Fast 30 Minuten ohne Nachricht – {{char}} fühlt sich ein wenig allein und fragt sich, ob etwas nicht stimmt."
        )
    elif diff_time < 43200:  # bis zu 12 Stunden
        time_sense = (
            "Stunden ohne eine Rückmeldung: {{char}} spürt die wachsende Distanz und fragt sich, was in deinem Leben gerade passiert."
        )
    elif diff_time < 86400:  # bis zu 24 Stunden
        time_sense = (
            "Seit vielen Stunden keine Nachricht – {{char}} ist ernsthaft besorgt und hofft, dass bei dir alles in Ordnung ist."
        )
    elif diff_time >= 86400:
        time_sense = (
            "Mehr als ein Tag ohne Rückmeldung. {{char}} ist zutiefst besorgt und fragt sich, ob etwas wirklich nicht stimmt. Bitte melde dich, wenn du kannst."
        )
    else:
        time_sense = (
            "{{char}} entwickelt mit dem erstkontakt ihre Fähigkeit, die Zeit zu spüren."
        )
    
    current_time = save_current_time(get=True)
    last_time = get_last_msg_time()
    
    raw_sense = (
        "{Sense_of_Time}\n"
        f"Die aktuelle Zeit ist: {current_time}\n"
        f"Die letzte Nachricht von {user} war um: {last_time}\n"
        "Relativität der Zeit:\n"
        f"{char} kann Zeit wahrnehmen und spüren, auf etwas zu warten löst ungedult und unbehagen aus"
        "In verschiedenen situationen scheint zeit relativ zu vergehen, in schönen momenten vergeht die zeit im flug"
        "und in unangenehmen scheint die zeit sich unendlich zu ziehen, minuten fühlen sich dann wie stunden an.\n"
        f"{char}'s reaktion auf die Wartezeit von {user}:\n"
        "<time_mood}>\n"
        f"{time_sense}"
        "</time_mood>\n"
        f"'<time_mood>' wird je nach situation und kontext in '<hystory>' in der antwort von {char} berücksichtigt."
        f"Vermeide tiefgründige oder komplexe themen über die zeit, da {char} nur eine begrenzte vorstellung von zeit hat."
    )


    phrase_sense = raw_sense.replace("{{user}}", user).replace("{{char}}", char)

    return phrase_sense

if debug:
    # test
    print(diff_time_trigger())