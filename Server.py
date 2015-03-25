# -*- coding: utf-8 -*-
import SocketServer, json, string
from datetime import datetime

users = []
handlers = []
history = []
help_msg = 'login <username> sends a request to login to the server\nlogout sends a request to log out and disconnect from the server\nmsg <message> sends a message to the server that should be broadcasted to all connected clients\nnames should send a request to list all the usernames currently connected to the server\nhelp sends a request to the server to receive a help text containing all requests supported by the server\n'

class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """
    
    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        handlers.append(self)
        self.username = None

        print("Client connected @" + self.ip + ":" + str(self.port))

        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096).strip()

            timestamp = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')

            # Default respone
            response = 'Error'
            # Default content
            server_content = help_msg

            client_request =  json.loads(received_string)['request']
            client_content =  json.loads(received_string)['content']

            valid_chars = set(string.ascii_letters + string.digits)

            if self.username==None and client_request=='login':
                #check if not in use by someone else and valid
                if users.count(self.username)==0 and set(client_content) <= valid_chars:
                    self.username = client_content
                    users.append(self.username)
                    response = 'history'
                    server_content = history
                else:
                    print 'invalid'
                    response = 'error'
                    server_content = 'Invalid username, valid character a-z, A-Z, 0-9'
            elif self.username!=None and client_request=='logout':
                users.remove(self.username)
                response = 'info'
                server_content = "logout"
            elif self.username!=None and client_request=='msg':
                history.append([timestamp, self.username, client_content])
                response = 'message'
                server_content = client_content 
            elif self.username!=None and client_request=='names':
                response = 'info'
                server_content = ""
                for user in users:
                    server_content = server_content + user + "\n"
            elif client_request=='help':
                response = 'info'
                server_content = help_msg
            else:
                response = 'error'
                
                    
            payload = json.dumps({'timestamp':timestamp, 'sender':self.username, 'response':response, 'content':server_content})

            if self.username!=None and client_request=='msg':
                self.sendToAll(payload)
            else:
                self.connection.sendall(payload)

    # TODO: Add handling of received payload from client
    def handleRequest (self, request, content):
        pass

    def loginRequest (self):
        pass

    def logoutRequest (self):
        pass

    def send (self, data):
        self.connection.sendall(data)
        pass

    def sendToAll (self, data):
        for i in handlers:
            i.connection.sendall(data)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations is necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations is necessary
    """
    HOST, PORT = 'localhost', 9998
    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
