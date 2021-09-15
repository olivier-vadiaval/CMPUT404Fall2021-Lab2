#!/usr/bin/env python3
import socket
import multiprocessing as mp

BUF_SIZE = 4096

def conn_handler(conn_socket, client_socket):
    try:
        while True:
            # Receive data from proxy client, forward to Google
            client_data = conn_socket.recv(BUF_SIZE)
            client_socket.sendall(client_data)

            # Receive response from Google
            response_data = client_socket.recv(BUF_SIZE)

            # Forward response to proxy client
            conn_socket.sendall(response_data)
    
    except BrokenPipeError:
        print("Client closed connection! Closing socket!")

    except Exception as e:
        print(type(e))
        print("Exception occurred:", e.args)

    finally:
        conn_socket.close()

def main():
    EXTERN_HOST = "www.google.com"   # Google hostname
    HOST = "127.0.0.1"          # localhost
    PORT = 8001                 # port number
    address = (HOST, PORT)

    try:

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            # Reuse port number
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

            server_socket.bind(address)
            print("Proxy server binded")

            print("Listening...")
            server_socket.listen()

            while True:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    client_socket.connect((GOOGLE, 80))
                    print("Connected to Google")
                    conn_socket, client_addr = server_socket.accept()

                    client_host, client_port = client_addr
                    print("Connected to client at", client_host, ",", client_port)

                    # Create Process object for new connection
                    new_conn = mp.Process(
                            target=conn_handler, 
                            args=(conn_socket, client_socket), 
                            daemon=True
                        )
                    
                    new_conn.start()    # fork

                    print("Number of processes:", len(mp.active_children()))

    except Exception as e:
        print("Exception occurred", e.args)

if __name__ == "__main__":
    main()