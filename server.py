import socket
import threading


HOST = '127.0.0.1'
PORT = 1239


class ClientInfo:
    def __init__(self, client_socket: socket.socket, address, nickname):
        self.client_socket = client_socket
        self.address = address
        self.nickname = nickname


clients_list: list[ClientInfo] = []


def initialize_server_socket() -> socket.socket:
    new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    new_socket.bind((HOST, PORT))
    new_socket.listen()
    return new_socket


def broadcast(message: str):
    global clients_list
    for client in clients_list:
        print('try to broadcast inside for')
        client.client_socket.send(message.encode())


def manage_client_socket(client: ClientInfo):
    global clients_list
    while True:
        try:
            message = client.nickname + ': ' + client.client_socket.recv(1024).decode()

            broadcast(message)
        except Exception as exception:
            print(exception)
            clients_list.remove(client)
            client.client_socket.close()

            message = f"{client.nickname} left, address: {client.address}"
            broadcast(message)
            print(message)

            break


if __name__ == '__main__':
    server_socket = initialize_server_socket()

    while True:
        client_socket, address = server_socket.accept()

        client_socket.send('Type you nickname: '.encode())
        nickname = client_socket.recv(1024).decode()

        clients_list.append(ClientInfo(client_socket, address, nickname))

        print(f"{address} connected")

        client_socket.send('Connected to server!'.encode())

        broadcast(f"{nickname} joined the chat. ")

        thread = threading.Thread(target=manage_client_socket, args=(clients_list[-1],))
        thread.start()




