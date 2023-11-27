import os
from jsonrpcserver import method, Success, serve
import threading

# Define the file path
file_path = "../server/server_file-rep1.txt"

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
            
        return Success("Write successful")
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    # Check if the server file exists, create it if not
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write("Initial content")

    # Start the JSON-RPC server
    serve(port=4001)