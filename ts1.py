import time
import sys
import socket
import hmac


def getASPort():
    out = sys.argv[1]
    return out

def getClientPort():
    out = sys.argv[2]
    return out

def processRequest(request):
    result= ts1_table.get(request,' - Error: HOST NOT FOUND')
    return result

if __name__ == "__main__":

    # Dictionary Setup
    ts1_table = dict()

    with open("PROJ3-DNSTS1.txt") as f:
        for line in f:
            temp = line.rstrip()
            lower = temp.split()[0].lower()
            ts1_table[lower] = temp

    # Gets key from file
    with open('PROJ3-KEY1.txt') as file:
        key = file.readline().rstrip()

    # Debug print
    #print(key)

    as_port = int(getASPort())
    client_port = int(getClientPort())

    #print(as_port)
    #print(client_port)

    # Create socket
    ts1_as_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ts1_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ts1_hostname = socket.gethostname()
    ts1_ip = socket.gethostbyname(ts1_hostname)

    as_connection = (ts1_ip, as_port)
    ts1_as_socket.bind(as_connection)

    ts1_as_socket.listen(1)
    as_socket, as_addr = ts1_as_socket.accept()
    print("Connected to as")

    client_address = (ts1_ip, client_port)
    ts1_client_socket.bind(client_address)

    ts1_client_socket.listen(1)
    client_socket, client_addr = ts1_client_socket.accept()
    print("Connected to client")

    inc_packet = key
    out_packet = ""

   # client_socket.send(inc_packet.encode('utf-8'))
    print("Key sent")

    inc_packet = as_socket.recv(256).decode('utf-8')
    print(str(inc_packet))

    client_socket.settimeout(5)

    counter = int(inc_packet)
    for x in range(counter):
        inc_packet = as_socket.recv(256).decode('utf-8')
        print(str(inc_packet))
        tempp= str(inc_packet)
        as_response = hmac.new(key.encode('utf-8'), tempp.encode('utf-8'))
        out_packet = as_response.hexdigest().encode('utf-8')

        print(as_response.hexdigest())
        as_socket.send(out_packet)

        try:
            inc_packet = client_socket.recv(256).decode('utf-8')
            print(str(inc_packet))
            lookup_result= processRequest(str(inc_packet))
            print(lookup_result+ "&&&")
            client_socket.send(lookup_result.encode('utf-8'))
        except socket.timeout:
            continue
    print('PROGRAM TERMINATING')
