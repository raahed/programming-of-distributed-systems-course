import sys
import socket as sk
import subprocess as sp
from datetime import datetime as dt

test_name = sys.argv[1]
send_content = sys.argv[2]
loop_counter = int(sys.argv[3])

serverAddressPort = ('130.243.124.183', 12345)
buffer_size = 65536

bytesToSend = str.encode(send_content)

filename = f'{test_name}-{dt.now().strftime("%H_%M_%S_%f")}.csv'
filestream = open(filename, 'a')

# csv headers
filestream.write('test group,test name,loop counter,send time,answer time,message,trace hops\n')

# Tracert
sp.run(f'traceroute {serverAddressPort[0]} > {filename}.trace', shell=True, check=True)

# Get trace route hops
trace_prog = sp.Popen(f'cat {filename}.trace | tail -n 1 | awk \'END{{ print $1 }}\'', shell=True, stdout=sp.PIPE)
hops = int(trace_prog.stdout.read().decode())

udp_client = None

for i in range(loop_counter):

    # Resets
    send_time = 0
    answer_time = 0
    message = 0

    try:
        # Socket Connection
        udp_client = sk.socket(family=sk.AF_INET, type=sk.SOCK_DGRAM)
        udp_client.settimeout(5)

        time_start = dt.now()

        # Send Message
        udp_client.sendto(bytesToSend, serverAddressPort)

        send_time = dt.now() - time_start

        time_start = dt.now()

        # Receive From
        msgFromServer = udp_client.recvfrom(buffer_size)
        message = len(msgFromServer[0].decode())

        answer_time = dt.now() - time_start

    except Exception as e:
        print(f'\tReceive failed: {e}')
        message = e

    finally:
        filestream.write(f'{test_name},{test_name}-{loop_counter},{i},{send_time},{answer_time},{message},{hops}\n')
        udp_client.close()

filestream.close()