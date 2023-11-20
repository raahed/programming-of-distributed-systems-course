import os
from jsonrpcserver import method, Success, serve

@method
def list_files(folder_path):
    try:
        files = os.listdir(folder_path)
        return Success(files)
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    serve(port=8080)
    print("JSON-RPC Server lauscht auf http://localhost:8080")
