import socket
import threading

HOST = '127.0.0.1'
PORT = 3389

client_socket: socket.socket


def initialize_connection():
    global client_socket

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    print(client_socket.recv(1024).decode())

    nickname = input()

    client_socket.send(nickname.encode())


def receive():
    while True:
        try:
            message = client_socket.recv(1024)
            print(message.decode())
        except Exception:
            print('Holy ... just god knows what happens')
            client_socket.close()
            break


def write():
    while True:
        message = input()
        client_socket.send(message.encode())


if __name__ == '__main__':
    initialize_connection()

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()






