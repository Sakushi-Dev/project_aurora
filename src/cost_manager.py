import os
import sys


def track_costs():
    """
    Funktion, um die Kosten für Eingabe und Ausgabe zu verfolgen.
    Stellt sicher, dass die Werte `total_input_cost` und `total_output_cost` geladen werden, 
    falls das Modul `history.costs` verfügbar ist.
    
    Returns:
        tuple: total_input_cost, total_output_cost
    """
    
    if os.path.exists("./src/history/costs.py"):
        if "history.costs" in sys.modules:
            del sys.modules["history.costs"]
        from history.costs import total_input_cost, total_output_cost  # type: ignore
    else:
        total_input_cost = 0.0
        total_output_cost = 0.0 
    
    return total_input_cost, total_output_cost
    


def save_costs(total_input_cost: float, total_output_cost: float):
    """
    Speichert die Kosten in der Datei `history/costs.py`.
    """
    if not os.path.exists("./src/history"):
        os.makedirs("./src/history")

    costs_path = "./src/history/costs.py"

    if not os.path.exists(costs_path):
        # Neu anlegen
        costs = (
            f"total_input_cost = {total_input_cost}\n"
            f"total_output_cost = {total_output_cost}"
        )
        with open(costs_path, "w", encoding="utf-8") as f:
            f.write(costs)
    else:
        # Überschreiben
        costs = (
            f"total_input_cost = {total_input_cost}\n"
            f"total_output_cost = {total_output_cost}"
        )

        with open(costs_path, "w", encoding="utf-8") as f:
            f.write(costs)


def calculate_cost(model_name: str, current_tokens: int, response_tokens: int) -> float:
    """
    Berechnet die Kosten basierend auf dem Modell.
    Aktualisiert die globalen Variablen total_input_cost und total_output_cost.
    """
    total_input_cost, total_output_cost = track_costs()

    if model_name == "claude-3-5-haiku-20241022":
        input_cost = (current_tokens / 1_000_000) * 0.80
        output_cost = (response_tokens / 1_000_000) * 4.00

    elif model_name == "claude-3-5-sonnet-20241022":
        input_cost = (current_tokens / 1_000_000) * 3.00
        output_cost = (response_tokens / 1_000_000) * 15.00

    # Weitere Modelle bei Bedarf hier ergänzen

    total_input_cost += input_cost
    total_output_cost += output_cost

    

    return total_input_cost, total_output_cost

