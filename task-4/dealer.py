from utils import json_rpc_request, participants
import jsonrpcserver as rpc
import random

def generateTwoIngredients():
    return random.sample([0, 1, 2], 2)

@rpc.method
def putIngredient(i):
    result = json_rpc_request("putIngredient", {"i": i}, participants["table"])
    if result is not None:
        print(f"Ingredient {i}: {result}")

@rpc.method
def serveTable():
    ingredients = generateTwoIngredients()
    putIngredient(ingredients[0])
    putIngredient(ingredients[1])

if __name__ == "__main__":
    # Serving the table for the first time
    serveTable()
    rpc.serve(port=participants["dealer"])