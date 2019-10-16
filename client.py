import time
import sys
import socket
import hmac

def getASName():
    out = sys.argv[1]
    #print(out)
    return out

def getASPort():
    out = sys.argv[2]
    print(out)
    return out

def getTS1Port():
    out = sys.argv[3]
    return out

def getTS2Port():
    out = sys.argv[4]
    return out

def writeOut(search, result):
    print("+++++++"+search)
    if(str(result)) == ' - Error: HOST NOT FOUND':
        err_string= search + str(result)
        outFile.write(err_string+"\n")
    else:
        outFile.write(str(result) + "\n")



if __name__ == "__main__":

    as_port = int(getASPort())
    ts1_port = int(getTS1Port())
    ts2_port = int(getTS2Port())

    # Creates array of queries to check
    with open("PROJ3-HNS.txt", "r") as client_hns:
        input = [line.rstrip('\n') for line in open('PROJ3-HNS.txt')]

    # Creates write file that will store results
    outFile= open("RESULTS.txt", 'a')

    # python client.py asHostname asListenPort ts1ListenPort_c ts2ListenPort_c

    # Create sockets
    ts1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ts2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    as_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Gets as ip from name from command line
    as_ip = socket.gethostbyname(getASName())

    as_socket.connect((as_ip, as_port))
    print("Connected to: " + as_ip + " on port " + str(as_port))

    inc_packet = "waiting"
    out_packet = "requesting ts1 name"

    inc_packet = as_socket.recv(256).decode('utf-8')
    ts1_ip = str(inc_packet)
    print(ts1_ip)

    inc_packet = str(as_socket.recv(256).decode('utf-8'))
    ts2_ip = str(inc_packet)
    print(ts2_ip)

    # Connects client to ts1 and ts2
    ts1_socket.connect((ts1_ip, ts1_port))
    print("Connected to: " + ts1_ip + " on port " + str(ts1_port))

    ts2_socket.connect((ts2_ip, ts2_port))
    print("Connected to: " + ts2_ip + " on port " + str(ts2_port))

    # small debug
    #inc_packet = str(ts1_socket.recv(256).decode('utf-8'))
    #ts1_key = inc_packet
    #print(ts1_key)

    #inc_packet = str(ts2_socket.recv(256).decode('utf-8'))
    #ts2_key = inc_packet
    #print(ts2_key)
    as_queries = []
    counter = 0

    # Seperates the key, challenge and query and store them in variable accordinglys
    for x in input:
        sep = x.split()
        key = sep[0]
        challenge = sep[1]
        query = sep[2]
        #print(key)
        #print(challenge)
        #print(query + "\n")

        # Digest associated with query to be sent to AS
        digest = hmac.new(key.encode("utf-8"), challenge.encode("utf-8"))
        to_as = challenge + " " + digest.hexdigest()
        as_queries.append(to_as)
        #print(str(counter))
        counter = counter + 1

    out_packet = str(counter)
    as_socket.send(out_packet.encode('utf-8'))

    ts1_socket.settimeout(5)
    ts2_socket.settimeout(5)

    for x in range(counter):
        out_packet = as_queries[x]
        #print(str(x) + ": " + out_packet)
        as_socket.send(out_packet.encode('utf-8'))
        time.sleep(1)

        ############### IP ADDRESS ###################
        ## SEND QUERY HERE##
        inc_packet = str(as_socket.recv(256).decode('utf-8'))

        #ip_address
        #print(inc_packet)

        temp = input[x].split()[2]

        ##QUERY IS IN TEMP
        print(temp)
        out_packet = temp

        if(inc_packet == ts2_ip):
            ts2_socket.send(out_packet.encode("utf-8"))
            time.sleep(2.5)
        else:
            ts1_socket.send(out_packet.encode("utf-8"))
        time.sleep(2.5)

        ##AT this point we are recieving the results from the DNS lookups

        try:
            lookup_ans_raw = ts1_socket.recv(256)
            lookup_final = lookup_ans_raw.decode('utf-8')
            if(str(lookup_final)) == ' - Error: HOST NOT FOUND':
                err_string= temp + str(lookup_final)
                outFile.write(err_string + "\n")
            else:
                outFile.write(str(lookup_final) + "\n")
        except socket.timeout:
            continue
        
        try:
            lookup_ans_raw = ts2_socket.recv(256)
            lookup_final = lookup_ans_raw.decode('utf-8')
            if(str(lookup_final)) == ' - Error: HOST NOT FOUND':
                err_string= temp + str(lookup_final)
                outFile.write(err_string + "\n")
            else:
                outFile.write(str(lookup_final) + "\n")
        except socket.timeout:
            continue