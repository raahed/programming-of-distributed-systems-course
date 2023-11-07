import sys
import socket as sk
import subprocess as sp
from datetime import datetime as dt

test_name = sys.argv[1]
send_content = sys.argv[2]
loop_counter = int(sys.argv[3])

serverAddressPort = ("130.243.124.183", 12345)
buffer_size = 65536

bytesToSend = str.encode(send_content)

filename = f'{test_name}-{dt.now().strftime("%H_%M_%S_%f")}.csv'
filestream = open(filename, "a")

# csv headers
filestream.write('test_name, loop counter, send time, send answer, message, trace hops\n')

# Tracert
sp.run(f'traceroute {serverAddressPort[0]} > {filename}.trace', shell=True, check=True)

# Get trace route hops
trace_prog = sp.Popen(f'cat {filename}.trace | tail -n 1 | awk \'END{{ print $1 }}\'', shell=True, stdout=sp.PIPE)
hops = int(trace_prog.stdout.read().decode())

# Socket Connection aufbauen
udp_client = sk.socket(family=sk.AF_INET, type=sk.SOCK_DGRAM)

for i in range(loop_counter):

    filestream.write(f'{filename}, {i},')

    try:
        time_start = dt.now()

        # Send Message
        udp_client.sendto(bytesToSend, serverAddressPort)

        time_send = dt.now()

        filestream.write(f'{time_send - time_start},')
        time_start = dt.now()

        #Receive From
        msgFromServer = udp_client.recvfrom(buffer_size)
        msg = msgFromServer[0].decode()

        time_answer = dt.now()

        filestream.write(f'{time_answer - time_start},{len(msg)}, {hops}')

    except Exception as e:
        print(f"Receive failed! {e}")
        filestream.write(f'0,0,{e},0')

    finally:
        filestream.write('\n')

udp_client.close()
filestream.close()