# Online Tic Tac Toe
## Player does initial connection with server:

- player sends request "NEW_PLAYER", player receives unique ID and saves it

## Player chooses lobby:

- player sends request `"JOIN_LOBBY <LOBBY_ID> <PLAYER_ID>"`

- if lobby exists and the playercount of the lobby is below 2 - the player can join and server will send to client `"JOINED_LOBBY <LOBBY_ID>"`.

- if lobby doesn't exist then server creates it, sets playercount to 1 and sends to client `"CREATED_LOBBY <LOBBY_ID>"`.

- if player tries to join a full lobby, server sends to client `"FAILED_TO_JOIN_LOBBY <REASON>"`, then user will be prompted for another lobby id.

## Player requests the board

- player sends request `"GET_BOARD"`, receives response `"GET_BOARD <BOARD>"`. `BOARD` is a string that the clients splits by `*` and then gets an array that contains the board data, then displays it in the console

## Player receives the id of the player who's turn it is currently

- player send request `"GET_CURRENT_TURN"`, player receives response `"CURRENT_TURN <PLAYER_ID>"`

## Player places his marker on the board

- player sends request `"PLACE_MARKER <POSITION>"`, `POSITION` being a number between 1 to 9.
  
- if player receives `"PLACE_MARKER ERROR"` then player will be prompted for the position again

- player will be prompted for position until the server response will be `"PLACE_MARKER OK"`

## Player won

- server sends to client `"PLAYER_WON <PLAYER_ID>"`

# List of responses

- `JOINED_LOBBY <LOBBY_ID>`
  
- `CREATED_LOBBY <LOBBY_ID>`

- `FAILED_TO_JOIN_LOBBY <REASON>`

- `GET_BOARD <BOARD>`

- `CURRENT_TURN <PLAYER_ID>`

- `PLACE_MARKER ERROR`

- `PLACE_MARKER OK`

- `PLAYER_WON <PLAYER_ID>`
