import socket
import random
import uuid
import thread

class Lobby(object):
    def __init__(self, id):
        self.board = ["0"," "," "," "," "," "," "," "," "," "]
        self.turn = "Player 1" if random.randint(0, 1) == 1 else "Player 2"
        self.id = id
        self.playercount = 1
        self.current_turn = None
        self.players = []


    def __str__(self):
        return "*".join(self.board)


class Player(object):
    def __init__(self, id, sock):
        self.id = id
        self.lobby = None
        self.marker = "X"
        self.sock = sock

    def join_lobby(self, lobby):
        self.lobby = lobby

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

def on_new_client(client_socket, address):
    
    global lobbies
    global players
    player_id = ""
    while True:
        data = client_socket.recv(1024)
        data = data.split()
        if data[0] == "NEW_PLAYER":
            player_id = str(uuid.uuid4())
            players.append(Player(player_id, client_socket))
            client_socket.send(player_id)
            continue
        if len(player_id) > 0:
            player = [x for x in players if x.id == player_id]
            if len(player) > 0:
                player = player[0]
                if data[0] == "JOIN_LOBBY":
                    lob_id = data[1]
                    # find lobby with id lob_id
                    lob = [x for x in lobbies if x.id == lob_id]

                    if len(lob) > 0:
                        if lob[0].playercount < 2:
                            lob[0].playercount += 1
                            player.lobby = lob[0]
                            player.marker = "O"
                            lob[0].players.append(player)
                            print "Player (id: " + player_id + ") joined lobby (id: " + lob_id + ")"
                            client_socket.send("JOIN_LOBBY " + lob_id)
                        else:
                            print "Player (id: " + player_id + ") attempted to join lobby (id: " + lob_id + ") but it is full"
                            client_socket.send("FAILED_TO_JOIN_LOBBY there are already 2 players")
                    else:
                        new_lobby = Lobby(lob_id)
                        new_lobby.current_turn = player
                        new_lobby.players.append(player)
                        lobbies.append(new_lobby)
                        player.lobby = new_lobby
                        print "New lobby created (id: " + lob_id + ") with 1 player (id: " + player_id + ")"
                        client_socket.send("CREATED_LOBBY " + lob_id)
                elif data[0] == "GET_BOARD":
                    client_socket.send(str(player.lobby))
                elif data[0] == "GET_CURRENT_TURN":
                    client_socket.send(player.lobby.current_turn.id)
                elif data[0] == "PLACE_MARKER":
                    pos = int(data[1])
                    if player.lobby.board[pos] == " " and player.lobby.current_turn == player:
                        player.lobby.board[pos] = player.marker
                        # set turn to other player
                        if player.lobby.players[0] == player:
                            player.lobby.current_turn = player.lobby.players[1]
                        else:
                            player.lobby.current_turn = player.lobby.players[0]
                        has_won = win_check(player.lobby.board, player.marker)
                        if has_won:
                            for p in player.lobby.players:
                                print p
                                p.sock.send("PLAYER_WON PLAYER " + player.id + " HAS WON")
                        else:
                            client_socket.send("OK")
                    else:
                        client_socket.send("ERROR")
            else:
                print "User not found"
                client_socket.send("FAILED_TO_JOIN_LOBBY User not found")


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 8080))
    server_socket.listen(2)
    global players
    global lobbies
    lobbies = []
    players = []

    while True:
        client_socket, address = server_socket.accept()
        thread.start_new_thread(on_new_client, (client_socket, address))


if __name__ == "__main__":
    main()