from data_handler import get_slot_cost, save_slot_cost



def save_costs(c_input: float, c_output: float):
    """
    Speichert die Kosten in der Datei `history/costs.py`.
    """
    save_slot_cost(c_input, c_output)


def calculate_cost(model_name: str, current_tokens: int, response_tokens: int) -> float:
    """
    Berechnet die Kosten basierend auf dem Modell.
    Aktualisiert die globalen Variablen total_input_cost und total_output_cost.
    """
    total_input_cost, total_output_cost = get_slot_cost()

    if model_name == "claude-3-5-haiku-20241022":
        input_cost = (current_tokens / 1_000_000) * 0.80
        output_cost = (response_tokens / 1_000_000) * 4.00

    elif model_name == "claude-3-5-sonnet-20241022":
        input_cost = (current_tokens / 1_000_000) * 3.00
        output_cost = (response_tokens / 1_000_000) * 15.00

    elif model_name == "claude-3-haiku-20240307":
        input_cost = (current_tokens / 1_000_000) * 0.25
        output_cost = (response_tokens / 1_000_000) * 1.25

    # Weitere Modelle bei Bedarf hier ergänzen

    total_input_cost += input_cost
    total_output_cost += output_cost

    

    return total_input_cost, total_output_cost

