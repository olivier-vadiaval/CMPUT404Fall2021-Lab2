#!/usr/bin/env python3
import socket

def main():
    HOST = "localhost"  # localhost
    PORT = 8001
    address = (HOST, PORT)

    BUF_SIZE = 4096

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            # Question 3
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            server_socket.bind(address)
            server_socket.listen()
            print("Listening on port", PORT)

            while True:
                conn_socket, client_addr = server_socket.accept()
                client_host, client_port = client_addr

                # Question 4
                print("Connected to client at", client_host, ",", client_port)

                # Use context manager, no need to call close()
                with conn_socket:
                    received_data = conn_socket.recv(BUF_SIZE)
                    print("Sending back data")
                    conn_socket.sendall(received_data)

    except Exception as e:
        print("Exception occurred: ", e.args)

if __name__ == "__main__":
    main()