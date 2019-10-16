import time
import sys
import socket
import hmac

def getClientPort():
    out = sys.argv[1]
    return out

def getTS1Name():
    out = sys.argv[2]
    return out

def getTS1Port():
    out = sys.argv[3]
    return out

def getTS2Name():
    out = sys.argv[4]
    return out

def getTS2Port():
        out = sys.argv[5]
        return out

if __name__ == "__main__":
#python as.py asListenPort ts1Hostname ts1ListenPort_a ts2Hostname ts2ListenPort_a

    # client_port = port used to connect to client
    client_port = int(getClientPort())
    ts1_name = getTS1Name()
    ts1_port = int(getTS1Port())
    ts2_name = getTS2Name()
    ts2_port = int(getTS2Port())

    #print(client_port)
    #print(ts1_name)
    #print(ts1_port)
    #print(ts2_name)
    #print(ts2_port)

    # Create sockets
    ts1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ts2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_as_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    as_name = socket.gethostname()
    as_ip = socket.gethostbyname(as_name)
    #print("as name is: " + as_name)
    #print("as ip is : " + str(as_ip))

    ts1_ip = socket.gethostbyname(ts1_name)
    ts2_ip = socket.gethostbyname(ts2_name)

    client_address = (as_ip, client_port)
    #print("listening for connection on " + str(as_ip) + " on " + str(client_port))
    client_as_socket.bind(client_address)

    client_as_socket.listen(1)

    client_socket, client_addr = client_as_socket.accept()
    #print("Got a connection from client at {}".format(client_addr))

    ts1_socket.connect((ts1_ip, ts1_port))
    print("Connected to TS1")

    ts2_socket.connect((ts2_ip, ts2_port))
    print("Connected to TS2")

    inc_packet = ""
    out_packet = ""

    out_packet = ts1_ip.encode('utf-8')
    client_socket.send(out_packet)
    #print("Sent " + str(ts1_ip))

    out_packet = ts2_ip.encode('utf-8')
    client_socket.send(out_packet)
    #print("Sent " + str(ts2_ip))

    inc_packet = client_socket.recv(256).decode('utf-8')
    print("num queries = " + str(inc_packet))

    out_packet = inc_packet

    ts1_socket.send(out_packet.encode('utf-8'))
    ts2_socket.send(out_packet.encode('utf-8'))

    counter = int(inc_packet)
    for x in range(counter):
        inc_packet = client_socket.recv(256).decode('utf-8')
        time.sleep(1)
        out_packet = inc_packet.split()[0]
        temp = str(inc_packet.split()[1])
        print(temp)

        ts1_socket.send(out_packet.encode('utf-8'))
        ts2_socket.send(out_packet.encode('utf-8'))

        inc_packet = ts1_socket.recv(256).decode('utf-8')
        ts1_response = str(inc_packet)
        print(ts1_response)

        inc_packet = ts2_socket.recv(256).decode('utf-8')
        ts2_response = str(inc_packet)
        print(ts2_response+'\n')

        if ts1_response == temp:
            client_socket.send(ts1_ip.encode('utf-8'))
        else:
            client_socket.send(ts2_ip.encode('utf-8'))
