import jsonrpcserver as rpc
from utils import json_rpc_request, participants
import time

@rpc.method
def checkIngredient():
    result1 = json_rpc_request("checkIngredient", {"i": 0}, participants["table"])
    if result1:
        result2 = json_rpc_request("checkIngredient", {"i": 1}, participants["table"])
        if result2:
            json_rpc_request("takeIngredient", {"i": 0}, participants["table"])
            json_rpc_request("takeIngredient", {"i": 1}, participants["table"])
            time.sleep(1)
            json_rpc_request("serveTable", participants["dealer"])

@rpc.method
def startCheckIngredientLoop():
    while(True):
        checkIngredient()

if __name__ == "__main__":
    # Check if the server file exists, create it if not
    rpc.serve(port=participants["smoker_tabaco"])