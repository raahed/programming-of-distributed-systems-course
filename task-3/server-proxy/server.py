import os
from jsonrpcserver import method, Success, serve
import threading
import requests
import json

url_primary = "https://oru-pds-serv-prim.raah.me"
url_rep1 = "https://oru-pds-serv-r1.raah.me/"
url_rep2 = "https://oru-pds-serv-r2.raah.me/"

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
def read_to_server(url):
    result = json_rpc_request("read", {}, url)
    if result is not None:
        print("Read result:", result)

@method
def write_to_server(data, url):
    result = json_rpc_request("write", {"data": data}, url)
    if result is not None:
        print("Write result:", result)


# server side

# Define the file path
file_path = "server_file.txt"

# Lock for synchronization

temp = "HAHA"; 

def read():
    try:
        with open(file_path, 'r') as file:
            try:
                try:
                    read_to_server(url_primary)
                except Exception as e:
                    return {"Main server error:": str(e)}
                try:
                    read_to_server(url_rep1)
                except Exception as e:
                    return {"Rep1 server error:": str(e)}
                try:
                    read_to_server(url_rep2)
                except Exception as e:
                    return {"Rep2 server error:": str(e)}
            except Exception as e:
                return {"All server error:" : str(e)}
            
            return Success("Read successful")
    except Exception as e:
        return {"error": str(e)}

@method
def write(data):
    try:
        try:
            try:
                write_to_server(data, url_primary)
            except Exception as e:
                return {"Main server error:": str(e)}
            try:
                write_to_server(data, url_rep1)
            except Exception as e:
                return {"Rep1 server error:": str(e)}
            try:
                write_to_server(data, url_rep2)
            except Exception as e:
                return {"Rep2 server error:": str(e)}
            
            return Success("Write successful")
        except Exception as e:
            return {"All server error:" : str(e)}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    # Start the JSON-RPC server
    serve(port=3999)