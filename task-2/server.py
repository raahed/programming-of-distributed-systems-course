import os
from jsonrpcserver import method, Success, serve

@method
def list_files(folder_path):
    try:
        files = os.listdir(folder_path)
        return Success(files)
    except Exception as e:
        return {"error": str(e)}


serve(port=8080)
