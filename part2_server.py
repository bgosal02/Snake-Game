from tkinter import *
import socket
import threading

class ChatServer:
    """
    This class implements the chat server.
    It uses the socket module to create a TCP socket and act as the chat server.
    Each chat client connects to the server and sends chat messages to it. When 
    the server receives a message, it displays it in its own GUI and also sends 
    the message to the other client.  
    It uses the tkinter module to create the GUI for the server client.
    See the project info/video for the specs.
    """
    def __init__(self, window):
        """
        Initializer sets the window, creates and binds the socket
        """
        #Set up the window and GUI
        self.window = window

        #Create label for displaying "Chat Server"
        self.label_message = Label(self.window, text="Chat Server", anchor='w')
        self.label_message.pack(pady=5, anchor='w')

        #Create label for displaying "Chat History:"
        self.label_message = Label(self.window, text="Chat History:", anchor='w')
        self.label_message.pack(pady=5, anchor='w')

        #Create a text display for the server
        self.display = Text(window, height=10, width=40)
        self.display.pack(padx=10, pady=10)

        #Create a server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #Server port and address
        self.port = 12000
        self.address = '127.0.0.1'

        #Bind the server socket
        self.server_socket.bind((self.address, self.port))

        #List to store connected clients and their process names
        self.clients = []

        #State server is ready
        print("The server is ready to receive")

        #Server starts listening for requests
        self.server_socket.listen(1)

        #Start the server loop using a thread
        serverloop_thread = threading.Thread(target=self.serverloop)
        serverloop_thread.start()

    def serverloop(self):
        """
        The main loop of the server, listens to connections,
        accepts clients
        """
        while True:
            #Accept a new client
            client_socket, client_addr = self.server_socket.accept()

            #Receive process name from the client
            process_name = client_socket.recv(1024).decode('utf-8')

            #Add the client and process name to the clients list
            self.clients.append((client_socket, process_name))

            #Start client messaging using a thread
            client_thread = threading.Thread(target=self.clientmessaging, args=(client_socket,))
            client_thread.start()

    def clientmessaging(self, client_socket):
        """
        Handles the messaging between the clients
        """
        while True:
            #Receive a message from the client
            message = client_socket.recv(1024).decode('utf-8')

            #Get the sender's process name
            sender_name = next(name for sock, name in self.clients if sock == client_socket)

            #Display the labeled message in the server window
            labeled_message = f"{sender_name}: {message}\n"
            self.display.insert(END, labeled_message)
            self.display.see(END)  # Scroll to the end

            #Send the message to all clients
            for other_client_socket, _ in self.clients:
                if other_client_socket != client_socket:
                    try:
                        #Send the sender's name and message to the other clients
                        other_client_socket.send(sender_name.encode('utf-8'))
                        other_client_socket.send(message.encode('utf-8'))
                    except socket.error:
                        #Remove broken connections
                        self.clients = [(sock, name) for sock, name in self.clients if sock != other_client_socket]

def main():
    window = Tk()
    ChatServer(window)
    window.mainloop()

if __name__ == '__main__':
    main()
