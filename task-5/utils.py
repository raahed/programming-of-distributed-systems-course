import random
import requests

philosophers = {
    0: 4000,
    1: 4001,
    2: 4002,
    3: 4003,
    4: 4004,
} 

num_of_philosophers = 5
prop_of_failure = 10

def json_rpc_request(method, params = None, philosophers: int = 0):
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": random.randint(0, 100000)
    }

    if params:
        payload["params"] = params

    
    if random.randint(0,100) > prop_of_failure:
        response = requests.post(f"http://localhost:{philosophers}", json=payload).json()
    else:
        print("RPC MESSAGE, NOT KNOWN TO THE PHILOSOPHERS: Unfortunately, the message got lost")
    
    if "error" in response:
        print("Error:", response["error"])
        return None

    return response["result"]