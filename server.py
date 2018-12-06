import socket
import random
import uuid
import thread

class Game(object):
    def __init__(self, id):
        self.board = ["0"," "," "," "," "," "," "," "," "," "]
        self.turn = "Player 1" if random.randint(0, 1) == 1 else "Player 2"
        self.id = id
        self.playercount = 1

    
    def __str__(self):
        return "*".join(self.board)

class Player(object):
    def __init__(self, id):
        self.id = id

    def join_lobby(self, lobbyid):
        self.lobbyid = lobbyid

def on_new_client(client_socket, address):
    
    while True:
        data = client_socket.recv(1024)
        data = data.split()
        if data[0] == "NEW_PLAYER":
            new_id = str(uuid.uuid4())
            players.append(Player(new_id))
            client_socket.send(new_id)
            continue
        # if the request isnt new player then one of the arguments must have the player id
        if data[2] in [player.id for player in players]:
            if data[0] == "JOIN_LOBBY":
                if len(data) == 3:
                    lob_id = data[1]
                    lob = [x for x in lobbies if x.id == lob_id]
                    if len(lob) > 0:
                        if lob[0].playercount < 2:
                            lob[0].playercount += 1
                            print "Player (id: " + data[2] + ") joined lobby (id: " + lob_id + ")"
                            print lob[0]
                            client_socket.send("JOIN_LOBBY " + lob_id)
                        else:
                            print "Player (id: " + data[2] + ") attempted to join lobby (id: " + lob_id + ") but it is full"
                            client_socket.send("FAILED_TO_JOIN_LOBBY there are already 2 players")
                    else:
                        lobbies.append(Game(lob_id))
                        print "New lobby created (id: " + lob_id + ") with 1 player (id: " + data[2] + ")"
                        client_socket.send("CREATED_LOBBY " + lob_id)
            
            # p_id = data[0]
            # if data[0] not in [player.id for player in players]:
            #     players.append(Player(data[0]))
            # if data[0] == "NEW_LOBBY":
            #     lobby_id = int(data[1])
            #     lobby = [lob for lob in lobbies if lob.id == lobby_id]
            #     if len(lobby) > 0 and lobby[0].playercount < 2:


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