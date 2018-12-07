import os 
import random
import socket

def clear():
    os.system('cls')

def display_board(board):
    clear()
    print "  " + board[1] + "  |  " + board[2] + "  |  " + board[3] + " "
    print " ---------------"
    print "  " + board[4] + "  |  " + board[5] + "  |  " + board[6] + " "
    print " ---------------"
    print "  " + board[7] + "  |  " + board[8] + "  |  " + board[9] + " "

def player_choice():
    position = ""
    while position not in '1 2 3 4 5 6 7 8 9'.split():
        position = raw_input("Choose your next position: (1 - 9) ")
    return position

def connect_to_lobby(my_sock):
    connected_to_lobby = False
    while not connected_to_lobby:
        lobby_id = raw_input("Enter lobby id: ")
        my_sock.send("JOIN_LOBBY " + lobby_id)
        data = my_sock.recv(1024).split()
        if data[0] == "FAILED_TO_JOIN_LOBBY":
            print " ".join(data[1:])
        else:
            connected_to_lobby = True


def handle_response(res, sock):
    global finished
    response = res.split()
    if response[0] == "GET_BOARD":
        board = " ".join(response[1:]).split("*")
        display_board(board)
    elif response[0] == "PLACE_MARKER":
        marker = player_choice()
        sock.send(marker)
    elif response[0] == "PLAYER_WON":
        print "PLAYER WON "+ response[1]
        finished = True
    elif response[0] == "TIE":
        print "IT'S A TIE!"
        finished = True


def main():
    print "Welcome to Tic Tac Toe!"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 8080))
    my_id = ""

    sock.send("NEW_PLAYER")
    my_id = sock.recv(1024)
    print "YOUR ID: " + my_id
    board = []
    connect_to_lobby(sock)
    global finished
    finished = False
    while not finished:
        data = sock.recv(1024)
        res = handle_response(data, sock)

        

if __name__ == "__main__":
    main()
    