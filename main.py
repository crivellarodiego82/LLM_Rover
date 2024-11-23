import websocket
import json
import time
import requests

# Carica configurazioni
with open("config.json", "r") as f:
    config = json.load(f)

ROVER_WS = f"ws://{config['rover_ip']}:{config['rover_port']}"
OLLAMA_MODEL = config["ollama_model"]

# Logica AI: chiama Ollama per decidere il comando
def ask_ollama(input_data):
    url = f"http://localhost:11434/api/completions"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": f"Decidi come controllare il rover con i seguenti dati sensoriali: {input_data}. Restituisci un JSON con i campi K, Q, D e A."
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        try:
            return json.loads(response.json()["completion"])
        except Exception as e:
            print("Errore nella risposta di Ollama:", e)
    return {"K": 0, "Q": 0, "D": 90, "A": 3}  # Default: ferma il rover

# Callback per i messaggi del WebSocket
def on_message(ws, message):
    print("Messaggio ricevuto:", message)
    try:
        # Processa il messaggio
        data = json.loads(message)
        decision = ask_ollama(data)
        print("Decisione AI:", decision)
        ws.send(json.dumps(decision))
    except json.JSONDecodeError:
        print("Messaggio non valido ricevuto:", message)

def on_error(ws, error):
    print("Errore WebSocket:", error)

def on_close(ws, close_status_code, close_msg):
    print("Connessione chiusa.")

def on_open(ws):
    print("Connessione al rover stabilita.")

# Connessione al WebSocket del rover
def main():
    ws = websocket.WebSocketApp(
        ROVER_WS,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.on_open = on_open
    ws.run_forever()

if __name__ == "__main__":
    main()
