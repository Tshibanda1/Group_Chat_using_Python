import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog


HOST = "192.168.56.1"
PORT = 9999


class Client:

    def __init__(self, host, port):
        # Get the username from the user
        self.Username = simpledialog.askstring("Username", "Enter your Username")

        # Initialize variables for GUI and networking
        self.gui_done = False
        self.running = True

        # Create a socket and connect to the server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        # Start separate threads for GUI and message receiving
        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        # Set up the GUI window
        self.win = tkinter.Tk()
        self.win.configure(bg="Lightgray")

        # Chat label
        self.chat_label = tkinter.Label(self.win, text="Chat:", bg="Lightgray")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        # Scrolled text area for displaying messages
        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state="disabled")


        # Message label
        self.msg_label = tkinter.Label(self.win, text="Message:", bg="Lightgray")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)

        # Text area for user input
        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)

        # Send button
        self.send_button = tkinter.Button(self.win, text="Send", command=self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)

        # Set GUI done flag
        self.gui_done = True

        # Set up the protocol for handling window close event
        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        # Start the GUI event loop
        self.win.mainloop()

    def write(self):
        # Send user's message to the server
        message = f"{self.Username}: {self.input_area.get('1.0', 'end')}"
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')

    def stop(self):
        # Stop the client, close the window, and exit the program
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        # Receive and display messages from the server
        while self.running:
            try:
                message = self.sock.recv(1024).decode("utf-8")
                if message == 'NICK':
                    self.sock.send(self.Username.encode('utf-8'))
                else:
                    if self.gui_done:
                        # Display the received message in the text area
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break


# Create a Client instance with the specified host and port
client = Client(HOST, PORT)
