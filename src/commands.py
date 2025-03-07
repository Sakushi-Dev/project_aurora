import os
import time

from globals import console

from task_organizer import (
    print_latest_messages
)

from cmd_operations import (
    cmd_exit,
    cmd_report,
    cmd_again,
    cmd_slot,
    cmd_delete,
    cmd_restart,
    cmd_reset,
    cmd_mood,
    cmd_think
)

handle_exit     = cmd_exit.execute_exit
handle_report   = cmd_report.execute_report
handle_again    = cmd_again.execute_again
handle_slot     = cmd_slot.execute_slot
handle_delete   = cmd_delete.execute_delete
handle_restart  = cmd_restart.execute_restart
handle_reset    = cmd_reset.execute_reset
handle_mood     = cmd_mood.execute_mood
handle_think    = cmd_think.execute_think

def get_commands():
    import sys
    from data_handler import load_set
    
    char = load_set(char=True)

    for _ in range(2):
        # delete last 1 lines
        sys.stdout.write("\033[F\033[K")

    commands = "\n[green]Commands:[/green]\n \n"

    command_list = {
        "exit": "   - End chat",
        "delete": " - Clear chat history",
        "reset": "  - Reset Aurora",
        "restart": "- Restart Aurora",
        "again": "  - Repeat the last message",
        "config": " - Change settings",
        "slot": "   - Switch chat slot",
        "report": " - Report an issue on GitHub",
        "mood": f"   - View {char}'s mood",
        "think":"   - Thoughts from the last message",
        "back": "   - Go back to chat",
    }

    slash = "[red]/[/red]"

    for key, value in command_list.items():
        commands += (f"{slash}[green]{key}[/green] {value}\n")
    
    return commands

def handle_unknown():
    console.print("[red]Befehl nicht erkannt. Gib /help ein, um verfügbare Befehle zu sehen.[/red]")

def handle_back():
    import sys

    cmd_string = get_commands()
    line = len(cmd_string.splitlines())

    for _ in range(line-1):
        # delete last line
        sys.stdout.write("\033[F\033[K")


    

def command_dispatcher(user_input: str, highlighted:str, history_len:int):
    # Settings-Import:
    import sys
    from settings import set_config
    from history_manager import (
    get_history_length,
    organize_chat_and_char
    )
    
    commands = {
    "/exit": handle_exit,
    "/config": set_config,
    "/again": handle_again,
    "/delete": handle_delete,
    "/slot": handle_slot,
    "/reset": handle_reset,
    "/report": handle_report,
    "/mood": handle_mood,
    "/think": handle_think,
    "/back": handle_back,
    }

    command = user_input.lower().split()[0]
    if command in commands:
        if command == "/again"and history_len > 2:
            sub_user_input = None
            history, sub_user_input = commands[command](highlighted)
            history_len = get_history_length(history)
            return [sub_user_input, history, history_len]
        elif command == "/again" and history_len <= 2:
            console.print("[red]No message to repeat.[/red]")
            time.sleep(2)
            for _ in range(2):
                # delete last 2 lines
                sys.stdout.write("\033[F\033[K")
            handle_back()
            return None
        else:
            result = commands[command]()
    
    if command in ["/delete", "/slot", "/reset"] and result in ["delete", "slot", "reset"] or command == "/restart":
        console.print(f"Aurora.py wird in neu gestartet", end="")
        for _ in range(5, 0, -1):
            console.print(f"[red].[/red]", end="")
            time.sleep(1)
        handle_restart()

    elif command == "/exit":
        time.sleep(3)
        os._exit(0) # Beendet das Programm

    elif command == "/config" or command == "/think":
        os.system('cls' if os.name == 'nt' else 'clear')
        history, list_msg = organize_chat_and_char()
        print_latest_messages(list_msg, highlighted=highlighted)
        return None # Falls config beendet wird, soll der Chat-Loop von vorne starten
    
    elif command == "/mood" or command == "/report":
        console.print("Countinue with [green]Enter[/green]")
        input()
        handle_restart()
        return None # Chat-Loop startet von vorne
    
    elif command == "/back":
        return None
    
    elif user_input.startswith("/"):
        handle_unknown()
        return None # Chat-Loop startet von vorne
    
    else:
        return True # Damit der Chat-Loop weiter läuft