import requests
import json

url = "http://localhost:8080"

def json_rpc_request(method, params):
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1,
    }
    response = requests.post(url, json=payload).json()
    
    # Check for errors in the response
    if "error" in response:
        print("Error:", response["error"])
        return None

    return response["result"]

def read():
    result = json_rpc_request("read", {})
    if result is not None:
        print("Read result:", result)

def write(data):
    result = json_rpc_request("write", {"data": data})
    if result is not None:
        print("Write result:", result)

# Example calls
write("Das schreiben geht!")  # Perform a write operation
