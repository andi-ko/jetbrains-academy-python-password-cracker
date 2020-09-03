# write your code here
import socket
import sys
import itertools
import string

if len(sys.argv) < 3:
    print("illegal parameters")
else:
    ip_address = sys.argv[1]
    port = int(sys.argv[2])
    if len(sys.argv) == 4:
        password = sys.argv[3]

    with socket.socket() as client_socket:
        try:
            # print(ip_address, port)
            client_socket.connect((ip_address, port))

            success = False
            blocked = False

            for length in range(1, 5):

                symbols = itertools.chain(string.ascii_lowercase, string.digits)
                permutations = itertools.product(symbols, repeat=length)

                for permutation in permutations:

                    password = ''.join(permutation)

                    client_socket.send(password.encode())
                    response = client_socket.recv(1024).decode()

                    if response == "Connection success!":
                        success = True
                        print(password)
                        break
                    elif response == "Too many attempts":
                        blocked = True
                        break

                if success or blocked:
                    break

        except ConnectionError:
            print("Connection Error")
