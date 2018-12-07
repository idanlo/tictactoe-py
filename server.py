import socket
import random
import uuid
import thread
import time

class Lobby(object):
    def __init__(self, id):
        self.board = ["0"," "," "," "," "," "," "," "," "," "]
        self.id = id
        self.playercount = 1
        self.current_turn = None
        self.players = []

    def __str__(self):
        return "*".join(self.board)

    def place_marker(self, pos, player):
        self.board[pos] = player.marker

    def win_check(self, marker):
        if self.board[7] == marker and self.board[8] == marker and self.board[9] == marker:
            return True
        if self.board[4] == marker and self.board[5] == marker and self.board[6] == marker:
            return True
        if self.board[1] == marker and self.board[2] == marker and self.board[3] == marker:
            return True
        if self.board[7] == marker and self.board[4] == marker and self.board[1] == marker:
            return True
        if self.board[8] == marker and self.board[5] == marker and self.board[2] == marker:
            return True
        if self.board[9] == marker and self.board[6] == marker and self.board[3] == marker:
            return True
        if self.board[7] == marker and self.board[5] == marker and self.board[3] == marker:
            return True
        if self.board[9] == marker and self.board[5] == marker and self.board[1] == marker:
            return True
        return False
    
    def full_board_check(self):
        for x in self.board:
            if x == " ":
                return False
        return True



class Player(object):
    def __init__(self, id, sock):
        self.id = id
        self.lobby = None
        self.marker = "X"
        self.sock = sock

    def join_lobby(self, lobby):
        self.lobby = lobby


def on_new_client(client_socket, address):
    
    global lobbies
    global players
    player_id = ""

    in_lobby = False
    logged_in = False
    while not in_lobby:
        data = client_socket.recv(1024)
        data = data.split()
        print data
        if not logged_in and data[0] == "NEW_PLAYER":
            player_id = str(uuid.uuid4())
            players.append(Player(player_id, client_socket))
            client_socket.send(player_id)
            logged_in = True
        elif data[0] == "JOIN_LOBBY" and len(player_id) > 0:
            player = [x for x in players if x.id == player_id]
            if len(player) > 0:
                lob_id = data[1]
                player = player[0]
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
                        in_lobby = True
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
                    in_lobby = True
    player = [x for x in players if x.id == player_id]
    if len(player) > 0:
        player = player[0]
        # wait for 2 players in lobby
        while player.lobby.playercount != 2:
            pass
        done = False
        client_socket.send("GET_BOARD " + str(player.lobby))
        while not done:
            # wait for players turn
            while player.lobby.current_turn != player:
                pass
            client_socket.send("GET_BOARD " + str(player.lobby))
            time.sleep(0.1)
            client_socket.send("PLACE_MARKER")
            pos = int(client_socket.recv(1024))
            while player.lobby.board[pos] != " ":
                print "ERR"
                client_socket.send("PLACE_MARKER")
                pos = int(client_socket.recv(1024))
            if player.lobby.current_turn == player:
                player.lobby.place_marker(pos, player)
                # set turn to other player
                if player.lobby.players[0] == player:
                    player.lobby.current_turn = player.lobby.players[1]
                else:
                    player.lobby.current_turn = player.lobby.players[0]
            else:
                print "ERR"
                client_socket.send("PLACE_MARKER ERROR")
            # check for win
            has_won = player.lobby.win_check(player.marker)
            if has_won:
                for p in player.lobby.players:
                    p.sock.send("PLAYER_WON " + player.id)
                    p.sock.close()
                # done = True
                return
            full_board = player.lobby.full_board_check()
            if full_board:
                for p in player.lobby.players:
                    p.sock.send("TIE")
                    p.sock.close()
                # done = True
                return
            client_socket.send("GET_BOARD " + str(player.lobby))


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