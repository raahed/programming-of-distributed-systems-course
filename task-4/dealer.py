from utils import json_rpc_request, participants
import jsonrpcserver as rpc
import random

def putIngredient(i):
    print(f"[Dealer] Putting {i} on the table!")
    json_rpc_request("putIngredient", {"i": i}, participants["table"])

@rpc.method
def serveTable():
    ingredients = random.sample([0, 1, 2], 2)

    # Serving two ingredients
    putIngredient(ingredients[0])
    putIngredient(ingredients[1])
    
    return rpc.Success()

if __name__ == "__main__":
    # Serving the table for the first time
    serveTable()
    rpc.serve(port=participants["dealer"])