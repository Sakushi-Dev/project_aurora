import os
import anthropic
from dotenv import load_dotenv


def load_api_key(env_path: str = "./API/api_key.env") -> str:
    """
    Lädt den API-Key aus einer .env-Datei.
    """
    load_dotenv(dotenv_path=env_path)
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("API-Schlüssel nicht gefunden. Bitte .env prüfen.")
    return api_key


def init_anthropic_client(api_key: str) -> anthropic.Anthropic:
    """
    Erstellt einen Anthropic-Client mit dem angegebenen API-Key.
    """
    return anthropic.Anthropic(api_key=api_key)