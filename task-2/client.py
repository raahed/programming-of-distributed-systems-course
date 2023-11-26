import requests

url = "http://localhost:8080"

def json_rpc_request(method, params):
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1,
    }
    response = requests.post(url, json=payload).json()
    print(response)

    if "error" in response:
        print("Error:", response["error"])
        return None

    return response["result"]


result_list_files = json_rpc_request("list_files", {"folder_path": "./"})
print("Result (list_files):", result_list_files)

