import socket
import threading

HOST = "192.168.56.1"
PORT = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            sender_index = clients.index(client)
            sender_nickname = nicknames[sender_index]

            print(f"{sender_nickname} says: {message.decode('utf-8')}")
            broadcast(message)
        except:
            handle_disconnect(client)
            break


def handle_disconnect(client):
    index = clients.index(client)
    client.close()
    nickname = nicknames[index]

    clients.remove(client)
    nicknames.remove(nickname)

    print(f"{nickname} has disconnected.")
    broadcast(f"{nickname} has disconnected.\n".encode('utf-8'))


def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send("NICK".encode("utf-8"))
        nickname = client.recv(1024).decode("utf-8")

        nicknames.append(nickname)
        clients.append(client)

        print(f"{nickname} has connected to the server!")
        broadcast(f"{nickname} has connected to the server!\n".encode('utf-8'))
        client.send("Connected to the server".encode("utf-8"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server running...")
receive()
