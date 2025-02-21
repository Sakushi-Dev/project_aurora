import tiktoken

def count_tokens(system_prompt, history, assistant_prompt = None):
    """
    Berechnet die Anzahl der Tokens in den system_prompts, history und assistant_prompts.
    """

    tokenizer = tiktoken.get_encoding("cl100k_base")
    total_tokens = 0

    # Um auch nur 2 werte zu erlauben
    if assistant_prompt != None:
        # Tokens in den assistant_prompts
        for prompt in assistant_prompt:
            if prompt.get("content"):  # Sicherstellen, dass "content" ein String ist
                total_tokens += len(tokenizer.encode(prompt["content"].strip()))

    # Tokens in den system_prompts
    for prompt in system_prompt:
        if prompt.get("text"):  # Sicherstellen, dass "text" ein String ist
            total_tokens += len(tokenizer.encode(prompt["text"].strip()))

    # Tokens in der history
    for msg in history:
        if msg.get("content"):  # Sicherstellen, dass "content" ein String ist
            total_tokens += len(tokenizer.encode(msg["content"].strip()))

    return total_tokens

def output_tokens(ki_output):
    """
    Gibt die Anzahl der Tokens in einer KI-Antwort aus.
    """

    tokenizer = tiktoken.get_encoding("cl100k_base")
    tokens = len(tokenizer.encode(ki_output.strip()))
    return tokens