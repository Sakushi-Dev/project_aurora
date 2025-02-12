import anthropic
from secure_api_key import load_api_key


def init_anthropic_client() -> anthropic.Anthropic:
    
    api_key = load_api_key()

    return anthropic.Anthropic(api_key=api_key)