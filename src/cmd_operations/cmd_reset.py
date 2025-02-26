import os
import time

from globals import console


def execute_reset():
    from init_data import spit_path
    from data_handler import (
        set_path as set_p,
        slot_path as slot_p,
        emo_score_path as emo_p,
        cost_path,
        last_msg_time_path,
        user_path as user_p,
        char_memory_path as mem_p,
    )

    # Formatiere zu relativen Order-Pfaden um alle Dateien innerhalb des Ordners zu löschen
    costs_p, _ = spit_path(cost_path)
    last_p, _ = spit_path(last_msg_time_path)

    os.system('cls' if os.name == 'nt' else 'clear')
    
    console.print(
        "[red]Achtung! Willst du wirklich [orange1]Aurora[/orange1] zurücksetzen?[/red]\n"
        "[orange1]Info:[/orange1] Alle Dialoge und Einstellungen werden gelöscht.\n"
        "API-Key bleibt erhalten, kann aber auch auf Wunsch gelöscht werden.\n"
        )
    reset = ""

    reset = console.input("[red]Willst du einen Reset durchführen? (Y/N): [/red]")
    if reset.lower() == "y":

        # Sicherheitsabfrage
        reset = console.input("[red]Bist du dir sicher? (Y/N): [/red]")
        if reset.lower() == "y":

            # Screen leeren
            os.system('cls' if os.name == 'nt' else 'clear')


            route_map = {
                "Kosten der Dialoge": costs_p, 
                "Zeiten für 'Impatience'": last_p,
                "Emotions-Score Daten": emo_p,
                "Settings": set_p,
                "User-Data": user_p,
                "Chat-Verläufe": slot_p,
                "Erinnerungen": mem_p,
            }
            
            # Löschen der Dateien
            for key, value in route_map.items():
                try:

                    if os.path.isdir(value):
                        for root, dirs, files in os.walk(value, topdown=False):
                            for name in files:
                                os.remove(os.path.join(root, name))
                            for name in dirs:
                                os.rmdir(os.path.join(root, name))
                        os.rmdir(value)
                    elif os.path.isfile(value):
                        os.remove(value)

                    console.print(f"\n[orange1]Lösche der {key} wird durchgeführt[/orange1]", end="")
                    for i in range(0, 3):
                        console.print(f"[red].[/red]", end="")
                        time.sleep(0.7)
                    console.print(f"\n[green]{key} gelöscht.[/green]")
                except FileNotFoundError:
                    console.print(f"\n[red]{key} nicht gefunden.[/red]")

            # Löschen von '__pycache__'
            try:
                os.system("rm -r ./src/__pycache__")
                console.print("\n[green]Cache gelöscht.[/green]")
            except FileNotFoundError:
                console.print("\n[red]Cache nicht gefunden.[/red]")
                pass

            console.print("[orange]Löschvorgang abgeschlossen.[/orange]")
            
            #==================================================================================================

            # Fragen ob API-Key gelöscht werden soll

            api_key = console.input("[red]Willst du den API-Key löschen? (Y/N): [/red]")
            if api_key.lower() == "y":
                # API-Key löschen file
                os.remove("./API/api_key.env")
                os.rmdir("./API")

                console.print("[orange]API-Key gelöscht.[/orange]")

            else:
                console.print("[green]API-Key bleibt erhalten.[/green]")
                
            
            os.system('cls' if os.name == 'nt' else 'clear')

            while True:
                choice = console.input(
                    "[green]Gebe [orange1]1[/orange1] ein, um Aurora neu zu starten"
                    "\nWenn du beenden möchtest, gebe [orange1]2[/orange1] ein: [/green]"
                    )
                if choice == "1":
                    return "reset"
                elif choice == "2":
                    os._exit(0)
                else:
                    console.print("[red]Ungültige Eingabe![/red]")
                    continue
        else:
            return "cancel"
    else:
        return "cancel"