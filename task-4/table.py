import jsonrpcserver as rpc
from utils import participants

table = {
    0: False, # match
    1: False, # paper
    2: False  # tabaco
}

@rpc.method
def putIngredient(i: int) -> rpc.Success:
    table[i] = True
    return rpc.Success()

@rpc.method
def takeIngredient(i: int) -> rpc.Success:
    table[i] = False
    return rpc.Success()

@rpc.method
def checkIngredient(i: int) -> rpc.Success:
    return rpc.Success(table[i])

if __name__ == "__main__":
    rpc.serve(port=participants["table"])