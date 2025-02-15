from data_handler import load_set, get_slot
from preload import first_of_all

def main():

    from chat_loop import main_chat_loop
    from anthropic_api import init_anthropic_client, API_KEY

    
    # 1) API-Key laden + Client initialisieren
    client = init_anthropic_client(API_KEY)

    # 2) Modell auswählen
    modell_list = {
        1: "claude-3-5-sonnet-20241022",    # Hauptmodell für Chat
        2: "claude-3-5-haiku-20241022",     # Modell für bugfixes
        3: "claude-3-haiku-20240307"        # Modell für bugfixes
    }
    model = modell_list[3]
    
    # 3) Sets laden

    max_tokens      = load_set(max_t=True)

    # Frequency of Mood-Check
    frequency       = load_set(freq=True)

    # Impatience-Modus
    imp             = load_set(imp=True)

    # Sense of Time
    time_sense      = load_set(time_sense=True)

    # Highlight-Color
    hightlighted    = load_set(color=True)

    # Slot für Chat History
    slot = get_slot()

    # 4) Chat-Loop starten
    main_chat_loop(
            imp=imp,
            slot=slot,
            model=model,
            client=client,
            frequency=frequency,
            max_tokens=max_tokens,
            time_sense=time_sense,
            highlighted=hightlighted
    )


if __name__ == "__main__":
    check = first_of_all()
    if check:
        main()

