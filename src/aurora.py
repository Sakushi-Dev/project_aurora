from preload import first_of_all

def main():
    '''
    Main-Function to start the Chat-Loop
    Gets all necessary Sets and starts the Chat-Loop
    '''
    from data_handler import load_set, get_slot
    from chat_loop import main_chat_loop
    from anthropic_api import init_anthropic_client, API_KEY

    
    # 1) API-Key Load and Client-Init
    client = init_anthropic_client(API_KEY)

    # 2) Modell auswählen
    modell_list = {
        1: "claude-3-7-sonnet-20250219",    # Sonnet 3.7    Cost: Input $3/MTok     Output $15/MTok
        2: "claude-3-5-sonnet-20241022",    # Sonnet 3.5    Cost: Input $3/MTok     Output $15/MTok
        3: "claude-3-5-haiku-20241022",     # Haiku 3.5     Cost: Input $0.80/MTok  Output $4/MTok
        4: "claude-3-haiku-20240307"        # Haiku 3       Cost: Input $0.25/MTok  Output $1.25/MTok
    }
    model = modell_list[2]
    
    # 3) Load all necessary Sets
    keys = [
        "max_t",
        "freq",
        "imp",
        "time_sense",
        "color"
    ]
    #NOTE: The order of the Keys is important 
    (
        max_tokens,
        frequency,
        imp,
        time_sense,
        highlighted
    ) = [load_set(**{key: True}) for key in keys]

    # Slot for the Chat
    slot = get_slot()

    # 4) Start Chat-Loop
    main_chat_loop(
            imp=imp,
            slot=slot,
            model=model,
            client=client,
            frequency=frequency,
            max_tokens=max_tokens,
            time_sense=time_sense,
            highlighted=highlighted
    )


if __name__ == "__main__":
    check = first_of_all()
    if check:
        main()

