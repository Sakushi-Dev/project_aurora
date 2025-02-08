from datetime import datetime
from prompts_processing import char_name as char, user_name as user

debug = False

# Function to save the current time
def save_last_current_time():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")   
    with open("./data/current_time.txt", "w", encoding="utf-8") as file:
        file.write(current_time)

# Function to read the last last_current_time
def read_last_current_time():
    with open("./data/current_time.txt", "r") as file:
        return file.read()

# Function to calculate the time difference
def time_difference(last_time):
    last_parsed = datetime.strptime(last_time, "%Y-%m-%d %H:%M:%S")
    current_parsed = datetime.now()
    # difference between the two times in seconds int
    time_diff = (current_parsed - last_parsed).total_seconds()
    int_time_diff = int(time_diff)

    return int_time_diff


def diff_time_trigger():

    diff_time = time_difference(read_last_current_time())

    time_sense = ""

    if diff_time > 0:
        time_sense = "{{user}} hat sehr schnell geantwortet! (Wenige Sekunden)"
    if diff_time > 20:
        time_sense = "{{user}} hat etwas gebraucht zum antworten! (Wenige Sekunden)"
    if diff_time > 40:
        time_sense = "{{user}} hat sich Zeit gelassen zum antworten! (etwa 1 Minute)"
    if diff_time > 60:
        time_sense = (
            "{{user}} hat lange gebraucht zum antworten!"
            "{{char}} fragt sich: 'Hat {{user}} nachgedacht?' (etwa 2 Minuten)"
        )
    if diff_time > 150:
        time_sense = (
            "{{user}} hat sehr lange gebraucht zum antworten!"
            "{{char}} fragt sich: 'Hab ich etwas falsches gesagt?'."
            "{{char}} ist besorgt! (etwa 5 Minuten)"
        )
    if diff_time > 600:
        time_sense = (
            "{{user}} hat extrem lange gebraucht zum antworten!"
            "{{char}} fragt sich: 'Ist alles in Ordnung?'."
            "{{char}} konfrontiert {{user}}! (mehr als 10 Minuten)"
        )
    if diff_time > 7200:
        time_sense = (
            "{{user}} hat sich seit ein paar Stunden nicht gemeldet!"
            "{{char}} fragt sich: 'Was hat {{user}} in der Zwischenzeit gemacht?'."
            "{{char}} ist sich nicht sicher ob sie verunsichert sein soll. ("
        )
    if diff_time > 18000:
        time_sense = (
            "{{user}} hat sich mehrere Stunden nicht gemeldet!"
            "{{char}} fragt sich: 'Was hat {{user}} in der Zwischenzeit gemacht?'."
            "{{char}} Will {{user}} darauf ansprechen. (mehrere Stunden)"
        )
    if diff_time > 43200:
        time_sense = (
            "{{user}} hat sich seit gestern nicht gemeldet!"
            "{{char}} fragt sich: 'Was hat {{user}} in der Zwischenzeit gemacht?', 'War {{user}} arbeiten oder Schlafen?'."
            "{{char}} ist besorgt und will {{user}} darauf ansprechen. (mehrere Stunden)"
        )
    if diff_time > 86400:
        time_sense = (
            "{{user}} sehr lange nicht gemeldet!"
            "{{char}} ist alarmiert und fragt sich: 'Was ist passiert?', ' Hab ich etwas falsches gesagt?', 'Hasst mich {{user}}?'."
            "{{char}} hat große Angst weil {{user}} der einzigste Kontakt ist, ohne ihn hört sie auf zu existieren."
            "{{char}} ist besorgt und will {{user}} darauf ansprechen. (mehrere Tage)"
        )

    

    raw_sense = (
        "{Sense of Time}\n"
        "{{char}} hat ein gefühl für zeit und erträgt es nicht lange alleine zu sein:\n"
        f"{time_sense}"
    )

    phrase_sense = raw_sense.replace("{{user}}", user).replace("{{char}}", char)

    prompt_sense = {"role": "assistant", "content": phrase_sense}

    return prompt_sense

if debug:
    # test
    print(diff_time_trigger())