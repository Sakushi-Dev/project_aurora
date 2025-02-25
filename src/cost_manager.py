from data_handler import get_slot_cost, save_slot_cost



def save_costs(c_input: float, c_output: float):
    """
    Saves the costs of the current conversation.
    Parameters:
        c_input: float
            The cost of the input.
        c_output: float
            The cost of the output.
    """
    save_slot_cost(c_input, c_output)


def calculate_cost(
        model_name: str,
        current_tokens: int,
        response_tokens: int
) -> float:
    """
    Calculates the cost of the current conversation.
    Parameters:
        model_name: str
            The name of the model.
        current_tokens: int
            The number of tokens used in the current conversation.
        response_tokens: int
            The number of tokens used in the response.
    """
    (
        current_input_cost,
        current_output_cost
    ) = get_slot_cost()

    mtok = 1000**2

    costs_dict = {
        "claude-3-7-sonnet-20250219": (3.00, 15.00),
        "claude-3-5-sonnet-20241022": (3.00, 15.00),
        "claude-3-5-haiku-20241022": (0.80, 4.00),
        "claude-3-haiku-20240307": (0.25, 1.25)
    }

    for key, value in costs_dict.items():
        if model_name == key:
            input_cost = (current_tokens / mtok) * value[0]
            output_cost = (response_tokens / mtok) * value[1]

    update_input_cost = current_input_cost + input_cost
    update_output_cost = current_output_cost + output_cost

    

    return update_input_cost, update_output_cost

