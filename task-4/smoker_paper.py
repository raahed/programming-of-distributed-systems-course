from utils import json_rpc_request, participants, wait_timer
import time

needs = [0,2]

if __name__ == "__main__":
    while True:
        time.sleep(wait_timer)
        print(f"[Smoker Paper] Checking for {needs[0]} and {needs[1]}!")
        ingredient1 = json_rpc_request("checkIngredient", {"i": needs[0]}, participants["table"])
        ingredient2 = json_rpc_request("checkIngredient", {"i": needs[1]}, participants["table"])

        if ingredient1 and ingredient2:
            print(f"[Smoker Paper] Taking {needs[0]} and {needs[1]}!")
            json_rpc_request("takeIngredient", {"i": needs[0]}, participants["table"])
            json_rpc_request("takeIngredient", {"i": needs[1]}, participants["table"])

            time.sleep(wait_timer)

            json_rpc_request("serveTable", participant=participants["dealer"])