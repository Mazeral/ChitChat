#!/usr/bin/env python3
"""Websockets server
This script creates a simple WebSocket echo server using the `websockets`
library.
It listens for incoming WebSocket connections on localhost port 8765.
For each connected client, it receives messages and sends the same message back.
The server runs indefinitely until manually stopped.
"""


import asyncio
import json
from websockets.asyncio.server import serve
import websockets


# Dictionary to store active rooms and the clients connected to them
# {
#     "room_identifier_1": {websocket_connection_1, websocket_connection_2,...},
#     "room_identifier_2": {websocket_connection_3, ...},
# }
rooms = {}


async def notify_room(room_id, message):
    """Sends a notification to all the users in a room"""
    if room_id in rooms:
        try:
            for client in rooms[room_id]:
                try:
                    await client.send(json.dumps(message))
                except websockets.exceptions.ConnectionClosedError:
                    print(
                        f"Error sending notification to a closed\
                            connection in room {room_id}.")
                except websockets.exceptions.ConnectionClosedOK:
                    pass
                except Exception as e:
                    pass  # Ignore other exceptions
        except Exception as e:
            print(f"Error iterating through clients in room {room_id}: {e}")


async def handler(websocket):
    """Handler for the websocket
    websocket: The websocket object, handles sending and receices via websocket
    protocol.

    We receive the sent JSON data in string format because we need to serialize
    the data to string, then we deserialize it into a JSON format
    """
    room_id = None
    try:
        async for serialized_json in websocket:
            try:
                # Deserialize the serialized_json string
                data = json.loads(serialized_json)

                action = data.get('action')
                if action == "join":
                    requested_room_id = data.get('room_id')
                    if requested_room_id:
                        room_id = requested_room_id
                        # handling new room requests
                        if room_id not in rooms:
                            rooms[room_id] = set()
                        # adding a user to an existing room
                        rooms[room_id].add(websocket)
                        await notify_room(room_id, {"type": "user_joined",
                                                    "user_id": id(websocket)})
                    else:
                        await websocket.send(
                            json.dumps({"type": "error",
                                        "message": "Room ID is\
                                                required to join."}))
                elif action == "send" and room_id:
                    message_content = data.get('message')
                    if message_content:
                        await notify_room(room_id, {"type": "message",
                                                    "user_name": id(websocket),
                                                    "content": message_content})
                    else:
                        await websocket.send(json.dumps({"type": "error",
                                                         "message": "Message\
                                                         content is missing."}))
                else:
                    await websocket.send(json.dumps({"type": "error",
                                                     "message": "Invalid\
                                                             action."}))
            except json.JSONDecodeError:
                await websocket.send(json.dumps({"type": "error",
                                                 "message": "Invalid JSON\
                                                         format."}))
            except Exception as e:
                print(f"Error processing message: {e}")
                await websocket.send(json.dumps({"type": "error",
                                                 "message": f"Server error:\
                                                         {e}"}))
    # Handling disconnections
    except websockets.exceptions.ConnectionClosedError:
        pass
    except websockets.exceptions.ConnectionClosedOK:
        pass
        action = serialized_json['action']
    finally:
        # Notifying if a user disconnected
        if room_id and websocket in rooms.get(room_id, set()):
            rooms[room_id].remove(websocket)
            await notify_room(room_id, {"type": "user_left",
                                        "user_name": id(websocket)})
            if not rooms[room_id]:
                del rooms[room_id]


async def main():
    """Sets up and starts the WebSocket server.

    This asynchronous function initializes the WebSocket server using the
    `websockets.serve` function.
    It binds the `echo` function as the handler for incoming connections on
    the specified host ("localhost")
    and port (8765). Once the server is successfully started, it prints a
    confirmation message
    and then enters an infinite loop (`server.serve_forever()`) to keep the
    server running and listening for new connections and messages.
    """
    async with serve(handler, "localhost", 8765) as server:
        print("Websocket server started")
        await server.serve_forever()  # To make it run forever

if __name__ == "__main__":
    asyncio.run(main())
