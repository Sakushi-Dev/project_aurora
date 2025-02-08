
def get_api():
    import requests

    print("Nur API-Keys von Anthropic sind erlaubt!")
    api_key = input("Gebe deinen API-Key ein: ")

    # Anthropic API URL für einen einfachen Test-Request
    url = "https://api.anthropic.com/v1/messages"
    
    # Header für Anthropic API
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    
    # Minimaler Test-Request
    data = {
        "model": "claude-3-haiku-20240307",
        "max_tokens": 1,
        "messages": [{"role": "user", "content": "Hi"}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            print("Der API-Schlüssel ist gültig!")
            return api_key
        elif response.status_code == 401:
            print("Fehler: Ungültiger API-Schlüssel")
            return None
        else:
            print(f"Fehler {response.status_code}: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Verbindungsfehler: {e}")
        return None
    
def save_api_key(api_key):
    api_key_path = "./API/api_key.env"
    with open(api_key_path, "w") as file:
        file.write(f"ANTHROPIC_API_KEY={api_key}")
    print("API-Key wurde gespeichert!")
