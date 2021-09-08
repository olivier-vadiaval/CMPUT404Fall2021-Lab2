import socket

HOST = "www.google.com"
PORT = "http"           # 80
address = (HOST, PORT)
BUF_SIZE = 4096
page_request = "GET / HTTP/1.1\r\nHost: %s\r\n\r\n" % HOST

try:
    with socket.create_connection(address) as client_socket:
        # Using create_connection is equivalent to using the
        # socket method and then using the connect method
        print('Connection established')
        
        client_socket.sendall(page_request.encode())
        print('Request sent!')

        data = ""
        while True:
            received_data = client_socket.recv(BUF_SIZE)
            if not received_data:
                break
            data += received_data.decode()

        print('Received data, have a look:')

        # Print response
        print(data)

except Exception as e:
    print('Exception Occurred: ', e.args)