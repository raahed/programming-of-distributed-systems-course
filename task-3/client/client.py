import requests
import json

url_test = "http://localhost:3999"


def json_rpc_request(method, params):
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1,
    }
    response = requests.post(url_test, json=payload).json()
    
    # Check for errors in the response
    if "error" in response:
        print("Error:", response["error"])
        return None

    return response["result"]

def read():
    result = json_rpc_request("read", {})
    if result is not None:
        print("Read result:", result)

def writing(data):
    result = json_rpc_request("write", {"data": data})
    if result is not None:
        print("Write result:", result)

# Example calls
read()  # Perform a write operation