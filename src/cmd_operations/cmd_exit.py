from rich.console import Console

console = Console(width=120)

def execute_exit():
    console.print("[green]Closing the program...[/green]")
    return "exit"