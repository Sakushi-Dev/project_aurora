import tiktoken

def count_tokens(system_prompt, history_prompt=None, assistant_prompt=None):
    """
    Berechnet die Anzahl der Tokens in den system_prompts, history und assistant_prompts.
    """

    tokenizer = tiktoken.get_encoding("cl100k_base")
    total_tokens = 0

    
    if assistant_prompt != None:
        # Tokens in den assistant_prompt
        for prompt in assistant_prompt:
            if prompt.get("content"):  # Sicherstellen, dass "content" ein String ist
                total_tokens += len(tokenizer.encode(prompt["content"].strip()))

    if history_prompt != None:
        # Tokens in der history_prompt
        for msg in history_prompt:
            if msg.get("content"):  # Sicherstellen, dass "content" ein String ist
                total_tokens += len(tokenizer.encode(msg["content"].strip()))

    # Tokens in den system_prompt
    for prompt in system_prompt:
        if prompt.get("text"):  # Sicherstellen, dass "text" ein String ist
            total_tokens += len(tokenizer.encode(prompt["text"].strip()))

    

    return total_tokens

def output_tokens(ki_output):
    """
    Gibt die Anzahl der Tokens in einer KI-Antwort aus.
    """

    tokenizer = tiktoken.get_encoding("cl100k_base")
    tokens = len(tokenizer.encode(ki_output.strip()))
    return tokens