import random
import requests

participants = {
    "table": 4000,
    "dealer": 4001,
    "smoker_match": 4002,
    "smoker_paper": 4003,
    "smoker_tabaco": 4004,
} 

wait_timer = 1

def json_rpc_request(method, params = None, participant: int = 0):
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": random.randint(0, 100000)
    }

    if params:
        payload["params"] = params

    response = requests.post(f"http://localhost:{participant}", json=payload).json()
    
    if "error" in response:
        print("Error:", response["error"])
        return None

    return response["result"]