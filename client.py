#!/usr/bin/env python3
import socket

def get_remote_ip(hostname):
    try:
        return socket.gethostbyname(hostname)
    
    except (socket.gaierror, msg):
        print("Exception occurred:", msg)
    
    except Exception as e:
        print("Exception occurred", e.args)

def main():
    HOST = "www.google.com"
    PORT = "http"
    address = (HOST, PORT)
    BUF_SIZE = 4096
    page_request = "GET / HTTP/1.0\r\nHost: %s\r\n\r\n" % HOST

    try:
        with socket.create_connection(address) as client_socket:
            # Using create_connection is equivalent to using the
            # socket method and then using the connect method
            print('Connection established')
            
            client_socket.sendall(page_request.encode())
            print('Request sent!')

            data = b""
            while True:
                received_data = client_socket.recv(BUF_SIZE)
                if not received_data:
                    break
                data += received_data

            print('Received data, have a look:')

            # Print response
            print(data)

    except Exception as e:
        print('Exception Occurred: ', e.args)

if __name__ == "__main__":
    main()