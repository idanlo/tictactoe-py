# Online Tic Tac Toe
## new player joins:

- player sends request "NEW_PLAYER", player receives unique ID and saves it

## player chooses lobby:

- player sends request `"JOIN_LOBBY <LOBBY_ID> <PLAYER_ID>"`

- if lobby exists and the playercount of the lobby is below 2 - the player can join and server will send to client `"JOINED_LOBBY <LOBBY_ID>"`.

- if lobby doesn't exist then server creates it, sets playercount to 1 and sends to client `"CREATED_LOBBY <LOBBY_ID>"`.

- if player tries to join a full lobby, server sends to client `"FAILED_TO_JOIN_LOBBY <REASON>"`, then user will be prompted for another lobby id.
