import anthropic
from secure_api_key import load_api_key

API_KEY = load_api_key()


def init_anthropic_client(API_KEY) -> anthropic.Anthropic:
    
    return anthropic.Anthropic(api_key=API_KEY)