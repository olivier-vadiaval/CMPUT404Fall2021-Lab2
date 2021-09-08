#!/usr/bin/env python3
import socket
import 

GOOGLE = "www.google.com"
HOST = "127.0.0.1"
PORT = "http"
address = (HOST, PORT)

BUF_SIZE = 4096

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        client_socket.bind(address)
        print("Proxy server binded")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(GOOGLE)
            print("Connected to Google")

            print("Listening...")
            server_socket.listen()

            while True:
                conn_socket, client_addr = server_socket.accept()

                client_host, client_port = client_addr
                print("Connected to client at", client_host, ",", client_port)

                with conn_socket:
                    while True:
                        proxy_data = server_socket.recv(BUF_SIZE)
                        client_socket.sendall(proxy_data)

                        google_data = client_socket.recv(BUF_SIZE)
                        proxy_data = server_socket.sendall(google_data)
                

except Exception as e:
    print("Exception occurred", e.args)