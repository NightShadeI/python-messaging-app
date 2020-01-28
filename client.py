from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import sys

BUFSIZ = 1024

def receive():
	while True:
		try:
			msg = client_socket.recv(BUFSIZ).decode("utf8")
			scroll_level = msg_list.yview()[1]
			msg_list.insert(tkinter.END, msg)
			if auto_scroll.get() == 1 or scroll_level == 1:
				msg_list.yview(tkinter.END)
		except OSError:
			print("OSError!!", flush=True)
			break


def send(event=None):
	msg = my_msg.get()
	my_msg.set("")
	client_socket.send(bytes(msg, "utf8"))
	if msg == "q":
		client_socket.close()
		top.destroy()


def on_closing(event=None):
	my_msg.set("q")
	send()


top = tkinter.Tk()
top.title("Messager")

auto_scroll = tkinter.IntVar()
check_button = tkinter.Checkbutton(top, text="Always autoscroll", variable=auto_scroll)
check_button.pack()

message_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()
my_msg.set("Type here.")
scrollbar = tkinter.Scrollbar(message_frame)

msg_list = tkinter.Listbox(message_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()

message_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

HOST = input("Enter host: ")
PORT = 33000

ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()
