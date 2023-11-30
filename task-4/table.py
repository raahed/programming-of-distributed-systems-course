import jsonrpcserver as rpc
from utils import participants
from utils import json_rpc_request, participants

table = {
    0: False, # match
    1: False, # paper
    2: False  # tabaco
}

@rpc.method
def putIngredient(i: int) -> int:
    table[i] = True
    return rpc.Success(i)

@rpc.method
def takeIngredient(i: int) -> int:
    table[i] = False
    return rpc.Success(i)

@rpc.method
def checkIngredient(i: int) -> bool:
    return rpc.Success(table[i])

if __name__ == "__main__":
    json_rpc_request("startCheckIngredientLoop", {"i": 0}, participants["smoker_tabaco"])
    json_rpc_request("startCheckIngredientLoop", {"i": 0}, participants["smoker_match"])
    json_rpc_request("startCheckIngredientLoop", {"i": 0}, participants["smoker_paper"])
    rpc.serve(port=participants["table"])