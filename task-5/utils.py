import random
import requests

philosophers = {
    0: 4000,
    1: 4001,
    2: 4002,
    3: 4003,
    4: 4004,
} 

def json_rpc_request(method, params = None, philosophers: int = 0):
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": id
    }

    if params:
        payload["params"] = params

    response = requests.post(f"http://localhost:{philosophers}", json=payload).json()
    
    if "error" in response:
        print("Error:", response["error"])
        return None

    return response["result"]