from tkinter import *
import socket
import threading
from multiprocessing import current_process

class ChatClient:
    """
    This class implements the chat client.
    It uses the socket module to create a TCP socket and to connect to the server.
    It uses the tkinter module to create the GUI for the chat client.
    """
    def __init__(self, window):
        """
        Create server address & port
        """
        self.server_address = '127.0.0.1'
        self.server_port = 12000

        #Create client socket & connect to server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_address, self.server_port))

        #Initialize GUI
        self.window = window
        self.window.title(f"{current_process().name} @port #{self.client_socket.getsockname()[1]}")

        #Create label for displaying "Chat Message:"
        self.label_message = Label(self.window, text="Chat Message:", anchor='w')
        self.label_message.pack(pady=5, anchor='w')

        #Create entry for typing messages
        self.entry_message = Entry(self.window, width=50)
        self.entry_message.pack(pady=10)

        #Create label for displaying "Chat History:"
        self.label_message = Label(self.window, text="Chat History:", anchor='w')
        self.label_message.pack(pady=5, anchor='w')

        #Create listbox to show messages
        self.message_listbox = Listbox(self.window, height=15, width=50)
        self.message_listbox.pack(pady=10)

        #Create button to send messages
        self.send_button = Button(self.window, text="Send", command=self.send_message)
        self.send_button.pack()

        #Send process name to the server
        self.client_socket.send(current_process().name.encode('utf-8'))

        #Start thread to receive messages from server
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

    def send_message(self):
        """
        Get the message from the entry and send it to the server
        """
        message = self.entry_message.get()
        if message:
            self.client_socket.send(message.encode('utf-8'))
            self.entry_message.delete(0, END)

            #Display the sent message in the client window with an indent
            labeled_message = f"    {current_process().name}: {message}\n"
            self.message_listbox.insert(END, labeled_message)

    def receive_messages(self):
        """
        Receive messages from the server and update the listbox
        """
        while True:
            try:
                #Receive sender's name and message
                sender_name = self.client_socket.recv(1024).decode('utf-8')
                message = self.client_socket.recv(1024).decode('utf-8')

                #Display the message in the client window with an indent for the original sender
                if sender_name != current_process().name:
                    labeled_message = f"{sender_name}: {message}\n"
                else:
                    labeled_message = f"    {sender_name}: {message}\n"

                self.message_listbox.insert(END, labeled_message)
            except ConnectionError:
                break

        #Close the client socket when the thread ends
        self.client_socket.close()

def main():
    window = Tk()
    c = ChatClient(window)
    window.mainloop()

if __name__ == '__main__':
    main()
