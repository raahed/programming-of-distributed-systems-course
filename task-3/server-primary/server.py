import os
from jsonrpcserver import method, Success, serve
import threading
import requests
import json

#url_test_rep1 = "https://oru-pds-serv-r1.raah.me/"
#url_test_rep2 = "https://oru-pds-serv-r2.raah.me/"

url_test_rep1 = "http://localhost:4001"
url_test_rep2 = "http://localhost:4002"


# client side


@method
def json_rpc_request(method, params, url):
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

@method
def read_rep(url):
    result = json_rpc_request("read", {}, url)
    if result is not None:
        print("Read result:", result)

@method
def write_rep(data, url):
    result = json_rpc_request("write", {"data": data}, url)
    if result is not None:
        print("Write result:", result)


# server side

# Define the file path
file_path = "server_file.txt"

# Lock for synchronization

@method
def read():
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return Success(content)
    except Exception as e:
        return {"error": str(e)}

@method
def write(data):
    try:
            # Write to the main server file
        with open(file_path, 'w') as file:
            file.write(data)
            try:
                write_rep(data, url_test_rep1)
            except Exception as e1:
                print(str(e1))
            try:
                write_rep(data, url_test_rep2)
            except Exception as e2:
                print(str(e2))        

        return Success("Write successful")
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    # Check if the server file exists, create it if not
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write("Initial content")

    # Start the JSON-RPC server
    serve(port=4000)













