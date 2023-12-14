import time
import random
import threading

import jsonrpcserver as rpc
from utils import json_rpc_request, philosophers, num_of_philosophers

id = 0
status = 0
left_fork = True
fork_in_left_hand = False
fork_in_rigt_hand = False
right_fork_id = None; 


def get_neighbours_id():
    global id
    if id + 1 > num_of_philosophers - 1:
        return 0
    else:
        return id + 1


def thinking():
    global id
    time_interval = random.randint(1,10)
    print("I am thinking for " + str(time_interval) + " seconds")
    time.sleep(time_interval)
    cycle_through_state()


def cycle_through_state():
    global status
    status = status +1
    if (status > 2):
        status = 0


# def check_forks():
#     global id
#     neigbour_id = get_neighbours_id()
#     for philosopher in philosophers:
#         try:
#             if json_rpc_request("answer_fork_availability", {}, philosophers[neigbour_id]):
#                 take_forks()
#                 break
#             else:      
#                 time_interval = random.randint(1,10)
#                 print("philosopher " + str(id) + " is waiting before sending another check_fork message for " + str(time_interval) + " seconds")
#                 time.sleep(time_interval)
#         except:


def eating():
    global id
    global right_fork_id
    global fork_in_left_hand
    global fork_in_rigt_hand
    global left_fork

    time_interval = random.randint(1,10)
    print(" I am eating for " + str(time_interval) + " seconds")
    time.sleep(time_interval)
    print("I'm done!")

    left_fork = True
    fork_in_left_hand = False
    fork_in_rigt_hand = False

    neighbours_id = get_neighbours_id()
    while(True):
        if neighbours_id != id:
                try:
                    if json_rpc_request("receive_fork_back", {"giversID": right_fork_id}, philosophers[neighbours_id]):
                        print("I gave the fork back to neigbour number " + str(right_fork_id))
                        break
                except:
                    neighbours_id = neighbours_id + 1
                    
                    if neighbours_id == num_of_philosophers:
                        neighbours_id = get_neighbours_id()

                    if neighbours_id > right_fork_id:
                        neighbours_id = get_neighbours_id()
                    print()

    cycle_through_state()

def take_forks():
    global left_fork
    global id
    global fork_in_left_hand
    global right_fork_id
    global fork_in_rigt_hand

    if left_fork == True:
        left_fork = False
        fork_in_left_hand = True
        neigbours_id = get_neighbours_id()
        for philosopher in philosophers:
            if neigbours_id != id:
                try:
                    print("I have my own fork, so I am requesting the fork of neigbour number " + str(neigbours_id))
                    if json_rpc_request("give_fork_away", None, philosophers[neigbours_id]):
                        print("I got a fork from my neighbour number " + str(neigbours_id))
                        right_fork_id = neigbours_id
                        fork_in_rigt_hand = True
                    else:
                        print("My neigbour would not give me his fork")
                        being_hungry()
                    break
                except Exception as e:
                    print("Take-Forks-Exception: " + str(e))
                    neigbours_id = neigbours_id + 1
                    if neigbours_id == num_of_philosophers:
                        neigbours_id = 0
                    right_fork_id = neigbours_id
            else:
                print("I haven't reached any other philosopher, so I can't get another fork.")
                being_hungry()
                break
    else:
        # error: I thought my fork was available but it is not
        print("I want to eat but my own fork is gone.")
        being_hungry()


@rpc.method
def give_fork_away() -> rpc.Success:
    global left_fork

    if left_fork:
        left_fork = False
        print("I have given my fork away.")
        return rpc.Success(True)
    else:
        print("A fork was requested but I am using it")
        return rpc.Success(left_fork)

    # if success == None: # I am the first one to answer
    #     if left_fork == True:
    #         left_fork = False
    #         success = True
    #         giversID = id
    #         json_rpc_request("give_fork_away", {success, sendersID, giversID}, get_neighbours_id())
    # else:
    #     json_rpc_request("give_fork_away", {success, sendersID, giversID}, get_neighbours_id())

    # if sendersID == id:
    #      if success == True:
    #           fork_in_rigt_hand = True
          
@rpc.method
def receive_fork_back(giversID: int) -> rpc.Success:
    global id
    global left_fork

    if giversID == id:
        left_fork = True
        print("I got my fork back")
        return rpc.Success(True)
    else:
        return rpc.Success(json_rpc_request("receive_fork_back", {"giversID":giversID}, philosophers[get_neighbours_id()]))


# @rpc.method
# def answer_fork_availability():
#     return rpc.Success(left_fork)

    # receiving your own message back
    # if id == _id:
    #     if (next_neighbour and last_neighbour):
    #         # the forks are free!
    #         take_forks()
    #     else:
    #         being_hungry()
    # else:
        # receiving a message from someone else
        # if next_neighbour == None:
        #     if status != 2:
        #         next_neighbour = True
        #     else:
        #         next_neighbour = False

        # # this part could be neglected as we implemented the forks 
        # if status != 2:
        #     last_neighbour = True
        # else:
        #     last_neighbour = False

        # # pass on the message
        # json_rpc_request("answer_fork_availability", {next_neighbour, last_neighbour, _id}, get_neighbours_id() )
    
def being_hungry():
    global id
    global left_fork
    global fork_in_left_hand

    left_fork = True
    fork_in_left_hand = False

    time_interval = random.randint(1,10)
    print("I am wating for free forks for " + str(time_interval) + " seconds")
    time.sleep(time_interval)

def start_server():
    global id
    
    rpc.serve(port=philosophers[id])

if __name__ == "__main__":
    id = int(input())
    time.sleep(5)
    
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    #thinking()

    while(True):
        if (status == 0):
            thinking()
        if (status == 1): # is hungry
            if (fork_in_left_hand and fork_in_rigt_hand):
                cycle_through_state()
            else:
                take_forks()
        if (status == 2): # is eating
            eating()