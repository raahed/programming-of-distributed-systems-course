import time
import random
import threading

import jsonrpcserver as rpc
from utils import json_rpc_request, philosophers

id = 0
status = 0
left_fork = True
fork_in_left_hand = False
fork_in_rigt_hand = False
right_fork_id = None; 

def get_neighbours_id():
    global id
    if id + 1 > 4:
        return 0
    else:
        return id + 1

def thinking():
    global id
    time_interval = random.randint(1,10)
    print("philosopher " + str(id) + " is thinking for " + str(time_interval) + " seconds")
    time.sleep(time_interval)
    cycle_through_state()

def cycle_through_state():
    global status
    status = status +1
    if (status > 2):
        status = 0

def check_forks():
    global id
    json_rpc_request("answer_fork_availability", {None, None, id}, get_neighbours_id() )
    time_interval = random.randint(1,10)
    print("philosopher " + str(id) + " is waiting before sending another check_fork message for " + str(time_interval) + " seconds")
    time.sleep(time_interval)


def eating():
    global id
    global right_fork_id
    global fork_in_left_hand
    global fork_in_rigt_hand
    global left_fork

    time_interval = random.randint(1,10)
    print("philosopher " + str(id) + " is eating for " + str(time_interval) + " seconds")
    time.sleep(time_interval)
    print("I'm done!")

    left_fork = True
    fork_in_left_hand = False
    fork_in_rigt_hand = False

    json_rpc_request("receive_fork_back", {right_fork_id}, get_neighbours_id())

    cycle_through_state()

def take_forks():
    global left_fork
    global id
    global fork_in_left_hand

    if left_fork == True:
        left_fork = False
        fork_in_left_hand = True
        json_rpc_request("give_fork_away",{None, id, None}, get_neighbours_id())
    else:
        # error: I thought my fork was available but it is not
        being_hungry()


@rpc.method
def give_fork_away(success, sendersID, giversID):
    global left_fork
    global id
    global fork_in_rigt_hand

    if success == None: # I am the first one to answer
        if left_fork == True:
            left_fork = False
            success = True
            giversID = id
            json_rpc_request("give_fork_away", {success, sendersID, giversID}, get_neighbours_id())
    else:
        json_rpc_request("give_fork_away", {success, sendersID, giversID}, get_neighbours_id())

    if sendersID == id:
         if success == True:
              fork_in_rigt_hand = True
          
@rpc.method
def receive_fork_back(giversID):
    global id
    global left_fork

    if giversID == id:
        left_fork = True
    else:
         json_rpc_request("receive_fork_back", {giversID}, get_neighbours_id())


@rpc.method
def answer_fork_availability(next_neighbour, last_neighbour, _id):
    global id

    # receiving your own message back
    if id == _id:
        if (next_neighbour and last_neighbour):
            # the forks are free!
            take_forks()
        else:
            being_hungry()
    else:
        # receiving a message from someone else
        if next_neighbour == None:
            if status != 2:
                next_neighbour = True
            else:
                next_neighbour = False

        # this part could be neglected as we implemented the forks 
        if status != 2:
            last_neighbour = True
        else:
            last_neighbour = False

        # pass on the message
        json_rpc_request("answer_fork_availability", {next_neighbour, last_neighbour, _id}, get_neighbours_id() )
    
def being_hungry():
    global id

    time_interval = random.randint(1,10)
    print("philosopher " + str(id) + " is wating for free forks for " + str(time_interval) + " seconds")
    time.sleep(time_interval)

def start_server():
    global id
    
    rpc.serve(port=philosophers[id])

if __name__ == "__main__":
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    thinking()

    while(True):
        if (status == 1): # is hungry
            check_forks()
            if (fork_in_left_hand and fork_in_rigt_hand):
                cycle_through_state()
        if (status == 2): # is eating
            eating()