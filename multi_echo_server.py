#!/usr/bin/env python3
import socket
import multiprocessing as mp

BUF_SIZE = 4096

def request_handler(conn_socket):
    try:
        while True:
            received_data = conn_socket.recv(BUF_SIZE)
            if received_data:
                print("Received the following data:\n", received_data.decode())
                print("Returning same data")
                conn_socket.sendall(received_data)
            else:
                break

    except (socket.error, msg):
        if client_data == b"":
            print("Client disconnected!")
        else:
            print("Exception occurred:", msg)

    except Exception as e:
        print("Exception occurred:", e.args)

    finally:
        print("Closing connection")
        conn_socket.close()


def main():
    HOST = "localhost"  # localhost
    PORT = 8001
    address = (HOST, PORT)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            # Question 3
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

            server_socket.bind(address)
            server_socket.listen()
            print("Listening on port", PORT)

            while True:
                conn_socket, client_addr = server_socket.accept()
                client_host, client_port = client_addr

                # Question 4
                print("Connected to client at", client_host, ",", client_port)

                # create new process to handle new connection
                new_conn = mp.Process(
                    target=request_handler,
                    args=(conn_socket,)
                )

                new_conn.daemon = True      # daemonize
                new_conn.start()            # fork

                print("New process started", new_conn)
                print("Number of processes:", len(mp.active_children()))

    except Exception as e:
        print("Exception occurred: ", e.args)

if __name__ == "__main__":
    main()