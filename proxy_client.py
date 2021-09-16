#!/usr/bin/env python3

import socket
BUF_SIZE = 4096

def main():

    GOOGLE_HOSTNAME = "www.google.com"
    HOST = "localhost"  # localhost
    PORT = 8001         # port number
    address = (HOST, PORT)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(address)
            print("Established connection with proxy server!")

            while True:
                # Send a GET request
                http_request = f"GET / HTTP/1.1\r\nHost: {GOOGLE_HOSTNAME}\r\n\r\n"
                client_socket.sendall(http_request.encode()) 
                response_data = client_socket.recv(BUF_SIZE)

                print(response_data)
                exit_input = input("Disconnect? (y/n)").lower()
                
                if exit_input == "y":
                    break

    except Exception as e:
        print("Exception occurred:", e.args)


if __name__ == "__main__":
    main()