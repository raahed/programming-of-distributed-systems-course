import os
from jsonrpcserver import method, Success, serve
import threading
import requests
import json

#url_primary = "https://oru-pds-serv-prim.raah.me"
#url_rep1 = "https://oru-pds-serv-r1.raah.me/"
#url_rep2 = "https://oru-pds-serv-r2.raah.me/"

url_primary = "http://localhost:4000"
url_rep1 = "http://localhost:4001"
url_rep2 = "http://localhost:4002"
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
        return result

@method
def write_to_server(data, url):
    result = json_rpc_request("write", {"data": data}, url)
    if result is not None:
        print("Write result:", result)


# server side

@method
def read():
    try:
        content = read_to_server(url_primary)
        return Success(content)
    except Exception as e_primary:
        print(str(e_primary))
        try:
            content = read_to_server(url_rep1)
            return Success(content)
        except Exception as e_rep1:
            print(str(e_rep1))
            try:
                content = read_to_server(url_rep2)
                return Success(content)
            except Exception as e_rep2:
                return {"All servers failed:": str(e_rep2)}


@method
def write(data):
    try:
        write_to_server(data, url_primary)
    except Exception as e_primary:
        try:
            write_to_server(data, url_rep1)
            try:
                write_to_server(data, url_rep2)
            except Exception as e_rep2:
                return {"All servers failed:" : str(e_rep2)}
        except Exception as e_rep1:
            try:
                write_to_server(data, url_rep2)
            except Exception as e_rep2:
                return {"All servers failed:": str(e_primary)}
    return Success("Write sucessful")

if __name__ == "__main__":
    # Start the JSON-RPC server
    serve(port=3999)