from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time

clients = {}
addresses = {}

HOST = ""
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)


def broadcast(msg, prefix=""):
	for sock in clients:
		sock.send(bytes(prefix, "utf8") + msg)


def handle_client(client):
	name = client.recv(BUFSIZ).decode("utf8")
	clients[client] = name
	client.send(bytes("if you ever want to quit simply type 'q'", "utf8"))
	broadcast(bytes("{} has joined the chat :)".format(name), "utf8"))
	clients[client] = name
	while True:
		try:
			msg = client.recv(BUFSIZ)
		except ConnectionResetError:
			del clients[client]
			broadcast(bytes("{} has left the chat".format(name), "utf8"))
			break
		if msg != bytes("q", "utf8"):
			broadcast(msg, name+": ")
		else:
			client.send(bytes("bye!", "utf8"))
			client.close()
			del clients[client]
			broadcast(bytes("{} has left the chat".format(name), "utf8"))
			break


def accept_incoming_connections():
	while True:
		client, client_address = SERVER.accept()
		print("{} has connected".format(client_address), flush=True)
		client.send(bytes("Enter your username: ", "utf8"))
		addresses[client] = client_address
		Thread(target=handle_client, args=(client,)).start()
		time.sleep(10)


if __name__ == "__main__":
	SERVER.listen(5)
	print("Waiting for connection ...")
	print(SERVER)
	ACCEPT_THREAD = Thread(target=accept_incoming_connections)
	ACCEPT_THREAD.start()
	ACCEPT_THREAD.join()
	SERVER.close()

