## TCP Reverse Shell Script

This repository performs a full TCP reverse shell connection with Python sockets on the `TCP` protocol along with many other features that complements a complete experience with file manipulation (upload/download), monitor screenshots, async command execution, admin privileges checker and many more with a persistence execution based on Windows registries manipulation and hiding a covered executable file in the `AppData` directory.

The `server.py` and the `shell.py` are the responsible files for each action; the `shell.py` will interact with `client.py` via Sockets, and will share back and forth information regarding the commands typed by the `attacker`. The `shell.py` file will be placed on the victim machine and will be listening to whatever the `attacker` sends.

Just to recap:

1. The server file will be listening for incoming connections
2. The client (or the reverse shell) will deliver to the target a hook to run a program, allowing the client to make actions with remote access via sockets

## How it works

Basically:

1. Create a socket object
2. Bind an IP address and port
3. Listen for incoming connection -> after listen (the Client will connect to the `C&C`)
4. The target will also create a socket object -> connect to the `C&C` (three-way handling), previously accepted by the Server
5. Send and `RECV` back and forth between (`C&C` and a target)
6. After all, close the socket connection; this will terminate the connection

## Using Wine and PyInstaller for binary generation

To generate an `exe`, you will need tools that will transform your `Python scripts` into a full working binary program for the `Windows OS` family.

My main PC  runs with `Ubuntu OS`, and for that OS family, you will need to use `Wine`, a tool for running Windows applications in `Linux-based OS's`, and `PyInstaller` is a package that lets you compile files in `Windows`.

The process is:

```
dpkg --add-architecture i386
apt-get update
apt-get install wine32

```

After this,  a `.wine` directory file is created, this is like the `C:/` drive in Windows with the `Program files` and `more`. Then you can download and install `Python 2.x msi` file for the `.wine` directory only; this is an isolated environment for the Windows "System" (I think) in the Ubuntu machine. (This is only for generating the binary file directly from the Ubuntu machine).

### Installing Python MSI

You can execute the MSI file from Python like:

`wine msiexec /i <Python>.msi`

This will start the wizard for the installation. After installation, a `Python27` directory inside the `.wine/drive_c`

### Installing Pyinstaller

Installing `pyInstaller` (Windows compatibility) with `Wine` like:

`wine /root/.wine/drive_c/Python27/python.exe -m pip install pyinstaller`

## Installing dependency packages with PyInstaller

You would need to download third-party libraries if needed, like:

`wine /root/.wine/drive_c/Python27/python.exe -m pip install requests`
`wine /root/.wine/drive_c/Python27/python.exe -m pip install mss`

## Creating an exe file

Just:

`wine /root/.wine/drive_c/Python27/pyinstaller.exe --onefile --noconsole shell.py`

This will generate a `shell.exe` file, ready to go.

## C&C Commands (Server side)

1. `help`: list of commands available
2. `download <path>`: Download a file from the target PC
3. `upload <path>`: Upload a File to Target PC
4. `get <url>`: Download a file to the Target PC from any Website
5. `start <path>`: Start a program without waiting on a single program to close before continuing (like parallel running)
6. `screenshot`: Take A Screenshot of Target Monitor
7. `check`: Check for Admin Privileges
8. `q`: Exiting the Reverse Shell

## Usage

- Server: `python server.py`
- Client: open `shell.exe` (Windows OS)

## Credits
[David Lares S](https://davidlares.com)

## License
[MIT](https://opensource.org/licenses/MIT)
