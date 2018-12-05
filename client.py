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

def place_marker(board, marker, position):
    board[position] = marker

def win_check(board, marker):
    if board[7] == marker and board[8] == marker and board[9] == marker:
        return True
    if board[4] == marker and board[5] == marker and board[6] == marker:
        return True
    if board[1] == marker and board[2] == marker and board[3] == marker:
        return True
    if board[7] == marker and board[4] == marker and board[1] == marker:
        return True
    if board[8] == marker and board[5] == marker and board[2] == marker:
        return True
    if board[9] == marker and board[6] == marker and board[3] == marker:
        return True
    if board[7] == marker and board[5] == marker and board[3] == marker:
        return True
    if board[9] == marker and board[5] == marker and board[1] == marker:
        return True

    return False

def choose_first():
    if random.randint(0,1) == 1:
        return "Player 1"
    else:
        return "Player 2"

def space_check(board, position):
    if board[position] == " ":
        return True
    else:
        return False

def full_board_check(board):
    for x in board:
        if x == " ":
            return False
    return True

def player_choice(board):
    position = ""
    while position not in '1 2 3 4 5 6 7 8 9'.split() or not space_check(board, int(position)):
        position = raw_input("Choose your next position: (1 - 9) ")
    return int(position)

def replay():
    replay_string = raw_input("Do you want to play again? (Enter Yes or No) ").upper()
    if replay_string[0] == "Y":
        return True
    else: 
        return False

def main():
    print "Welcome to Tic Tac Toe!"
    while True:
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
        while not game_on:
            data = ""
            err = True
            while not err:
                lobby_id = raw_input("Enter lobby id: ")
                sock.send("JOIN_LOBBY " + lobby_id + " " + my_id)
                data = sock.recv(1024)
                print data
                data = data.split()
                print data[0] != "FAILED_TO_JOIN_LOBBY"
                if data[0] != "FAILED_TO_JOIN_LOBBY":
                    err = False
            raw_input("somethin ")
                


        while game_on:
            if turn == "Player 1":
                display_board(game_board)
                position = player_choice(game_board)
                place_marker(game_board, player1_marker, position)
                
                if win_check(game_board, player1_marker):
                    display_board(game_board)
                    print "Player 1 Won! "
                    game_on = False
                else:
                    if full_board_check(game_board):
                        display_board(game_board)
                        print "The game is a draw! "
                        break
                    else:
                        turn = "Player 2"
            elif turn == "Player 2":
                display_board(game_board)
                position = player_choice(game_board)
                place_marker(game_board, player2_marker, position)
                
                if win_check(game_board, player2_marker):
                    display_board(game_board)
                    print "Player 2 Won! "
                    game_on = False
                else:
                    if full_board_check(game_board):
                        display_board(game_board)
                        print "The game is a draw! "
                        break
                    else:
                        turn = "Player 1"
        if not replay():
            break


if __name__ == "__main__":
    main()
    