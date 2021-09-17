#!/usr/bin/env python3
import socket
import multiprocessing as mp

BUF_SIZE = 4096

def request_handler(intern_socket, extern_socket):
    try:
        while True:
            # Receive data from proxy client, forward to Google
            client_data = intern_socket.recv(BUF_SIZE)
            if client_data:
                extern_socket.sendall(client_data)

                # Receive response from Google
                response_data = extern_socket.recv(BUF_SIZE)

                # Forward response to proxy client
                intern_socket.sendall(response_data)
            else:
                break


    except socket.error as e:
        if client_data == b"":
            print("Client disconnected!")
        else:
            print("Exception occurred:", e.args)

    finally:
        
        print("Closing connection")
        intern_socket.close()
        extern_socket.close()


def get_remote_ip(hostname):
    try:
        return socket.gethostbyname(hostname)
    
    except socket.gaierror as e:
        print("Exception occurred:", e.args)
    
    except Exception as e:
        print("Exception occurred", e.args)


def main():
    EXTERN_HOST = "www.google.com"   # Google hostname
    HOST = "127.0.0.1"          # localhost
    PORT = 8001                 # port number
    address = (HOST, PORT)

    extern_host_ip = get_remote_ip(EXTERN_HOST)

    try:

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as intern_socket:
            # Reuse port number
            intern_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            intern_socket.bind(address)
            print("Proxy server binded")

            print("Listening...")
            intern_socket.listen()

            while True:
                conn_socket, client_addr = intern_socket.accept()   # accept connections

                client_host, client_port = client_addr
                print("Connected to client at", client_host, ",", client_port)
                
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as extern_socket:  
                    extern_socket.connect((extern_host_ip, 80))     # connect to Google
                    print("Connected to Google")

                    # Create Process object for new connection
                    new_conn = mp.Process(
                            target=request_handler, 
                            args=(conn_socket, extern_socket)
                        )
                    new_conn.daemon = True
                    
                    new_conn.start()    # fork
                    
                    print("New process started", new_conn)
                    print("Number of processes:", len(mp.active_children()))

    except socket.error as e:
        print("Exception occurred", e.args)

    except Exception as e:
        print("Exception occurred", e.args)

if __name__ == "__main__":
    main()