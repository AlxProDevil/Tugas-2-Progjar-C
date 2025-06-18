from socket import *
import socket
import threading
import logging
import time
import sys
from datetime import datetime

logging.basicConfig(level=logging.INFO,
                    format='(%(threadName)-10s) %(message)s',)

class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        logging.info(f"Handling connection from {self.address}")
        try:
            while True:
                data = self.connection.recv(100).decode('utf-8').strip()
                
                if data:
                    if data == "TIME":
                        now = datetime.now()
                        
                        jam_sekarang = now.strftime("%H:%M:%S")
                        response = f"JAM {jam_sekarang}\r\n"
                        logging.info(f"Client {self.address} sent TIME.")
                        logging.info(f"Sending response: {response.strip()} to {self.address}")
                        self.connection.sendall(response.encode('utf-8'))
                    elif data == "QUIT":
                        logging.info(f"Client {self.address} sent QUIT. Closing connection.")
                        break
                    else:
                        logging.warning(f"Invalid request from {self.address}: {data}")
                        self.connection.sendall("INVALID_REQUEST\r\n".encode('utf-8'))
                else:
                    logging.info(f"Client {self.address} disconnected.")
                    break
        except Exception as e:
            logging.error(f"Error handling client {self.address}: {e}")
        finally:
            self.connection.close()
            logging.info(f"Connection with {self.address} closed.")

class Server(threading.Thread):
    def __init__(self):
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        threading.Thread.__init__(self)
        self.port = 45000

    def run(self):
        logging.info(f"Starting server on port {self.port}...")
        try:
            self.my_socket.bind(('0.0.0.0', self.port))
            self.my_socket.listen(5)
            logging.info("Server is listening for incoming connections.")
            while True:
                connection, client_address = self.my_socket.accept()
                logging.info(f"Accepted connection from {client_address}")
                
                clt = ProcessTheClient(connection, client_address)
                clt.start()
                self.the_clients.append(clt)
                
                self.the_clients = [t for t in self.the_clients if t.is_alive()]
        except Exception as e:
            logging.error(f"Server error: {e}")
        finally:
            self.my_socket.close()
            logging.info("Server socket closed.")

def main():
    svr = Server()
    svr.start()

if __name__ == "__main__":
    main()