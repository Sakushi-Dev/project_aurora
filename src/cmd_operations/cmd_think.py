import os

from data_handler import load_set
from globals import console

from rich.panel import Panel


def execute_think():
    from chat_loop import inner_reflection

    char = load_set(char=True)

    os.system('cls' if os.name == 'nt' else 'clear')

    if inner_reflection == "":
        inner_reflection = f"No current thoughts from {char}. Try again later."

    console.print(
        Panel(
            inner_reflection,
            title=f"[bold yellow]{char}'s thoughts[/bold yellow]",
            expand=True, border_style="orange1"
        )
    )

    console.input("\n[bold yellow]Press Enter to continue...[/bold yellow]")