import re
import time
import textwrap
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.live import Live

from tiktoken_function import count_tokens

from data_handler import load_set


from prompts_processing import (
    user_name as user,
)



# Rich-Console-Objekt:
console = Console(width=120)

def truncate_history_for_api(
        history: list,
        system_text: str,
        assistant_text: list,
        max_tokens: int = 2048
) -> list:
    """
    Trunkiert so lange Nachrichten, bis die Gesamttokenanzahl unter max_tokens fällt.
    """
    truncate_h = history[:]
    while count_tokens(system_text, truncate_h, assistant_text) > max_tokens:
        if len(truncate_h) < 2:
            break
        truncate_h.pop(0)  # Lösche ersten Eintrag
        
    return truncate_h

def print_latest_messages(
        history: list,
        limit: int = 40,
        highlighted: str = "purple"
        ):
    """
    Gibt die letzten N Nachrichten formatiert in der Konsole aus.
    """
    # Lade Charakter Namen
    char = load_set(char=True)

    # Farbe für Highlighting
    color = highlighted

    # Falls history leer ist
    if not history:
        return

    last_n = history[-limit:]

    for msg in last_n:
        # Sicherstellen, dass msg ein Dictionary ist
        if not isinstance(msg, list):
            console.print(f"[red]Warnung: Unerwarteter Eintrag in history: {msg}[/red]")
            continue

        
        msg_role    = msg[0]
        
        content     = msg[1]
        # hole analyse, falls vorhanden
        analysis    = msg[3] if len(msg) > 3 else None
        
        # Rolle bestimmen
        if msg_role == "user":
            role_str = user
        else:
            role_str = char

        first_msg = False    

        if analysis:
            if role_str == user:
                input_t = analysis["input_t"]
                msg_len = analysis["msg"]
            elif role_str == char:
                output_t = analysis["output_t"]
                # lösche ersten 2 "\n" Zeichen
                msg_len = analysis["msg"]
        else:
            first_msg = True
        

        content = content.lstrip(" ")
        content = content.lstrip("\n")
        content = content.rstrip("\n")
        

        # Gemeinsames Highlighting
        highlighted_text = re.sub(
            r"\*\s*(.*?)\*",
            r"[orange1]\1[/orange1]",
            content,
            flags=re.DOTALL
        )

        if role_str == user:
            
            console.print(Panel(highlighted_text, title=f"[bold]{role_str}[/bold]", expand=True, border_style="white"))
            console.print(
            f"\n[black]{'─'*120}[/black]\n"
            f"[black]Msg: {msg_len} | Input-Tokens: {input_t}[/black]\n"
            f"[black]{'─'*120}[/black]\n"
            )

        elif role_str == char:
            
            rich_text = Text.from_markup(f"[{color}]{highlighted_text}[/{color}]")
            console.print(Panel(rich_text, title=f"[bold {color}]{role_str}[/bold {color}]", expand=True, border_style="white"))
            if first_msg == True:
                console.print(
                    f"\n[black]{'─'*120}[/black]\n"
                    f"[black] Start chat with {char}[/black]\n"
                    f"[black]{'─'*120}[/black]\n"
                )
            if first_msg == False:
                console.print(
                f"\n[black]{'─'*120}[/black]\n"
                f"[black]Msg: {msg_len} | Output-Tokens: {output_t}[/black]\n"
                f"[black]{'─'*120}[/black]\n"
                )

#test
#print_latest_messages([["user", "hallo *sagte ich*\nWie heißt du?", {"input_t": 10, "msg": 1}, True], ["char", "\n\nhallo *sagte ich*\nWie heißt du?", {"output_t": 10, "msg": 2}, True]])

def animated_typing_panel(char: str, response_text: str, color: str = "cyan", delay: float = 0.02):
    """
    Zeigt die zeichenweise Ausgabe eines Charakters innerhalb eines `rich`-Panels mit Animation.
    Der gesamte Text wird in der benutzerdefinierten Farbe angezeigt,
    wobei Markup (z.B. [orange1]) erhalten bleibt.
    """
    
    # Textverarbeitung und Hervorhebung
    wrapped_text = textwrap.dedent(response_text).strip()
    # Markiere Text zwischen Sternchen in Orange. Achte darauf, dass der gesamte Text von [color] umschlossen wird.
    highlighted_text = re.sub(r"\*\s*(.*?)\*", r"[orange1]\1[/orange1]", wrapped_text, flags=re.DOTALL)
    
    # Umbruch & Formatierung:
    lines = highlighted_text.splitlines()
    formatted_text = "\n".join(textwrap.fill(line, width=84) for line in lines)
    # Hier wird der gesamte Text in den Standardfarbblock (user-definierte Farbe) gehüllt.
    final_text = Text.from_markup(f"[{color}]{formatted_text}[/{color}]")

    # Zeichenweise Animation mithilfe von Slicing:
    with Live(Panel("", expand=True), refresh_per_second=20) as live:
        plain_length = len(final_text.plain)
        for i in range(1, plain_length + 1):
            # Slicing des Text-Objekts: Das behält alle Formatierungen im jeweiligen Bereich bei.
            current_subtext = final_text[:i]
            live.update(
                Panel(
                    current_subtext,
                    title=f"[bold {color}]{char}[/bold {color}]",
                    width=120,
                    expand=True,
                    border_style="white"
                )
            )
            time.sleep(delay)
        # Abschließende Aktualisierung (kompletter Text)
        live.update(
            Panel(
                final_text,
                title=f"[bold {color}]{char}[/bold {color}]",
                width=120,
                expand=True,
                border_style="white"
            )
        )