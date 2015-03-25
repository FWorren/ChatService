# -*- coding: utf-8 -*-
import socket, json
from MessageReceiver import MessageReceiver

class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.server_port = server_port

        receiver = MessageReceiver(self, self.connection)

        self.run()

        while True:
                
            msg = raw_input('Client: ')

            msg = msg.split()

            request = msg[0]
            if len(msg)==2:
                content = msg[1]
            else:
                content = None

            payload = json.dumps({'request':request, 'content':content})


            self.send_payload(payload)


        self.disconnect()

        # TODO: Finish init process with necessary code

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))

    def disconnect(self):
        # TODO: Handle disconnection
        self.connection.close()
        #pass

    def receive_message(self, message):
        # TODO: Handle incoming message
        pass

    def send_payload(self, data):
        # TODO: Handle sending of a payload
        self.connection.sendall(data)
        #pass


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations is necessary
    """
    client = Client('localhost', 9998)
