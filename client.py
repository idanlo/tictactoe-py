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
    


def player_input():
    marker = ""
    while not (marker == "X" or marker == "O"):
        marker = raw_input("Do you want to be X or O? ").upper()

    if marker == "O":
        return ("O", "X")
    else:
        return ("X", "O")

def full_board_check(board):
    for x in board:
        if x == " ":
            return False
    return True

def player_choice():
    position = ""
    while position not in '1 2 3 4 5 6 7 8 9'.split():
        position = raw_input("Choose your next position: (1 - 9) ")
    return position


def main():
    print "Welcome to Tic Tac Toe!"
    game_board = ["0"," "," "," "," "," "," "," "," "," "]
    player1_marker, player2_marker = player_input()
    turn = "Player 1"
    game_on = False
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 8080))
    my_id = ""

    sock.send("NEW_PLAYER")
    my_id = sock.recv(1024)
    print my_id
    is_user_turn = False
    connected_to_lobby = False
    board = []
    while True:
        data = ""
        while not connected_to_lobby:
            lobby_id = raw_input("Enter lobby id: ")
            sock.send("JOIN_LOBBY " + lobby_id)
            data = sock.recv(1024)
            print data
            data = data.split()
            print data[0] != "FAILED_TO_JOIN_LOBBY"
            if data[0] != "FAILED_TO_JOIN_LOBBY":
                connected_to_lobby = True
        # display initial board
        sock.send("GET_BOARD")
        board = sock.recv(1024).split("*")
        display_board(board)
        # wait until it is the users turn
        data = ""
        while data != my_id:
            sock.send("GET_CURRENT_TURN")
            data = sock.recv(1024)
        # display board again if there were any changes
        sock.send("GET_BOARD")
        board = sock.recv(1024).split("*")
        display_board(board)
        # position is a number to index the board array
        err = True
        while err:
            position = player_choice()
            sock.send("PLACE_MARKER " + position)
            data = sock.recv(1024).split()
            if data[0] == "OK":
                err = False
            elif data[0] == "PLAYER_WON":
                print " ".join(data[1:])
        # break


    # while game_on:
    #     if turn == "Player 1":
    #         display_board(game_board)
    #         position = player_choice(game_board)
    #         place_marker(game_board, player1_marker, position)
            
    #         if win_check(game_board, player1_marker):
    #             display_board(game_board)
    #             print "Player 1 Won! "
    #             game_on = False
    #         else:
    #             if full_board_check(game_board):
    #                 display_board(game_board)
    #                 print "The game is a draw! "
    #                 break
    #             else:
    #                 turn = "Player 2"


if __name__ == "__main__":
    main()
    